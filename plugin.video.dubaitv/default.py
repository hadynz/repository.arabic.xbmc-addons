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

__settings__ = xbmcaddon.Addon(id='plugin.video.dubaitv')
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

def checkUrl(url):
    p = urlparse(url)
    conn = httplib.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400



def getCategories():
    
    url='http://vod.dmi.ae/'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    response = urllib2.urlopen(req)
    link=response.read()
    url_categories=(re.compile('<li><a href="/(.+?)">(.+?)</a></li>').findall(link))
    for myItems in url_categories:
        myTempObj= str(myItems[0])
        myTempName= str(myItems[1])
        if 'category' in myTempObj:
            
            catPath ='http://vod.dmi.ae/'+ myTempObj
            catPath=str(catPath).strip()
            catName=myTempName
            catName=str(catName).strip()
            addDir(catName,catPath,1,'http://1.bp.blogspot.com/-2dgsZzVtZdo/TsVKjel898I/AAAAAAAAA90/A0bD4FRKHuU/s200/dubai-tv.jpg')
            
        
def getSeries(url):
    counter=0
    
    for sites in range(0,50):
        counter=counter+1
        url=url+'/'+str(counter)
        if checkUrl(url):
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            response = urllib2.urlopen(req)
            link=response.read()
            target= re.findall(r'<div class="video" style="height: 140px;"(.*?)\s(.*?)</div>', link, re.DOTALL)
            for items in target:
				myPath=str( items[1]).replace('<div class="thumb">', ' DELIM ').replace('<img src="', ' DELIM ').replace('alt="', ' DELIM ')
				myPath=str(myPath).split(' DELIM ')
				try:
					theUrl='http://vod.dmi.ae/'+str(myPath[1]).replace('<a href="/', '').replace('">', '').strip()
					theImage=str(myPath[2]).replace('<img src="', '').replace('"', '').strip()
					theName=str(myPath[3]).replace('" />', '').strip()
					addDir(theName,theUrl,2,theImage)
				except:
					pass

def getEpisodes(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    response = urllib2.urlopen(req)
    link=response.read()
    target= re.findall(r'<div class="thumb">(.*?)\s<div class="icon"></div>', link, re.DOTALL)
    for items in target:
        myPath=str(items).replace('<a href="', ' DELIM ').replace('"><img src="', ' DELIM ').replace('" alt="', ' DELIM ').replace('" /></a>', ' DELIM ')
        myPath=str(myPath).split(' DELIM ')
        path='http://vod.dmi.ae'+str( myPath[1]).strip()
        thumbNail=str( myPath[2]).strip()
        serieName=str( myPath[3]).strip()
        addLink(serieName,path,3,thumbNail)
        
def playVideo(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	response = urllib2.urlopen(req)
	link=response.read()
	target= re.findall(r'var mediaItem =(.*?)\jwplayer.key =', link, re.DOTALL)
	videoPath=str( target).split('"fileUrl":"')[1]
	videoPath=str(videoPath).split('?cdnParams=')[0]
	videoPath=str(videoPath).replace('\/','deli').strip()
	videoPath=str(videoPath).replace('\deli','/').strip()
	listItem = xbmcgui.ListItem(path=str(videoPath))
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
        getCategories()
       
elif mode==1:
        print ""+url
        getSeries(url)
	
elif mode==2:
        getEpisodes(url)
		
elif mode==3:
        print ""+url
        playVideo(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
