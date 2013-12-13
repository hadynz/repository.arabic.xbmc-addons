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

__settings__ = xbmcaddon.Addon(id='plugin.video.alqudseyes')
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
	#xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('WARNING','This addon is completely FREE DO NOT buy any products from http://tvtoyz.com/', 16000, 'https://pbs.twimg.com/profile_images/1124212894/qudseyes.jpg'))
	addDir('افلام','http://aflam.alqudseyes.com/',1,'http://aflam.alqudseyes.com/site_images/aqe_logo_new.png')
	addDir('مسلسلات','http://mosalsalat.alqudseyes.com/',2,'http://mosalsalat.alqudseyes.com/site_images/aqe_logo_new.png')
	addDir('برامج تلفزيون','http://mosalsalat.alqudseyes.com/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/%D8%A8%D8%B1%D8%A7%D9%85%D8%AC-%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86/c8',2,'http://mosalsalat.alqudseyes.com/site_images/aqe_logo_new.png')
	addDir('مسلسلات تركية','http://mosalsalat.alqudseyes.com/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%AA%D8%B1%D9%83%D9%8A%D8%A9/c1',2,'http://mosalsalat.alqudseyes.com/site_images/aqe_logo_new.png')
	addDir('مسلسلات خليجية','http://mosalsalat.alqudseyes.com/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%AE%D9%84%D9%8A%D8%AC%D9%8A%D8%A9/c6',2,'http://mosalsalat.alqudseyes.com/site_images/aqe_logo_new.png')
	addDir('مسلسلات رمضان 2011','http://mosalsalat.alqudseyes.com/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B1%D9%85%D8%B6%D8%A7%D9%86-2011/c10',2,'http://mosalsalat.alqudseyes.com/site_images/aqe_logo_new.png')
	addDir('مسلسلات رمضان 2012','http://mosalsalat.alqudseyes.com/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B1%D9%85%D8%B6%D8%A7%D9%86-2012/c11',2,'http://mosalsalat.alqudseyes.com/site_images/aqe_logo_new.png')
	addDir('مسلسلات سورية','http://mosalsalat.alqudseyes.com/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B3%D9%88%D8%B1%D9%8A%D8%A9/c4',2,'http://mosalsalat.alqudseyes.com/site_images/aqe_logo_new.png')
	addDir('مسلسلات كارتون','http://mosalsalat.alqudseyes.com/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%83%D8%A7%D8%B1%D8%AA%D9%88%D9%86/c7',2,'http://mosalsalat.alqudseyes.com/site_images/aqe_logo_new.png')
	addDir('مسلسلات لبنانية','http://mosalsalat.alqudseyes.com/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%84%D8%A8%D9%86%D8%A7%D9%86%D9%8A%D8%A9/c5',2,'http://mosalsalat.alqudseyes.com/site_images/aqe_logo_new.png')
	addDir('مسلسلات مدبلجة','http://mosalsalat.alqudseyes.com/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%85%D8%AF%D8%A8%D9%84%D8%AC%D8%A9/c12',2,'http://mosalsalat.alqudseyes.com/site_images/aqe_logo_new.png')
	addDir('مسلسلات مصرية','http://mosalsalat.alqudseyes.com/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%85%D8%B5%D8%B1%D9%8A%D8%A9/c9',2,'http://mosalsalat.alqudseyes.com/site_images/aqe_logo_new.png')
	
def checkURL(url):
    p = urlparse(url)
    h = HTTP(p[1])
    h.putrequest('HEAD', p[2])
    h.endheaders()
    if h.getreply()[0] == 200: return 1
    else: return 0
	

def listEpos(url):
    
   
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    target= re.findall(r'<div class="thumbnail">(.*?)\s(.*?)<h2 class="itemtitle">', link, re.DOTALL)
    response.close()
    for items in  target:
        mytarg=str( items[1]).split('" width="150" height="225" /><br />')
        mytarg=str( mytarg[0]).strip()
        mytarg=str( mytarg).split('">')
        name_and_path=str(mytarg[0]).replace('<a title="', '')
            #print name_and_path
        thumb=str(mytarg[1]).replace('<img src="', '').strip()
        thumb=(str(thumb).split('" width="150"'))[0]
        name=str((str( name_and_path).split(" href="))[0]).replace('"', '').strip()
        path=str((str( name_and_path).split(" href="))[1]).replace('"', '').strip()
            #print path
        path='http://mosalsalat.alqudseyes.com'+path
        thumb='http://mosalsalat.alqudseyes.com'+thumb
        print name
        print path
        addLink(name,path,3,thumb)
		
def getAllFilms(url,videoType):
    
    my_url=url
    for i in range(0,40):
        url=my_url+"/page/"+str(i)
    
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        target= re.findall(r'<div class="thumbnail">(.*?)\s(.*?)<h2 class="itemtitle">', link, re.DOTALL)
        response.close()
        for items in  target:
            mytarg=str( items[1]).split('" width="150" height="225" /><br />')
            mytarg=str( mytarg[0]).strip()
            mytarg=str( mytarg).split('">')
            name_and_path=str(mytarg[0]).replace('<a title="', '')
            #print name_and_path
            thumb=str(mytarg[1]).replace('<img src="', '').strip()
            name=str((str( name_and_path).split(" href="))[0]).replace('"', '').strip()
            path=str((str( name_and_path).split(" href="))[1]).replace('"', '').strip()
            #print path
            if videoType=='film':
				path='http://aflam.alqudseyes.com'+path
				thumb='http://aflam.alqudseyes.com'+thumb
				addLink(name,path,3,thumb)
                
            elif videoType=='mosalsal':
				path='http://mosalsalat.alqudseyes.com'+path
				thumb='http://mosalsalat.alqudseyes.com'+thumb
				addDir(name,path,4,thumb)
           


	
def get_film_video_file(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
   
	url_ch=str(re.compile("'file': '(.+?)',").findall(link))
	url_ch=url_ch.replace("['", "")
	url_ch=url_ch.replace("']", "").strip()
    #rtmp://media.alqudseyes.com/vod/ swfUrl=http://mosalsalat.alqudseyes.com/player/jw6/jwplayer.flash.swf playpath=mp4:/series/Tarabish/E003.m4v
	url_ch=str(url_ch).split('mp4:')
    
	url_ch=url_ch[0]+' swfUrl=http://mosalsalat.alqudseyes.com/player/jw6/jwplayer.flash.swf playpath=mp4:'+url_ch[1]
	#url_ch='http://assets.delvenetworks.com/player/loader.swf?playerForm=64fc5d4a5f47400fac523fba125a8de8&&mediaId=92bb83bb29d145d99b057cb8ef7d3020&&defaultQuality=Download&amp;allowHttpDownload=true&amp;pdBitrate=224&amp;allowSharePanel=true&amp;allowEmbed=true'
	listItem = xbmcgui.ListItem(path=str(url_ch))
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

from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
try:
    import json
except:
    import simplejson as json
	
	
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
        getAllFilms(url,'film')
	
elif mode==2:
        print ""+url
        getAllFilms(url,'mosalsal')
elif mode==3:
        print ""+url
        get_film_video_file(url)
elif mode==4:
        print ""+url
        listEpos(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
