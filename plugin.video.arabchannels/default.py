# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import urllib2,urllib
import re,os
import httplib
import time
from urllib import urlencode
from xbmcswift2 import Plugin



__settings__ = xbmcaddon.Addon(id='plugin.video.arabchannels')
__icon__ = __settings__.getAddonInfo('icon')
__fanart__ = __settings__.getAddonInfo('fanart')
__language__ = __settings__.getLocalizedString


def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner
httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)


def CATEGORIES():
	addDir('Group 1','http://servechannels.itholster.com/HandMeChannels.aspx?country=&typeofapp=tv&epirus=Arabic&typeofchannel=',1,'http://www.userlogos.org/files/logos/Rog/livetv_ru_09.png')
	addDir('Group 3',' ',5,'http://www.userlogos.org/files/logos/Rog/livetv_ru_09.png')
	addDir('Group 4','https://www.youtube.com/results?filters=live&search_query=%D8%A8%D8%AB+%D8%AD%D9%8A&page=',6,'http://www.userlogos.org/files/logos/Rog/livetv_ru_09.png')
	addDir('Group 5','https://www.youtube.com/results?search_query=بث+مباشر&filters=live&page=',6,'http://www.userlogos.org/files/logos/Rog/livetv_ru_09.png')
	
def VideoLinksGroupOne(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		link=str(link).split(",")
		for items in link:
			if '{"channels": [{"name": "' in items:
				name=str(items).replace('{"channels": [{"name": "','').replace('"', '').strip()
				name=str(name).replace('{channels: [', '')
			if '{"name": "' in items:
				name=str(items).replace('{"name": "', '') .replace('"', '').strip()
				name=str(name).replace('{channels: [', '')
			if '"url": "' in items:
				turl=str(items).replace('"url": "', '') .replace('"', '').strip()
				response.close()
				addLink(name,turl,'')
	except:
		pass

def FilmonCh(url):
	addLink("Al Arabiya",'rtsp://mi5.gv.filmon.com:1935/live/_definst_/366.high.stream',"")
	addLink("MBC",'rtsp://mi5.gv.filmon.com:1935/live/_definst_/367.high.stream',"")
	addLink("MBC2",'rtsp://mi5.gv.filmon.com:1935/live/_definst_/368.high.stream',"")

def listYoutbeChannels(url):
	try:
		for counter in range(1,9):
				req = urllib2.Request(url+str(counter))
				req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
				response = urllib2.urlopen(req)
				link=response.read()
				scriptPl=(re.compile('<h3 class="yt-lockup2-title"(.+?)title="(.+?)data-sessionlink="(.+?)" href="(.+?)"').findall(link))
				listofChannels=[]
				
				for elements in scriptPl:
					for items in elements:
					   
						name=str( elements[1]).strip()
						path=str( elements[3]).split("=")
						path=str(path[1]).strip()
						if path not in listofChannels:
							listofChannels.append(name)
							listofChannels.append(path)
				for el in listofChannels:
					name=listofChannels.pop(0)
					name=str(name).replace('"', '').strip()
					path=listofChannels.pop(0)
					path=str(path).strip()
					addDir(name,path,7,'')
	except:
		pass
def playYoutubeChannel(name,url):
	try:
		playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s'%url
		xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(playback_url)
		addLink("","","")
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




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
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
        VideoLinksGroupOne(url)
elif mode==3:
        print ""+url
        listGglarabMobChannels(url)

elif mode==5:
        print ""+url
        FilmonCh(url)
elif mode==6:
        print ""+url
        listYoutbeChannels(url)	
elif mode==7:
        print ""+url
        playYoutubeChannel(name,url)	


xbmcplugin.endOfDirectory(int(sys.argv[1]))
