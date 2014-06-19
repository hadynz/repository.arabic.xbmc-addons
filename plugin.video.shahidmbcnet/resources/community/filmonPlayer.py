# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re
import HTMLParser
import xbmcaddon
import json
import traceback
import os
import cookielib
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
import datetime
import time
import sys
import CustomPlayer
try:
    import json
except:
    import simplejson as json
	
try:    
	import StorageServer
except:
	print 'using dummy storage'
	import storageserverdummy as StorageServer

__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.shahidmbcnet'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonArt = os.path.join(addonPath,'resources/images')
#communityStreamPath = os.path.join(addonPath,'resources/community')
communityStreamPath = os.path.join(addonPath,'resources')
communityStreamPath =os.path.join(communityStreamPath,'community')

COOKIEFILE = communityStreamPath+'/filmonPlayerLoginCookie.lwp'
cache_table         = __addonname__
cache2Hr              = StorageServer.StorageServer(cache_table,2)
cache2Hr.table_name = cache_table		
#teledunet_htmlfile='TeledunetchannelList.html'
profile_path =  xbmc.translatePath(selfAddon.getAddonInfo('profile'))
def PlayStream(sourceEtree, urlSoup, name, url):
	try:
		channelId = urlSoup.url.text
		pDialog = xbmcgui.DialogProgress()
		pDialog.create('XBMC', 'Communicating with Filmon')
		pDialog.update(10, 'fetching channel page')

		current_try=0
		firstTry=0
#		try:
#			howMaytimes=int(selfAddon.getSetting( "teledunetRetryCount" ))
#		except:pass
		totaltries=0
		while True:
			totaltries+=1
			try:
				cookie_jar=getCookieJar()
				newURL='http://www.filmon.com/'
				link=getUrl(newURL,cookie_jar)
				break
			except:
				if totaltries>=2:
					break
		
		current_try=0
		if selfAddon.getSetting( "filmonDontPlayplayHigh" )=="true":
			current_try=1#skip high
		tryTypes=['high','low']
		while current_try<len(tryTypes):
			current_Q=tryTypes[current_try]
			name+='-FilmOn(%s)'%current_Q
			pDialog.update((current_try*100)/len(tryTypes), 'Trying Quality  '+current_Q)
            		
  			newURL='http://www.filmon.com/ajax/getChannelInfo'
			print 'newURL',newURL
			#cookieJar=None,post=None,headers=None
			post_val={'channel_id':channelId,'quality':current_Q}
			post_val = urllib.urlencode(post_val)
			headers_val=[('Origin','http://www.filmon.com'),('X-Requested-With','XMLHttpRequest')]
			link=getUrl(newURL,cookieJar=cookie_jar,post=post_val,headers=headers_val)
			print link
			json_data=json.loads(link)
			rtmp,playpath=json_data['serverURL'],json_data['streamName']
			if 'live/?id=' in rtmp:
				rtmp+=' app='+'live/?id='+rtmp.split('live/?id=')[1]
			#playpath=playpath.split(':')[1]
			pre_liveLink= sourceEtree.findtext('rtmpstring');

			liveLink=pre_liveLink%(rtmp,playpath)
			print 'rtmpstring',pre_liveLink,rtmp,playpath, liveLink

			listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=liveLink )            
			player = CustomPlayer.MyXBMCPlayer()
			#xbmc.Player().play( liveLink,listitem)
			start = time.time()  
			player.pdialogue=pDialog
			if pDialog.iscanceled():
				break
			player.play( liveLink,listitem)  
			if pDialog.iscanceled():
				break
			#pDialog.close()
			while player.is_active:
				xbmc.sleep(200)
			#return player.urlplayed
			done = time.time()
			elapsed = done - start
			if player.urlplayed and elapsed>=3:
				return True
			current_try+=1
		pDialog.close()
		return False
	except:
		traceback.print_exc(file=sys.stdout)    
	return False  

	
def getCookieJar():
	cookieJar=None
	try:
		cookieJar = cookielib.LWPCookieJar()
		cookieJar.load(COOKIEFILE,ignore_discard=True)
	except: 
		cookieJar=None
	
	if not cookieJar:
		cookieJar = cookielib.LWPCookieJar()

	return cookieJar

def getUrl(url, cookieJar=None,post=None,headers=None):

	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	#opener = urllib2.install_opener(opener)
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	if headers:
		for h,v in headers:
			req.add_header(h,v)

	response = opener.open(req,post,timeout=30)
	link=response.read()
	response.close()
	return link;

