# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import httplib
import time


__settings__ = xbmcaddon.Addon(id='plugin.video.arabicchannels')
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
	addDir('All Channels','http://arabichannels.com/index.php',1,'http://arabichannels.com/images/general.jpg')
	
	
		
def indexChannels(url):
  
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link=response.read()
    channelnr=0
    matchObj=(re.compile('<div class="(.+?)"><a href="#" onclick="document.getElementById(.+?)><span class="nume"(.+?)</span><img src="(.+?)"/></a></div>').findall(link))
    for items in matchObj:
       
        path=str( items[1]).split("src='")
        path=path[1]
        path="http://www.arabichannels.com/"+str(path).replace(';"',"").replace("'", '').strip()
        name=str( items[2]).replace(">", "").strip()
        image=str( items[3]).strip()
        
        if not "http:"  in image:
            if "./"  in image:
                image=str(image).replace("./","")
                image="http://www.arabichannels.com/"+image
            elif "/images/" in image:
                image="http://www.arabichannels.com"+image
        if "IPTV Receiver" not in str(name):
			addLink(name,path,2,image)
		
def playChannel(url):

	if ".php" in str(url):

		req = urllib2.Request(url)
		req.add_header('Accept', ' text/html, application/xhtml+xml, */*')
		req.add_header('Referer', 'http://arabichannels.com/')
		req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)')
		req.add_header('Accept-Encoding', ' gzip, deflate')
		req.add_header('Accept-Language', 'sv,en-US;q=0.8,en;q=0.6,en-GB;q=0.4')
		req.add_header('DNT', '1')
		req.add_header('Host', 'arabichannels.com')
		req.add_header('Cookie', 'tzLogin=jsuobfug5ef93ct6c93bnu8f46; __qca=P0-995007673-1378149031936; _pk_id.1.c9f1=18ee4dc4b5730162.1378149032.2.1379954957.1378149081.; _pk_ses.1.c9f1=*; HstCfa2398318=1378149046964; HstCla2398318=1379954941158; HstCmu2398318=1378149046964; HstPn2398318=1; HstPt2398318=2; HstCnv2398318=2; HstCns2398318=2; MLR72398318=1379954942000; MLRV_72398318=1379954942025; __zlcmid=L5dBUG7j5BRBI6')
		response = urllib2.urlopen(req)
		link=response.read()
		streamer=(re.compile("'streamer':(.+?)',").findall(link))
		swf=(re.compile("{type: 'flash', src: '(.+?)'},").findall(link))
		swf=str(swf).replace("['", "").replace("']", "").strip()
		streamer=str(streamer).replace('[', "").replace('"]', "").strip()
		streamer=str(streamer).replace("'", "").replace('"', "").strip().replace("]/", "").strip()
		fileLoc=(re.compile("'file':(.+?)',").findall(link))
		fileLoc=str(fileLoc[0]).replace("'", "").strip()
		fileLoc=str(fileLoc).replace("'", "").replace('"', "").strip()
		complete=streamer + ' playpath=' + fileLoc + ' swfUrl=http://arabichannels.com' + swf + ' flashver=WIN25252011,8,800,175 live=1 timeout=15 swfVfy=1 pageUrl='+str(url)
		listItem = xbmcgui.ListItem(path=str(complete))
		xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
		
	elif ".html" in str(url):
        
			myfinalpath=' '
			req = urllib2.Request(url)
			req.add_header('Accept', ' text/html, application/xhtml+xml, */*')
			req.add_header('Referer', 'http://arabichannels.com/')
			req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)')
			req.add_header('Accept-Encoding', ' gzip, deflate')
			req.add_header('Accept-Language', 'sv,en-US;q=0.8,en;q=0.6,en-GB;q=0.4')
			req.add_header('DNT', '1')
			req.add_header('Host', 'arabichannels.com')
			req.add_header('Cookie', 'tzLogin=jsuobfug5ef93ct6c93bnu8f46; __qca=P0-995007673-1378149031936; _pk_id.1.c9f1=18ee4dc4b5730162.1378149032.2.1379954957.1378149081.; _pk_ses.1.c9f1=*; HstCfa2398318=1378149046964; HstCla2398318=1379954941158; HstCmu2398318=1378149046964; HstPn2398318=1; HstPt2398318=2; HstCnv2398318=2; HstCns2398318=2; MLR72398318=1379954942000; MLRV_72398318=1379954942025; __zlcmid=L5dBUG7j5BRBI6')
			response = urllib2.urlopen(req)
			link=response.read()
			mypath=(re.compile("file: '(.+?)',").findall(link))
			for item in  mypath:
				if "smil" in str(item):
					mydest="http://www.arabichannels.com/"+str( item).strip()
					req2 = urllib2.Request(mydest)
					req2.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
					response2 = urllib2.urlopen(req2)
					link2=response2.read()
					videosource=(re.compile('<video src="(.+?)" system-bitrate="400000"').findall(link2))
					myfinalpath=(re.compile(' <meta base="(.+?)"/>').findall(link2))
					myfinalpath=str(myfinalpath).replace("['", "").replace("']", "").strip()
					videosource=str(videosource).replace("['", "").replace("']", "").replace("'","").strip()
					myfinalpath=myfinalpath + ' playpath=' + videosource + ' swfUrl=http://arabichannels.com/player4/jwplayer.flash.swf live=1 buffer=300000 timeout=15 swfVfy=1 pageUrl=http://arabichannels.com'
					listItem = xbmcgui.ListItem(path=str(myfinalpath))
					xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
	
			

def retrieveChannel(url):
	if "youtube" in str(url):
		finalurl=str(url).split("v=")
		finalurl=finalurl[1]
		playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % finalurl
	elif "youtube" not in str(url):
		playback_url=url
	return playback_url
	
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
        indexChannels(url)
	
elif mode==2:
        print ""+url
        playChannel(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
