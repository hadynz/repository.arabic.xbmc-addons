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

__settings__ = xbmcaddon.Addon(id='plugin.video.panet')
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




def get_series(url):
	max = 25
	orig = url
	for i in range(1,max):
		try:
			url = orig+str(i)
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			link = response.read()
			result = re.search('class="panet-thumbnail"(.*)</h2></div><div', link)
			for item in result.group(1).split('"panet-thumbnail"'):
				path ='http://www.panet.co.il'+str(item).split('href="')[1].split('""><img')[0].strip()
				path = path[:-1]
				img = str(item).split('<img src="')[1].split('" alt=')[0].strip()
				name = str(item).split('"panet-title"><h2>')[1].split('</h2></div><div')[0].strip()
				addDir(name,path,2,img)
		except:
			break

def get_epos(url):
	max = 15
	orig = url
	for i in range(1, max):
		try:
			url = orig+str(i)
			print url
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			link = response.read()
			counter =0
			result = re.search('</div></div></div></div></div></div><a class="panet-thumbnail" href=(.*)</div></a>', link)
			for itr in result.group().split('panet-thumbnail"'):
				counter = counter+1
				if counter >1:
					path ='http://www.panet.co.il'+str( itr).split('href="')[1].split('"><img')[0].strip()
					name = str(itr).split('" alt="')[1].split('"><div')[0].strip()
					img = str(itr).split('src="')[1].split('" alt')[0].strip()
					addLink(name,path,3,img)
					print path
		except:
			break
                    
def get_video_file(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	link = response.read()
	result = re.search('content="(.*)" /></div><div', link)
	video_path= result.group().split('"contentURL" content="')[1].split('"')[0]
	listItem = xbmcgui.ListItem(path=str(video_path))
	xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    

def get_cats():
    req = urllib2.Request('http://www.panet.co.il/series/')
    response = urllib2.urlopen(req)
    link = response.read()
    counter =0
    result = re.search('class="panet-grid-row">(.*)</a></div></div></div><div', link)
    for item in result.group().split('href="'):
        counter = counter + 1
        if counter > 1:
			path='http://www.panet.co.il'+str( item).split('">')[0].strip()
			path =path[:-1]
			name =str(item).split('">')[1].split(' </a>')[0].strip()
			addDir(name,path,1,'')
          
			

                
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
        get_cats()
       
elif mode==1:
        print ""+url
        get_series(url)
	
elif mode==2:
        print ""+url
        get_epos(url) 

if mode==3:
	get_video_file(url)

	
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
