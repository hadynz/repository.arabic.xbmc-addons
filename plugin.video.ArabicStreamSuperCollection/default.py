# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO,itertools
import urllib2,urllib
import re
import httplib
import time
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import cookielib
from random import randint

__settings__ = xbmcaddon.Addon(id='plugin.video.ArabicStreamSuperCollection')
__icon__ = __settings__.getAddonInfo('icon')
__fanart__ = __settings__.getAddonInfo('fanart')
__language__ = __settings__.getLocalizedString
_thisPlugin = int(sys.argv[1])
_pluginName = (sys.argv[0])

def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner
	
httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)

def mainDir():
	addDir('Teledunet Channels','http://www.teledunet.com/list_chaines.php',9,'http://www.itwebsystems.co.uk/resources/icon.png')
	addDir('Arabic Filmon Channels','http://www.filmon.com/group/arabic-tv',3,'http://static.filmon.com/couch/channels/689/extra_big_logo.png')
	addDir('Mashup Arabic Streams','https://raw.github.com/mash2k3/MashUpStreams/master/CrusadersDir.xml',5,'http://www.mirrorservice.org/sites/addons.superrepo.org/Frodo/.metadata/plugin.video.movie25.jpg')
	addDir('TvIraq.net','http://www.tviraq.net/',8,'http://4.bp.blogspot.com/-mAFM9C7G3x8/Urg65k7EBsI/AAAAAAAADBU/FJ1UVeYz-5s/s1600/al+jazeera+mubasher++tv+live+logo.png')
	#addDir('hdarabic.com (Free channels)','http://www.hdarabic.com/',11,'http://www.hdarabic.com/images/general.jpg')
	addDir('OtherSources',' ',13,'http://t1.ftcdn.net/jpg/00/29/62/30/400_F_29623050_hk7Oy2QPH8ZS6qa2vrYXz28O65G248ic.jpg')
	addDir('Livestation','http://www.livestation.com/',16,'http://www.livestation.com/assets/new_logo.png')
	
def otherSourcesCat():
	addDir('Entertainment','http://jinnahtv.com/apps_mng/service_files/arab_tv_entertainment_channels.php',14,'http://t1.ftcdn.net/jpg/00/29/62/30/400_F_29623050_hk7Oy2QPH8ZS6qa2vrYXz28O65G248ic.jpg')
	addDir('Relegious','http://jinnahtv.com/apps_mng/service_files/live_tv_religious_channels.php',14,'http://t1.ftcdn.net/jpg/00/29/62/30/400_F_29623050_hk7Oy2QPH8ZS6qa2vrYXz28O65G248ic.jpg')
	addDir('News','http://jinnahtv.com/apps_mng/service_files/live_tv_news_channels.php',14,'http://t1.ftcdn.net/jpg/00/29/62/30/400_F_29623050_hk7Oy2QPH8ZS6qa2vrYXz28O65G248ic.jpg')
	addDir('Sports','http://jinnahtv.com/apps_mng/service_files/live_tv_sports_channels.php',14,'http://t1.ftcdn.net/jpg/00/29/62/30/400_F_29623050_hk7Oy2QPH8ZS6qa2vrYXz28O65G248ic.jpg')
	addDir('Different channels','http://steinmann.webs.com/tvhd.xml',18,'http://t1.ftcdn.net/jpg/00/29/62/30/400_F_29623050_hk7Oy2QPH8ZS6qa2vrYXz28O65G248ic.jpg')
def GetOtherChannels(url):
    
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	chName=(re.compile(' <title>(.+?)</title>').findall(link))
	chName.pop(0)
	chPath=(re.compile('<otherUrl url="(.+?)" />').findall(link))
	for elements,items in itertools.izip(chName,chPath):
		myChannelName=str( elements).strip()
		myChannelPath=str( items).strip()
		addLink(myChannelName,myChannelPath,15,'')

def GetLiveStations(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    base='http://www.livestation.com'
    url_target=(re.compile('<a href="(.+?)" class="(.+?)" data-action="(.+?)data-label="(.+?)" itemprop="(.+?)src="(.+?)"').findall(link))
    for items in url_target:
        if'language_selector' not in str(items):
            path=base+str( items[0]).strip()
            name=str( items[3]).strip()
            img=str( items[5]).strip()
            addLink(name,path,17,img)
            
def playLiveStations(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	try:
		url_target=(re.compile('<video id="(.+?)"video/').findall(link))
		url_target=str( url_target).split('><source src="')[1]
		url_target=str( url_target).split('m3u8')[0]+'m3u8'
		listItem = xbmcgui.ListItem(path=str(url_target))
		xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
	except:
		pass


	
def PlayOtherChannels(url):
	listItem = xbmcgui.ListItem(path=str(url))
	xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)

def checkUrl(url):
    p = urlparse(url)
    conn = httplib.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400

def getCookies(url):

    #Create a CookieJar object to hold the cookies
    cj = cookielib.CookieJar()
    #Create an opener to open pages using the http protocol and to process cookies.
    opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
    #create a request object to be used to get the page.
    req = urllib2.Request(url)
    req.add_header('Host', 'www.teledunet.com')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Referer', 'http://www.teledunet.com/')
    req.add_header('Connection', 'keep-alive')
    f = opener.open(req)
    #see the first few lines of the page
    cj=str(cj).replace('<cookielib.CookieJar[<Cookie', '').replace('/>]>', '').replace('for www.tviraq.net', '')
    cj=str(cj).strip()
    return cj
	

def getFilmOnCreds(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	filmOnUrl=(re.compile('<iframe frameborder=(.+?)width=').findall(link))
	filmOnUrl=str(str( filmOnUrl).split('src="')[1]).replace("']", "").replace('"', '').strip()
	req = urllib2.Request(filmOnUrl)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	myUrl=(re.compile('var startupChannel =(.+?);').findall(link))
	myUrl=str( myUrl).split(',')
	idStream=''
	rtmp=''
	stream=''
	for itr in myUrl:
		
		if 'streams' in itr:
			print 'this is stream '+itr
			stream=str( itr).replace('"streams":[{"name":"', '').replace('"', '').replace("low","high").strip()
   
		if 'rtmp' in itr:
			itr2=str( itr).replace('itr','').replace('"}]', '').replace('"', "").replace("\\", "").replace("url:",'').strip()
			rtmp= itr2
			idStream=str(itr2).split('id=')[1]
        
	
	if len(stream)>1 and len (idStream)>1 and len(rtmp)>1 :
		finalUrl=rtmp+' playpath='+str(stream)+' app=live/?id='+str(idStream)+' swfUrl=http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'+' tcUrl='+str(rtmp)+' pageurl=http://www.filmon.com/ live=true'
		listItem = xbmcgui.ListItem(path=str(finalUrl))
		xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
	
def isFilmOnCreds(url):
    try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		filmOnUrl=(re.compile('<iframe frameborder=(.+?)width=').findall(link))
		print filmOnUrl
		
        
		if 'filmon' in str(filmOnUrl):
			filmOnUrl=str(str( filmOnUrl).split('src="')[1]).replace("']", "").replace('"', '').strip()
			return 'OK'
            
    except (urllib2.HTTPError):
        pass
        return 'Error'

def getCategories(url):
	
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	name=''
	path=''
	target= re.findall(r"<div class='widget-content list-label-widget-content'>(.*?)\s(.*?)<div class='clear'></div>", link, re.DOTALL)
	for items in target:
		myChannels=str( items[1]).split('>')
		for itr in myChannels:
			if "<a dir='rtl' href='" in itr:
				path= str(itr).split("href=")[1]
				path=str(path).replace("'","")
			if "</a" in itr:
				name=str( itr).replace("</a", "").strip()
				print name
				print path
				addDir(name,path,1,'')
				
def getCrusaderDir(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    
    response.close()
    target= re.findall(r'<name>(.*?)\s(.*?)<date>', link, re.DOTALL)
    for items in  target:
        names=str( items[0]).replace("</name>", "").strip()
        ImgPath=str( items[1])
        ImgPath=str( ImgPath).split('</link>')
        path=str( ImgPath[0]).replace('<link>', '').strip()
        image=str( ImgPath[1]).replace("</thumbnail>", "").replace("<thumbnail>", "").strip()
        addDir(names,path,6,image)
 

 
def getCrusaderChannels(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    target= re.findall(r'<item>(.*?)\s(.*?)</item>', link, re.DOTALL)
    for itr in target:
		mytarget=str( itr[1]).split('>')
		name=str( mytarget[1]).replace("</title", "").strip()
		path= str( mytarget[3]).replace("</link", "").strip()
		image= str( mytarget[5]).replace("</thumbnail", "").strip()
		addLink(name,path,7,image)
		
def playCrusadersChannel(url):
	listItem = xbmcgui.ListItem(path=str(url))
	xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
		
def indexIraqiChannels(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    thumbnail=''
    path=''
    name=''
    target= re.findall(r"<h3 class='post-title entry-title' itemprop='name'>(.*?)\s(.*?)<script type=", link, re.DOTALL)
    for ch in  target:
        myPath=str( ch[1]).split('>')
        for items in myPath:
           
            if '<a href=' in str(items):
                path=str(items).replace("<a href='", '').replace("'", "").replace('<a href="', "").replace('" target="_blank"', "").strip()
				
            if 'img border=' in str(items):
                thumbnail=str(items).split('src="')[1]
                thumbnail=str(thumbnail).split('" width="')[0]
                thumbnail=str(thumbnail).strip()
            if '</a' in str(items):
                name=str(items).replace('</a', '').strip()
            
        print name
        print path
        addLink(name,path,2,thumbnail)
        
def playIraqiChannels(url):
	if isFilmOnCreds(url)=='OK':
		getFilmOnCreds(url)
    
	else:
	
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		#print link
		swfPlayer=(re.compile('<object bgcolor="#000000" data="(.+?)" height=').findall(link))
		target= re.findall(r'aboutlink: "http://www.tviraq.net",(.*?)\s(.*?)logo:', link, re.DOTALL) 
		swfPlayer=str(swfPlayer).replace("['", "").replace("']", "").strip()
		mytarget=str( target[0]).split(',') 
		path=str( mytarget[1] ).replace("' file: ", '').replace('"', "").strip()   
		#image=str( mytarget[2] ).split("image: ")[1]
		#image=str(image).replace('"', "").strip()
		rtmpUrl=path
		base=str(rtmpUrl).split("/")
		playPath= base.pop()
		playPath=str( playPath).strip()
		app=base.pop()
		if "www.youtube" in str(path):
			video=path.split("v=")
			#print "youtube after split: "+str(video)
			video_id=str(video[1])
			video_id=video_id.replace(".flv","").strip()
			print "first item of youtube: "+str(video_id)
			playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id
			listItem = xbmcgui.ListItem(path=str(playback_url))
			xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
		if 'm3u8' in str(path):
			playback_url = path
			listItem = xbmcgui.ListItem(path=str(playback_url))
			xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
		
		
		else:
			
			playback_url=str(path)+" playpath="+str(playPath)+" swfUrl="+str(swfPlayer)+" flashVer=WIN119900170"+" live=true swfVfy=true timeout=10"
			listItem = xbmcgui.ListItem(path=str(playback_url))
			xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
			
def getFilmonChannels(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    channelId=(re.compile('<li class="(.+?)channel_id="(.+?)">').findall(link))
    channelNameImage=(re.compile('<img class="channel_logo" src="(.+?)" title="(.+?)" style=').findall(link))
    for (items,itr) in itertools.izip  (channelId,channelNameImage):
        channelid='http://www.filmon.com/tv/channel/export?channel_id='+str( items[1]).strip()
        nameImage= itr
        image=str(nameImage).split(',')[0]
        name=str(nameImage).split(',')[1]
        name=str(name).replace("'", '').replace(")", "").strip()
        image=str(image).replace("('", '').replace("'", "").strip()
        addLink(name,channelid,4,image)
			
def playFilmOnChannel(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	myUrl=(re.compile('var startupChannel =(.+?);').findall(link))
	myUrl=str( myUrl).split(',')
	idStream=''
	rtmp=''
	stream=''
	for itr in myUrl:
		if 'streams' in itr:
			stream=str( itr).replace('"streams":[{"name":"', '').replace('"', '').replace("low","high").strip()
		if 'rtmp' in itr:
			itr2=str( itr).replace('itr','').replace('"}]', '').replace('"', "").replace("\\", "").replace("url:",'').strip()
			rtmp= itr2
			idStream=str(itr2).split('id=')[1]

	finalUrl=rtmp+' playpath='+str(stream)+' app=live/?id='+str(idStream)+' swfUrl=http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'+' tcUrl='+str(rtmp)+' pageurl=http://www.filmon.com/ live=true timeout=15'
	listItem = xbmcgui.ListItem(path=str(finalUrl))
	xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)

def getFilmOnCreds2(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    filmOnUrl=(re.compile('<iframe frameborder=(.+?)width=').findall(link))
    if len(filmOnUrl)>1:
        
        filmOnUrl=str(str( filmOnUrl).split('src="')[1]).replace("']", "").replace('"', '').strip()
        
        req = urllib2.Request(filmOnUrl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        myUrl=(re.compile('var startupChannel =(.+?);').findall(link))
        myUrl=str( myUrl).split(',')
        idStream=''
        rtmp=''
        stream=''
        for itr in myUrl:
            if 'streams' in itr:
                stream=str( itr).replace('"streams":[{"name":"', '').replace('"', '').replace("low","high").strip()
                
            if 'rtmp' in itr:
                itr2=str( itr).replace('itr','').replace('"}]', '').replace('"', "").replace("\\", "").replace("url:",'').strip()
                rtmp= itr2
                idStream=str(itr2).split('id=')[1]
               
            
       
        finalUrl=rtmp+' playpath='+str(stream)+' app=live/?id='+str(idStream)+' swfUrl=http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'+' tcUrl='+str(rtmp)+' pageurl=http://www.filmon.com/ live=true'
        listItem = xbmcgui.ListItem(path=str(finalUrl))
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    else:
        
        myUrl=(re.compile('var startupChannel =(.+?);').findall(link))
        myUrl=str( myUrl).split(',')
        idStream=''
        rtmp=''
        stream=''
        for itr in myUrl:
            if 'streams' in itr:
                stream=str( itr).replace('"streams":[{"name":"', '').replace('"', '').replace("low","high").strip()
            
            
            if 'live' in itr:
                itr2=str( itr).replace('itr','').replace('"}]', '').replace('"', "").replace("\\", "").replace("url:",'').strip()
                rtmp= itr2
                idStream=str(itr2).split('id=')[1]
                
        finalUrl=rtmp+' playpath='+str(stream)+' app=live/?id='+str(idStream)+' swfUrl=http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'+' tcUrl='+str(rtmp)+' pageurl=http://www.filmon.com/ live=true'
        listItem = xbmcgui.ListItem(path=str(finalUrl))
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
		
	 ###########################TELEDUNET CODE ##########################################
def index_Teledunet(url):
	url="http://www.teledunet.com/list_chaines.php"
	req = urllib2.Request(url)
	req.add_header('Host', 'www.teledunet.com')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	req.add_header('Accept-Language', 'sv-SE,sv;q=0.8,en-US;q=0.5,en;q=0.3')
	req.add_header('Accept-Encoding', 'gzip, deflate')
	req.add_header('Connection', ' keep-alive')
	
	response = urllib2.urlopen(req,timeout=15)
	link=response.read()
	response.close()
	style=(re.compile('<div  id="(.+?)class=div_channel>').findall(link))
	image=(re.compile('<img onerror="(.+?)src="(.+?)" height=').findall(link))
	nameUrl=(re.compile('onclick="set_favoris(.+?);" style=').findall(link))
	imgArray=[]
	colorArray=[]
	nameArray=[]
	pathArray=[]
	global globalIp
	
	addLink('MBC','rtmp://www.teledunet.com:1935/teledunet/mbc_1',10,'https://si0.twimg.com/profile_images/1133033554/mbc-fb.JPG')
	addLink('MBC DRAMA','rtmp://www.teledunet.com:1935/teledunet/mbc_drama',10,'http://www.allied-media.com/ARABTV/images/mbc_drama.jpg')
	#addLink('beIn Sports 1','rtmp://www.teledunet.com:1935/teledunet/jsc_1',10,'')
	#addLink('beIn Sports 2','rtmp://www.teledunet.com:1935/teledunet/jsc_2',10,'')
	#addLink('beIn Sports 3','rtmp://www.teledunet.com:1935/teledunet/jsc_3',10,'')
	#addLink('beIn Sports 4','rtmp://www.teledunet.com:1935/teledunet/jsc_4',10,'')
	#addLink('beIn Sports 5','rtmp://www.teledunet.com:1935/teledunet/jsc_5',10,'')
	#addLink('beIn Sports 6','rtmp://www.teledunet.com:1935/teledunet/jsc_6',10,'')
	#addLink('beIn Sports 7','rtmp://www.teledunet.com:1935/teledunet/jsc_7',10,'')
	#addLink('beIn Sports 8','rtmp://www.teledunet.com:1935/teledunet/jsc_8',10,'')
	#addLink('beIn Sports 11','rtmp://www.teledunet.com:1935/teledunet/jsc_9',10,'')
	#addLink('beIn Sports 12','rtmp://www.teledunet.com:1935/teledunet/jsc_10',10,'')
	#addLink('JSC 1 HD','rtmp://www.teledunet.com:1935/teledunet/tele_1_hd',10,'')
	#addLink('JSC 2 HD','rtmp://www.teledunet.com:1935/teledunet/tele_2_hd',10,'')
	addLink('Abu Dhabi Al Oula','rtmp://www.teledunet.com:1935/teledunet/abu_dhabi',10,'https://www.zawya.com/pr/images/2009/ADTV_One_RGB_2009_10_08.jpg')
	addLink('Abu Dhabi Sports','rtmp://www.teledunet.com:1935/teledunet/abu_dhabi_sports_1',10,'https://si0.twimg.com/profile_images/2485587448/2121.png')
	addLink('Al Jazeera','rtmp://www.teledunet.com:1935/teledunet/aljazeera',10,'http://www.chicagonow.com/chicago-sports-media-watch/files/2013/04/Al-Jazeera.jpg')
	addLink('Al Jazeera Mubasher Masr','rtmp://www.teledunet.com:1935/teledunet/aljazeera_mubasher_masr',10,'http://www.chicagonow.com/chicago-sports-media-watch/files/2013/04/Al-Jazeera.jpg')
	addLink('Al Jazeera Children','rtmp://www.teledunet.com:1935/teledunet/aljazeera_children',10,'http://3.bp.blogspot.com/-UX1XBY8-02g/Uoku7OTIrFI/AAAAAAAAASk/-0eEX7fumJw/s1600/al_jazeera_children.png')
	addLink('Al Jazeera Documentation','rtmp://www.teledunet.com:1935/teledunet/aljazeera_doc',10,'http://upload.wikimedia.org/wikipedia/en/e/e6/Al_Jazeera_Doc.png')
	addLink('ART Cinema','rtmp://www.teledunet.com:1935/teledunet/art_aflam_1',10,'http://www.lyngsat-logo.com/hires/aa/art_cinema.png')
	addLink('ART Aflam 2','rtmp://www.teledunet.com:1935/teledunet/art_aflam_2',10,'http://www.invision.com.sa/en/sites/default/files/imagecache/216x216/channels/2011/10/11/1138.jpg')
	addLink('Cartoon Network','rtmp://www.teledunet.com:1935/teledunet/cartoon_network',10,'http://upload.wikimedia.org/wikipedia/commons/b/bb/Cartoon_Network_Arabic_logo.png')
	addLink('MTV Lebanon','rtmp://www.teledunet.com:1935/teledunet/mtv',10,'http://mtv.com.lb/images/mtv-social-logo1.jpg')
	addLink('AlJadeed','rtmp://www.teledunet.com:1935/teledunet/aljaded_sat',10,'')
	addLink('NBN','rtmp://www.teledunet.com:1935/teledunet/nbn',10,'http://upload.wikimedia.org/wikipedia/en/1/14/Nbn_lebanon.png')
	addLink('Otv Lebanon','rtmp://www.teledunet.com:1935/teledunet/otv_lebanon',10,'http://www.worldmedia.com.au/Portals/0/Images/Logo_s/otv.png')
	addLink('Al Hayat','rtmp://www.teledunet.com:1935/teledunet/alhayat_1',10,'http://3.bp.blogspot.com/--uP1DsoBB7s/T4EMosYH5uI/AAAAAAAAF9E/RdbY8-E3Riw/s320/Al%2Bhayat.jpg')
	addLink('Al Hayat Cinema','rtmp://www.teledunet.com:1935/teledunet/alhayat_cinema',10,'http://www.lyngsat-logo.com/hires/aa/alhayat_cinema.png')
	addLink('Alarabiya','rtmp://www.teledunet.com:1935/teledunet/alarabiya',10,'http://www.debbieschlussel.com/archives/alarabiya2.jpg')
	addLink('Tele Sports','rtmp://www.teledunet.com:1935/teledunet/tele_sports',10,'http://www.itwebsystems.co.uk/resources/icon.png')
	addLink('Noursat','rtmp://www.teledunet.com:1935/teledunet/noursat',10,'')
	addLink('TF1','rtmp://www.teledunet.com:1935/teledunet/tf1',10,'')
	addLink('Al Masriyah','rtmp://www.teledunet.com:1935/teledunet/al_masriyah',10,'')
	addLink('Iqra','rtmp://www.teledunet.com:1935/teledunet/Iqra',10,'')
	addLink('Canal Plus','rtmp://www.teledunet.com:1935/teledunet/canal_plus',10,'')
	addLink('Melody TV','rtmp://www.teledunet.com:1935/teledunet/melody',10,'')
	addLink('Alrahma','rtmp://www.teledunet.com:1935/teledunet/alrahma',10,'')
	addLink('Assadissa','rtmp://www.teledunet.com:1935/teledunet/assadissa',10,'')
	addLink('Dzair 24','rtmp://www.teledunet.com:1935/teledunet/dzair_24',10,'')
	addLink('Dzair TV','rtmp://www.teledunet.com:1935/teledunet/dzair_tv',10,'')
	addLink('M6','rtmp://www.teledunet.com:1935/teledunet/m6',10,'')
	addLink('Noursat','rtmp://www.teledunet.com:1935/teledunet/noursat',10,'')
	addLink('ORTB TV','rtmp://www.teledunet.com:1935/teledunet/ortb_tv',10,'')
	addLink('Roya','rtmp://www.teledunet.com:1935/teledunet/roya',10,'')
	addLink('TNN','rtmp://www.teledunet.com:1935/teledunet/tnn',10,'')
	addLink('W9','rtmp://www.teledunet.com:1935/teledunet/w9',10,'')
    
	for itemNameUrl in nameUrl:
		myItems=str(itemNameUrl).split(',')
		name=str(myItems[1]).replace("'",'').strip()
		path=str(myItems[2]).replace("'",'').replace(")",'').strip()
		if not 'www' in path:
			globalIp=str( path).split('teledunet')[0]
			globalIp=str(globalIp).replace("1935/","1935")
			#print globalIp
		#path=str(path).replace("rtmp://www.teledunet.com:1935/",str(globalIp))
		nameArray.append(name) 
		pathArray.append(path) 
    
	for itemsImg in  image:
		myImage="http://www.teledunet.com/"+str( itemsImg[1] )
		imgArray.append(myImage) 
	
	for (names,images,paths) in itertools.izip (nameArray,imgArray,pathArray):
		
		addLink(names,paths,10,images)

def getCookies(url):

    #Create a CookieJar object to hold the cookies
	cj = cookielib.CookieJar()
	print "this is oookie " + str(url)
    #Create an opener to open pages using the http protocol and to process cookies.
	opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
	#create a request object to be used to get the page.
	req = urllib2.Request(url)
	req.add_header('Host', 'www.teledunet.com')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	req.add_header('Accept-Encoding', 'gzip, deflate')
	req.add_header('Referer', 'http://www.teledunet.com/')
	req.add_header('Connection', 'keep-alive')
	f = opener.open(req)
    #see the first few lines of the page
	cj=str(cj).replace('<cookielib.CookieJar[<Cookie', '').replace('/>]>', '').replace('for www.teledunet.com', '')
	cj=str(cj).strip()
	return cj


def getId(channel):
    url="http://www.teledunet.com/player/?channel="+channel+"&no_pub"
    req = urllib2.Request(url)
    req.add_header('Host', 'www.teledunet.com')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Language', 'sv-SE,sv;q=0.8,en-US;q=0.5,en;q=0.3')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Referer', "http://www.teledunet.com/?channel="+channel)
    req.add_header('Connection', ' keep-alive')
    response = urllib2.urlopen(req,timeout=5)
    link=response.read()
    response.close()
    nameUrl=(re.compile("time_player=(.+?);").findall(link))
    nameUrl = str(nameUrl).replace('"]',"").strip()
    nameUrl=str( nameUrl).replace("['", '').replace("']", '').replace(".","").replace("E+13","00").strip()
    return nameUrl
	

def GetHDSITEChannels(url):
	req = urllib2.Request('http://steinmann.webs.com/tvhd.xml')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
   
	response.close()
	target= re.findall(r'<items>(.*?)\s(.*?)</items>', link, re.DOTALL)
	target=str( target).split('<item')
	name=''
	img=''
	path=''

	for itr in target:
		if ('TV="') in itr:
			mypath=str( itr).replace('title="', ' DELIM ').replace('coverImage="', ' DELIM ').replace('TV="', ' DELIM ').replace('picture="', ' DELIM ')
			mypath=str(mypath).split(' DELIM ')
			for items in mypath:
				newpath=str( items).split('\r\n')
				for itr in newpath:
					if ('http' in str( itr)) or '"' in itr:
						finalPath=itr.replace('"',"").strip()
						if 'http://www.cookiesjar.net/letsapp/listen/quran/free.jpg' not in itr:
							if 'http' in str(finalPath):
								if "png" in str(finalPath) or "gif" in str(finalPath) or "jpg" in str(finalPath):
									img=finalPath
								else:
									path=finalPath
							else:
								name=finalPath
								name= name[:-4]
								img= img[:-4]
								path= path[:-4]
								addLink('',path,15,img)
	
def getChanelRtmp(channel):
    url="http://www.teledunet.com/player/?channel="+channel
    req = urllib2.Request(url)
    req.add_header('Host', 'www.teledunet.com')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Language', 'sv-SE,sv;q=0.8,en-US;q=0.5,en;q=0.3')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Referer', "http://www.teledunet.com/?channel="+channel)
    req.add_header('Connection', ' keep-alive')
    response = urllib2.urlopen(req,timeout=5)
    link=response.read()
    
    response.close()
    nameUrl=(re.compile("curent_media='(.+?)';").findall(link))
    return nameUrl[0]
	
                    
def PlayTeledunet(url):
	firstPart=str(url).split('teledunet/')[1]
	streamer = getChanelRtmp(firstPart)
	finalPayPath=streamer+' app=teledunet swfUrl=http://www.teledunet.com/player/player/player_2.swf?bufferlength=5&repeat=single&autostart=true&id0='+str(getId(firstPart))+'&streamer='+streamer+'&file='+str(firstPart)+'&provider=rtmp playpath='+str(firstPart)+' live=1 pageUrl=http://www.teledunet.com/tv/?channel='+str(firstPart)+'&no_pub'
	listItem = xbmcgui.ListItem(path=str(finalPayPath))
	xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
	

############################################ hdarabic.com################################################################

def getCookiesARC(url):

    #Create a CookieJar object to hold the cookies
    cj = cookielib.CookieJar()
    #Create an opener to open pages using the http protocol and to process cookies.
    opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
    #create a request object to be used to get the page.
    req = Request(url)
    req.add_header('Host', 'www.hdarabic.com')
    req.add_header('Cache-Control', 'max-age=0')
    req.add_header('Accept', ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36')
    req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
    req.add_header('Referer', 'http://www.hdarabic.com/')
    req.add_header('Accept-Language', 'sv,en-US;q=0.8,en;q=0.6,en-GB;q=0.4')
    f = opener.open(req)
    #see the first few lines of the page
    cj=str(cj).replace('<cookielib.CookieJar[<Cookie', '').replace('/>]>', '')
    cj=str(cj).strip()
    return cj

def indexArChannels(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	link=response.read()
    
	req = urllib2.Request(url)
	req.add_header('Host', 'hdarabic.com')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	#req.add_header('Referer', ' http://arabichannels.com/')
	req.add_header('Accept-Language', 'sv,en-US;q=0.8,en;q=0.6,en-GB;q=0.4')
	req.add_header('Accept-Encoding', 'identity')
	req.add_header('Connection', 'close')
	target= re.findall(r'<ul id="menu">(.*?)\s(.*?)<ul></div> ', link, re.DOTALL)
    
	for items in target:
		myBaseUrl= items[1]
		myBaseUrl=str(myBaseUrl).split('"/></a></div>')
		for itr in myBaseUrl:
			try:
				theTarget=str( itr).split("src='")[1]
				theTarget=str(theTarget).replace(';"><span class="nume">', 'DELIM').replace('" alt="','DELIM')
				theTarget=str(theTarget).split('DELIM')
				path='http://www.hdarabic.com/'+str( theTarget[0]).replace("'", "").strip()
				nameImage= str(theTarget[1]).split('</span><img src="')
				name=str( nameImage[0]).strip()
				image=str(nameImage[1]).replace("./", "/").strip()
                
				if 'http' in str( image):
					image=image
				else:
					image="http://www.hdarabic.com"+image
                
				if 'iptv' not in str(path):
					addLink(name,path,12,image)
			except:
				pass
   
					
	
            
					
					
def playARCChannel(url):

	if ".php" in str(url):

		req = urllib2.Request(url)
		req.add_header('Host', 'www.hdarabic.com')
		req.add_header('Cache-Control', 'max-age=0')
		req.add_header('Accept', ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
		req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36')
		req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
		req.add_header('Referer', 'http://www.hdarabic.com/')
		req.add_header('Accept-Language', 'sv,en-US;q=0.8,en;q=0.6,en-GB;q=0.4')
		req.add_header('Cookie', '  tzLogin='+str(getCookies('http://www.hdarabic.com/')))
		response = urllib2.urlopen(req)
		link=response.read()
		streamer=(re.compile("'streamer':(.+?)',").findall(link))
		swf=(re.compile("{type: 'flash', src: '(.+?)'},").findall(link))
		swf=str(swf).replace("['", "").replace("']", "").strip()
		streamer=str(streamer).replace('[', "").replace('"]', "").strip()
		streamer=str(streamer).replace("'", "").replace('"', "").strip().replace("]/", "").strip()
		fileLoc=(re.compile("'file':(.+?)',").findall(link))
		fileLoc=str(fileLoc[0]).replace("'", "").strip()
		fileLoc=str(fileLoc).replace("'", "").replace('"', "").strip()
		mynr1=randint(10,20)
		mynr2=randint(0,10)
		mynr3=randint(100,900)
		mynr=randint(10000,500000)
		
		#complete=streamer + ' swfUrl=http://hdarabic.com' + swf + ' playpath=' + fileLoc +  ' flashVer='+str(mynr1)+'.'+str(mynr2)+'.'+str(mynr3)+' live=1 swfVfy=true pageUrl='+str(url)
		complete=streamer +'/'+fileLoc+ ' swfUrl=http://www.hdarabic.com' + swf + ' playpath=' + fileLoc +  ' flashVer='+str(mynr1)+'.'+str(mynr2)+'.'+str(mynr3)+' live=1 swfVfy=true pageUrl='+str(url)
		listItem = xbmcgui.ListItem(path=str(complete))
		xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
		time.sleep(6)
		if xbmc.Player().isPlayingVideo()==False:
			complete=streamer + ' swfUrl=http://www.hdarabic.com' + swf + ' playpath=' + fileLoc +  ' flashVer='+str(mynr1)+'.'+str(mynr2)+'.'+str(mynr3)+' live=1 swfVfy=true pageUrl='+str(url)
			listItem = xbmcgui.ListItem(path=str(complete))
			xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
		
		
		
		
		
	elif ".html" in str(url):
        
			myfinalpath=' '
			req = urllib2.Request(url)
			req.add_header('Host', 'www.hdarabic.com')
			req.add_header('Cache-Control', 'max-age=0')
			req.add_header('Accept', ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
			req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36')
			req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
			req.add_header('Referer', 'http://www.hdarabic.com/')
			req.add_header('Accept-Language', 'sv,en-US;q=0.8,en;q=0.6,en-GB;q=0.4')
			req.add_header('Cookie', '  tzLogin='+str(getCookies('http://www.hdarabic.com/')))
			#req.add_header('Cookie', '  tzLogin=t5r8fm4vpck03ap6feeakj3of4; __qca=P0-831467814-1383850814929; HstCfa2398318=1383850815237; HstCmu2398318=1383850815237; HstCla2398318=1384292777596; HstPn2398318=1; HstPt2398318=6; HstCnv2398318=3; HstCns2398318=5; MLR72398318=1384292780000; __zlcmid=LodILVkuY96YpR; _pk_id.1.c9f1=ab7e13fd2cf6be07.1383850815.4.1384292879.1384285142.')
			response = urllib2.urlopen(req)
			link=response.read()
			mypath=(re.compile("file: '(.+?)',").findall(link))
			for item in  mypath:
				if "smil" in str(item):
					mydest="http://www.hdarabic.com/"+str( item).strip()
					req2 = urllib2.Request(mydest)
					req2.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
					response2 = urllib2.urlopen(req2)
					link2=response2.read()
					videosource=(re.compile('<video src="(.+?)" system-bitrate="400000"').findall(link2))
					myfinalpath=(re.compile(' <meta base="(.+?)"/>').findall(link2))
					myfinalpath=str(myfinalpath).replace("['", "").replace("']", "").strip()
					videosource=str(videosource).replace("['", "").replace("']", "").replace("'","").strip()
					myfinalpath=myfinalpath + ' playpath=' + videosource + ' swfUrl=http://www.hdarabic.com/player4/jwplayer.flash.swf live=1 buffer=300000 timeout=15 swfVfy=1 pageUrl=http://www.hdarabic.com'
					listItem = xbmcgui.ListItem(path=str(myfinalpath))
					xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
	
			

def retrieveChannel(url):
	if "youtube" in str(url):
		finalurl=str(url).split("v=")
		finalurl=finalurl[1]
		playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % finalurl
	elif "youtube" not in str(url):
		playback_url=url
	return playback_url


		
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
        mainDir()
       
elif mode==1:
        print ""+url
        indexIraqiChannels(url)
	
elif mode==2:
        playIraqiChannels(url)
elif mode==3:
        getFilmonChannels(url)
elif mode==4:
        getFilmOnCreds2(url)
elif mode==5:
        getCrusaderDir(url)
elif mode==6:
        getCrusaderChannels(url)
elif mode==7:
        playCrusadersChannel(url)		
elif mode==8:
        getCategories(url)	
elif mode==9:
        index_Teledunet(url)
elif mode==10:
        PlayTeledunet(url)
elif mode==11:
        indexArChannels(url)
elif mode==12:
        playARCChannel(url)
elif mode==13:
        otherSourcesCat()
elif mode==14:
        GetOtherChannels(url)
elif mode==15:
        PlayOtherChannels(url)
elif mode==16:
        GetLiveStations(url)
elif mode==17:
        playLiveStations(url)
elif mode==18:
	GetHDSITEChannels(url)
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))
