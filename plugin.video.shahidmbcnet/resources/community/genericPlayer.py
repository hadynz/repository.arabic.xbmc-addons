# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re
import HTMLParser
import xbmcaddon
import json
import traceback
import os
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP

__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')

def PlayStream(sourceSoup, urlSoup, name, url):
	#url = urlSoup.url.text
	title=''
	link=''
	sc=''
	try:
		title=urlSoup.item.title.text
		
		link=urlSoup.item.link.text
		sc=sourceSoup.sname.text
	except: pass
	if link=='':
		time = 2000  #in miliseconds
		line1="couldn't read title and link"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		return 
	regexs = urlSoup.find('regex')
	if (not regexs==None) and len(regexs)>0:
		liveLink=	getRegexParsed(urlSoup,link)
	else:
		liveLink=	link
	if len(liveLink)==0:
		time = 2000  #in miliseconds
		line1="couldn't read title and link"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		return 
		
	time = 2000  #in miliseconds
	line1="Resource found,playing now."
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

	name+='-'+sc+':'+title
	print 'liveLink',liveLink
	listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=liveLink )
	xbmc.Player().play( liveLink,listitem)
	return


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



