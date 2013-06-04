# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import httplib
import time


__settings__ = xbmcaddon.Addon(id='plugin.video.sonara')
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


def CATEGORIES():
	addDir('مسلسلات عربية','http://www.sonara.net/videon-49.html',1,'http://profile.ak.fbcdn.net/hprofile-ak-ash4/s160x160/416801_327989490581599_1718150811_a.jpg')
	addDir('برامج','http://www.sonara.net/videon-52.html',1,'http://profile.ak.fbcdn.net/hprofile-ak-ash4/s160x160/416801_327989490581599_1718150811_a.jpg')
	addDir('مسلسلات تركية','http://www.sonara.net/videon-50.html',1,'http://profile.ak.fbcdn.net/hprofile-ak-ash4/s160x160/416801_327989490581599_1718150811_a.jpg')
		
def listContent(url):
	try:
    #url="http://www.sonara.net/videon-50.html"
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		target= re.findall(r'<div class="thumb" style="position: relative;">(.*?)\s(.*?)</a>(.*?)</div>(.*?)</a>', link, re.DOTALL)
		for items in target:
			for i in items:
				
				if '<a href="video' in str(i):
					mystring=str(i).split("<")
					for i in mystring:
						
						if len( str(i))>1:
							if 'img' in str(i):
								image=str(i).replace('img src="', '').replace('" width="150" height="98">', '').strip()
							if 'a href="video' in str(i):
								target=str(i).split('">')
								name=str( target[1]).strip()
								path='http://www.sonara.net/'+str( target[0]).replace('a href="',"").strip()
								if len(name)>1:
									addDir(name,path,2,image)
	except:
		pass
def listEpos(url):
    try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		target= re.findall(r'<div class="thumb">(.*?)\s(.*?)<div class="video_holder">', link, re.DOTALL)
		
		target2= re.findall(r'<div class="name">(.*?)\s(.*?)<td width="800" align="center" style="padding-top: 25px;">', link, re.DOTALL)
		
		
		for epost in target:
			mystring= epost[1]
			mystring=str(mystring).split('">')
			name=str( mystring[4]).replace('</a>','').replace('</div>','').strip()
			path=str( mystring[0]).replace('<a href="','').replace('" target="_self','').strip()
			path=str(path).replace('video-', '').replace('.html', '').strip()
			#print 'THIS is video url '+path
			image=str( mystring[1]).replace('<img src="','').replace('" width="192" height="125','').strip()
			addLink(name,path,3,image)
    except:
		pass

def getVideoFile(url):
    try:
		url='http://www.sonara.net/video_player_new.php?ID='+str(url) 
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		link=str(link).split(';')
		firstpath=''
		secpath=''
		firsbool=False
		secbool=False
		for items in link:
			if 'rtmp' in str( items):
				firstpath=str(items).replace("dlk.addVariable('streamer','", '').replace("')","").strip()
				firsbool=True
			if 'file' in str( items):
				secpath=str( items).replace("dlk.addVariable('file','", '').split("&image=")
				secpath=str( secpath[0]).strip()
				secbool=True
			if firsbool and secbool:
				final= firstpath+'/'+secpath
				listItem = xbmcgui.ListItem(path=str(final))
				xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    except:
		pass
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
        CATEGORIES()
       
elif mode==1:
        print ""+url
        listContent(url)
	
elif mode==2:
        print ""+url
        listEpos(url)
elif mode==3:
	print ""+url
	getVideoFile(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
