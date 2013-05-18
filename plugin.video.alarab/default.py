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


__settings__ = xbmcaddon.Addon(id='plugin.video.alarab')
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
	addDir('مسلسلات عربية','http://tv1.alarab.net/view-1_%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9_8',1,'http://www.alfnnews.com/files/pic/2012/5/19/2012561916144-alarb.gif')
	addDir('افلام عربية','http://tv1.alarab.net/view-1_%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9_1',4,'http://www.alfnnews.com/files/pic/2012/5/19/2012561916144-alarb.gif')
	addDir('افلام كرتون','http://tv1.alarab.net/view-1_%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%83%D8%B1%D8%AA%D9%88%D9%86_295',4,'http://www.alfnnews.com/files/pic/2012/5/19/2012561916144-alarb.gif')
	addDir('فيديو كليب','http://tv1.alarab.net/view-1_%D9%81%D9%8A%D8%AF%D9%8A%D9%88-%D9%83%D9%84%D9%8A%D8%A8_10',4,'http://www.alfnnews.com/files/pic/2012/5/19/2012561916144-alarb.gif')
	addDir('برامج تلفزيون','http://tv1.alarab.net/view-1_%D8%A8%D8%B1%D8%A7%D9%85%D8%AC-%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86_311',1,'http://www.alfnnews.com/files/pic/2012/5/19/2012561916144-alarb.gif')
	addDir('مسلسلات كرتون','http://tv1.alarab.net/view-1_%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%83%D8%B1%D8%AA%D9%88%D9%86_4',1,'http://www.alfnnews.com/files/pic/2012/5/19/2012561916144-alarb.gif')
	addDir('مسلسلات تركية','http://tv1.alarab.net/view-1_%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%AA%D8%B1%D9%83%D9%8A%D8%A9_299',1,'http://www.alfnnews.com/files/pic/2012/5/19/2012561916144-alarb.gif')
	addDir('مسلسلات اجنبية','http://tv1.alarab.net/view-1_%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9_1951',1,'http://www.alfnnews.com/files/pic/2012/5/19/2012561916144-alarb.gif')
	addDir('افلام هندية','http://tv1.alarab.net/view-1_افلام-هندية_297',4,'http://www.alfnnews.com/files/pic/2012/5/19/2012561916144-alarb.gif')
	addDir('افلام اجنبية','http://tv1.alarab.net/view-1_%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9_5553',4,'http://www.alfnnews.com/files/pic/2012/5/19/2012561916144-alarb.gif')
	addDir('مقاطع مضحكة ','http://tv1.alarab.net/view-1_%D9%85%D9%82%D8%A7%D8%B7%D8%B9-%D9%85%D8%B6%D8%AD%D9%83%D8%A9_309',4,'http://www.alfnnews.com/files/pic/2012/5/19/2012561916144-alarb.gif')
	addDir('مسرحيات','http://tv1.alarab.net/view-1_%D9%85%D8%B3%D8%B1%D8%AD%D9%8A%D8%A7%D8%AA_313',4,'http://www.alfnnews.com/files/pic/2012/5/19/2012561916144-alarb.gif')
	
	
	
	
def checkURL(url):
    p = urlparse(url)
    h = HTTP(p[1])
    h.putrequest('HEAD', p[2])
    h.endheaders()
    if h.getreply()[0] == 200: return 1
    else: return 0


def index_series(url):
	try:
		url_mod=url
		url_mod=url_mod.split("_")
		
		for items in url_mod:
			mooded= str( url_mod[0]).split("-")
			for elements in mooded:
				second= mooded[0]
				first= mooded[1]
		
		for i in range(1,20):
		
			result_url=second+"-"+str(i)+"_"+url_mod[1]+"_"+url_mod[2]
			req = urllib2.Request(result_url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			link=response.read()
			url_ch=(re.compile('<img src="(.+?)" alt="(.+?)"  />').findall(link))
			url_ch_2=(re.compile('<a href="(.+?)" title="').findall(link))
			final_series=[]
			response.close()
			for items in url_ch_2:
				if "series" in items:
					if items not in final_series:
						final_series.append(items)
			for items,elements in itertools.izip(url_ch,final_series):
				image= items[0]
				name= items [1]
				url_serie=elements
				#print name
				#print "http://tv1.alarab.net"+url_serie
				addDir(name,"http://tv1.alarab.net"+str(url_serie),2,image)
	except Exception:
		print "Exception in index_series "

def list_eposodes(url):
    try:
		for counter in range(1,8):
			req = urllib2.Request(url+"_"+str(counter))
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			link=response.read()
			url_ch=(re.compile('<a href="(.+?)" title="(.+?)" class="vd_title">').findall(link))
			response.close()
			item_list=[]
			for items in url_ch:
				for element in items:
					if items[1] not in item_list:
						
						name= str(items[1])
						name=name.replace("تحميل", "")
						name=name.replace("مسلسل", "")
						name=name.replace("مدبلجة", "")
						name=name.replace("مدبلجة", "")
						name=name.replace("بالعربية", "")
						name=name.replace("لاين", "")
						name=name.replace("كاملة", "")
						name=name.replace("مدبلجة", "")
						name=name.replace("مترجم", "")
						name=name.replace("فيلم", "")
						name=name.replace("dvd", "")
						name=name.replace("لابن", "")
						name=name.replace("مشاهدة", "")
						name=name.replace("اونلاين", "")
						name=name.replace("بجودة", "")
						name=name.replace("عالية", "")
						name=name.replace("مباشرة", "")
						name=name.replace("على", "")
						name=name.replace("العرب", "")
						name=name.replace("تحميل", "")
						name=name.replace("جودة", "")
						name=name.replace("كامل", "")
						name=name.replace("بدون", "")
						name=name.replace("اون", "")
						name=name.replace("كواليتي", "")
						name=name.strip()
						
						#print name
						#print items[0]
						addLink(name,"http://tv1.alarab.net"+str(items[0]),3,"")
						item_list.append(items[1])
    except Exception:
		print "Exception in list_epos "
					
def list_films(url):
	try:
		url_mod=url
		url_mod=url_mod.split("_")
		
		for items in url_mod:
			mooded= str( url_mod[0]).split("-")
			for elements in mooded:
				second= mooded[0]
				first= mooded[1]
		
		for i in range(1,20):
		
			result_url=second+"-"+str(i)+"_"+url_mod[1]+"_"+url_mod[2]
			req = urllib2.Request(result_url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
			url_ch=(re.compile('<a href="(.+?)" title="(.+?)dvd اونلاين ">').findall(link))
			url_ch_2=(re.compile('<img src="(.+?)" alt="(.+?)"  />').findall(link))
			 
			for items,elements in itertools.izip( url_ch,url_ch_2):
				#print items[1]
				name=str( items[1]).replace("جودة", "")
				name=name.replace("مشاهدة", "").strip()
				name=name.replace("dvd", "")
				name=name.replace("فيلم", "")
				name=name.replace("لاين", "")
				name=name.replace("اون", "")
				name=name.replace("اونلاين", "")
				name=name.replace("بجودة", "")
				name=name.replace("عالية", "")
				name=name.replace("مباشرة", "")
				name=name.replace("على", "")
				name=name.replace("العرب", "")
				name=name.replace("تحميل", "")
				name=name.replace("جودة", "")
				name=name.replace("كواليتي", "")
				name=name.replace("بدون", "")
				name=name.replace("كامل", "")
				name=name.strip()
				print name
				print items[0]
				print elements[0]
				addLink(name,"http://tv1.alarab.net"+str(items[0]),3,elements[0])
	except Exception:
		print "Exception in list_films "
	
				

def get_epos_video(url,name):
	try:
		url=str(url).split("_")
    
		tnumber=str( url[0])
		tnumber=tnumber.replace("http://tv1.alarab.net/viewVedio/","")
		tnumber=tnumber.replace("http://tv1.alarab.net/v", "")
		tnumber=tnumber.replace("-", "").strip()
		tnumber="http://alarabplayers.alarab.net/test.php?vid="+tnumber
		
		req = urllib2.Request(tnumber)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		
		response.close()
		url_ch=(re.compile("'file': '(.+?)',").findall(link))
		url_ch=str(url_ch).replace("['", "")
		video=str(url_ch).replace("']", "").strip()
		
		image=(re.compile("'image': '(.+?)',").findall(link))
		image=str(image).replace("['", "")
		image=str(image).replace("']", "").strip()
		
		print video
		print image
		if "www.youtube" in video:
			video=video.split("v=")
			print "youtube after split: "+str(video)
			video_id=str(video[1])
			video_id=video_id.replace(".flv","").strip()
			print "first item of youtube: "+str(video_id)
			playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id
			
			listItem = xbmcgui.ListItem(path=str(playback_url))
			xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
			
			
				
		else:
			listItem = xbmcgui.ListItem(path=str(video))
			xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
			
	except Exception:
		print "Exception in get_epos_video "
			
	

	
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




def addLinkOLD(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

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
        index_series(url)
	
elif mode==2:
        print ""+url
        list_eposodes(url)
elif mode==3:
		get_epos_video(url,name)
elif mode==4:
		list_films(url)

	

xbmcplugin.endOfDirectory(int(sys.argv[1]))
