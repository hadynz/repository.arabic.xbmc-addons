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
import sys
import time
import CustomPlayer


__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.shahidmbcnet'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonArt = os.path.join(addonPath,'resources/images')
communityStreamPath = os.path.join(addonPath,'resources/community')


def PlayStream(sourceEtree, urlSoup, name, url):
	try:
		playpath=urlSoup.chnumber.text
		pDialog = xbmcgui.DialogProgress()
		pDialog.create('XBMC', 'Communicating with Livetv')
		pDialog.update(40, 'Attempting to Login')
		code=getcode(shoudforceLogin());
		print 'firstCode',code
		if not code or code[0:1]=="w":
			pDialog.update(40, 'Refreshing Login')
			code=getcode(True);
			print 'secondCode',code
		liveLink= sourceEtree.findtext('rtmpstring')
		pDialog.update(80, 'Login Completed, now playing')
		print 'rtmpstring',liveLink
		#liveLink=liveLink%(playpath,match)
		liveLink=liveLink%(playpath,code)
		name+='-LiveTV'
		print 'liveLink',liveLink
		listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=liveLink )
		pDialog.close()
		player = CustomPlayer.MyXBMCPlayer()
		start = time.time()
		#xbmc.Player().play( liveLink,listitem)
		player.play( liveLink,listitem)
		while player.is_active:
			xbmc.sleep(200)
		#return player.urlplayed
		#done = time.time()
		done = time.time()
		elapsed = done - start
		if player.urlplayed and elapsed>=3:
			return True
		else:
			return False 
	except:
		traceback.print_exc(file=sys.stdout)    
	return False    

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
	print 'performing login'
	userName=selfAddon.getSetting( "liveTvLogin" )
	password=selfAddon.getSetting( "liveTvPassword" )
	cookieJar = cookielib.LWPCookieJar()
	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	opener = urllib2.install_opener(opener)
	req = urllib2.Request('http://www.livetv.tn/login.php')
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	post={'pseudo':userName,'mpass':password}
	post = urllib.urlencode(post)
	response = urllib2.urlopen(req,post)
	now_datetime=datetime.datetime.now()
	selfAddon.setSetting( id="lastLivetvLogin" ,value=now_datetime.strftime("%Y-%m-%d %H:%M:%S"))
	return cookieJar;


def shoudforceLogin():
    try:
#        import dateime
        lastUpdate=selfAddon.getSetting( "lastLivetvLogin" )
        print 'lastUpdate',lastUpdate
        do_login=False
        now_datetime=datetime.datetime.now()
        if lastUpdate==None or lastUpdate=="":
            do_login=True
        else:
            print 'lastlogin',lastUpdate
            try:
                lastUpdate=datetime.datetime.strptime(lastUpdate,"%Y-%m-%d %H:%M:%S")
            except TypeError:
                lastUpdate = datetime.datetime.fromtimestamp(time.mktime(time.strptime(lastUpdate, "%Y-%m-%d %H:%M:%S")))
        
            t=(now_datetime-lastUpdate).seconds/60
            print 'lastUpdate',lastUpdate,now_datetime
            print 't',t
            if t>15:
                do_login=True
        print 'do_login',do_login
        return do_login
    except:
        traceback.print_exc(file=sys.stdout)
    return True
