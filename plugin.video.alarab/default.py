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


__settings__ = xbmcaddon.Addon(id='plugin.video.alarab')
__icon__ = __settings__.getAddonInfo('icon')
__fanart__ = __settings__.getAddonInfo('fanart')
__language__ = __settings__.getLocalizedString
_thisPlugin = int(sys.argv[1])
_pluginName = (sys.argv[0])


def getCats(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	link = response.read()
	target = re.findall(r'<div id="nav">(.*?)</div>', link, re.DOTALL)
	for items in target:
		mypath = re.findall(r' href="/(.*?)/', items)
		myname = myname = re.findall(r'" >(.*?)</a></li>', items)
		for it_name, it_mypath in zip(myname, mypath):
			holder = 'http://tv1.alarab.com/'+it_mypath +'/'
			addDir(it_name,holder,2,"")



def getTVSeries(url): 
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	link = response.read()
	target_pg = re.findall(r'<a class="tsc_3d(.*?)</a>', link, re.DOTALL)
	target_ep = re.findall(r'<div class="video-box">(.*?)</a></div>', link, re.DOTALL)
	target_page_counter = re.findall(r'<a class="tsc_3d_button blue"(.*?)</a>', link)
	for counts in target_page_counter:
		real_number = counts.split('title=" \xd8\xb5\xd9\x81\xd8\xad\xd8\xa9 ')[1].split('" >')[0]
	counter = int(real_number)+1
	for eps in target_ep:
		ep_path = re.findall(r' href="/(.*?)">', eps)
		ep_name = re.findall(r'alt="(.*?)" />', eps)
		for names, paths in zip(ep_name, ep_path):
			holder = 'http://tv1.alarab.com/' + paths #set path
			addDir(names,holder,3,"")
	for pg in target_pg:

		pg_path_str = pg.split('href="')[1].split('"')[0]
		pg_path_link = 'http://tv1.alarab.com/' + pg_path_str
		#pg_number_str = re.findall(r' title=" \xd8\xb5\xd9\x81\xd8\xad\xd8\xa9 (.*?)" >',pg)
		pg_number_str = pg.split('title=" \xd8\xb5\xd9\x81\xd8\xad\xd8\xa9 ')[1].split('" >')[0]
		pg_number = int(pg_number_str)
		if (counter == pg_number):
			addDir('Next Page', pg_path_link, 2, "")

	


def getSerieFolge(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	link = response.read()
	#target_episodes = re.findall(r'<div class="fav">(.*?)</div>\s+</a>', link, re.DOTALL)
	target_episodes = re.findall(r'<div class="related_on">(.*?)<div id="results">', link, re.DOTALL)
	print target_episodes
	for episodes in target_episodes:
		episode_name = re.findall(r'div class="">(.*?)</div',episodes,re.DOTALL)
		episode_path = re.findall(r'a href="/(.*?)"', episodes,re.DOTALL)
		for name, paths in zip(episode_name, episode_path):
			holder = 'http://tv1.alarab.com/'+paths
			print name
			print paths
			addLink(name,holder,4,"")

def Play(url):
	url1 = 'http://alarabplayers.alarab.com/?vid='+url.split('v')[2]
	url2 = url1.split('-')[0]
	req = urllib2.Request(url2)
	response = urllib2.urlopen(req)
	link=response.read()
	video_url = str(link).split('file: "')[1].split('"')[0]
	listItem = xbmcgui.ListItem(path=str(video_url))
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
        getCats('http://tv1.alarab.com')
elif mode==1:
	print ""+url
	getMovie(url)
elif mode==2:
	print ""+url
	getTVSeries(url)
elif mode==3:
	print ""+url
	getSerieFolge(url)
elif mode==4:
	print ""+url
	Play(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]), updateListing=True)
