# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import httplib
import time,itertools



__settings__ = xbmcaddon.Addon(id='plugin.video.rotana')
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
	addDir('مسلسلات','http://khalijia.rotana.net/r/tv-series?page=',1,'https://sphotos-a-ord.xx.fbcdn.net/hphotos-ash4/p206x206/406270_444278592272780_2031707310_n.jpg')
	addDir('برامج','http://khalijia.rotana.net/r/tv-shows?page=',1,'https://sphotos-a-ord.xx.fbcdn.net/hphotos-ash4/p206x206/406270_444278592272780_2031707310_n.jpg')
	addDir('افلام','http://cinema.rotana.net/r/movies-asc?page=',2,'http://img809.imageshack.us/img809/5535/rotana.jpg')
	addDir('موسيقا','http://mousica.rotana.net/r/clips?page=',5,'http://www.arabasl.com/pic/rotana_mousica.png')
	
	
		
def indexSeries(url):
            page=0
            try:
                for i in range(0,40):
                    page=page+1
                    req = urllib2.Request(url+str(page))
                    response = urllib2.urlopen(req)
                    link=response.read()
                    matchObj=(re.compile('<a href="(.+?)" class="pull-left item"><img src="(.+?)"><h2 class="site_color">(.+?)</h2><span class="viewFull">').findall(link))
                    for items in matchObj:
                        name=str( items[2]).strip()
                        path='http://khalijia.rotana.net'+str( items[0]).strip()
                        thumbnail=str( items[1]).strip()
                        print name
                        print path
                        addDir(name,path,3,thumbnail)
            except:
                pass
	

def indexFilms(url):
            
            page=0
            try:
                for i in range(0,40):
                    page=page+1
                    req = urllib2.Request(url+str(page))
                    response = urllib2.urlopen(req)
                    link=response.read()
                    matchObj= re.findall(r'<div class="carousel-item pull-left ">(.*?)\s(.*?)<div class="overlay-text">(.*?)</div>', link, re.DOTALL)
                    for items in matchObj:
                        thum_film=str( items[1]).split('<a href="')
                        thumb=str(thum_film[0]).replace('<img src="', '').replace('" width="150" height="190">', '').strip()
                        path=str(thum_film[1]).replace('"></a>', '').strip()
                        path=str(path).split('" class="click-layer')
                        path="http://cinema.rotana.net"+str(path[0]).strip()
                        name=str( items[2]).split('</a><br><br')
                        name=str(name[0]).split('"overlay-link">')
                        name=str(name[1]).strip()
                        print name
                        print path
                        addLink(name,path,4,thumb)
            except:
                pass
				
   
                                 

def getEpos(url):
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            matchObjPath=(re.compile('a href="(.+?)" class="pull-left r-item"').findall(link))
            matchObjThumb=(re.compile('style="background-image: url(.+?)"><h2 class="belowtxt">(.+?)<span class="hasVideo">').findall(link))
            for (items,itr)in itertools.izip( matchObjPath,matchObjThumb):
                
                thumb=str( itr[0])
                thumb=str(thumb).replace("('", '').replace("')","")
                thumb=str(thumb).strip()
                
                path='http://khalijia.rotana.net'+str(items)
                name=str(items).split('episodes/')
                name=str(name[1]).replace("-", " ").strip()
                print name
                print path
                addLink(name,path,4,thumb)

def playSerieVideio(url):
            try:
				req = urllib2.Request(url)
				response = urllib2.urlopen(req)
				link=response.read()
				matchObj=(re.compile('<span class="LimelightEmbeddedPlayer"><object id="kaltura_player_1364712831" name="kaltura_player_1364712831" type="application/x-shockwave-flash" allowFullScreen="true" allowNetworking="all" allowScriptAccess="always" height="373" width="620" bgcolor="#000000" xmlns:dc="http://purl.org/dc/terms/" xmlns:media="http://search.yahoo.com/searchmonkey/media/" rel="media:video" resource="(.+?)" data="').findall(link))
				matchObj=str(matchObj).split('entry_id/')
				matchObj=str(matchObj[1]).replace("']",'').strip()
				matchObj='http://myvideo.itworkscdn.com/p/105/sp/10500/raw/entry_id/'+matchObj
				listItem = xbmcgui.ListItem(path=str(matchObj))
				xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
				print matchObj
            except:
				req = urllib2.Request(url)
				response = urllib2.urlopen(req)
				link=response.read()
				matchObj=(re.compile('<object id="kaltura_player_1364712831" name="kaltura_player_1364712831" type="application/x-shockwave-flash" allowFullScreen="true" allowNetworking="all" allowScriptAccess="always" height="565" width="940" bgcolor="#000000" xmlns:dc="http://purl.org/dc/terms/" xmlns:media="http://search.yahoo.com/searchmonkey/media/" rel="media:video" resource="(.+?)" data="').findall(link))
				matchObj=str(matchObj).split('entry_id/')
				matchObj=str(matchObj[1]).replace("']",'').strip()
				matchObj='http://myvideo.itworkscdn.com/p/105/sp/10500/raw/entry_id/'+matchObj
				listItem = xbmcgui.ListItem(path=str(matchObj))
				xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
				pass
				
def indexClips(url):
	try:
		page=0
		for i in range(0,100):
			page=page+1
			req = urllib2.Request(str(url)+str(page))
			response = urllib2.urlopen(req)
			link=response.read()
			matchObj= re.findall(r'<div class="items">(.*?)\s(.*?)<div class="pagination pagination-inverse">', link, re.DOTALL)
			for items in matchObj:
				mypath= items[1]
				mypath=str(mypath).split('</h3><span')
				for itr in mypath:
					mytarget= str(itr).split('" class="pull-left item"><img src="')
									
					try:
						mypath= mytarget[0]
						thumb=mytarget[1]
						thumb=str( thumb).split('&w=150&h=')
						thumb=thumb[0]
						thumb=str(thumb).strip()
						mypath=str(mypath).split('<a href="')
						path='http://mousica.rotana.net'+str(mypath[1])
						name=str(path).split('video_clips/')
						name=str(name[1]).replace('-', ' ')
						addLink(name,path,4,thumb)
					except:
						pass
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
        indexSeries(url)
	
elif mode==2:
        print ""+url
        indexFilms(url)
elif mode==3:
	print ""+url
	getEpos(url)
	
elif mode==4:
        print ""+url
        playSerieVideio(url)
elif mode==5:
        print ""+url
        indexClips(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
