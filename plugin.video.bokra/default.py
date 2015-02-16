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
	#xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('WARNING','This addon is completely FREE DO NOT buy any products from http://tvtoyz.com/', 16000, 'http://upload.wikimedia.org/wikipedia/he/b/b1/Bokra.net_logo.jpg'))
	addDir('مسلسلات رمضان 2014','http://www.bokra.net/VideoCategory/127/%D8%B1%D9%85%D8%B6%D8%A7%D9%86_2014.html',1,'http://images.bokra.net/bokra//28-11-2010/4shobek.jpg')
	addDir('مسلسلات رمضان 2013','http://www.bokra.net/VideoCategory/125/مسلسلات_رمضان_2013.html',1,'http://images.bokra.net/bokra//28-11-2010/4shobek.jpg')
	addDir('مسلسلات عربية','http://www.bokra.net/VideoCategory/98/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9.html',1,'http://images.bokra.net/bokra//28-11-2010/4shobek.jpg')
	addDir('مسلسلات متنوعة','http://www.bokra.net/VideoCategory/43/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA.html',1,'http://images.bokra.net/bokra//28-11-2010/4shobek.jpg')
	addDir('افلام عربية','http://www.bokra.net/VideoCategory/100/أفلام_عربية.html',4,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg')
	addDir(' افلام فلسطينية','http://www.bokra.net/VideoCategory/18/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D9%81%D9%84%D8%B3%D8%B7%D9%8A%D9%86%D9%8A%D8%A9.html',4,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg')
	addDir('افلام وثائقيه','http://www.bokra.net/VideoCategory/23/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A%D8%A9.html',4,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg')
	addDir('افلام قديمة','http://www.bokra.net/VideoCategory/51/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D9%82%D8%AF%D9%8A%D9%85%D8%A9.html',4,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg')
	addDir('افلام دينية','http://www.bokra.net/VideoCategory/24/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%AF%D9%8A%D9%86%D9%8A%D8%A9.html',4,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg')
	addDir('مسرحيات','http://www.bokra.net/VideoCategory/44/%D9%85%D8%B3%D8%B1%D8%AD%D9%8A%D8%A7%D8%AA.html',4,'http://images.bokra.net/bokra/25.10.2011/msr7//DSCF0480.jpg')
	addDir('كليبات وحفلات','http://www.bokra.net/VideoCategory/118/%D9%83%D9%84%D9%8A%D8%A8%D8%A7%D8%AA_%D9%88%D8%AD%D9%81%D9%84%D8%A7%D8%AA.html',4,'http://images.bokra.net/new/402839.jpg')
	addDir('برامج تلفزيونية','http://www.bokra.net/VideoCategory/39/%D8%A8%D8%B1%D8%A7%D9%85%D8%AC_%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86.html',1,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg')
	addDir('افلام اطفال ','http://www.bokra.net/VideoCategory/57/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%A7%D8%B7%D9%81%D8%A7%D9%84.html',4,'http://images.bokra.net/bokra/15.8.2012/kods//1231.JPG')
	addDir('بكرا TV','http://www.bokra.net/VideoCategory/113/%D8%A8%D9%83%D8%B1%D8%A7_TV.html',1,'http://www.bokra.net/images//logobokra.png')
	addDir('مسلسلات كرتون','http://www.bokra.net/VideoCategory/56/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA_%D9%83%D8%B1%D8%AA%D9%88%D9%86.html',1,'http://images.bokra.net/bokra//16-10-2011/0WeddingCartoon1.jpg')
	addDir('مسلسلات اجنبية','http://www.bokra.net/VideoCategory/93/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA_%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9.html',1,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg')
	addDir('مسلسلات تركية','http://www.bokra.net/VideoCategory/27/مسلسلات_تركية_.html',1,'http://images.bokra.net/bokra//28-11-2010/4shobek.jpg')
	addDir('افلام تركية','http://www.bokra.net/VideoCategory/48/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%AA%D8%B1%D9%83%D9%8A%D8%A9.html',4,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg')
	addDir('افلام اجنبية','http://www.bokra.net/VideoCategory/46/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9.html',4,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg')
	addDir('منوعات','http://www.bokra.net/VideoCategory/45/%D9%85%D9%86%D9%88%D8%B9%D8%A7%D8%AA_+.html',3,'http://images.bokra.net/bokra//25-11-2012/0777777.jpg')

def get_max_pages(url):
    max_pages = 1
    try:
	    url = url.replace(' ', '%20')
	    req = urllib2.Request(url)
	    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	    response = urllib2.urlopen(req)
	    link=response.read()
	    max_pag = re.compile('<span class="curpage"(.+?)</div>').findall(link)
	    max_pag= str(max_pag)

	    my_integers = []
	    for itr in (max_pag.split('<a class="number"')):

		if '.html' and '</a>' in itr:

		    myitem = (str(itr).split('.html/')[1]).split('"')[0]
		    my_integers.append(int(myitem))

	    max_pages= max(my_integers)
    except:
	   pass
	   max_pages= 1
    return max_pages	


def get_series(url):
    url = url.replace(' ', '%20')
    base_url = url
    max_pages = get_max_pages(base_url)
    for i in range(1,max_pages):
        url = base_url+'/'+str(i)

        print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        matchSerie = re.compile('<div class="video_box"(.+?)"/></a>', re.DOTALL).findall(link)
        try:
            for items in  matchSerie:
                path = (str( items).split('" onClick=')[0]).split('href="')[1]
                image = (str( items).split('data-original="')[1]).split('" width=')[0]
                title = str(items).split('title="')[1]
                addDir(title,path.strip(),2,image)
                
        except:
            pass


def get_epos(url):
    url = url.replace(' ', '%20')
    base_url = url
    
    try:
	
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	matchSerie = re.compile('<div class="video_box"(.+?)"/></a>', re.DOTALL).findall(link)
	for items in  matchSerie:
		path = (str( items).split('" onClick=')[0]).split('href="')[1]
		image = (str( items).split('data-original="')[1]).split('" width=')[0]
		title = str(items).split('title="')[1]
		addLink(title,path,3,image)
    except:
	pass
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('تنبيه','الحلقات غير متوفرة حاليا حاول لاحقا', 16000, 'http://upload.wikimedia.org/wikipedia/he/b/b1/Bokra.net_logo.jpg'))


def get_films(url):
    url = url.replace(' ', '%20')
    base_url = url
    max_pages = get_max_pages(base_url)
    try:

	    for i in range(0,max_pages):
		    url = base_url+'/'+str(i)
		    req = urllib2.Request(url)
		    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		    response = urllib2.urlopen(req)
		    link=response.read()
		    matchSerie = re.compile('<div class="video_box"(.+?)"/></a>', re.DOTALL).findall(link)

		    for items in  matchSerie:
			path = (str( items).split('" onClick=')[0]).split('href="')[1]
			image = (str( items).split('data-original="')[1]).split('" width=')[0]
			title = str(items).split('title="')[1]
			addLink(title,path,3,image)
    except:
	pass
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('تنبيه','الحلقات غير متوفرة حاليا حاول لاحقا', 16000, 'http://upload.wikimedia.org/wikipedia/he/b/b1/Bokra.net_logo.jpg'))


def get_video_file(url):
    url = url.replace(' ', '%20')
    try:
	    req = urllib2.Request(url)
	    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	    response = urllib2.urlopen(req)
	    link=response.read()
	    flash_path = re.compile('<iframe class="video_frame" src="(.+?)"').findall(link)
	    req_video = urllib2.Request(flash_path[0])

	    response_video = urllib2.urlopen(req_video)
	    link_video=response_video.read()
	    my_data = (link_video.split("jwplayer('nadPlayer').setup({")[1]).split(' "shows": {')[0]
	    for itr in  my_data.split(','):

		if 'file' in itr:
		    file_name = (str(itr).split('file": "')[1]).replace('"','').strip()


	    my_video_url = 'rtmp://vod.bokra.net:1935/vod/_definst_/ playpath='+file_name+' swfUrl=http://bokra.net/inc/player/jwplayer5.swf pageURL='+url+' swfVfy=true timeout=90'

#my_video_url = 'rtmp://vod.bokra.net:1935/vod/_definst_/ playpath='+file_name+' swfUrl=http://bokra.net/inc/player/jwplayer5.swf pageURL='+url+' swfVfy=true'
	    listItem = xbmcgui.ListItem(path=str(my_video_url))
	    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    except:
	pass
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('تنبيه','الفيديو غير متوفر حاليا حاول لاحقا', 16000, 'http://upload.wikimedia.org/wikipedia/he/b/b1/Bokra.net_logo.jpg'))

			

	
	
	

def checkURL(url):
    p = urlparse(url)
    h = HTTP(p[1])
    h.putrequest('HEAD', p[2])
    h.endheaders()
    if h.getreply()[0] == 200: return 1
    else: return 0

                
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
        get_series(url)
	
elif mode==2:
	print ""+url
	get_epos(url)

elif mode==3:
	print ""+url
	get_video_file(url)
elif mode==4:
	print ""+url
	get_films(url)
			

xbmcplugin.endOfDirectory(int(sys.argv[1]))
