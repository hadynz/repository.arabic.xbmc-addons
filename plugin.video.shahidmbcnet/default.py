# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re
import HTMLParser
import xbmcaddon
import json
import traceback
import os
import sys
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP, Tag,NavigableString
try:
  from lxmlERRRORRRR import etree
  print("running with lxml.etree")
except ImportError:
	try:
	  # Python 2.5
	  import xml.etree.ElementTree as etree
	  print("running with ElementTree on Python 2.5+")
	except ImportError:
	  try:
		# normal cElementTree install
		import cElementTree as etree
		print("running with cElementTree")
	  except ImportError:
		try:
		  # normal ElementTree install
		  import elementtree.ElementTree as etree
		  print("running with ElementTree")
		except ImportError:
		  print("Failed to import ElementTree from any known place")

import json

__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.shahidmbcnet'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonArt = os.path.join(addonPath,'resources/images')
communityStreamPath = os.path.join(addonPath,'resources')
communityStreamPath =os.path.join(communityStreamPath,'community')
profile_path =  xbmc.translatePath(selfAddon.getAddonInfo('profile'))
 
mainurl='http://shahid.mbc.net'
apikey='AIzaSyCl5mHLlE0mwsyG4uvNHu5k1Ej1LQ_3RO4'

def getMainUrl():
	rMain=mainurl
	#check setting and see if we have proxy define, ifso, use that
	isProxyEnabled=defaultCDN=selfAddon.getSetting( "isProxyEnabled" )
	proxyAddress=defaultCDN=selfAddon.getSetting( "proxyName" )
	if isProxyEnabled:#if its not None
		#print 'isProxyEnabled',isProxyEnabled,proxyAddress
		if isProxyEnabled=="true":
			#print 'its enabled'
			rMain=proxyAddress
		#else: #print 'Proxy not enable'
	return rMain
	
	
	

VIEW_MODES = {
    'thumbnail': {
        'skin.confluence': 500,
        'skin.aeon.nox': 551,
        'skin.confluence-vertical': 500,
        'skin.jx720': 52,
        'skin.pm3-hd': 53,
        'skin.rapier': 50,
        'skin.simplicity': 500,
        'skin.slik': 53,
        'skin.touched': 500,
        'skin.transparency': 53,
        'skin.xeebo': 55,
    },
}

def get_view_mode_id( view_mode):
	default_view_mode=selfAddon.getSetting( "usethisviewmode" )
	if default_view_mode=="":
		view_mode_ids = VIEW_MODES.get(view_mode.lower())
		if view_mode_ids:
			return view_mode_ids.get(xbmc.getSkinDir())
	else:
		return int(default_view_mode)
	return None

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def Colored(text = '', colorid = '', isBold = False):
	if colorid == 'one':
		color = 'FF11b500'
	elif colorid == 'two':
		color = 'FFe37101'
	elif colorid == 'bold':
		return '[B]' + text + '[/B]'
	else:
		color = colorid
		
	if isBold == True:
		text = '[B]' + text + '[/B]'
	return '[COLOR ' + color + ']' + text + '[/COLOR]'	
	
def addDir(name,url,mode,iconimage	,showContext=False,isItFolder=True,pageNumber="", isHTML=True,addIconForPlaylist=False, AddRemoveMyChannels=None, SelectDefaultSource=None, hideChannel=None):
#	print name
#	name=name.decode('utf-8','replace')
	if isHTML:
		h = HTMLParser.HTMLParser()
		name= h.unescape(name).decode("utf-8")
		rname=  name.encode("utf-8")
	else:
		#h = HTMLParser.HTMLParser()
		#name =h.unescape(name).decode("utf-8")
		rname=  name.encode("utf-8")
#		url=  url.encode("utf-8")
#	url= url.encode('ascii','ignore')

	
	#print rname
	#print iconimage
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(rname)
	if len(pageNumber):
		u+="&pagenum="+pageNumber
	if addIconForPlaylist:
		u+="&addIconForPlaylist=yes"
	ok=True
#	print iconimage
	liz=xbmcgui.ListItem(rname, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	#liz.setInfo( type="Video", infoLabels={ "Title": name } )

	if showContext==True:
		cmd1 = "XBMC.RunPlugin(%s&cdnType=%s)" % (u, "l3")
		cmd2 = "XBMC.RunPlugin(%s&cdnType=%s)" % (u, "xdn")
		cmd3 = "XBMC.RunPlugin(%s&cdnType=%s)" % (u, "ak")
		liz.addContextMenuItems([('Play using L3 Cdn',cmd1),('Play using XDN Cdn',cmd2),('Play using AK Cdn',cmd3)])

	context_menu=[]
	if not AddRemoveMyChannels==None:
		if AddRemoveMyChannels:
			cmd1 = "XBMC.RunPlugin(%s&AddRemoveMyChannels=add)" % (u)
			context_menu.append(('Add to My Channels',cmd1))
		else:
			cmd1 = "XBMC.RunPlugin(%s&AddRemoveMyChannels=remove)" % (u)
			context_menu.append(('Remove from My Channels',cmd1))


	if SelectDefaultSource:
		#print 'select defauly'
		cmd2 = "XBMC.RunPlugin(%s&selectDefaultSource=yes)" % (u)
		context_menu.append(('Select default source',cmd2))

	if not hideChannel==None:
		if hideChannel:
			cmd3 = "XBMC.RunPlugin(%s&HideChannel=yes)" % (u)
			context_menu.append(('Hide this Channel',cmd3))
		else:
			cmd3 = "XBMC.RunPlugin(%s&HideChannel=no)" % (u)
			context_menu.append(('Unhide this Channel',cmd3))

            
	if len(context_menu)>0:
		liz.addContextMenuItems(context_menu,replaceItems=False)
	#	if selfAddon.getSetting( "addToFavMode" )=="true":
	#		liz.addContextMenuItems(context_menu,replaceItems=False)
	#	else:
	#		liz.addContextMenuItems(context_menu,replaceItems=True)
			
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isItFolder)
	return ok
	


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




def Addtypes():
	#2 is series=3 are links
	addDir('Shahid Vod by Channels' ,getMainUrl()+'/ar/channel-browser.html' ,2,addonArt+'/channels.png') #links #2 channels,3 series,4 video entry, 5 play
	addDir('Shahid Vod by Series' ,getMainUrl()+'/ar/series-browser.html' ,6,addonArt+'/serial.png')
	#addDir('Streams' ,'streams' ,9,addonArt+'/stream.png')
	addDir('Shahid Live' ,'CCats' ,14,addonArt+'/Network-1-icon.png')
	addDir('Shahid Youtube' ,'http://gdata.youtube.com/feeds/api/users/aljadeedonline' ,18,addonArt+'/youtube.png')    
	addDir('Download Files' ,'cRefresh' ,17,addonArt+'/download-icon.png',isItFolder=False)
	addDir('Settings' ,'Settings' ,8,addonArt+'/setting.png',isItFolder=False) ##
	addDir('Livetv.tn Login' ,'Livetv' ,24,addonArt+'/setting.png',isItFolder=False) ##
	return

def AddYoutubeLanding(url):
	if not url.lower().startswith('http'):
		if url=='LOCAL':
			filename=selfAddon.getSetting( "localyoutubexmlpath" )
		else:
			filename=url
		#print 'filename',filename
		if len(filename)>0:
			data = open(filename.decode('utf-8'), "r").read()
			#print data
			directories=getETreeFromString(data)
		else:
			dialog = xbmcgui.Dialog()
			ok = dialog.ok('XBMC', 'File not defined')
			return
	else:
		directories=getETreeFromUrl(url)
	for dir in directories.findall('dir'):
		name = dir.find('name').text
		link= dir.find('link')
		if not link==None: link=link.text
		videouser= dir.find('youtubeuser')
		if not videouser==None: videouser=videouser.text
		
		channelID= dir.find('channelid')
		if not channelID==None: channelID=channelID.text
		
		thumbnail= dir.find('thumbnail')
		if not thumbnail==None: thumbnail=thumbnail.text
		
		
		#print name,link
		thumbnail= dir.find('thumbnail').text
		if thumbnail==None:
			thumbnail=''
		#print 'thumbnail',thumbnail
		type = dir.find('type')

		if type==None:
			#check the link and decide
			if not link==None:
				if link.endswith('playlists'):
					type='playlist'
				elif link.endswith('uploads'):
					type='videos'
				elif 'watch?v' in link:
					type='video'
				else:
					type='dir'
			else:
				type='dir'
		else:
			type=type.text
		#print 'channelID',channelID
		if type=='playlist' or  type=='videos':
			if channelID==None or  len(channelID)==0:
				if videouser==None:
					#get it from the link
					link=link.split('/')[-2]
				else:
					link=videouser
				#print 'link for Channelid',link
				link=getChannelIdByUserName(link)#passusername
			else:
				link=channelID
		icon=addonArt+'/video.png'
		if (not thumbnail==None) and len(thumbnail)>0:
			icon=thumbnail
		#print 'icon',icon
		if type=='playlist':
			addDir(name ,link ,22,addonArt+'/playlist.png',isHTML=False) 
		elif type=='videos':
			addDir(name ,link ,20,icon,isHTML=False)
		elif type=='video':
			addDir(name ,link  ,21,thumbnail,isItFolder=False, isHTML=False)		#name,url,mode,icon
		else:
			addDir(name ,link  ,19,thumbnail,isItFolder=True, isHTML=False)		#name,url,mode,icon
	 
	
	
def checkAndRefresh():
	try:
		import time
		lastUpdate=selfAddon.getSetting( "lastupdate" )
		do_update=False
		now_date=time.strftime("%d/%m/%Y")
		if lastUpdate==None or lastUpdate=="":
			do_update=True
		else:
			#print 'lastUpdate',lastUpdate,now_date
			if not now_date==lastUpdate:
				do_update=True
		selfAddon.setSetting( id="lastupdate" ,value=now_date)
		if do_update:
			RefreshResources(True)
	except: pass

def RefreshResources(auto=False):
#	print Fromurl
	pDialog = xbmcgui.DialogProgress()
	if auto:
		ret = pDialog.create('XBMC', 'Daily Auto loading Fetching resources...')
	else:
		ret = pDialog.create('XBMC', 'Fetching resources...')
	baseUrlForDownload='https://raw.githubusercontent.com/Shani-08/ShaniXBMCWork/master/plugin.video.shahidmbcnet/resources/community/'
	Fromurl=baseUrlForDownload+'Resources.xml'
	req = urllib2.Request(Fromurl)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	response = urllib2.urlopen(req)
	data=response.read()
	response.close()
	#data='<resources><file fname="Categories.xml"/><file fname="palestinecoolUrls.xml" url="http://goo.gl/yNlwCM"/></resources>'
	pDialog.update(20, 'Importing modules...')
	soup= BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
	resources=soup('file')
	fileno=1
	totalFile = len(resources)
	
	for rfile in resources:
		progr = (fileno*80)/totalFile
		fname = rfile['fname']
		remoteUrl=None
		try:
			remoteUrl = rfile['url']
		except: pass
		if remoteUrl:
			fileToDownload = remoteUrl
		else:
			fileToDownload = baseUrlForDownload+fname
		#print fileToDownload
		req = urllib2.Request(fileToDownload)
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
		response = urllib2.urlopen(req)
		data=response.read()
		if len(data)>0:
			with open(os.path.join(communityStreamPath, fname), "wb") as filewriter:
				filewriter.write(data)
			pDialog.update(20+progr, 'imported ...'+fname)
		else:
			pDialog.update(20+progr, 'Failed..zero byte.'+fname)
		fileno+=1
	pDialog.close()
	dialog = xbmcgui.Dialog()
	ok = dialog.ok('XBMC', 'Download finished. Close Addon and come back')

def removeLoginFile(livePlayer,TeleDunet,showMsg=True):
	something_done=False
	try:
		if livePlayer:
			something_done=True
			selfAddon.setSetting( id="lastLivetvWorkingCode" ,value="")
			COOKIEFILE = communityStreamPath+'/livePlayerLoginCookie.lwp'
			os.remove(COOKIEFILE)
			
	except: pass
	try:
		if TeleDunet:
			if communityStreamPath not in sys.path:
				sys.path.append(communityStreamPath)
			#print processor
		
		
			#from importlib import import_module
			processorObject=import_module('teledunetPlayer')
			processorObject.clearFileCache()
			something_done=True
			COOKIEFILE = communityStreamPath+'/teletdunetPlayerLoginCookie.lwp'
			os.remove(COOKIEFILE)
	except: pass
	if something_done and showMsg:
		time = 2000  #in miliseconds
		line1="Session data removed!"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

def ShowSettings(Fromurl):
	current_LivePlayerLogin=selfAddon.getSetting( "liveTvLogin" )+selfAddon.getSetting( "liveTvPassword")
	current_teleDunetLogin=selfAddon.getSetting( "teledunetTvLogin" )+selfAddon.getSetting( "teledunetTvPassword")
	selfAddon.setSetting( id="clearLogonSettings" ,value="false")
	selfAddon.openSettings()
	#print 'after settings'
	clearLogonSettings=selfAddon.getSetting( "clearLogonSettings" )
	after_LivePlayerLogin=selfAddon.getSetting( "liveTvLogin" )+selfAddon.getSetting( "liveTvPassword")
	after_teleDunetLogin=selfAddon.getSetting( "teledunetTvLogin" )+selfAddon.getSetting( "teledunetTvPassword")
	removeLoginFile(clearLogonSettings=="true" or not current_LivePlayerLogin==after_LivePlayerLogin, clearLogonSettings=="true" or not current_teleDunetLogin==after_teleDunetLogin )
	return

def LIVETvLogin(Fromurl):
	Msg=""
	try:
	
		if communityStreamPath not in sys.path:
				sys.path.append(communityStreamPath)
		removeLoginFile(True,False,showMsg=False)
		processorObject=import_module('livetvPlayer')
		new_code=processorObject.getLoginCode()
		if new_code:
			selfAddon.setSetting( id="liveTvNonPremiumCode" ,value=new_code)
			Msg="Login successful"
		else:
			Msg="Login failed.If login not working then enter the code manually in the settings."
	except:
		traceback.print_exc(file=sys.stdout)
		Msg="Login failed.If login not working then enter the code manually in the settings."
	dialog = xbmcgui.Dialog()
	ok = dialog.ok('Livetv Login', Msg)
	return
	
def AddSeries(Fromurl,pageNumber=""):
#	print Fromurl
	req = urllib2.Request(Fromurl)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	#print Fromurl
#	print "addshows"
#	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
#	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)
	#regstring='<a href="(.*?)">[\s\t\r\n\f]*.*[\s\t\r\n\f]+.*[\s\t\r\n\f].*<img .*?alt="(.*?)" src="(.*?)"'
	regstring='<a href="(\/ar\/(show|series).*?)">\s.*\s*.*\s.*alt="(.*)" src="(.*?)" '
	match =re.findall(regstring, link)
	#print match
	#match=re.compile('<a href="(.*?)"targe.*?<img.*?alt="(.*?)" src="(.*?)"').findall(link)
	#print Fromurl


	for cname in match:
		addDir(cname[2] ,getMainUrl()+cname[0] ,4,cname[3])#name,url,img
	if mode==6:
		if not pageNumber=="":
			pageNumber=str(int(pageNumber)+1);#parseInt(1)+1;
		else:
			pageNumber="1";

		purl=getMainUrl()+'/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.sort-latest.pageNumber-%s.html' % pageNumber
		addDir('Next Page' ,purl ,6,addonArt+'/next.png', False,pageNumber=pageNumber)		#name,url,mode,icon
	
#	<a href="http://www.zemtv.com/page/2/">&gt;</a></li>
#	match =re.findall('<a href="(.*)">&gt;<\/a><\/li>', link, re.IGNORECASE)
	
#	if len(match)==1:
#		addDir('Next Page' ,match[0] ,2,'')
#       print match
	
	return

def AddEnteries(Fromurl,pageNumber=0):
#	print Fromurl
	req = urllib2.Request(Fromurl)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
#	print "addshows"
#	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
#	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)
#	print Fromurl
	match =re.findall('<a href="(\/ar\/episode.*?)">\s.*\s.*\s.*\s.*\s.*\s.*<img .*?alt="(.*?)" src="(.*?)".*\s.*.*\s.*.*\s.*.*\s.*.*\s.*.*\s.*\s*.*?>(.*?)<\/div>\s*.*?>(.*?)<\/div>', link, re.UNICODE)
#	print Fromurl

	#print match
	#h = HTMLParser.HTMLParser()
	
	#print match
	totalEnteries=len(match)
	for cname in match:
		finalName=cname[1];
		if len(finalName)>0: finalName+=' '
		finalName+=cname[3].replace('<span>','').replace('</span>','')
		
		#print 'a1'
		
		#if len(finalName)>0: finalName+=u" ";
		#print 'a2'
		if len(finalName)>0: finalName+=' '
		finalName+=cname[4]
		#print 'a3'
		#finalName+=cname[3]
		#print 'a4'
        
		#print cname[2]
		addDir(finalName ,getMainUrl()+cname[0] ,5,cname[2],showContext=True,isItFolder=False)
		
		
	if totalEnteries==24:
		match =re.findall('<li class="arrowrgt"><a.*?this, \'(.*?(relatedEpisodeListingDynamic).*?)\'', link, re.UNICODE)
		if len(match)>0 or mode==7  :
			if not pageNumber=="":
				pageNumber=str(int(pageNumber)+1);#parseInt(1)+1;
			else:
				pageNumber="1";
			if mode==7:
				newurl=(Fromurl.split('pageNumber')[0]+'-%s.html')%pageNumber
			else:
				newurl=getMainUrl()+match[0][0]+'.sort-number:DESC.pageNumber-%s.html'%pageNumber;
			addDir('Next Page' ,newurl ,7,addonArt+'/next.png', False,pageNumber=pageNumber)		#name,url,mode,icon
	
		
		
#	<a href="http://www.zemtv.com/page/2/">&gt;</a></li>
	#match =re.findall('<link rel=\'next\' href=\'(.*?)\' \/>', link, re.IGNORECASE)
	
	#if len(match)==1:
#		addDir('Next Page' ,match[0] ,3,'')
#       print match
	
	return
	
def AddChannels(liveURL):
	req = urllib2.Request(liveURL)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
#	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
#	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)

	match =re.findall('<div class="subitem".*?id="(.*)">\s*.*\s*<a href="(.*?)".*\s.*\s*<.*src="(.*?)"', link,re.M)

	#print match
	#h = HTMLParser.HTMLParser()
	#print match
	for cname in match:
		chName=cname[1].split('/')[-1].split('.htm')[0]
		#print chName
		addDir(chName ,getMainUrl()+cname[1] ,3,cname[2], False,isItFolder=True)		#name,url,mode,icon

	return	
	
def AddYoutubeSources(url):
	addDir('Most Popular' ,'MOSTPOP' ,23,addonArt+'/top.png',isHTML=False)
	addDir('Most Popular Today' ,'MOSTPOPToday' ,23,addonArt+'/toptday.png',isHTML=False)
	#addDir('Most Viewed' ,'https://gdata.youtube.com/feeds/api/standardfeeds/most_popular?orderby=viewCount' ,20,addonArt+'/topview.png',isHTML=False)
	data=getYoutubeSources()
	addDir('Your Videos' ,'LOCAL' ,19,addonArt+'/yourtube.png',isItFolder=True, isHTML=False)		#name,url,mode,icon

	for stuff in data:
		addDir(stuff[0] ,stuff[1] ,19,stuff[2],isItFolder=True, isHTML=False)		#name,url,mode,icon
	



def getYoutubeSources():
	#Ssoup=getSoup('YoutubeSources.xml');
	sources=getEtreeFromFile('YoutubeSources.xml');
	ret=[]
	try:
		for source in sources.findall('source'):
			isEnabled = source.findtext('enabled').lower()
			if isEnabled=="true":
				ret.append([source.findtext('sname'),source.findtext('url'),source.findtext('imageurl')])
	except:
		traceback.print_exc(file=sys.stdout)
		pass
	return ret
		
def PlayYoutube(url):
	youtubecode=url
	uurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubecode
	xbmc.executebuiltin("xbmc.PlayMedia("+uurl+")")

def AddYoutubePlaylists(channelId):
	#if not username.startswith('https://www.googleapis'):
	#	channelId=getChannelIdByUserName(username)#passusername
	#else:
	#	channelId=username
	#channelId=username
	playlists,next_page=getYouTubePlayList(channelId);
	for playList in playlists:
		#print playList
		addDir(playList[0] ,playList[1] ,23,playList[2],isItFolder=True, isHTML=False)		#name,url,mode,icon
	if next_page:
		addDir('Next' ,next_page ,22,addonArt+'/next.png',isItFolder=True)		#name,url,mode,icon
	
		
def getYouTubePlayList(channelId):
	if not channelId.startswith('https://www.googleapis'):
		u_url='https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=%s&maxResults=25&key=%s'%(channelId,apikey)
	else:
		u_url=channelId
	doc=getJson(u_url)
	ret=[]
	for playlist_item in doc['items']:
		
		title = playlist_item["snippet"]["title"]
		id = playlist_item["id"]
		if not title=='Private video':
			imgurl=''
			try:
				imgurl= playlist_item["snippet"]["thumbnails"]["high"]["url"]
			except: pass
			if imgurl=='':
				try:
					imgurl= playlist_item["snippet"]["thumbnails"]["default"]["url"]
				except: pass
			ret.append([title,id,imgurl])
	nextItem=None
	if 'nextPageToken' in doc:
		nextItem=doc["nextPageToken"]
	else:
		nextItem=None
		
	nextUrl=None
	if nextItem:
		if not '&pageToken' in u_url:
			nextUrl=u_url+'&pageToken='+nextItem
		else:
			nextUrl=u_url.split('&pageToken=')[0]+'&pageToken='+nextItem
		
	return ret,nextUrl;
	
def AddYoutubeVideosByChannelID(channelId,addIconForPlaylist):
	AddPlayListIcon=True #add all the time
	#if AddPlayListIcon="yes":
	#	AddPlayListIcon=True
	#channelId=getChannelIdByUserName(url)#passusername
	playlist=getUploadPlaylist(channelId)
	AddYoutubeVideosByPlaylist(playlist,AddPlayListIcon,channelId)

def AddYoutubeVideosByPlaylist(playListId,AddPlayListIcon=False, channelid=None):
	#print 'AddYoutube',url
	if playListId=='MOSTPOP':
		videos,next_page=getYoutubeVideosPopular();
	elif playListId=='MOSTPOPToday':
		videos,next_page=getYoutubeVideosPopular(True);
	else:
		videos,next_page=getYoutubeVideosByPlaylist(playListId);
	if AddPlayListIcon:
		addDir('Playlists' ,channelid ,22,addonArt+'/playlist.png',isHTML=False) 
	
	for video in videos:
		#print chName
		#print video
		addDir(video[0] ,video[1] ,21,video[2],isItFolder=False, isHTML=False)		#name,url,mode,icon
	if next_page:
		addDir('Next' ,next_page ,23,addonArt+'/next.png',isItFolder=True)		#name,url,mode,icon

def getFirstElement(elements,attrib, val):
	for el in elements:
		#print el.attrib[attrib]
		if el.attrib[attrib]==val:
			#print 'found next'
			return el
	return None

def getJson(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	response = urllib2.urlopen(req)
	#link=response.read()
	#response.close()
	decoded = json.load(response)
	return decoded
	
	
def getChannelIdByUserName(username):
	u_url='https://www.googleapis.com/youtube/v3/channels?part=id&forUsername=%s&key=%s'%(username,apikey)
	channelData=getJson(u_url)
	return channelData['items'][0]['id']

def getUploadPlaylist(mainChannel):
	u_url='https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id=%s&key=%s'%(mainChannel,apikey)
	doc=getJson(u_url)
	upload_feed=doc['items'][0]['contentDetails']['relatedPlaylists']['uploads']
	return upload_feed

	
def getYoutubeVideosByPlaylist(playlistId):
	if playlistId.startswith('https://www'):
		#nextpage
		u_url=playlistId
	else:
		u_url='https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=25&playlistId=%s&key=%s'%(playlistId,apikey)
	videos=getJson(u_url)
	return prepareYoutubeVideoItems(videos,u_url)

def getYoutubeVideosPopular(today=False):
	if not today:
		u_url='https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&order=viewCount&type=video&key=%s'%(apikey)
	else:
		import datetime
		t=datetime.datetime.utcnow()-datetime.timedelta(days=1)
		yesterday=t.strftime("%Y-%m-%dT%H:%M:%SZ")
		u_url='https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&order=viewCount&type=video&key=%s&publishedAfter=%s'%(apikey,yesterday)
	videos=getJson(u_url)
	return prepareYoutubeVideoItems(videos,u_url)




def prepareYoutubeVideoItems(videos,urlUsed):
	#print 'urlUsed',urlUsed
	if 'nextPageToken' in videos:
		nextItem=videos["nextPageToken"]
	else:
		nextItem=None
	ret=[]
	for playlist_item in videos["items"]:
		title = playlist_item["snippet"]["title"]
		#print 'urlUsed',urlUsed
		if not 'search?part=snippet' in urlUsed:
			video_id = playlist_item["snippet"]["resourceId"]["videoId"]
		else:
			video_id =playlist_item["id"]["videoId"]
		if not title=='Private video':
			imgurl=''
			try:
				imgurl= playlist_item["snippet"]["thumbnails"]["high"]["url"]
			except: pass
			if imgurl=='':
				try:
					imgurl= playlist_item["snippet"]["thumbnails"]["default"]["url"]
				except: pass
		#print "%s (%s)" % (title, video_id)
			ret.append([title,video_id,imgurl])
	nextUrl=None
	if nextItem:
		if not '&pageToken' in urlUsed:
			nextUrl=urlUsed+'&pageToken='+nextItem
		else:
			nextUrl=urlUsed.split('&pageToken=')[0]+'&pageToken='+nextItem
	return ret,nextUrl;

def AddStreams():
	match=getStreams();
	#print 'match',match
	match=sorted(match,key=lambda x:x[0].lower())
	cstream='<channels>'
	infostream='<streamingInfos>'
	#print 'match',match
	for cname in match:
		if 'hdarabic' in cname[1]:
			chName=Colored(cname[0],'one',False);
			chUrl = cname[1]
			if not 'http:' in cname[2]:
				imageUrl = 'http://www.hdarabic.com/./images/'+cname[2]+'.jpg'
			else:
				imageUrl=cname[2]
			#print imageUrl
			#print chName
			addDir(chName ,chUrl ,10,imageUrl, False,isItFolder=False)		#name,url,mode,icon
		else:
			chName=Colored(cname[1],'two',False);
			chUrl = cname[0]
			imageUrl = 'http://www.teledunet.com/tv_/icones/%s.jpg'%cname[0]
			#print imageUrl
			#print chName
			addDir(chName ,chUrl ,11,imageUrl, False,isItFolder=False)		#name,url,mode,icon#<assignedcategory></assignedcategory>
			cstream+='<channel><id>%s</id><cname>%s</cname><imageurl>%s</imageurl><enabled>True</enabled></channel>'%(chUrl,cname[1],imageUrl)
			infostream+='<streaminginfo><id>%s</id><url>%s</url></streaminginfo>'%(chUrl,chUrl)
	cstream+='</channels>'
	infostream+='</streamingInfos>'
	#print cstream
	#print infostream
	return
	
def PlayStream(url, name, mode):

	if mode==10:
		req = urllib2.Request(url)
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		match =re.findall('file: "rtmp([^"]*)', link)

		rtmpLink=match[0]
		#rtmpLink='://192.95.32.7:1935/live/dubai_sport?user=MjA5N2Q3YjA2M2Q2ZjhiNWNjODAzYWJmM2RmNzU4YWE=&pass=fc9226bd032346a2deab1f903652229b'
		liveLink="rtmp%s app=live/ swfUrl=http://www.hdarabic.com/jwplayer.flash.swf pageUrl=http://www.hdarabic.com live=1 timeout=15"%rtmpLink
	else:
		newURL='http://www.teledunet.com/tv_/?channel=%s&no_pub'%url
		req = urllib2.Request(newURL)
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
		req.add_header('Referer',newURL)

		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		match =re.findall('time_player=(.*?);', link)
		match=str(long(float(match[0])))

		liveLink='rtmp://5.135.134.110:1935/teledunet playpath=%s swfUrl=http://www.teledunet.com/tv_/player.swf?id0=%s&skin=bekle/bekle.xml&channel=%s  pageUrl=http://www.teledunet.com/tv_/?channel=%s&no_pub live=1  timeout=15'%(url,match,url,url)
		
	#print 'liveLink',liveLink

	listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=liveLink )
	xbmc.Player().play( liveLink,listitem)


def getSourceAndStreamInfo(channelId, returnOnFirst,pDialog):
	try:
		ret=[]
		#Ssoup=getSoup('Sources.xml');
		sourcesXml=getEtreeFromFile('Sources.xml');
		default_source=''
		config=getChannelSettings( channelId)
		match_title=''
		if config and 'defaultsource' in config:
			default_source=config['defaultsource'].split(':')[0]
			try:
				match_title= ''.join(config['defaultsource'].split(':')[1:])
				print 'match_title in settings',match_title,default_source
			except: pass
		#print 'default_source',default_source
		orderlist={}
		default_source_exists=False
		total_sources=12
		for n in range(total_sources):
			val=selfAddon.getSetting( "order"+str(n+1) )
			if val and not val=="":
				#print 'val',val,default_source
				orderlist[val]=n*100
				if not default_source=='' and default_source ==val:
					orderlist[val]=-100



					
			
		#print orderlist
		#print 'sources',sources
		num=0

		
		pDialog.update(30, 'Looping on sources')
		sources=sourcesXml.findall('source')
		for source in sources:
			num+=1
			pDialog.update(30+(num*70)/len(sources) , 'Checking ..'+source.findtext('sname'))
			try:
				#print 'source....................',source
				xmlfile = source.findtext('urlfile')
				isEnabled = source.findtext('enabled').lower()
				sid = source.findtext('id')
				sname = source.findtext('sname')
				#print 'sid',sid,xmlfile
				isAbSolutePath=False
				if sname=="Local":
					#
					isAbSolutePath=True
					isEnabled="false"
					filename=selfAddon.getSetting( "localstreampath" ).decode('utf-8')
					if filename and len(filename)>0:
						isEnabled="true"
						xmlfile=filename
				settingname="is"+sname.replace('.','')+"SourceDisabled"
				settingDisabled=selfAddon.getSetting(settingname)  
				#print 'settingDisabled',settingDisabled
				if isEnabled=="true" and not settingDisabled=="true":
					#print 'source is enabled',sid
					#csoup=getSoup(xmlfile,isAbSolutePath);
					streamingxml=getEtreeFromFile(xmlfile,isAbSolutePath);
					#ccsoup = csoup("streaminginfo")
					#print 'csoup',csoup,channelId
					#print csoup 
					#sInfo=csoup.findAll('streaminginfo',{'cname':re.compile("^"+channelId+"$", re.I)})
					#sInfo=csoup.findAll('streaminginfo',{'cname':channelId})
					#sInfo=csoup.findAll('streaminginfo',{'cname':channelId})
					sInfos=streamingxml.findall('streaminginfo')
					sInfo=[]
					for inf in sInfos:
						if inf.findtext('cname').lower()==channelId.lower():
							source_title=''
							if match_title<>'':
								try:
									if source.findtext('id')=='generic':
										source_title=inf.find('item').findtext('title')
									else:
										source_title=inf.findtext('title')
								except: pass
                                    
							#print default_source,sid,match_title,inf.findtext('title'),inf
							if not default_source=='' and default_source==sname and (match_title =='' or match_title==source_title):                       
								default_source_exists=True
							sInfo.append(inf)
					name_find=sname
					if name_find in orderlist:
						order= orderlist[name_find]
					else:
						print 'not found',name_find,orderlist
						order=20000
					order+=num
					if not sInfo==None and len(sInfo)>0:
						print 'sInfo...................',len(sInfo)
						
						for single in sInfo:
							source_title=''
							if match_title<>'':
								try:
									if source.findtext('id')=='generic':
										source_title=single.find('item').findtext('title')
									else:
										source_title=single.findtext('title')
								except: pass
							if (match_title =='' or match_title==source_title):
								print 'title match for order', match_title,source_title
								order-=1
							ret.append([source,single,order])
						#if returnOnFirst:
						#	break;
			except:
				traceback.print_exc(file=sys.stdout)
				pass
	except:
		traceback.print_exc(file=sys.stdout)
		pass
	#print 'unsorted ret',ret

	#print ret
	ret= sorted(ret,key=lambda x:x[2])
	print ret
	return ret,default_source_exists and not default_source==''

def selectSource(sources,fromSelectSource=False):
    if 1==1 or len(sources) > 1:
        #print 'total sources',len(sources)
        dialog = xbmcgui.Dialog()
        titles = []
        for source in sources:
            (s,i,o) =source
            #print 'i',i.id,i
            if s.findtext('id')=="generic":
                try:
                    #print 'trying generic name'
                    titles.append(s.findtext('sname')+': '+i.find('item').findtext('title'))
                    #print 'trying generic name end '
                except:
                    titles.append(s.findtext('sname'))
            else:
                try:
                    titles.append(s.findtext('sname')+': '+i.findtext('title'))
                except: titles.append(s.findtext('sname'))

        if fromSelectSource:
            titles.append(Colored('Clear Default Source setting','one',True))

        index = dialog.select('Choose your stream', titles)
        if index > -1:
            if index>len(sources)-1:
                return 'remove'#remove it
            else:
                return sources[index]
        else:
            return False

def selectDefaultSourcesForChannel(channelId ):
	try:
		pDialog = xbmcgui.DialogProgress()
		ret = pDialog.create('XBMC', 'Finding available resources...')
		pDialog.update(20, 'Finding sources..')
		providers, default_source_exists=getSourceAndStreamInfo(channelId,False,pDialog)
		if len(providers)==0:
			pDialog.close()
			time = 2000  #in miliseconds
			line1="No sources found"
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
			return None
		selectedprovider=selectSource(providers,True)
		if not selectedprovider:
			return None
		if selectedprovider=='remove':
			return ''
		fav_source=''   
		source,sInfo,order=selectedprovider #pick first one
		fav_source=source.findtext('sname')
		try:
			if source.findtext('id')=="generic":
				fav_source=source.findtext('sname')+':'+sInfo.find('item').findtext('title')
			else:
				fav_source=source.findtext('sname')+':'+sInfo.findtext('title')
		except:pass

		return fav_source
	except:
		traceback.print_exc(file=sys.stdout)
		return None
		
def PlayCommunityStream(channelId, name, mode):
	try:
		#print 'PlayCommunityStream'
		xbmcplugin.endOfDirectory(int(sys.argv[1]))
		pDialog = xbmcgui.DialogProgress()
		ret = pDialog.create('XBMC', 'Finding available resources...')
		#print 'channelId',channelId
		playFirst=selfAddon.getSetting( "playFirstChannel" )
		if playFirst==None or playFirst=="" or playFirst=="false":
			playFirst=False
		else:
			playFirst=True
		playFirst=bool(playFirst)
		pDialog.update(20, 'Finding sources..')
		providers,default_source_exists=getSourceAndStreamInfo(channelId,playFirst,pDialog)
		if default_source_exists:
			playFirst=True
		if len(providers)==0:
			pDialog.close()
			time = 2000  #in miliseconds
			line1="No sources found"
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
			return
		pDialog.update(30, 'Processing sources..')
		pDialog.close()
		#source=providers[""]

		
		enforceSourceSelection=False
		#print 'playFirst',playFirst
		done_playing=False
		current_index=0
		auto_skip=False
		auto_skip=True if selfAddon.getSetting( "playOneByOne" )=="true" else False
		while not done_playing:
			#print 'trying again',enforceSourceSelection
			ret = pDialog.create('XBMC', 'Trying to play the source')
			#print 'dialogue creation'
			done_playing=True
			if (enforceSourceSelection or (len (providers)>1 and not playFirst)) and not auto_skip:
				#print 'select sources'
				selectedprovider=selectSource(providers)
				if not selectedprovider:
					return
			else:
				selectedprovider=providers[current_index]
				enforceSourceSelection=True
			#print 'picking source'
			(source,sInfo,order)=selectedprovider #pick first one
			#print source

			processor = source.findtext('processor')
			sourcename = source.findtext('sname')

			if communityStreamPath not in sys.path:
				sys.path.append(communityStreamPath)
			#print processor
		
		
			#from importlib import import_module
			processorObject=import_module(processor.replace('.py',''))
		
		
			pDialog.update(60, 'Trying to play..')
			pDialog.close()
			sinfoSoup= BeautifulSOAP(etree.tostring(sInfo), convertEntities=BeautifulStoneSoup.XML_ENTITIES)
			done_playing=processorObject.PlayStream(source,sinfoSoup,name,channelId)
			#print 'done_playing',done_playing
			if not done_playing:
				time = 2000  #in miliseconds
				line1="Failed playing from "+sourcename
				xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
				if auto_skip:
					done_playing=False
					current_index+=1
					if current_index>len(providers):
						done_playing=True
					if not done_playing:
						(s,i,o) =providers[current_index]
						titles=''
						if s.findtext('id')=="generic":
							try:
								#print 'trying generic name'
								titles=s.findtext('sname')+': '+i.find('item').findtext('title')
								#print 'trying generic name end '
							except:
								titles=s.findtext('sname')
						else:
							try:
								titles=s.findtext('sname')+': '+i.findtext('title')
							except: titles=s.findtext('sname')                       

						ret = pDialog.create('XBMC', 'Trying to play the Item# %d of %d, Cancel in 3 seconds.\n Source:%s'%(current_index+1, len(providers),titles))

						xbmc.sleep(3000)
						if pDialog.iscanceled():
							current_index=0
							done_playing=False
							enforceSourceSelection=True
							auto_skip=False
			#print 'donexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
		return 
	except:
		traceback.print_exc(file=sys.stdout)

def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]
	
def PlayShowLink ( url ): 
#	url = tabURL.replace('%s',channelName);

	line1 = "Finding stream"
	time = 500  #in miliseconds
	line1 = "Playing video Link"
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print url


	#print "PlayLINK"
	playURL= match =re.findall('id  : "(.*?)",\s*pricingPlanId  : "(.*?)"', link)
	videoID=match[0][0]# check if not found then try other methods
	paymentID=match[0][1]
	playlistURL=getMainUrl()+"/arContent/getPlayerContent-param-.id-%s.type-player.pricingPlanId-%s.html" % ( videoID,paymentID)
	req = urllib2.Request(playlistURL)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	jsonData=json.loads(link)
	#print jsonData;
	url=jsonData["data"]["url"]
	#print url
	
	
	defaultCDN="Default"
	defaultCDN=selfAddon.getSetting( "DefaultCDN" )
	
	#print 'default CDN',defaultCDN,cdnType
	changeCDN=""
	
	#print 'tesing if cdn change is rquired'
	if cdnType=="l3" or (cdnType=="" and defaultCDN=="l3"):
		changeCDN="l3"
	elif cdnType=="xdn" or (cdnType=="" and defaultCDN=="xdn"):
		changeCDN="xdn"
	elif cdnType=="ak" or (cdnType=="" and defaultCDN=="ak"):
		changeCDN="ak"
	#print 'changeCDN',changeCDN
	if len(changeCDN)>0:
		#print 'Changing CDN based on critertia',changeCDN
		#http://l3md.shahid.net/web/mediaDelivery/media/12af648b9ffe4423a64e8ab8c0100701.m3u8?cdn=l3
		#print 'url received',url
		playURL= re.findall('\/media\/(.*?)\.', url)
		url="http://%smd.shahid.net/web/mediaDelivery/media/%s.m3u8?cdn=%s" % (changeCDN,playURL[0],changeCDN)
		
		#print 'new url',url
		line1 = "Using the CDN %s" % changeCDN
		time = 2000  #in miliseconds
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

		
	cName=name
	listitem = xbmcgui.ListItem( label = str(cName), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=url )
	#print "playing stream name: " + str(cName) 
	listitem.setInfo( type="video", infoLabels={ "Title": cName, "Path" : url } )
	listitem.setInfo( type="video", infoLabels={ "Title": cName, "Plot" : cName, "TVShowTitle": cName } )
	#print 'playurl',url
	xbmc.Player().play( url,listitem)
	#print 'ol..'
	return

def addToMyChannels(cname):
	try:
		fileName=os.path.join(profile_path, 'MyChannels.xml')
		print fileName
		MyChannelList=getSoup(fileName,True)
	except: MyChannelList=None
	if not MyChannelList:
		MyChannelList= BeautifulSOAP('<channels></channels>')
	
	val=MyChannelList.find("channel",{"cname":cname})
	#print 'val is ',val
	if not val:
		channeltag = Tag(MyChannelList, "channel")
		channeltag['cname']=cname
		#cnametag = Tag(MyChannelList, "cname")
		#ctext = NavigableString(cname)
		#cnametag.insert(0, ctext)
		#channeltag.insert(0, cnametag)
		MyChannelList.channels.insert(0, channeltag)
		#print MyChannelList.prettify()

		with open(fileName, "wb") as filewriter:
			filewriter.write(str(MyChannelList))

def removeFromMyChannels(cname):
	try:
		fileName=os.path.join(profile_path, 'MyChannels.xml')
		print fileName
		MyChannelList=getSoup(fileName,True)
	except: return
	if not MyChannelList:
		return
	
	val=MyChannelList.find("channel",{"cname":cname})
	if val:
		#print 'val to be deleted',val
		val.extract()

		with open(fileName, "wb") as filewriter:
			filewriter.write(str(MyChannelList))

def addCommunityCats():
	#soup=getSoup('Categories.xml');
	cats=getEtreeFromFile('Categories.xml');
	#print cats 

	addDir('My Channels' ,'My Channels' ,15,addonArt+'/mychannels.png', False,isItFolder=True)		#name,url,mode,icon

	for cat in cats.findall('category'):
		chName=cat.findtext('catname')
		chUrl = cat.findtext('id')
		imageUrl = cat.findtext('imageurl')
		addDir(chName ,chUrl ,15,imageUrl, False,isItFolder=True)		#name,url,mode,icon
	return

def getCommunityChannels(catType):
	#soup=getSoup('Channels.xml');#changetoEtree
	Channelsxml=getEtreeFromFile('Channels.xml')
	#channels=soup('channel')
	retVal=[]
		
	#for channel in channels:
	searchCall='channel'
	#if not catType=="all":
	searchCall='.//category'
	#print searchCall
	MyChannelList=None
	hidechanneloption=True
	sourcesXml=getEtreeFromFile('Sources.xml');
	sources_list={}
	for sources in sourcesXml.findall('source'): 
		sname=sources.findtext('sname')
		ssname=sources.findtext('shortname')
		scolour=sources.findtext('colour')
		sources_list[sname]=[ssname,scolour]
	if catType=="My Channels":
		try:
			fileName=os.path.join(profile_path, 'MyChannels.xml')
			#print fileName
			MyChannelList=getSoup(fileName,True)
			#print MyChannelList
		except: MyChannelList=None
		
	for channel in Channelsxml.findall('channel'):
		#print channel
		chName=channel.findtext('cname')
		if 1==1:
			config=getChannelSettings( chName)
			#print 'config is ',config
			if not catType=="all":
				exists=False
				if not catType=="My Channels":
					supportCats= channel.findall(searchCall)
					if len(supportCats)==0:
						continue
					
					for c in supportCats:
						if c.text.lower()==catType.lower():
							exists=True
							break
				else:
					#check if channel exists in file
					if MyChannelList:
						val=MyChannelList.find("channel",{"cname":chName})
						if val:
							exists=True
				if config and 'hidden' in config:
					exists=not config['hidden']=="yes"
				if not exists:
					continue

			

		
		if config and 'hidden' in config:
			hidechanneloption=not config['hidden']=="yes"
		#chUrl = channel.id.text
		imageUrl =channel.findtext('imageurl')
		chUrl=chName
		if config and 'defaultsource' in config:
			default_source=config['defaultsource'].split(':')[0]
			#chName+='['+default_source+']'
			if default_source in sources_list:
				short_name='['+sources_list[default_source][0]+']'
				colour=sources_list[default_source][1]
				short_name=Colored(text = short_name, colorid = colour, isBold = False)
				print short_name

				chName+=' '+short_name
				
 		retVal.append([chUrl,chName,imageUrl,hidechanneloption])
	return retVal
	

def addCommunityChannels(catType):
	channels=getCommunityChannels(catType)
	channels=sorted(channels,key=lambda x:x[1].lower())
	for channel in channels:
		chName=channel[1]
		chUrl = channel[0]
		imageUrl = channel[2]
		hideChannel=channel[3]
		addRemoveMyChannel=not catType=="My Channels"
 		addDir(chName ,chUrl ,16,imageUrl, False,isItFolder=False,AddRemoveMyChannels=addRemoveMyChannel, SelectDefaultSource=True,hideChannel=hideChannel )		#name,url,mode,icon
	return

def setChannelSettings(cname,settingName,SettingVal):
	current_setting=getChannelSettings(cname)
	if current_setting==None:
		current_setting={settingName:SettingVal}
	else:
		current_setting[settingName]=SettingVal
	#print 'current_setting',current_setting
	saveChannelSettings(cname,current_setting)


def getChannelSettings(cname):
	current_string=selfAddon.getSetting( cname+"-settings")
	#print cname+"-settings",current_string
	if current_string=="":
		return None
	#print 'current_string',current_string
	return json.loads(current_string)


def saveChannelSettings(cname, json_data):
	store=""
	if json_data:
		store=json_data
	selfAddon.setSetting( id=cname+"-settings" ,value=json.dumps(store))



	
	
def getEtreeFromFile(fileName, isabsolutePath=False):
	try:
		#print 'communityStreamPath',communityStreamPath
		#print 'fileName',fileName
		strpath=os.path.join(communityStreamPath, fileName)
		#print 'strpath',strpath
		if isabsolutePath:
			strpath=fileName
		data = open(strpath, "r").read()
		return getETreeFromString(data)
	except:
		print 'somethingwrong'
		traceback.print_exc(file=sys.stdout)
	
#obselete
def getSoup(fileName, isabsolutePath=False):
	strpath=os.path.join(communityStreamPath, fileName)
	if isabsolutePath:
		strpath=fileName
	data = open(strpath, "r").read()
	return BeautifulSOAP(data)#, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
	#return BeautifulStoneSoup(data,convertEntities=BeautifulStoneSoup.XML_ENTITIES);

def getETreeFromUrl(video_url):
	req = urllib2.Request(video_url)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	response = urllib2.urlopen(req)
	data=response.read()
	response.close()

	return getETreeFromString(data)
	#return BeautifulSOAP(data)
def getETreeFromString(str):
	return etree.fromstring(str)
	
def getStreams():
	defaultStream="All"
	defaultStream=selfAddon.getSetting( "DefaultStream" )
	if defaultStream=="": defaultStream="All"
	hdArab= [('Al Jazeera','http://www.hdarabic.com/aljazeera.php','jazeera'),
	('Al Jazeera Mubasher','http://www.hdarabic.com/aljazeera.php','jazeera'),
	('Al Jazeera Egypt','http://www.hdarabic.com/aljazeera.php','jazeera'),
	('Al Jazeera Documentary','http://www.hdarabic.com/aljazeera.php','jazeera'),
	('Al Jazeera English','http://www.hdarabic.com/aljazeera.php','jazeera'),
	('Al Jazeera America','http://www.hdarabic.com/aljazeera.php','jazeera'),
	('Hurra Iraq','http://www.hdarabic.com/alhurra_iraq.php','hurra_iraq'),
	('Al Iraqia','http://www.hdarabic.com/aliraqiya.php','iraqiay'),
	('SemSem','http://www.hdarabic.com/semsem.php','semsem_tv'),
	('Al Arabiya','http://www.hdarabic.com/alarabiya.php','alarabiya'),
	('France 24','http://www.hdarabic.com/f24.php','f24'), 
	('France 24 English','http://www.hdarabic.com/f24.php','f24'),
	('France 24 France','http://www.hdarabic.com/f24.php','f24'),
	('Al hiwar','http://www.hdarabic.com/alhiwar.php','alhiwar'),
	('Skynews','http://www.hdarabic.com/skynews.php','skynews'),
	('Skynews English','http://www.hdarabic.com/skynews.php','skynews'),
	('BBC Arabic','http://www.hdarabic.com/bbc.php','bbc'),
	('Al mayadeen','http://www.hdarabic.com/almayaden.php','almayaden'),
	('TAHA','http://www.hdarabic.com/taha.php','taha'),
	('National Wild','http://www.hdarabic.com/national_wild.php','national_wild'),
	('National Geographic Abu','http://www.hdarabic.com/national.php','ng'),
	('HODHOD','http://www.hdarabic.com/hod_hod.php','hod_hod'),
	('Karamesh','http://www.hdarabic.com/karamesh.php','karamesh'),
	('Al Jazeera Children','http://www.hdarabic.com/jazeerakids.php','jsckids'),
	('Qatar','http://www.hdarabic.com/qatar.php','qatar'),
	('Tunisia 1','http://www.hdarabic.com/tunis1.php','tunisia1'),
	('Tunisia 2','http://www.hdarabic.com/tunisia_2.php','tv_tunisia2'),
	('Sama Dubai','http://www.hdarabic.com/sama_dubai.php','Sama-dubai'),
	('B4U plus','http://www.hdarabic.com/b4u+.php','b4u+'),
	('B4U Aflam','http://www.hdarabic.com/b4u_aflam.php','b4u_aflam'),
	('Saudi Sport','http://www.hdarabic.com/saudi_sport.php','saudi_sport'),
	('Dubai Sport','http://www.hdarabic.com/dubai_sport.php','dubai-sport'),
	('Dubai Sport 3','http://www.hdarabic.com/dubai_sport_3.php','dubai-sport'),
	('Dubai Racing','http://www.hdarabic.com/dubai_racing.php','dubai_racing'),
	('Oman','http://www.hdarabic.com/oman.php','oman_tv'),
	('Dubai','http://www.hdarabic.com/dubai.php','dubai'),
	('Play Hekayat','http://www.hdarabic.com/play_hekayat.php','play_hekayat'),
	('Watan','http://www.hdarabic.com/play_hekayat.php','watan'),
	('Watan Plus','http://www.hdarabic.com/play_hekayat.php','watan_plus'),
	('Watan ghanawi','http://www.hdarabic.com/play_hekayat.php','watan_ghanawi'),
	('Fox Movie','http://www.hdarabic.com/fox_movie.php','fox_movies'),
	('ART Aflam 1','http://www.hdarabic.com/art_1.php','art1'),
	('ART Aflam 2','http://www.hdarabic.com/art2.php','art_aflam2'),
	('ART Cinema ','http://www.hdarabic.com/art.php','art'),
	('ART Hekayat','http://www.hdarabic.com/art_hekayat.php','art_hekayat'),
	('ART Hekayat 2','http://www.hdarabic.com/art_hekayat_2.php','art_hekayat_2'),
	('Melody Arabia','http://www.hdarabic.com/melody.php','melodytv'),
	('Melody Aflam','http://www.hdarabic.com/melody_aflam.php','melodytv'),
	('Melody Classic','http://www.hdarabic.com/melody_classic.php','melodytv'),
	('Melody Hits','http://www.hdarabic.com/melody_hits.php','melodytv'),
	('Melody Drama','http://www.hdarabic.com/melody_drama.php','melodytv'),
	('Mehwar','http://www.hdarabic.com/mehwar.php','mehwar'),
	('Mehwar 2','http://www.hdarabic.com/mehwar2.php','mehwar2'),
	('Talaki','http://www.hdarabic.com/mehwar2.php','talaki'),
	('Syria News','http://www.hdarabic.com/mehwar2.php','syria_news'),
	('Oscar Drama','http://www.hdarabic.com/oscar_drama.php','oscar_drama'),
	('Cima','http://www.hdarabic.com/cima.php','cima'),
	('Cairo Cinema','http://www.hdarabic.com/cairo_cinema.php','cairo_cinema'),
	('Cairo Film','http://www.hdarabic.com/cairo_film.php','cairo_film'),
	('Cairo Drama','http://www.hdarabic.com/cairo_drama.php','cairo_drama'),
	('IFilm Arabic','http://www.hdarabic.com/cairo_drama.php','ifilm'),
	('IFilm English','http://www.hdarabic.com/cairo_drama.php','ifilm'),
	('IFilm Farsi','http://www.hdarabic.com/cairo_drama.php','ifilm'),
	('Gladiator','http://www.hdarabic.com/gladiator.php','gladiator'),
	('ESC1','http://www.hdarabic.com/esc1.php','al_masriya_eg'),
	('ESC2','http://www.hdarabic.com/esc2.php','masriaesc2'),
	('Bein Sport 1','http://www.hdarabic.com/jsc1.php','bein_sport'),
	('Bein Sport 2','http://www.hdarabic.com/jsc2.php','bein_sport'),
	('Bein Sport 3','http://www.hdarabic.com/jsc3.php','bein_sport'),
	('Bein Sport 4','http://www.hdarabic.com/jsc4.php','bein_sport'),
	('Bein Sport 5','http://www.hdarabic.com/jsc5.php','bein_sport'),
	('Bein Sport 6','http://www.hdarabic.com/jsc6.php','bein_sport'),
	('Bein Sport 7','http://www.hdarabic.com/jsc7.php','bein_sport'),
	('Bein Sport 8','http://www.hdarabic.com/jsc8.php','bein_sport'),
	('Bein Sport 11','http://www.hdarabic.com/jsc9.php','bein_sport'),
	('Bein Sport 12','http://www.hdarabic.com/jsc10.php','bein_sport'),
	('Panorama Film','http://www.hdarabic.com/panorama_film.php','panorama_film'),
	('TF1','http://www.hdarabic.com/tf1.php','tf1'),
	('M6 Boutique','http://www.hdarabic.com/m6_boutique.php','m6'),
	('TV5','http://www.hdarabic.com/tv5.php','tv5_monde_europe'),
	('Guilli','http://www.hdarabic.com/guilli.php','guilli'),
	('Libya','http://www.hdarabic.com/libya.php','libya'),
	('Assema','http://www.hdarabic.com/assema.php','assema'),
	('Libya Awalan','http://www.hdarabic.com/libya_awalan.php','libya_awalan'),
	('RTM Tamazight','http://www.hdarabic.com/tamazight.php','tamazight'),
	('Al maghribiya','http://www.hdarabic.com/maghribiya.php','maghribiya'),
	('Sadissa','http://www.hdarabic.com/sadissa.php','sadisa'),
	('A3','http://www.hdarabic.com/a3.php','a3'),
	('Algerie 4','http://www.hdarabic.com/algerie_4.php','algerie_4'),
	('Algerie 5','http://www.hdarabic.com/algerie5.php','algerie5'),
	('Al Nahar Algerie','http://www.hdarabic.com/nahar_algerie.php','nahar_algerie'),
	('Chorouk TV','http://www.hdarabic.com/chorouk.php','chorouk'),
	('El Beit Beitak','http://www.hdarabic.com/beitak.php','beitak'),
	('Insen','http://www.hdarabic.com/insen.php','insen'),
	('Nesma','http://www.hdarabic.com/nesma.php','rouge'),
	('Tounsiya','http://www.hdarabic.com/tounsiya.php','tounsiya'),
	('Aghanina','http://www.hdarabic.com/aghanina.php','aghanina'),
	('Nojoom','http://www.hdarabic.com/nojoom.php','nojoom'),
	('Funoon','http://www.hdarabic.com/funoon.php','funoon'),
	('Mazazik','http://www.hdarabic.com/mazazik.php','mazazik'),
	('Mazzika','http://www.hdarabic.com/mazzika.php','logo-mazzika'),
	('Power Turk','http://www.hdarabic.com/power_turk.php','power_turk'),
	('Al Haneen','http://www.hdarabic.com/alhaneen.php','alhaneen'),
	('Heya','http://www.hdarabic.com/heya.php','heya'),
	('CBC','http://www.hdarabic.com/cbc.php','cbc'),
	('CBC Extra','http://www.hdarabic.com/cbc.php','cbc_extra'),
	('CBC Drama','http://www.hdarabic.com/cbc_drama.php','cbc_drama'),
	('CBC Sofra','http://www.hdarabic.com/cbc_sofra.php','cbc_sofra'),
	('Al Hayat 2 TV ','http://www.hdarabic.com/hayat_2.php','hayat_2'),
	('Top Movies ','http://www.hdarabic.com/top_movie.php','top_movies_eg'),
	('Dream 1','http://www.hdarabic.com/dream1.php','dream1'),
	('Nile Comedy','http://www.hdarabic.com/nile_comedy.php','nile_comedy'),
	('Nile News','http://www.hdarabic.com/nile_news.php','nile_news'),
	('Nile Family','http://www.hdarabic.com/nile_family.php','nile_family'),
	('Nile Education','http://www.hdarabic.com/nile_educ.php','nile_educational'),
	('Rotana Cinema','http://www.hdarabic.com/rotana_cinema.php','rotana_cinema'),
	('Rotana Clip','http://www.hdarabic.com/rotana_clip.php','rotana_clip'),
	('Rotana Classic','http://www.hdarabic.com/rotana_classic.php','rotana_classic'),
	('Rotana Khalijia','http://www.hdarabic.com/rotana_khalijiya.php','rotana-khalijia'),
	('ANB','http://www.hdarabic.com/anb.php','anb'),
	('MTV Lebanon','http://www.hdarabic.com/mtvlebanon.php','mtv1'),
	('Arabica ','http://www.hdarabic.com/arabica.php','arabica-tv'),
	('MTV Arabia','http://www.hdarabic.com/mtv_arabia.php','mtv_arabia'),
	('MBC','http://www.hdarabic.com/mbc.php','mbc'),
	('MBC 2','http://www.hdarabic.com/mbc2.php','mbc2'),
	('MBC 3','http://www.hdarabic.com/mbc3.php','mbc3'),
	('MBC Action','http://www.hdarabic.com/mbc_action.php','mbc_action'),
	('MBC Max','http://www.hdarabic.com/mbc_max.php','mbc_max'),
	('MBC Drama','http://www.hdarabic.com/mbc_drama.php','mbc_drama'),
	('MBC Masr','http://www.hdarabic.com/mbc_masr.php','mbc_masr'),
	('MBC Masr Drama','http://www.hdarabic.com/mbc_masr_drama.php','mbc_masr_drama'),
	('MBC Bollywood','http://www.hdarabic.com/mbc_bollywood.php','mbc_bollywoodl'),
	('Wanasah','http://www.hdarabic.com/wanasah.php','wanasah'),
	('Al Nahar','http://www.hdarabic.com/nahar_egy.php','Nahar-TV'),
	('Nahar +2','http://www.hdarabic.com/nahar_egy.php','nahar+2'),
	('Nahar Sport','http://www.hdarabic.com/nahar_sport.php','al_nahar_sport'),
	('LBC Europe','http://www.hdarabic.com/lbc_europe.php','lbc'),
	('Tele Liban','http://www.hdarabic.com/teleliban.php','teleliban'),
	('Syria ','http://www.hdarabic.com/syria.php','syria'),
	('Sama Syria ','http://www.hdarabic.com/sama_syria.php','sama_syria'),
	('MBC Maghreb','http://www.hdarabic.com/mbc_maghreb.php','mbc_maghreb'),
	('Abu Dhabi Sport','http://www.hdarabic.com/abu_dhabi_sport.php','abu_dhabi_sporti'),
	('Abu Dhabi','http://www.hdarabic.com/abu_dhabi_sport.php','abudhabi'),
	('Abu Dhabi Emarate','http://www.hdarabic.com/abu_emarat.php','abu_dhabi_al_emarat'),
	('Bahrain','http://www.hdarabic.com/bahrein.php','bahrain_tv'),
	('Kuwait','http://www.hdarabic.com/kowait1.php','kuwait'),
	('Kuwait 2','http://www.hdarabic.com/kowait2.php','kuwait2'),
	('Kuwait 3','http://www.hdarabic.com/kowait3.php','kuwait3'),
	('Kuwait 4','http://www.hdarabic.com/kowait4.php','kuwait4'),
	('Kuwait 5','http://www.hdarabic.com/kowait5.php','kuwait5'),
	('Kuwait 6','http://www.hdarabic.com/kowait6.php','kuwait6'),
	('LBC','http://www.hdarabic.com/lbc.php','lbc'),
	('LBC Drama','http://www.hdarabic.com/lbc_drama.php','lbc_drama'),
	('LDC','http://www.hdarabic.com/ldc.php','ldc'),
	('AL Sharqia','http://www.hdarabic.com/sharqia.php','sharqia'),
	('Al Sharqia News','http://www.hdarabic.com/sharqia_news.php','al_sharqiya_news'),
	('Orient News','http://www.hdarabic.com/orient_news.php','orientnews'),
	('Al Alam','http://www.hdarabic.com/alalam.php','alalam'),
	('Nabaa ','http://www.hdarabic.com/nabaa.php','nabaa_tv_sa'),
	('Baghdadia ','http://www.hdarabic.com/baghdad.php','al-baghdadia'),
	('Baghdadia 2','http://www.hdarabic.com/baghdad2.php','baghdad2'),
	('Kaifa','http://www.hdarabic.com/kaifa.php','kaifa'),
	('Suna Nabawiya','http://www.hdarabic.com/sunah.php','sunah'),
	('Iqrae','http://www.hdarabic.com/iqra.php','iqra'),
	('Rahma','http://www.hdarabic.com/rahma.php','rahma'),
	('Al Maaref','http://www.hdarabic.com/almaaref.php','almaaref'),
	('Sirat','http://www.hdarabic.com/sirat.php','sirat'),
	('Wesal TV','http://www.hdarabic.com/wesal.php','wesal_tv'),
	('Al Majd Massah','http://www.hdarabic.com/majd_massah.php','al_majd'),
	('Al Majd Nature','http://www.hdarabic.com/majd_nature.php','al_majd'),
	('Al Afassi','http://www.hdarabic.com/afasi.php','afasi'),
	('Al AAN','http://www.hdarabic.com/alan.php','al_aan_tv'),
	('Al Ressala','http://www.hdarabic.com/resala.php','alressala'),
	('Ctv Coptic','http://www.hdarabic.com/ctv_coptic.php','ctv_eg'),
	('Sat7','http://www.hdarabic.com/sat7.php','sat7'),
	('Sat7 Kids','http://www.hdarabic.com/sat7_kids.php','sat7_kids'),
	('Aghapy','http://www.hdarabic.com/aghapy.php','aghapy_tv'),
	('Noursat','http://www.hdarabic.com/nour_sat.php','nour_sat'),
	('Miracle','http://www.hdarabic.com/miracle.php','miracle'),
	('Royali Somali','http://www.hdarabic.com/royali_somali.php','royali_somali'),
	('Somali Channel','http://www.hdarabic.com/somali_channel.php','somali_channel'),
	('Cartoon Network','http://www.hdarabic.com/cartoon.php','cartoon_network'),
	('Baraem','http://www.hdarabic.com/baraem.php','baraem_95x64'),
	('Space Power','http://www.hdarabic.com/space_power.php','space_power'),
	('Majd Kids','http://www.hdarabic.com/majd_kids.php','majd_kids'),
	('Majd Kids 2','http://www.hdarabic.com/majd_kids_2.php','majd_kids'),
	('Majd Roda','http://www.hdarabic.com/majd_roda.php','almajd'),
	('Majd Taghrid','http://www.hdarabic.com/majd_taghrid.php','almajd'),
	('Toyor Al Janah 1','http://www.hdarabic.com/toyorjana1.php','toyor'),
	('Toyor Baby','http://www.hdarabic.com/toyorbaby.php','baby'),
	('Ajyal','http://www.hdarabic.com/ajyal.php','ajyal'),
	('ANN','http://www.hdarabic.com/ann.php','ann_95x44'),
	('Al Magharibiya','http://www.hdarabic.com/magharibia.php','http://tv.webactu-webtv.com/algerie1/magharibia.png')]
	
	if defaultStream=="hdarabic.com": return hdArab
	
	req = urllib2.Request('http://www.teledunet.com/')
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match =re.findall('set_favoris\(\'(.*?)\',\'(.*?)\'\s?(.)', link)
	if defaultStream=="teledunet.com": return match
	
	return match+hdArab
	
	


	
#print "i am here"
params=get_params()
url=None
name=None
mode=None
linkType=None
pageNumber=None
AddRemoveMyChannels=None
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

try:
	pageNumber=params["pagenum"]
except:
	pageNumber="";

args = cgi.parse_qs(sys.argv[2][1:])
cdnType=''
try:
	cdnType=args.get('cdnType', '')[0]
except:
	pass

addIconForPlaylist=""
try:
	addIconForPlaylist=args.get('addIconForPlaylist', '')[0]
except:
	pass


AddRemoveMyChannels=None
try:
	AddRemoveMyChannels=args.get('AddRemoveMyChannels', None)[0]
except:
	pass

selectDefaultSource=None

try:
	selectDefaultSource=args.get('selectDefaultSource', None)[0]
except:
	pass

HidChannel=None
try:
	HidChannel=args.get('HideChannel', None)[0]
except:
	pass

	

print 	mode,pageNumber

try:
	if not AddRemoveMyChannels==None:
		if AddRemoveMyChannels=="add":
			addToMyChannels(url)
			line1 = 'Channel has been added to My Channels list'
			time = 2000  #in miliseconds
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
			mode=-1
		else:
			removeFromMyChannels(url)
			line1 = 'Channel has been removed from My Channels list'
			time = 2000  #in miliseconds
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
			mode=15
			url="My Channels"
			print mode

	if not HidChannel==None:
		if HidChannel=="yes":
			setChannelSettings(url,'hidden',HidChannel)
			line1 = 'Channel has been hidden in categories'
			time = 2000  #in miliseconds
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
			mode=-1
		else:
			setChannelSettings(url,'hidden','')
			line1 = 'Channel has been unhidden in categories'
			time = 2000  #in miliseconds
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
			mode=-1
			url=""
			
	if not selectDefaultSource==None:
		default_source=selectDefaultSourcesForChannel(url)
		print 'v',default_source
		if not default_source==None:
			print 'saving settings',default_source    
			setChannelSettings(url,'defaultsource',default_source)
			line1 = 'setting saved'
			time = 2000  #in miliseconds
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		mode=-1

	if mode==299: #add communutycats
		print 'delete cache'
		removeLoginFile(True,True)
		line1 = 'Login sessions cleared!'
		time = 2000  #in miliseconds
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		xbmc.executebuiltin('Container.Update(plugin://plugin.video.shahidmbcnet)')
		mode=-1
		
	if mode==None or url==None or len(url)<1:
		print "InAddTypes"
		checkAndRefresh()        
		Addtypes()

	elif mode==2:
		print "Ent url is "+name,url
		AddChannels(url)

	elif mode==3 or mode==6:
		print "Ent url is "+url
		AddSeries(url,pageNumber)

	elif mode==4 or mode==7:
		print "Play url is "+url
		AddEnteries(url,pageNumber)

	elif mode==5:
		PlayShowLink(url)
	elif mode==8:
		print "Play url is "+url,mode
		ShowSettings(url)
	elif mode==24:
		print "Play url is "+url,mode
		LIVETvLogin(url)
	elif mode==9:
		print "Play url is "+url,mode
		AddStreams();
	elif mode==10 or mode==11:
		print "Play url is "+url,mode
		PlayStream(url,name,mode);
	elif mode==14: #add communutycats
		print "Play url is "+url,mode
		addCommunityCats();
	elif mode==15: #add communutycats
		print "Play url is "+url,mode
		addCommunityChannels(url);
	elif mode==16: #add communutycats
		print "PlayCommunityStream Play url is "+url,mode
		PlayCommunityStream(url,name,mode);	
	elif mode==17: #add communutycats
		print "RefreshResources Play url is "+url,mode
		RefreshResources();
	elif mode==18: #
		print "youtube url is "+url,mode
		AddYoutubeSources(url)
	elif mode==19: #
		print "youtube url is "+url,mode
		AddYoutubeLanding(url)
	elif mode==20: #add communutycats
		print "youtube url is "+url,mode
		AddYoutubeVideosByChannelID(url,addIconForPlaylist);	
	elif mode==21: #add communutycats
		print "play youtube url is "+url,mode
		PlayYoutube(url);	
	elif mode==22: #add communutycats
		print "play youtube url is "+url,mode
		AddYoutubePlaylists(url);	
	elif mode==23: #add communutycats
		print "play youtube url is "+url,mode
		AddYoutubeVideosByPlaylist(url);	

except:
	print 'somethingwrong'
	traceback.print_exc(file=sys.stdout)

try:
	if (not mode==None) and mode>1:
		view_mode_id = get_view_mode_id('thumbnail')
		if view_mode_id is not None:
			print 'view_mode_id',view_mode_id
			xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
except: pass
if not ( mode==5 or mode==10 or mode==8 or mode==11 or mode==16 or mode==17):
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

