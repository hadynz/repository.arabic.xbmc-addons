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
		channelId = urlSoup.url.text
		pDialog = xbmcgui.DialogProgress()
		pDialog.create('XBMC', 'Communicating with Teledunet')
		pDialog.update(10, 'fetching channel page')
		loginName=selfAddon.getSetting( "teledunetTvLogin" )

		if not (loginName==None or loginName==""):
			cookieJar,loginPerformed= getCookieJar(shoudforceLogin())
			if cookieJar and not loginPerformed:
				print 'adding cookie jar'
				now_datetime=datetime.datetime.now()
				selfAddon.setSetting( id="lastteledunetLogin" ,value=now_datetime.strftime("%Y-%m-%d %H:%M:%S"))
				cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
				opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
				opener = urllib2.install_opener(opener)
			
		if 1==1:
			newURL='http://www.teledunet.com/mobile/?con'
			print 'newURL',newURL
			req = urllib2.Request(newURL)
			req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
			req.add_header('Referer',newURL)
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
			match =re.findall('aut=\'\?id0=(.*?)\'', link)
			print match
			timesegment=match[0];str(long(float(match[0])))
			try:
				rtmp =re.findall(('rtmp://(.*?)/%s\''%channelId), link)[0]
				rtmp='rtmp://%s/%s'%(rtmp,channelId)
				#if '5.135.134.110' in rtmp and 'bein' in channelId:
				#	rtmp=rtmp.replace('5.135.134.110','www.teledunet.com')
			except:
				traceback.print_exc(file=sys.stdout)  
				rtmp='rtmp://5.135.134.110:1935/teledunet/%s'%(channelId)
		pDialog.update(80, 'trying to play')
		liveLink= sourceEtree.findtext('rtmpstring');

		print 'rtmpstring',liveLink,rtmp
#		liveLink=liveLink%(rtmp,channelId,match,channelId,channelId)
		liveLink=liveLink%(rtmp,channelId,timesegment,channelId)
		name+='-Teledunet'
		print 'liveLink',liveLink
		pDialog.close()
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



def getCookieJar(login=False):
	try:
		cookieJar=None
		COOKIEFILE = communityStreamPath+'/teletdunetPlayerLoginCookie.lwp'
		try:
			cookieJar = cookielib.LWPCookieJar()
			cookieJar.load(COOKIEFILE)
		except:
			traceback.print_exc(file=sys.stdout)	
			cookieJar=None
		loginPerformed=False
		if login or not cookieJar==None:
			cookieJar=performLogin()
			loginPerformed=True
		if cookieJar:
			cookieJar.save (COOKIEFILE)
		return cookieJar,loginPerformed
	except:
		traceback.print_exc(file=sys.stdout)
		return None, False
	
def performLogin():
	print 'performing login'
	userName=selfAddon.getSetting( "teledunetTvLogin" )
	password=selfAddon.getSetting( "teledunetTvPassword" )
	cookieJar = cookielib.LWPCookieJar()
	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	opener = urllib2.install_opener(opener)
	req = urllib2.Request('http://www.teledunet.com/boutique/connexion.php')
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	post={'login_user':userName,'pass_user':password}
	post = urllib.urlencode(post)
	response = urllib2.urlopen(req,post)
	link=response.read()
	response.close()
	now_datetime=datetime.datetime.now()
	req = urllib2.Request('http://www.teledunet.com/')#access main page too
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return cookieJar;


def shoudforceLogin():
    return True #disable login
    try:
#        import dateime
        lastUpdate=selfAddon.getSetting( "lastteledunetLogin" )
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
