# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re
import HTMLParser
import xbmcaddon
import json
import traceback
import os
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
import time
import sys
import  CustomPlayer

__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.shahidmbcnet'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonArt = os.path.join(addonPath,'resources/images')
#communityStreamPath = os.path.join(addonPath,'resources/community')
communityStreamPath = os.path.join(addonPath,'resources')
communityStreamPath =os.path.join(communityStreamPath,'community')


def PlayStream(sourceEtree, urlSoup, name, url):
    try:
        #url = urlSoup.url.text
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('XBMC', 'Parsing the xml file')
        pDialog.update(10, 'fetching channel info')
        title=''
        link=''
        sc=''
        try:
            title=urlSoup.item.title.text
            
            link=urlSoup.item.link.text
            sc=sourceEtree.findtext('sname')
        except: pass
        if link=='':
            timeD = 2000  #in miliseconds
            line1="couldn't read title and link"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeD, __icon__))
            return False
        regexs = urlSoup.find('regex')
        pDialog.update(80, 'Parsing info')
        if (not regexs==None) and len(regexs)>0:
            liveLink=    getRegexParsed(urlSoup,link)
        else:
            liveLink=    link
        liveLink=liveLink
        if len(liveLink)==0:
            timeD = 2000  #in miliseconds
            line1="couldn't read title and link"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeD, __icon__))
            return False
            
        timeD = 2000  #in miliseconds
        line1="Resource found,playing now."
        pDialog.update(80, line1)
        liveLink=replaceSettingsVariables(liveLink)
        name+='-'+sc+':'+title
        print 'liveLink',liveLink
        pDialog.close()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=liveLink )
        if not 'plugin.video.f4mTester' in liveLink:
            player = CustomPlayer.MyXBMCPlayer()
            start = time.time() 
            #xbmc.Player().play( liveLink,listitem)
            player.play( liveLink,listitem)
            xbmc.sleep(2000)
            while player.is_active:
                xbmc.sleep(200)
            #return player.urlplayed
            done = time.time()
            elapsed = done - start
            if player.urlplayed and elapsed>=3:
                return True
            else:
                return False
        else:
            xbmc.executebuiltin('XBMC.RunPlugin('+liveLink+')')
            return True
                
    except:
        traceback.print_exc(file=sys.stdout)    
    return False  

def getRegexParsed(regexs, url,cookieJar=None,forCookieJarOnly=False,recursiveCall=False,cachedPages={}, rawPost=False):#0,1,2 = URL, regexOnly, CookieJarOnly

#    cachedPages = {}
    #print 'url',url
    doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(url)
    print 'doRegexs',doRegexs,regexs

    for rege in doRegexs:
        k=regexs.find("regex",{"name":rege})
        if not k==None:
            cookieJarParam=False
            if k.cookiejar:
                cookieJarParam=k.cookiejar.text;
                if  '$doregex' in cookieJarParam:
                    cookieJar=getRegexParsed(regexs, cookieJarParam,cookieJar,True, True,cachedPages)
                    cookieJarParam=True
                else:
                    cookieJarParam=True
            if cookieJarParam:
                if cookieJar==None:
                    #print 'create cookie jar'
                    import cookielib
                    cookieJar = cookielib.LWPCookieJar()
                    #print 'cookieJar new',cookieJar
            page=''
            try:
                page = k.page.text
            except: pass
            if  '$doregex' in page:
                page=getRegexParsed(regexs, page,cookieJar,recursiveCall=True,cachedPages=cachedPages)
                
            postInput=None
            if k.post:
                postInput = k.post.text
                if  '$doregex' in postInput:
                    postInput=getRegexParsed(regexs, postInput,cookieJar,recursiveCall=True,cachedPages=cachedPages)
                print 'post is now',postInput
            
            if k.rawpost:
                postInput = k.rawpost.text
                if  '$doregex' in postInput:
                    postInput=getRegexParsed(regexs, postInput,cookieJar,recursiveCall=True,cachedPages=cachedPages,rawPost=True)
                print 'rawpost is now',postInput    
            link=''    
            if not page=='' and page in cachedPages and forCookieJarOnly==False :
                link = cachedPages[page]
            else:
                if page.startswith('http'):
                    print 'Ingoring Cache',page
                    req = urllib2.Request(page)
                    
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
                    if k.referer:
                        req.add_header('Referer', k.referer.text)
                    if k.agent:
                        req.add_header('User-agent', k.agent.text)

                    if not cookieJar==None:
                        #print 'cookieJarVal',cookieJar
                        cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
                        opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
                        opener = urllib2.install_opener(opener)
                    #print 'after cookie jar'

                    post=None
                    if postInput and not k.rawpost:
                        postData=postInput
                        splitpost=postData.split(',');
                        post={}
                        for p in splitpost:
                            n=p.split(':')[0];
                            v=p.split(':')[1];
                            post[n]=v
                        post = urllib.urlencode(post)
                        
                    if postInput and k.rawpost:
                        post=postInput

                    if post:
                        response = urllib2.urlopen(req,post)
                    else:
                        response = urllib2.urlopen(req)

                    link = response.read()
                    link=javascriptUnEscape(link)

                    response.close()
                    cachedPages[page] = link
                    if forCookieJarOnly:
                        return cookieJar# do nothing
                elif not page.startswith('http'):
                    link=page
            
            expres=k.expres.text
            if  '$doregex' in expres:
                expres=getRegexParsed(regexs, expres,cookieJar,recursiveCall=True,cachedPages=cachedPages)
                        
            print 'link',link
            print expres
            if not expres=='':
                if expres.startswith('$pyFunction:'):
                    val=doEval(expres.split('$pyFunction:')[1],link)
                    url = url.replace("$doregex[" + rege + "]", val)
                else:
                    if not link=='': 
                        reg = re.compile(expres).search(link)
                        val=reg.group(1).strip()

                    else:
                        val=expres
                    if k.rawpost:
                        print 'rawpost'
                        val=urllib.quote_plus(val)
                    if k.htmlunescape:
                            #val=urllib.unquote_plus(val)
                        import HTMLParser
                        val=HTMLParser.HTMLParser().unescape(val)
                        
                    url = url.replace("$doregex[" + rege + "]",val )
                        
            else:
                url = url.replace("$doregex[" + rege + "]", '')
            
            if '$epoctime$' in url:
                url=url.replace('$epoctime$',getEpocTime())
            
            if recursiveCall: return url
    print 'final url',url
    return url

def getEpocTime():
    import time
    return str(int(time.time()*1000))
    
def javascriptUnEscape(str):
	js=re.findall('unescape\(\'(.*?)\'',str)
	print 'js',js
	if (not js==None) and len(js)>0:
		for j in js:
			print urllib.unquote(j)
			str=str.replace(j ,urllib.unquote(j))
	return str
    
def doEval(fun_call,page_data):
    ret_val=''
    #if functions_dir not in sys.path:
    #    sys.path.append(functions_dir)
    
    print fun_call
    py_file='import '+fun_call.split('.')[0]
    #print py_file
    exec( py_file)
    exec ('ret_val='+fun_call)
    #exec('ret_val=1+1')
    return str(ret_val)
    
def replaceSettingsVariables(str):
    retVal=str
    if '$setting' in str:
        matches=re.findall('\$(setting_.*?)\$', str)
        for m in matches:
            setting_val=selfAddon.getSetting( m )
            retVal=retVal.replace('$'+m+'$',setting_val)
    return retVal
