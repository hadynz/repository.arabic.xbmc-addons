# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import urllib2,urllib
import re
import httplib,itertools

import time


__settings__ = xbmcaddon.Addon(id='plugin.video.syriadrama')
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
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('WARNING','This addon is completely FREE DO NOT buy any products from http://tvtoyz.com/', 16000, 'https://lh5.googleusercontent.com/-ZaRTz8kxk-k/AAAAAAAAAAI/AAAAAAAAAAA/f643_NNxkOU/s48-c-k-no/photo.jpg'))
	addDir('SYRIA DRAMA','http://www.syria-drama.net/video-category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/',1,'http://www.english.globalarabnetwork.com/images/stories/2009/August/Syria_Drama_Channel_Officially_Launched.jpg')
	
	
def indexContent(url):
   
	max=6
	for counter in range(1,max):
		try:
			myPath=str(url)+"page/"+str(counter)+"/"
			req = urllib2.Request(myPath)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			link=response.read()
			target= re.findall(r'tooltip_n" href="(.*?)\s(.*?)</span></a>', link, re.DOTALL)
			for items in target:
				mySerie=items[1]              
				myUrl=str( items[0]).replace('"','').strip()
				name=str(mySerie).split('"><img width=')[0]
				name=str(name).replace('title="', '').strip()
				image=str(mySerie).split('class="attachment-post-thumbnail')[0]
				image=str(image).split('src="')[1]
				image=str(image).replace('"', "").replace("..jpg",".jpg").strip()
				print name
				print image
				print myUrl
				
				if "مسلسل" in name:
					addDir(name,myUrl,2,image)
				else:
					addLink(name,myUrl,3,image)
					
		except:
			pass	

def indexEpos (url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	target= re.findall(r'<ul class="episode">(.*?)\s(.*?)<div class="clear"></div>', link, re.DOTALL)
	try:
		for items in target:
			myPath=str( items[1]).split('</li>')
			for i in myPath:
				name=str( i).split(' href="')[0]
				myPath=str( i).split(' href="')[1]
				myPath=str(myPath).split('">')[0]
				myPath=str(myPath).replace('"', '').strip()
				name=str(name).replace('<li><a class="tooltip_s" title="', '').replace('"',"").replace("</ul>","").strip()
				addLink(name,myPath,3,'')
				print name
				print myPath
	except:
		pass
def playVideo(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		myVideo=(re.compile('<iframe width="520" height="400" src="(.+?)"></iframe>').findall(link))
		
		myVideo=str(myVideo).replace("['", '').replace("']", '').replace("http://www.youtube.com/embed/","").strip()
		if  str(myVideo) > 1 :
			print "YOUTUBE VIDEO "+str(myVideo)
			playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % myVideo
			listItem = xbmcgui.ListItem(path=str(playback_url))
			xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
		else :
			 myVideo2=(re.compile('<source src="(.+?)" type="video/flash" />').findall(link))
			 myVideo2=str(myVideo).replace("['", '').replace("']", '').strip()
			 listItem = xbmcgui.ListItem(path=str(myVideo2))
			 xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
        
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
        indexContent(url)
	
elif mode==2:
        print ""+url
        indexEpos(url)
elif mode==3:
	print ""+url
	playVideo(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
