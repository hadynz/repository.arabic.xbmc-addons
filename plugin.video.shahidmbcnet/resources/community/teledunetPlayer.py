# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re
import HTMLParser
import xbmcaddon
import json
import traceback
import os
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
import time
import sys
import CustomPlayer


def PlayStream(sourceSoup, urlSoup, name, url):
	try:
		channelId = urlSoup.url.text
		newURL='http://www.teledunet.com/player/?channel=%s&no_pub'%channelId
		print 'newURL',newURL
		req = urllib2.Request(newURL)
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
		req.add_header('Referer',newURL)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		match =re.findall('time_player=(.*?);', link)
		match=str(long(float(match[0])))
		rtmp =re.findall('curent_media=\'(.*?)\'', link)[0]

		liveLink= sourceSoup.rtmpstring.text;

		print 'rtmpstring',liveLink
		liveLink=liveLink%(rtmp,channelId,match,channelId,channelId)
		name+='-Teledunet'
		print 'liveLink',liveLink
		listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=liveLink )
		player = CustomPlayer.MyXBMCPlayer()
		#xbmc.Player().play( liveLink,listitem)
		start = time.time()  
		player.play( liveLink,listitem)  
		while player.is_active:
			xbmc.sleep(200)
		#return player.urlplayed
		done = time.time()
		elapsed = done - start
		if player.urlplayed and elapsed>=3:
			return True
		else:
			return False
	except:
		traceback.print_exc(file=sys.stdout)    
	return False  


