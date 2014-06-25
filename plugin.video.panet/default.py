# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import urllib2,urllib
import re
import httplib
import time

__settings__ = xbmcaddon.Addon(id='plugin.video.panet')
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


def CATEGORIES():
	#xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('WARNING','This addon is completely FREE DO NOT buy any products from http://tvtoyz.com/', 16000, 'http://pschools.haifanet.org.il/abd.relchaj/2010/panet.jpg'))
	addDir('مسلسلات رمضان','http://www.panet.co.il/Ext/series.php?name=category&id=34&country=TN&page=',29,'',0,0)
	addDir('مسلسلات سورية ولبنانية','http://www.panet.co.il/Ext/series.php?name=category&id=18&country=LB&page=',29,'',0,0)
	addDir('مسلسلات مصرية','http://www.panet.co.il/Ext/series.php?name=category&id=19&country=NL&page=',29,'',0,0)
	addDir('مسلسلات خليجية','http://www.panet.co.il/Ext/series.php?name=category&id=21&country=NL&page=',29,'',0,0)
	addDir('افلام عربية ','http://www.panet.co.il/online/video/movies/P-0.html/',1,'',0,30)
	addDir('افلام متحركة  ','http://www.panet.co.il/Ext/series.php?name=folder&id=257',29,'',0,0)
	addDir('مسلسلات تركية','http://www.panet.co.il/Ext/series.php?name=category&id=17&country=TR&page=',29,'',0,0)
	addDir('مسلسلات مكسيكية و عالمية','http://www.panet.co.il/Ext/series.php?name=category&id=20&country=NL&page=',29,'',0,0)
	addDir('رسوم متحركة , برامج اطفال','http://www.panet.co.il/Ext/series.php?name=category&id=15&country=NL&page=',29,'',0,0)
	addDir('برامج ومنوعات','http://www.panet.co.il/Ext/series.php?name=category&id=27&country=NL&page=',29,'',0,0)
	
		

	
def checkURL(url):
    p = urlparse(url)
    h = HTTP(p[1])
    h.putrequest('HEAD', p[2])
    h.endheaders()
    if h.getreply()[0] == 200: return 1
    else: return 0
	
def PanetListSeries(url):
    siteMax=15
    Serie=0
    mynamearray=[]
    myimagesarray=[]
    myurlarray=[]
    
    
    while Serie!=siteMax:
		
		kurl=str(url)+str(Serie)
		req = urllib2.Request(kurl)
		req.add_header('Host', 'www.panet.co.il')
		req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36')
		req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
		req.add_header('Accept-Language', 'sv-SE,sv;q=0.8,en-US;q=0.6,en;q=0.4')
		response = urllib2.urlopen(req)
		link=response.read()
		Serie=Serie+1
		buf = StringIO.StringIO(link)
		buf2 = StringIO.StringIO(link)
        
		for names in link.split():
			line=buf.readline()
			if ('><font face="Tahoma" size="2" color="Black"><b>') in line:
				name=str((str(line).split('"Black"><b>'))[1]).replace('</b><br/>', '').strip()
				mynamearray.append(name)
		for imagesandurls in link.split():
			line=buf2.readline()
			if '<a href="/Ext/series.php?name=folder&id=' and '"><img border="0" src="' and '" width="150" height="83"></a><br>' in line:
				both=str( line).split('"><img border="0" src="')
				myurl=str(both[0]).replace('<a href="', '').strip()
				myurl='http://www.panet.co.il'+myurl
				myurl=str(myurl).split('&country=')
				myurl=str(myurl[0]).strip()
				myurlarray.append(myurl)
				myimage=str(both[1]).replace('" width="150" height="83"></a><br>', '').strip()
				myimagesarray.append(myimage)
    for i in range(0,400):
        try:
            
            addDir(mynamearray[i],myurlarray[i],30,myimagesarray[i],0,0)
        except:
            pass
         
def getPanetEpos(url): 
    
    for i in range(0,5):   
        req = urllib2.Request(url+"&autostart=105194&page="+str(i))
        response = urllib2.urlopen(req)
        link=response.read()
        target= re.findall(r'<div class="series-table-item">(.*?)\s(.*?)</font>', link, re.DOTALL)
        counter =0
        for items in target:
            counter = counter +1
        for itr in  target:
			path = str( itr).split('"><img')[0]
			path = str(path).split('href="')[1]
			path = str(path).replace('&autostart=105194&page=0', '')
			path=str(path).strip()
			path =str(path).split('autostart=')[1]
			path =str(path).split('&page=0')[0]
			img = str( itr).split('" width="')[0]
			img = str( img).split('src="')[1]
			img =str(img).strip()
			name = "الحلقة" +" "+ str(counter)
			counter = counter -1
			addLink(name,path,31,img)

	
def GET_VIDEO_FILE(name, url):
	url="http://www.panet.co.il/Ext/vplayer_lib.php?media="+str(url)+'&start=false'
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	req.add_header('Accept',' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	req.add_header('Accept-Language',' en-US,en;q=0.5')
	req.add_header('Accept-Encoding', 'deflate')
	req.add_header('Referer',' http://www.panet.co.il/Ext/players/flv5/player.swf')
	req.add_header('Cookie',' __auc=82d7ffe213cb1b4ce1d273c7ba1; __utma=31848767.848342890.1360191082.1360611183.1360620657.4; __utmz=31848767.1360191082.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=31848767.4.10.1360620660; __utmc=31848767; __asc=169c084d13ccb4fa36df421055e')
	req.add_header('Connection',' keep-alive')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match_url_thumb=(re.compile('<link rel="video_src" href="(.+?)"/>').findall(link))
	match_url_thumb=str(match_url_thumb).replace("['", "")
	match_url_thumb=str(match_url_thumb).replace("']", "").strip()
	match_url_thumb=match_url_thumb.replace('%3A',':')
	match_url_thumb=match_url_thumb.replace('%2F','/')
	match_url_thumb=match_url_thumb.replace('http://','')
	match_url_thumb=match_url_thumb.replace('file=','file=http://')
	match_url_thumb=match_url_thumb.replace("www.panet.co.il/Ext/players/flv/playern.swf?type=http&streamer=start&file=","")
	match_url_thumb=str(match_url_thumb).replace('%3F','?').replace('%26','&').replace('%3D','=')
	listItem = xbmcgui.ListItem(path=str(match_url_thumb))
	xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
	


def retrievePanetMovies(MINIMUM,MAXIMUM):
	try:

		for iterator in range(MINIMUM,MAXIMUM+1):
			url=str('http://www.panet.co.il/online/video/movies/P-'+str(iterator)+'.html')
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			link=response.read()
			mytarget = (re.compile('<div style="float:right; margin-left:4px;"><a href="(.+?)" border=').findall(link))
			for items in  mytarget:
				filmPath = str(items).split('"><img src=')[0]
				filmPath ="http://pms.panet.co.il"+str(filmPath).strip()
				image = str(items).split('img src="')[1]
				image = str(image).split('" height=')[0]
				image =str(image).strip()
				name = str(items).split('alt="')[1]
				name = str(name).strip()
				addLink(name,filmPath,2,image)
		
	except:
		pass
	
	MINIMUM = MINIMUM+30
	MAXIMUM = MAXIMUM+30
	addDir('View more movies -->',url,1,'',MINIMUM,MAXIMUM)				
		
def VIDEOLINKS(url,name):
	
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match2=re.compile('"video_src" href="(.+?)"/>').findall(link)
	refer = re.compile('<iframe src="(.+?)" width=').findall(link)
	
	if len(match2) :
		filmPath = str(match2).split('type=')[1]
		filmPath = str(filmPath).split('&image')[0]
		filmPath = str(filmPath).strip()
		videoPath= filmPath.replace('%3A',':')
		videoPath=videoPath.replace('%2F','/')
		print videoPath
		videoPath =str(videoPath) .split('file=')[1]
		videoPath = str(videoPath).split("il")[1]
		videoPath = 'http://vod-movies.panet.co.il'+str(videoPath).strip()
		listItem = xbmcgui.ListItem(path=str(videoPath)+"|Referer=http://www.panet.co.il/Ext/players/flv/playern.swf")
		xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
			

                
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


def addDir(name,url,mode,iconimage,MINIMUM,MAXIMUM):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&MINIMUM="+str(MINIMUM)+"&MAXIMUM="+str(MAXIMUM)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

              
params=get_params()
url=None
name=None
mode=None
MINIMUM = None
MAXIMUM = None


	
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
        MINIMUM=int(params["MINIMUM"])
except:
        pass
try:
        MAXIMUM=int(params["MAXIMUM"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        retrievePanetMovies(MINIMUM,MAXIMUM)
	
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name) 

if mode==29:
	PanetListSeries(url)
elif mode==30:
	getPanetEpos(url)
elif mode==31:
	GET_VIDEO_FILE(name,url)
	
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
