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

COOKIEFILE = communityStreamPath+'/teletdunetPlayerLoginCookie.lwp'
cache_table         = __addonname__
cache2Hr              = StorageServer.StorageServer(cache_table,2)
cache2Hr.table_name = cache_table		
teledunet_htmlfile='TeledunetchannelList.html'
profile_path =  xbmc.translatePath(selfAddon.getAddonInfo('profile'))
def PlayStream(sourceEtree, urlSoup, name, url):
	try:
		channelId = urlSoup.url.text
		pDialog = xbmcgui.DialogProgress()
		pDialog.create('XBMC', 'Communicating with Teledunet')
		pDialog.update(10, 'fetching channel page')
		loginName=selfAddon.getSetting( "teledunetTvLogin" )

		
		

		if 1==1:
			newURL='http://www.teledunet.com/mobile/?con'
			print 'newURL',newURL
			#req = urllib2.Request(newURL)
			#req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
			#req.add_header('Referer',newURL)
			#response = urllib2.urlopen(req)
			#link=response.read()
			#response.close()

			try:

				cache2Hr.table_name = cache_table	
				file_exists=cache2Hr.get('MainChannelPage')
				print 'file_exists',file_exists
				link=None
				if file_exists and file_exists=='yes':
					print 'it says use local file'
					link=getStoredFile(teledunet_htmlfile)
				
				if link==None:
					print 'Oopps, not using local file'
					if not loginName=="":
						if shouldforceLogin():
							if performLogin():
								print 'done login'
							else:
								print 'login failed??'
						else:
							print 'Login not forced.. perhaps reusing the session'
					else:
						print 'login name not defined'

					
					link=getUrl(newURL,getCookieJar() ,None,'http://www.teledunet.com/')
					if storeInFile(link,teledunet_htmlfile):
						cache2Hr.table_name = cache_table	
						cache2Hr.set('MainChannelPage','yes')
						print 'Stored in local file',cache2Hr.get('MainChannelPage')
					

				match =re.findall('aut=\'\?id0=(.*?)\'', link)
				print match
				timesegment=str(long(float(match[0])))
				
				rtmp =re.findall(('rtmp://(.*?)/%s\''%channelId), link)[0]
				rtmp='rtmp://%s/%s'%(rtmp,channelId)
				#if '5.135.134.110' in rtmp and 'bein' in channelId:
				#	rtmp=rtmp.replace('5.135.134.110','www.teledunet.com')
			except:
				traceback.print_exc(file=sys.stdout)
				print 'trying backup'
				try:
					link=getUrl("https://dl.dropboxusercontent.com/s/ku3n4n53qphqnmn/Frame-code.txt", getCookieJar())
					rtmp =re.findall(('rtmp://(.*?)/%s\''%channelId), link)[0]
					rtmp='rtmp://%s/%s'%(rtmp,channelId)
				except:
					traceback.print_exc(file=sys.stdout)
					rtmp='rtmp://5.135.134.110:1935/teledunet/%s'%(channelId)
					print 'error in channel using hardcoded value'
		pDialog.update(80, 'trying to play')
		liveLink= sourceEtree.findtext('rtmpstring');

		print 'rtmpstring',liveLink,rtmp
#		liveLink=liveLink%(rtmp,channelId,match,channelId,channelId)
		liveLink=liveLink%(rtmp,channelId,timesegment,channelId)
		name+='-Teledunet'
		print 'liveLink',liveLink
		pDialog.close()
		totalTried=0
		howMaytimes=15
		try:
			howMaytimes=int(selfAddon.getSetting( "teledunetRetryCount" ))
		except:pass

		
		pDialog = xbmcgui.DialogProgress()
		pDialog.create('XBMC', 'Playing channel')
		while totalTried<howMaytimes:

			totalTried+=1
			pDialog.update((totalTried*100)/howMaytimes, 'Try #' + str(totalTried) +' of ' + str(howMaytimes))
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
		pDialog.close()
		return False
	except:
		traceback.print_exc(file=sys.stdout)    
	return False  



def getCookieJarOld(login=False):
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
		print 'saved'
		return cookieJar,loginPerformed
	except:
		traceback.print_exc(file=sys.stdout)
		return None, False
	
def performLoginOLD():
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

def performLogin():
	try:
		cookieJar=cookielib.LWPCookieJar()
		userName=selfAddon.getSetting( "teledunetTvLogin" )
		password=selfAddon.getSetting( "teledunetTvPassword" )
		print 'Values are ',userName,password
		post={'login_user':userName,'pass_user':password}
		post = urllib.urlencode(post)
		html_text=getUrl("http://www.teledunet.com/boutique/connexion.php",cookieJar,post)
		cookieJar.save (COOKIEFILE,ignore_discard=True)
		print 'cookie jar saved',cookieJar
		html_text=getUrl("http://www.teledunet.com/",cookieJar)
		cookieJar.save (COOKIEFILE,ignore_discard=True)
		return shouldforceLogin(cookieJar)==False
	except:
		traceback.print_exc(file=sys.stdout)
		return False


def shoudforceLoginOLD():
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

def clearFileCache():
	cache2Hr.table_name = cache_table
	cache2Hr.delete('%')
	
def storeInFile(text_to_store,FileName):
	try:
		File_name=os.path.join(profile_path,FileName )
		localFile = open(File_name, "wb")
		localFile.write(text_to_store)
		localFile.close()
		return True
	except:
		traceback.print_exc(file=sys.stdout)
	return False

def getStoredFile(FileName):
	ret_value=None
	File_name=os.path.join(profile_path,FileName )
	try:
		data = open(File_name, "r").read()
		ret_value=data
	except:
		traceback.print_exc(file=sys.stdout)
	return ret_value
	
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

def getUrl(url, cookieJar=None,post=None,referer=None):

	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	#opener = urllib2.install_opener(opener)
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	if referer:
		req.add_header('Referer',referer)
	response = opener.open(req,post,timeout=30)
	link=response.read()
	response.close()
	return link;
	
def shouldforceLogin(cookieJar=None):
    try:
        url="http://www.teledunet.com/boutique/connexion.php"
        if not cookieJar:
            cookieJar=getCookieJar()
        html_txt=getUrl(url,cookieJar)
        
            
        if '<input name="login_user"' in html_txt:
            return True
        else:
            return False
    except:
        traceback.print_exc(file=sys.stdout)
    return True

