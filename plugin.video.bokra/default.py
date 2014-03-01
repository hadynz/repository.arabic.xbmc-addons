# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import urllib2,urllib
import re
import httplib
import time
import xbmcgui
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import cookielib
import datetime
import socket

socket.setdefaulttimeout(60)
__settings__ = xbmcaddon.Addon(id='plugin.video.bokra')
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
	addDir('مسلسلات رمضان 2013','http://www.bokra.net/VideoCategory/125/مسلسلات_رمضان_2013.html',1,'http://images.bokra.net/bokra//28-11-2010/4shobek.jpg','http://bokra1-id.appspot.com/SignIndexNewSeries')
	addDir('مسلسلات عربية','http://www.bokra.net/VideoCategory/98/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9.html',5,'http://images.bokra.net/bokra//28-11-2010/4shobek.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir('مسلسلات متنوعة','http://www.bokra.net/VideoCategory/43/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA.html',5,'http://images.bokra.net/bokra//28-11-2010/4shobek.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir('افلام عربية','http://www.bokra.net/VideoCategory/100/أفلام_عربية.html',3,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir(' افلام فلسطينية','http://www.bokra.net/VideoCategory/18/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D9%81%D9%84%D8%B3%D8%B7%D9%8A%D9%86%D9%8A%D8%A9.html',3,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir('افلام وثائقيه','http://www.bokra.net/VideoCategory/23/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A%D8%A9.html',3,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir('افلام قديمة','http://www.bokra.net/VideoCategory/51/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D9%82%D8%AF%D9%8A%D9%85%D8%A9.html',3,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir('افلام دينية','http://www.bokra.net/VideoCategory/24/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%AF%D9%8A%D9%86%D9%8A%D8%A9.html',3,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir('مسرحيات','http://www.bokra.net/VideoCategory/44/%D9%85%D8%B3%D8%B1%D8%AD%D9%8A%D8%A7%D8%AA.html',3,'http://images.bokra.net/bokra/25.10.2011/msr7//DSCF0480.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir('كليبات وحفلات','http://www.bokra.net/VideoCategory/118/%D9%83%D9%84%D9%8A%D8%A8%D8%A7%D8%AA_%D9%88%D8%AD%D9%81%D9%84%D8%A7%D8%AA.html',3,'http://images.bokra.net/new/402839.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir('برامج تلفزيونية','http://www.bokra.net/VideoCategory/39/%D8%A8%D8%B1%D8%A7%D9%85%D8%AC_%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86.html',5,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir('افلام اطفال ','http://www.bokra.net/VideoCategory/57/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%A7%D8%B7%D9%81%D8%A7%D9%84.html',3,'http://images.bokra.net/bokra/15.8.2012/kods//1231.JPG','http://bokra1-id.appspot.com/signIndex')
	addDir('بكرا TV','http://www.bokra.net/VideoCategory/113/%D8%A8%D9%83%D8%B1%D8%A7_TV.html',5,'http://www.bokra.net/images//logobokra.png','http://bokra1-id.appspot.com/signIndex')
	addDir('مسلسلات كرتون','http://www.bokra.net/VideoCategory/56/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA_%D9%83%D8%B1%D8%AA%D9%88%D9%86.html',5,'http://images.bokra.net/bokra//16-10-2011/0WeddingCartoon1.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir('مسلسلات اجنبية','http://www.bokra.net/VideoCategory/93/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA_%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9.html',5,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir('مسلسلات تركية','http://www.bokra.net/VideoCategory/27/مسلسلات_تركية_.html',5,'http://images.bokra.net/bokra//28-11-2010/4shobek.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir('افلام تركية','http://www.bokra.net/VideoCategory/48/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%AA%D8%B1%D9%83%D9%8A%D8%A9.html',3,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir('افلام اجنبية','http://www.bokra.net/VideoCategory/46/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9.html',3,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg','http://bokra1-id.appspot.com/signIndex')
	addDir('منوعات','http://www.bokra.net/VideoCategory/45/%D9%85%D9%86%D9%88%D8%B9%D8%A7%D8%AA_+.html',3,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg','http://bokra1-id.appspot.com/signIndex')

def lisBokraCont(url,mode,func):
    post_params = {
    'content' : url
        }
    post_args = urllib.urlencode(post_params)
    url = func
    fp = urllib2.urlopen(url, post_args)
    soup = fp.read()
    url_ch=(re.compile('<p>(.+?)</p>').findall(soup))
    for items in url_ch:
		if mode==1:
			myTarget = str(items).split(',')
			name =str(myTarget[0]).strip()
			myUrl =str( myTarget[1]).strip()
			myImage =str( myTarget[2]).strip()
			addDir(name,myUrl,2,myImage,'http://bokra1-id.appspot.com/signBokraEpis')
		if mode==5:
			myTarget = str(items).split(',')
			name =str(myTarget[0]).strip()
			myUrl =str( myTarget[1]).strip()
			myImage =str( myTarget[2]).strip()
			addDir(name,myUrl,2,myImage,'http://bokra1-id.appspot.com/signBokraNewEpisodes')
			
		if mode==3:
			myTarget = str(items).split(',')
			name =str(myTarget[0]).strip()
			myUrl =str( myTarget[1]).strip()
			myImage =str( myTarget[2]).strip()
			addLink(name,myUrl,4,myImage,'http://bokra1-id.appspot.com/sign/')
			


def listRamadanEpos(url,func):
	post_params = {'content' : url}
	post_args = urllib.urlencode(post_params)
	url = func
	fp = urllib2.urlopen(url, post_args)
	soup = fp.read()
	url_ch=(re.compile('<p>(.+?)</p>').findall(soup))
	
	for items in url_ch:
		myTarget = str(items).split(',')
		name =str(myTarget[0]).strip()
		myUrl =str( myTarget[1]).strip()
		try:
			myImage =str( myTarget[2]).strip()
		except:
			myImage=""
			pass
		addLink(name,myUrl,4,myImage,'http://bokra1-id.appspot.com/sign/')
		

def playEposCont(url,func):
	post_params = {'content' : url}
	post_args = urllib.urlencode(post_params)
	url = func
	fp = urllib2.urlopen(url, post_args)
	soup = fp.read()
	url_ch=(re.compile('<p>(.+?)</p>').findall(soup))
	url_ch=url_ch[0]
	listItem = xbmcgui.ListItem(path=str(str(url_ch).strip()))
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



def addLink(name,url,mode,iconimage,func=""):
    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&func="+str(func)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty("IsPlayable","true");
    ok=xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=False)
    return ok
	


def addDir(name,url,mode,iconimage,func=""):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&func="+str(func)
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
        func=urllib.unquote_plus(params["func"])
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
       
elif mode==1 or mode==3 or mode==5:
        print ""+url
        lisBokraCont(url,mode,func)
elif mode==2:
	print ""+url
	listRamadanEpos(url,func)
	
elif mode==4:
	print ""+url
	playEposCont(url,func)
	

xbmcplugin.endOfDirectory(int(sys.argv[1]))
