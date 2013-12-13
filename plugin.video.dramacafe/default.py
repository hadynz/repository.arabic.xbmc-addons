# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import httplib



__settings__ = xbmcaddon.Addon(id='plugin.video.dramacafe')
__icon__ = __settings__.getAddonInfo('icon')
__fanart__ = __settings__.getAddonInfo('fanart')
__language__ = __settings__.getLocalizedString
_thisPlugin = int(sys.argv[1])
_pluginName = (sys.argv[0])

def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner
	
httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)

def GetCategories():
	#xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('WARNING','This addon is completely, Nobody has the right to charge you for this addon', 16000, 'https://pbs.twimg.com/profile_images/1908891822/R5MpO.gif'))
	url='http://www.online.dramacafe.tv/index.html'
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	req.add_header('Host', 'www.online.dramacafe.tv')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	req.add_header('Cookie', 'popNum=8; __atuvc=6%7C34%2C3%7C35; popundr=1; PHPSESSID=478ff84e532ad811df5d63854f4f0fe1; watched_video_list=MTgzNDY%3D')
	response = urllib2.urlopen(req)
	link=response.read()
	mylist=[]
	
	url_categories=(re.compile('<li class="topcat"><a href="(.+?)" class="topcat">(.+?)</a>').findall(link))
	url_categories_2=(re.compile('<li class=""><a href="(.+?)" class="">(.+?)</a>').findall(link))
	for items in url_categories:
		catName= str(items[1]).strip()
		catPath=str(items[0]).strip()
		if 'افلام اجنبية' not in catName:
			if 'Movies Pack | سلاسل افلام' not in catName:
				if 'افلام هندية' not in catName:
					if 'Movies | افلام الانمي المدبلجة والمترجمة' not in catName:
						if catName not in mylist:
								mylist.append(catName)
								if 'مسلسلات'  in catName:
									addDir(catName,str(catPath),1,'http://www.portal.dramacafe.tv/themes/nhstyle_4cols/images/header/header.jpg')
								
								if 'افلام'  in catName:
									addDir(catName,str(catPath),4,'http://www.portal.dramacafe.tv/themes/nhstyle_4cols/images/header/header.jpg')
								if 'المسرحيات'  in catName:
									addDir(catName,str(catPath),1,'http://www.portal.dramacafe.tv/themes/nhstyle_4cols/images/header/header.jpg')
			
				
	for itr in url_categories_2:
		catName_2= str(itr[1]).strip()
		catPath_2=str(itr[0]).strip()
		if 'افلام اجنبية' not in catName_2:
			if 'Movies Pack | سلاسل افلام' not in catName_2:
				if 'افلام هندية' not in catName_2:
					if 'Movies | افلام الانمي المدبلجة والمترجمة' not in catName_2:
					
						if catName_2 not in mylist:
							mylist.append(catName_2)
							if 'Movies' in catName_2:
								addDir(catName_2,str(catPath_2),4,'http://www.portal.dramacafe.tv/themes/nhstyle_4cols/images/header/header.jpg')
							if 'الدراما' in catName_2:
								addDir(catName_2,str(catPath_2),1,'http://www.portal.dramacafe.tv/themes/nhstyle_4cols/images/header/header.jpg')
							if 'افلام'  in catName_2:
								addDir(catName_2,str(catPath_2),4,'http://www.portal.dramacafe.tv/themes/nhstyle_4cols/images/header/header.jpg')
							if 'المسرحيات'  in catName_2:
								addDir(catName_2,str(catPath_2),1,'http://www.portal.dramacafe.tv/themes/nhstyle_4cols/images/header/header.jpg')
							if 'مسلسلات'  in catName_2:
									addDir(catName_2,str(catPath_2),1,'http://www.portal.dramacafe.tv/themes/nhstyle_4cols/images/header/header.jpg')
				
def indexSerie(url):
    firstPart=str(url).split('videos')[0]
    nameList=[]
    secPart='videos-'
    lastPart='-date.html'
    counter=0
    for myIndex in range (0,20):
        counter=counter+1
        url=str(firstPart)+secPart+str(counter)+(lastPart)
        print url
        if checkUrl(url):
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            req.add_header('Host', 'www.online.dramacafe.tv')
            req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            req.add_header('Cookie', 'popNum=8; __atuvc=6%7C34%2C3%7C35; popundr=1; PHPSESSID=478ff84e532ad811df5d63854f4f0fe1; watched_video_list=MTgzNDY%3D')
            response = urllib2.urlopen(req)
            link=response.read()
            target= re.findall(r'<span class="pm-video-li-thumb-info">(.*?)\s(.*?) <div class="pm-video-attr">', link, re.DOTALL)
            finalSerieImage=''
            for items in target:
                if str( items[1].split('</span>')[1]):
                    myPath=str( items[1].split('</span>')[1])
                    entirePath=str( myPath).replace("str( items[1].split('</span>')[1])", ' deLiM ').replace('" class="pm-thumb-fix pm-thumb-145"><span class="pm-thumb-fix-clip"><img src="',' deLiM ').replace('" alt="',' deLiM ').replace('" width="',' deLiM ')
                    entirePath=str(entirePath).split(' deLiM ')
                    try:
                        finalSerieImage=str( entirePath[1]).strip()
                    except:
                        finalSerieImage=''
                    if len(entirePath)>1:
                        finalSeriePath=str( entirePath[0]).replace('<a href="', '').strip()
                        finalSerieName=str( entirePath[2]).strip()
                        serieName= str(finalSerieName).split('-')[0]
                        serieName=str(serieName).strip()
                        if ('شارة' and 'الافلام' and 'افلام' and 'المسرحيات ' ) not in serieName:
                            if serieName not in nameList:
                                nameList.append(serieName)
                                addDir(serieName,finalSeriePath,2,finalSerieImage)
								

def indexFilm(url):
    firstPart=str(url).split('videos')[0]
    nameList=[]
    secPart='videos-'
    lastPart='-date.html'
    counter=0
    for myIndex in range (0,20):
        counter=counter+1
        url=str(firstPart)+secPart+str(counter)+(lastPart)
        print url
        if checkUrl(url):
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            req.add_header('Host', 'www.online.dramacafe.tv')
            req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            req.add_header('Cookie', 'popNum=8; __atuvc=6%7C34%2C3%7C35; popundr=1; PHPSESSID=478ff84e532ad811df5d63854f4f0fe1; watched_video_list=MTgzNDY%3D')
            response = urllib2.urlopen(req)
            link=response.read()
            target= re.findall(r'<span class="pm-video-li-thumb-info">(.*?)\s(.*?) <div class="pm-video-attr">', link, re.DOTALL)
            finalSerieImage=''
            for items in target:
                if str( items[1].split('</span>')[1]):
                    myPath=str( items[1].split('</span>')[1])
                    entirePath=str( myPath).replace("str( items[1].split('</span>')[1])", ' deLiM ').replace('" class="pm-thumb-fix pm-thumb-145"><span class="pm-thumb-fix-clip"><img src="',' deLiM ').replace('" alt="',' deLiM ').replace('" width="',' deLiM ')
                    entirePath=str(entirePath).split(' deLiM ')
                    try:
                        finalSerieImage=str( entirePath[1]).strip()
                    except:
                        finalSerieImage=''
                    if len(entirePath)>1:
                        finalSeriePath=str( entirePath[0]).replace('<a href="', '').strip()
                        finalSerieName=str( entirePath[2]).strip()
                        serieName= str(finalSerieName).split('-')[0]
                        serieName=str(serieName).strip()
                        if ('شارة' and 'الافلام' and 'افلام' and 'المسرحيات ' ) not in serieName:
                            if serieName not in nameList:
                                nameList.append(serieName)
                                addLink(serieName,finalSeriePath,3,finalSerieImage)



def checkUrl(url):
	p = urlparse(url)
	conn = httplib.HTTPConnection(p.netloc)
	conn.request('HEAD', p.path)
	resp = conn.getresponse()
	return resp.status < 400
								
def getEpos(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	req.add_header('Host', 'www.online.dramacafe.tv')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	req.add_header('Cookie', 'popNum=8; __atuvc=6%7C34%2C3%7C35; popundr=1; PHPSESSID=478ff84e532ad811df5d63854f4f0fe1; watched_video_list=MTgzNDY%3D')
	response = urllib2.urlopen(req)
	link=response.read()
	target= re.findall(r'<span class="pm-video-li-thumb-info">(.*?)\s(.*?)<h3 dir=', link, re.DOTALL)
	for items in target:
		myItems=str( items[1]).split('</span>')[1]
		myItems=str(myItems).replace('<a href="', ' DELIM ').replace('" class="pm-thumb-fix pm-thumb-74"><span class="pm-thumb-fix-clip"><img src="', ' DELIM ').replace('" alt="', ' DELIM ').replace('" width="74"><span class="vertical-align">', ' DELIM ')
		myItems=str(myItems).split(' DELIM ')
		myPath=str( myItems[1]).strip()
		myImage=str( myItems[2]).strip()
		myName=str( myItems[3]).strip()
		if '|' not in myName:
			addLink(myName,myPath,3,myImage)


def playContent(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	req.add_header('Host', 'www.online.dramacafe.tv')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	req.add_header('Cookie', 'popNum=8; __atuvc=6%7C34%2C3%7C35; popundr=1; PHPSESSID=478ff84e532ad811df5d63854f4f0fe1; watched_video_list=MTgzNDY%3D')
	response = urllib2.urlopen(req)
	link=response.read()
	url_video=(re.compile('<iframe frameborder="0" width="560" height="317" src="(.+?)"></iframe>').findall(link))
	try:
		url_video=str(url_video).split('video/')
		url_video=str(url_video[1]).split('?syndication=')[0]
		url_video=str(url_video).strip()
		playback_url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url='+ str(url_video)
		listItem = xbmcgui.ListItem(path=str(playback_url))
		xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
	except:
		addLink('No video was found !','',334,'http://portal.aolcdn.com/p5/forms/4344/2af553bd-0f81-41d1-a061-8858924b83ca.jpg')
	
		
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param



def addLink(name,url,mode,iconimage):
    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty("IsPlayable","true");
    ok=xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=False)
    return ok
	


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

              
params=get_params()
url=None
name=None
mode=None


	
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        GetCategories()
       
elif mode==1:
        print ""+url
        indexSerie(url)
	
elif mode==2:
		print ""+url
		getEpos(url)
			
elif mode==3:
	print ""+url
	playContent(url)
	
elif mode==4:
	print ""+url
	indexFilm(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))