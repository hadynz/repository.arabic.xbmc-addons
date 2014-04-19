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
__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.shahidmbcnet'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonArt = os.path.join(addonPath,'resources/images')
communityStreamPath = os.path.join(addonPath,'resources/community')


def PlayStream(sourceSoup, urlSoup, name, url):

	playpath=urlSoup.chnumber.text
	code=getcode();
	print 'firstCode',code
	if not code or code[0:1]=="w":
		code=getcode(True);
		print 'secondCode',code
	liveLink= sourceSoup.rtmpstring.text;

	print 'rtmpstring',liveLink
	#liveLink=liveLink%(playpath,match)
	liveLink=liveLink%(playpath,code)
	name+='-LiveTV'
	print 'liveLink',liveLink
	listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=liveLink )
	xbmc.Player().play( liveLink,listitem)

def getcode(forceLogin=False):
	#url = urlSoup.url.text
	cookieJar= getCookieJar(forceLogin)
	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	opener = urllib2.install_opener(opener)
	req = urllib2.Request('http://www.livetv.tn/index.php')
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match =re.findall('code=([^\']*)', link)
	return match[0]

def getCookieJar(login=False):
	cookieJar=None
	COOKIEFILE = communityStreamPath+'/livePlayerLoginCookie.lwp'
	try:
		cookieJar = cookielib.LWPCookieJar()
		cookieJar.load(COOKIEFILE)
	except: 
		cookieJar=None
	
	if login or not cookieJar:
		cookieJar=performLogin()
	if cookieJar:
		cookieJar.save (COOKIEFILE)
	return cookieJar

	
def performLogin():
	userName=selfAddon.getSetting( "liveTvLogin" )
	password=selfAddon.getSetting( "liveTvPassword" )
	cookieJar = cookielib.LWPCookieJar()
	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	opener = urllib2.install_opener(opener)
	req = urllib2.Request('http://www.livetv.tn/login.php')
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	post={'pseudo':userName,'xpass':password}
	post = urllib.urlencode(post)
	response = urllib2.urlopen(req,post)
	return cookieJar;