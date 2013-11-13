# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import httplib
import time
from random import randint

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
	addDir('All Channels','http://arabichannels.com/',1,'http://arabichannels.com/images/general.jpg')
	
	
		
def indexChannels(url):
	req = urllib2.Request(url)
	req.add_header('Host', 'arabichannels.com')
	req.add_header('Cache-Control', 'max-age=0')
	req.add_header('Accept', ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36')
	req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
	req.add_header('Referer', 'http://arabichannels.com/')
	req.add_header('Accept-Language', 'sv,en-US;q=0.8,en;q=0.6,en-GB;q=0.4')
	req.add_header('Cookie', ' __qca=P0-131665082-1378312345646; HstCfa2398318=1378312346484; c_ref_2398318=http%3A%2F%2Fforum.xbmc.org%2Fshowthread.php%3Ftid%3D173949%26highlight%3Darabic; tzLogin=shgt7sskuulgi2fiuo88d19bv2; _pk_ref.1.c9f1=%5B%22%22%2C%22%22%2C1381342881%2C%22http%3A%2F%2Fforum.xbmc.org%2Fshowthread.php%3Ftid%3D173949%26highlight%3Darabic%22%5D; HstCmu2398318=1381342881259; MLRV_72398318=1381342891622; MLR72398318=1381342888000; __zlcmid=Kmd8axlKuhiHGM; HstCla2398318=1381343208529; HstPn2398318=3; HstPt2398318=17; HstCnv2398318=11; HstCns2398318=11; _pk_id.1.c9f1=fbf663c0b4b5b54e.1378312346.7.1381343209.1380731782.; _pk_ses.1.c9f1=*')

	response = urllib2.urlopen(req)
	link=response.read()
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
			if "ArabiChannels TV" not in str(name):
				addLink(name,path,2,image)
		
def playChannel(url):

	if ".php" in str(url):

		req = urllib2.Request(url)
		req.add_header('Host', 'arabichannels.com')
		req.add_header('Cache-Control', 'max-age=0')
		req.add_header('Accept', ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
		req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36')
		req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
		req.add_header('Referer', 'http://arabichannels.com/')
		req.add_header('Accept-Language', 'sv,en-US;q=0.8,en;q=0.6,en-GB;q=0.4')
		req.add_header('Cookie', ' __qca=P0-131665082-1378312345646; HstCfa2398318=1378312346484; c_ref_2398318=http%3A%2F%2Fforum.xbmc.org%2Fshowthread.php%3Ftid%3D173949%26highlight%3Darabic; tzLogin=shgt7sskuulgi2fiuo88d19bv2; _pk_ref.1.c9f1=%5B%22%22%2C%22%22%2C1381342881%2C%22http%3A%2F%2Fforum.xbmc.org%2Fshowthread.php%3Ftid%3D173949%26highlight%3Darabic%22%5D; HstCmu2398318=1381342881259; MLRV_72398318=1381342891622; MLR72398318=1381342888000; __zlcmid=Kmd8axlKuhiHGM; HstCla2398318=1381343208529; HstPn2398318=3; HstPt2398318=17; HstCnv2398318=11; HstCns2398318=11; _pk_id.1.c9f1=fbf663c0b4b5b54e.1378312346.7.1381343209.1380731782.; _pk_ses.1.c9f1=*')
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
		mynr1=randint(10,20)
		mynr2=randint(0,10)
		mynr3=randint(100,900)
		
		mynr=randint(10000,500000)
		complete=streamer +'/'+fileLoc+ ' swfUrl=http://arabichannels.com' + swf + ' playpath=' + fileLoc +  ' flashVer='+str(mynr1)+'.'+str(mynr2)+'.'+str(mynr3)+' live=1 swfVfy=true pageUrl='+str(url)
		listItem = xbmcgui.ListItem(path=str(complete))
		xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
		
	elif ".html" in str(url):
        
			myfinalpath=' '
			req = urllib2.Request(url)
			req.add_header('Host', 'arabichannels.com')
			req.add_header('Cache-Control', 'max-age=0')
			req.add_header('Accept', ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
			req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36')
			req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
			req.add_header('Referer', 'http://arabichannels.com/')
			req.add_header('Accept-Language', 'sv,en-US;q=0.8,en;q=0.6,en-GB;q=0.4')
			#req.add_header('Cookie', ' __qca=P0-131665082-1378312345646; HstCfa2398318=1378312346484; c_ref_2398318=http%3A%2F%2Fforum.xbmc.org%2Fshowthread.php%3Ftid%3D173949%26highlight%3Darabic; tzLogin=shgt7sskuulgi2fiuo88d19bv2; _pk_ref.1.c9f1=%5B%22%22%2C%22%22%2C1381342881%2C%22http%3A%2F%2Fforum.xbmc.org%2Fshowthread.php%3Ftid%3D173949%26highlight%3Darabic%22%5D; HstCmu2398318=1381342881259; MLRV_72398318=1381342891622; MLR72398318=1381342888000; __zlcmid=Kmd8axlKuhiHGM; HstCla2398318=1381343208529; HstPn2398318=3; HstPt2398318=17; HstCnv2398318=11; HstCns2398318=11; _pk_id.1.c9f1=fbf663c0b4b5b54e.1378312346.7.1381343209.1380731782.; _pk_ses.1.c9f1=*')
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
