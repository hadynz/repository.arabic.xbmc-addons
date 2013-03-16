# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import urllib2,urllib
import re


__settings__ = xbmcaddon.Addon(id='plugin.video.panet')
__icon__ = __settings__.getAddonInfo('icon')
__fanart__ = __settings__.getAddonInfo('fanart')
__language__ = __settings__.getLocalizedString


def CATEGORIES():
	addDir('Arab films','http://www.panet.co.il/online/video/movies/P-0.html/',1,'http://images2.layoutsparks.com/1/188565/passion-photo-graph-film.jpg')
	
	#addDir( 'Turkish drama','http://www.panet.co.il/Ext/series.php?name=category&id=17&country=TR&page=',29,'')
	#addDir( 'Egyptian drama','',1,'')
	#addDir( 'Syrian drama','',1,'')
	#addDir( 'Lebanese drama','',1,'')
	#addDir( 'Golf drama','',1,'')
		
def checkURL(url):
    p = urlparse(url)
    h = HTTP(p[1])
    h.putrequest('HEAD', p[2])
    h.endheaders()
    if h.getreply()[0] == 200: return 1
    else: return 0

def INDEX_TURKISH(url):
    siteMax=10
    Serie=0
    
    while Serie!=siteMax:
    
        #filmo=str(film)
        url='http://www.panet.co.il/Ext/series.php?name=category&id=17&country=TR&page='+str(Serie)
        Serie=Serie+1
        if checkURL(url):
                    req = urllib2.Request(url)
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                    response = urllib2.urlopen(req)
                    link=response.read()
                   
                    response.close()
                    
                    serierList=[]
                   
                    match_url_thumb=(re.compile('a href="(.+?)"><font face="Tahoma" size="2" color="Black"><b>(.+?)</b><br/>').findall(link))
                    
                    for i in match_url_thumb:
                        
                        url=match_url_thumb.pop(0)
                        #print url
                        for url_thumb in url :
                            url_path=url[0].replace("'",'')
                            serieName=url[1].replace("'",'')
                            #thumb_path=url[1].replace('"','')
                            #url_path='http://www.panet.co.i'+url_path
                             
                            if not url_path in serierList:
                                serierList.append(serieName)
                                serierList.append(url_path)
                    for item in serierList:
                        serieName=serierList.pop(0)
                        serieUrl=serierList.pop(0)
                        print serieName
                        serieUrl="http://www.panet.co.il"+serieUrl
                        print serieUrl
                        addDir(serieName,serieUrl,30,'')
def LIST_SERIES(url):
    #url='http://www.panet.co.il/Ext/series.php?name=folder&id=163'
    #&country=TR&page=
	
    for counter in range(0,10):
        url=url+"&country=TR&page="+str(counter)
        if checkURL(url):
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            serierList=[]
            match_url_thumb=(re.compile('<a href="(.+?)"><img border="0" src="(.+?)" width="150" height="83"></a><br>').findall(link))
           
            buf = StringIO.StringIO(link)
            bisha= str(match_url_thumb).split()
            counter=0
            for names in link.split():
                
                line=buf.readline()
                if ('الحلقة ') in line:
                    if len(line)<50:
                        name= line.strip()
                        
                        page_url= bisha[counter].replace("[('","")
                        page_url=page_url.replace("',","").strip()
                        thumNail=bisha[1].replace("'),","")
                        thumNail=thumNail.replace("'","").strip()
                        page_url=page_url.replace("('","").strip()
                        page_url="http://www.panet.co.il"+page_url
                        print name
                        print page_url
                        addDir(name,page_url,31,thumNail)

def GET_VIDEO_FILE(url):
    url= url.split("autostart=")
    temp=url.pop(0)
    url=url.pop(0)
    url=url.replace("&page=0","").strip()
   
    url="http://www.panet.co.il/Ext/vplayer_lib.php?media="+url+'&start=false'
   
    if checkURL(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		req.add_header('Host',' fms-eu0.panet.co.il')
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
        #print match_url_thumb
		match_url_thumb=str(match_url_thumb).replace("['", "")
		match_url_thumb=str(match_url_thumb).replace("']", "").strip()
        #match_url_thumb=match_url_thumb.replace("http://www.panet.co.il/Ext/players/flv/playern.swf?type=http&streamer=start&file=", "http://www.panet.co.il/Ext/players/flv/playern.swf?type=http&amp;streamer=start&amp;file=")
		match_url_thumb=match_url_thumb.replace('%3A',':')
		match_url_thumb=match_url_thumb.replace('%2F','/')
		match_url_thumb=match_url_thumb.replace('http://','')
		match_url_thumb=match_url_thumb.replace('file=','file=http://')
		match_url_thumb=match_url_thumb.replace("www.panet.co.il/Ext/players/flv/playern.swf?type=http&streamer=start&file=","")+"?start=0"
		match_url_thumb=str(match_url_thumb.replace("?start=0",""))
		match_url_thumb='rtmp://fms-eu1.panet.co.il swfUrl=http://www.panet.co.il/Ext/players/flv/playern.swf? repeat=single streamer=start file='+match_url_thumb+' provider=rtmp start=0'
		#match_url_thumb='rtmp://fms-eu1.panet.co.il swfUrl=http://www.panet.co.il/Ext/players/flv/playern.swf? file=/vod//96/96534/96534.mp4'
		print "This is video :"+match_url_thumb
		addLink(name,'match_url_thumb','')
	
def INDEX(url,start,max):
    film=start
	
	
    while film<max :
        film=film+1
        filmo=str(film)
        programurl=[str('http://www.panet.co.il/online/video/movies/movie/'+filmo+'.html')]
        for currurl in programurl:
            url=programurl.pop(0)
            
            if checkURL(url):
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                
                match=(re.compile('name="title" content=(.+?)/>').findall(link))
                
                if len(match) :
                    
                        name= ''.join(match).replace('"', '')
                        
                match2=re.compile('"video_src" href="(.+?)"/>').findall(link)
                if len(match2) :
                        VideoImg= (''.join(match2).replace('"', '').split('&image='))
                        temp=VideoImg.pop(0).strip(' ')
                        thumbnail=VideoImg.pop(0).strip(' ')
			addDir(name,url,2,thumbnail)
		

		
def VIDEOLINKS(url,name):
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match2=re.compile('"video_src" href="(.+?)"/>').findall(link)
                
                if len(match2) :
                        VideoImg= (''.join(match2).replace('"', '').split('&image='))
                        videoPath=VideoImg.pop(0).strip('')
                        videoPath=videoPath[81:]
                        videoPath=videoPath.replace('%3A',':')
                        videoPath=videoPath.replace('%2F','/')
		addLink(name,videoPath,'')
        

                
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




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
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

from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
try:
    import json
except:
    import simplejson as json
	
	
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
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url,0,100)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',3,'')
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name) 
elif mode==3:
	print ""+url
	INDEX(url,100,200)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',4,'')
elif mode==4:
	print ""+url
	INDEX(url,200,300)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',5,'')
	
elif mode==5:
	print ""+url
	INDEX(url,300,400)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',6,'')
elif mode==6:
	print ""+url
	INDEX(url,400,500)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',7,'')
elif mode==7:
	print ""+url
	INDEX(url,500,600)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',8,'')
	
elif mode==8:
	print ""+url
	INDEX(url,600,700)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',9,'')
elif mode==9:
	print ""+url
	INDEX(url,700,800)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',10,'')
elif mode==10:
	print ""+url
	INDEX(url,800,900)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',11,'')
	
elif mode==11:
	print ""+url
	INDEX(url,900,1000)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',12,'')
elif mode==12:
	print ""+url
	INDEX(url,1000,1100)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',13,'')
elif mode==13:
	print ""+url
	INDEX(url,1100,1200)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',14,'')
	
elif mode==14:
	print ""+url
	INDEX(url,1200,1300)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',15,'')

elif mode==15:
	print ""+url
	INDEX(url,1300,1400)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',16,'')
elif mode==16:
	print ""+url
	INDEX(url,1400,1500)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',17,'')
	
elif mode==17:
	print ""+url
	INDEX(url,1500,1600)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',18,'')
	
elif mode==18:
	print ""+url
	INDEX(url,1600,1700)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',19,'')
elif mode==19:
	print ""+url
	INDEX(url,1700,1800)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',20,'')
	
elif mode==20:
	print ""+url
	INDEX(url,1800,2000)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',21,'')
elif mode==21:
	print ""+url
	INDEX(url,2000,2100)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',22,'')

elif mode==22:
	print ""+url
	INDEX(url,2100,2200)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',23,'')

elif mode==23:
	print ""+url
	INDEX(url,2200,2300)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',24,'')

elif mode==24:
	print ""+url
	INDEX(url,2300,2400)
	#addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',25,'')


	
if mode==29:
	#print ""+url
	INDEX_TURKISH(url)
elif mode==30:
	#print ""+url
	LIST_SERIES(url)
elif mode==31:
	#print ""+url
	GET_VIDEO_FILE(url)
	
	







       

xbmcplugin.endOfDirectory(int(sys.argv[1]))
