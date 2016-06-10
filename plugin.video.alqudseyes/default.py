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
	addDir(' 2016 مسلسلات رمضان  ','http://www.alqudseyes.com/series?sort=desc&category=78&sort_by=date&series=100&page=',2,'')

	addDir('مسلسلات تركية ','http://www.alqudseyes.com/series?sort=desc&category=19&sort_by=date&series=100&page=',2,'')
	addDir('مسلسلات عربية ','http://www.alqudseyes.com/series?sort=desc&category=20&sort_by=date&series=100&page=',2,'')
	addDir('مسلسلات مصرية ','http://www.alqudseyes.com/series?sort=desc&category=21&sort_by=date&series=100&page=',2,'')
	addDir('مسلسلات سورية ','http://www.alqudseyes.com/series?sort=desc&category=22&sort_by=date&series=100&page=',2,'')
	addDir('مسلسلات لبنانية ','http://www.alqudseyes.com/series?sort=desc&category=23&sort_by=date&series=100&page=',2,'')
	addDir('مسلسلات خليجية ','http://www.alqudseyes.com/series?sort=desc&category=24&sort_by=date&series=100&page=',2,'')
	addDir('مسلسلات كرتون ','http://www.alqudseyes.com/series?sort=desc&category=25&sort_by=date&series=100&page=',2,'')
	addDir('برامج ','http://www.alqudseyes.com/series?sort=desc&category=26&sort_by=date&series=100&page=',2,'')
	addDir('مسلسلات رمضان 2011 ','http://www.alqudseyes.com/series?sort=desc&category=27&sort_by=date&series=100&page=',2,'')
	addDir('مسلسلات رمضان 2012 ','http://www.alqudseyes.com/series?sort=desc&category=28&sort_by=date&series=100&page=',2,'')
	addDir('مسلسلات رمضان 2014 ','http://www.alqudseyes.com/series?sort=desc&category=30&sort_by=date&series=100&page=',2,'')
	addDir('مسلسلات مدبلجة ','http://www.alqudseyes.com/series?sort=desc&category=29&sort_by=date&series=100&page=',2,'')

	addDir('افلام دراما ','http://www.alqudseyes.com/movies?sort=desc&category=2&sort_by=date&movies=100&page=',1,'')
	addDir('افلام كوميديا ','http://www.alqudseyes.com/movies?sort=desc&category=3&sort_by=date&movies=100&page=',1,'')
	addDir('افلام رومانس وحب  ','http://www.alqudseyes.com/movies?sort=desc&category=4&sort_by=date&movies=100&page=',1,'')
	addDir('افلام اكشن ومغامرات ','http://www.alqudseyes.com/movies?sort=desc&category=5&sort_by=date&movies=100&page=',1,'')
	addDir('مسرحيات','http://www.alqudseyes.com/movies?sort=desc&category=6&sort_by=date&movies=100&page=',1,'')
	addDir('افلام اجتماعي','http://www.alqudseyes.com/movies?sort=desc&category=7&sort_by=date&movies=100&page=',1,'')
	addDir('افلام تركية ومدبلجة','http://www.alqudseyes.com/movies?sort=desc&category=11&sort_by=date&movies=100&page=',1,'')
	addDir('افلام الزمن القديم ','http://www.alqudseyes.com/movies?sort=desc&category=13&sort_by=date&movies=100&page=',1,'')
	addDir('افلام وثائقية ','http://www.alqudseyes.com/movies?sort=desc&category=14&sort_by=date&movies=100&page=',1,'')
	addDir('افلام عادل امام ','http://www.alqudseyes.com/movies?sort=desc&category=15&sort_by=date&movies=100&page=',1,'')
	addDir('افلام سورية ','http://www.alqudseyes.com/movies?sort=desc&category=16&sort_by=date&movies=100&page=',1,'')
	addDir('افلام مصرية ','http://www.alqudseyes.com/movies?sort=desc&category=17&sort_by=date&movies=100&page=',1,'')
	addDir('افلام هندية ','http://www.alqudseyes.com/movies?sort=desc&category=18&sort_by=date&movies=100&page=',1,'')



def listAlqudsFilmContent(url):

    try:
    	for i in range(1,6):
	    req = urllib2.Request(url+str(i))
	    response = urllib2.urlopen(req,timeout=1)
	    link=response.read()
	    target= re.findall(r'<article class="movie">(.*?)\s(.*?)<div class="grid-col">', link, re.DOTALL)

	    for items in target:
		for itr in items:
		   my_data = str(itr).split('</figure>')[0].split(' <figure class="movie-image">')
		   my_url = my_data[0].replace(' <a href="','').replace('">','').strip()

		   for i in my_data:
		       if ' <img src=' in i :
		            my_name =  i.split('alt="')[1].replace('">','').strip()
		            my_img =  i.split('alt="')[0].replace('<img src="','').replace('"','').strip()
			    print my_img

		            my_url =my_url.split('movies')
		            my_final_url = my_url[0]+'movies/watch'+my_url[1]
		            print my_name
		            print my_final_url
		            print my_img.strip()
			    addLink(my_name,my_final_url,3,my_img)
    except:
	pass

def listAlqudsSerieContent(url):
    try:
    	for i in range(1,6):
	    req = urllib2.Request(url+str(i))
	    response = urllib2.urlopen(req,timeout=1)
	    link=response.read()
	    target= re.findall(r'<article class="movie">(.*?)\s(.*?)<div class="grid-col">', link, re.DOTALL)

	    for items in target:
		for itr in items:
		   my_data = str(itr).split('</figure>')[0].split(' <figure class="movie-image">')
		   my_url = my_data[0].replace(' <a href="','').replace('">','').strip()

		   for i in my_data:
		       if ' <img src=' in i :
		            my_name =  i.split('alt="')[1].replace('">','').strip()
		            my_img =  i.split('alt="')[0].replace('<img src="','').replace('"','').strip()
			    try:
				name = str(name).split('<div')[0]
				
			    except:
				print 'exception caught'
			        pass
		            print my_name
		            print my_url
		            print my_img.strip()
			    addDir(my_name,my_url,4,my_img )
    except:
	pass

def getAlgudsSerie(url):

    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    target= re.findall(r'<div class="info-episodes">(.*?)\s(.*?)</div>', link, re.DOTALL)
    for items in target:
        for i in  items:
            if i !='':
                my_url_data = i.split('">')[0].replace('<h5><a href="','').strip()
                my_name_data = i.split('">')[1].replace('</a></h5>','').strip()
                my_url_data =my_url_data.split('series')
                my_final_url = my_url_data[0]+'series'+my_url_data[1]
                print my_name_data
                print my_final_url
		addLink(my_name_data,my_final_url,3,'')


def get_film_video_file(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    my_film =''
    target= re.findall(r'videoType:"HTML5",(.*?)\s(.*?)prerollAD:"yes",', link, re.DOTALL)
    for items in str(target).split(','):
        if "mp4:" in items:
            my_film= items.split('mp4:')[1].replace('"',"").strip()
    if my_film=='':
        target= re.findall(r'{ type: "video/mp4",(.*?)" }', link, re.DOTALL)

        my_film= target[0].split('src:')[1].replace('"',"").strip()

    
    listItem = xbmcgui.ListItem(path=str(my_film))
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
        listAlqudsFilmContent(url)
	
elif mode==2:
        print ""+url
        listAlqudsSerieContent(url)
elif mode==3:
        print ""+url
        get_film_video_file(url)
elif mode==4:
        print ""+url
        getAlgudsSerie(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
