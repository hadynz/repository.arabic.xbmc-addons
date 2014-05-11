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
import  CustomPlayer

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
		#url = urlSoup.url.text
		pDialog = xbmcgui.DialogProgress()
		pDialog.create('XBMC', 'Parsing the xml file')
		pDialog.update(10, 'fetching channel info')
		title=''
		link=''
		sc=''
		try:
			title=urlSoup.item.title.text
			
			link=urlSoup.item.link.text
			sc=sourceEtree.findtext('sname')
		except: pass
		if link=='':
			timeD = 2000  #in miliseconds
			line1="couldn't read title and link"
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeD, __icon__))
			return False
		regexs = urlSoup.find('regex')
		pDialog.update(80, 'Parsing info')
		if (not regexs==None) and len(regexs)>0:
			liveLink=	getRegexParsed(urlSoup,link)
		else:
			liveLink=	link
		liveLink=liveLink
		if len(liveLink)==0:
			timeD = 2000  #in miliseconds
			line1="couldn't read title and link"
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeD, __icon__))
			return False
			
		timeD = 2000  #in miliseconds
		line1="Resource found,playing now."
		pDialog.update(80, line1)
		liveLink=replaceSettingsVariables(liveLink)
		name+='-'+sc+':'+title
		print 'liveLink',liveLink
		pDialog.close()
		listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=liveLink )
		player = CustomPlayer.MyXBMCPlayer()
		start = time.time() 
		#xbmc.Player().play( liveLink,listitem)
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

def getRegexParsed(regexs, url,cookieJar=None,forCookieJarOnly=False,recursiveCall=False):#0,1,2 = URL, regexOnly, CookieJarOnly

	cachedPages = {}
	#print 'url',url
	doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(url)
	print 'doRegexs',doRegexs,regexs

	for rege in doRegexs:
		k=regexs.find("regex",{"name":rege})
		if not k==None:
			cookieJarParam=False
			if k.cookiejar:
				cookieJarParam=k.cookiejar.text;
				if  '$doregex' in cookieJarParam:
					cookieJar=getRegexParsed(regexs, cookieJarParam,cookieJar,True, True)
					cookieJarParam=True
				else:
					cookieJarParam=True
			if cookieJarParam:
				if cookieJar==None:
					#print 'create cookie jar'
					import cookielib
					cookieJar = cookielib.LWPCookieJar()
					#print 'cookieJar new',cookieJar
			page = k.page.text
			if  '$doregex' in page:
				page=getRegexParsed(regexs, page,cookieJar,recursiveCall=True)
				
			postInput=None
			if k.post:
				postInput = k.post.text
				if  '$doregex' in postInput:
					postInput=getRegexParsed(regexs, postInput,cookieJar,recursiveCall=True)
				print 'post is now',postInput
				
				
			if page in cachedPages :
				link = cachedPages[page]
			else:
				#print 'Ingoring Cache',m['page']
				req = urllib2.Request(page)
				req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
				if k.refer:
					req.add_header('Referer', k.refer.text)
				if k.agent:
					req.add_header('User-agent', k.agent.text)

				if not cookieJar==None:
					#print 'cookieJarVal',cookieJar
					cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
					opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
					opener = urllib2.install_opener(opener)
				#print 'after cookie jar'

				post=None
				if postInput:
					postData=postInput
					splitpost=postData.split(',');
					post={}
					for p in splitpost:
						n=p.split(':')[0];
						v=p.split(':')[1];
						post[n]=v
					post = urllib.urlencode(post)

				if post:
					response = urllib2.urlopen(req,post)
				else:
					response = urllib2.urlopen(req)

				link = response.read()

				response.close()
				cachedPages[page] = link
				if forCookieJarOnly:
					return cookieJar# do nothing
			print 'link',link
			print k.expres.text
			reg = re.compile(k.expres.text).search(link)
			
			url = url.replace("$doregex[" + rege + "]", reg.group(1).strip())
			if recursiveCall: return url
	print 'final url',url
	return url

def replaceSettingsVariables(str):
	retVal=str
	if '$setting' in str:
		matches=re.findall('\$(setting_.*?)\$', str)
		for m in matches:
			setting_val=selfAddon.getSetting( m )
			retVal=retVal.replace('$'+m+'$',setting_val)
	return retVal
