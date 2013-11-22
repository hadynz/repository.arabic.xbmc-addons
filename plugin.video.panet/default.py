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
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('WARNING','This addon is completely FREE DO NOT buy any products from http://tvtoyz.com/', 16000, 'http://pschools.haifanet.org.il/abd.relchaj/2010/panet.jpg'))
	addDir('مسلسلات رمضان 2013','http://www.panet.co.il/Ext/series.php?name=category&id=32&country=NL&page=',29,'')
	addDir('مسلسلات سورية ولبنانية','http://www.panet.co.il/Ext/series.php?name=category&id=18&country=NL&page=',29,'')
	addDir('مسلسلات مصرية','http://www.panet.co.il/Ext/series.php?name=category&id=19&country=NL&page=',29,'')
	addDir('مسلسلات خليجية','http://www.panet.co.il/Ext/series.php?name=category&id=21&country=NL&page=',29,'')
	addDir('افلام عربية ','http://www.panet.co.il/online/video/movies/P-0.html/',1,'')
	#addDir('افلام متحركة  ','http://www.panet.co.il/Ext/series.php?name=folder&id=257',1,'')
	addDir('مسلسلات تركية','http://www.panet.co.il/Ext/series.php?name=category&id=17&country=TR&page=',29,'')
	addDir('مسلسلات مكسيكية و عالمية','http://www.panet.co.il/Ext/series.php?name=category&id=20&country=NL&page=',29,'')
	addDir('رسوم متحركة , برامج اطفال','http://www.panet.co.il/Ext/series.php?name=category&id=15&country=NL&page=',29,'')
	#addDir('كليبات مضحكة','http://www.panet.co.il/Ext/series.php?name=category&id=2&country=NL&page=',29,'')
	addDir('برامج ومنوعات','http://www.panet.co.il/Ext/series.php?name=category&id=27&country=NL&page=',29,'')
	
		

	
def checkURL(url):
    p = urlparse(url)
    h = HTTP(p[1])
    h.putrequest('HEAD', p[2])
    h.endheaders()
    if h.getreply()[0] == 200: return 1
    else: return 0
	
def PanetListSeries(url):
    siteMax=10
    Serie=0
    mynamearray=[]
    myimagesarray=[]
    myurlarray=[]
    
    
    while Serie!=siteMax:
        Serie=Serie+1
        kurl=str(url)+str(Serie)
        req = urllib2.Request(kurl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        
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
				print "SONSON "+myurl
				myurlarray.append(myurl)
                
				myimage=str(both[1]).replace('" width="150" height="83"></a><br>', '').strip()
				myimagesarray.append(myimage)
    for i in range(0,400):
        try:
            
            print mynamearray[i]
            print myurlarray[i]
            addDir(mynamearray[i],myurlarray[i],30,myimagesarray[i])
        except:
            pass
            


def getEpesodes(url):
	
	 
    siteMax=10
    counter=0
    c2=0
       
    while counter!=siteMax:
        kurl=url+"&country=NL&page="+str(counter)
        #print "MY URL "+kurl
        
        if checkURL(kurl):
            req = urllib2.Request(kurl)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            counter=counter+1
            target= re.findall(r'<div class="series-table-item">(.*?)\s(.*?)</font>', link, re.DOTALL)
            for items in target:
                try:   
                    mypageurl="http://www.panet.co.il"+str(str((str(items).split('&page='+str(0)+'"><img border="0" src="'))[0]).split('href="')[1]).strip()
                    myimageurl=str((str(items).split('&page='+str(0)+'"><img border="0" src="'))[1]).strip()
                    myimageurl=str(str(myimageurl).split('jpg"')[0]).strip()+'jpg'
                    myseriename=str(items).split('<br/>')
                    myseriename= myseriename[1]
                    myseriename=myseriename[0:0]+myseriename[13+1:]
                    myseriename=myseriename[0:53]+myseriename[65+1:]
                    myseriename=str(myseriename).split(' ')
                    epos="الحلقة" +" "+ (str(myseriename[1]).strip())
                    print epos
                    print myimageurl
                    addLink(epos,mypageurl,31,'')
                except IndexError:
                    print ""
                    try:
                        mypageurl="http://www.panet.co.il"+str(str((str(items).split('&page='+str(1)+'"><img border="0" src="'))[0]).split('href="')[1]).strip()
                        myimageurl=str((str(items).split('&page='+str(1)+'"><img border="0" src="'))[1]).strip()
                        myimageurl=str(str(myimageurl).split('jpg"')[0]).strip()+'jpg'
                        myseriename=str(items).split('<br/>')
                        myseriename= myseriename[1]
                        myseriename=myseriename[0:0]+myseriename[13+1:]
                        myseriename=myseriename[0:53]+myseriename[65+1:]
                        myseriename=str(myseriename).split(' ')
                        epos="الحلقة" +" "+ (str(myseriename[1]).strip())
                        print epos
                        print myimageurl
                        addLink(epos,mypageurl,31,'')
                    except IndexError:
                        print ""
                        try:
                            mypageurl="http://www.panet.co.il"+str(str((str(items).split('&page='+str(2)+'"><img border="0" src="'))[0]).split('href="')[1]).strip()
                            myimageurl=str((str(items).split('&page='+str(2)+'"><img border="0" src="'))[1]).strip()
                            myimageurl=str(str(myimageurl).split('jpg"')[0]).strip()+'jpg'
                            myseriename=str(items).split('<br/>')
                            myseriename= myseriename[1]
                            myseriename=myseriename[0:0]+myseriename[13+1:]
                            myseriename=myseriename[0:53]+myseriename[65+1:]
                            myseriename=str(myseriename).split(' ')
                            epos="الحلقة" +" "+ (str(myseriename[1]).strip())
                            print epos
                            print myimageurl
                            addLink(epos,mypageurl,31,'')
                        except IndexError:
                            print ""
                            try:
                                mypageurl="http://www.panet.co.il"+str(str((str(items).split('&page='+str(3)+'"><img border="0" src="'))[0]).split('href="')[1]).strip()
                                myimageurl=str((str(items).split('&page='+str(3)+'"><img border="0" src="'))[1]).strip()
                                myimageurl=str(str(myimageurl).split('jpg"')[0]).strip()+'jpg'
                                myseriename=str(items).split('<br/>')
                                myseriename= myseriename[1]
                                myseriename=myseriename[0:0]+myseriename[13+1:]
                                myseriename=myseriename[0:53]+myseriename[65+1:]
                                myseriename=str(myseriename).split(' ')
                                epos="الحلقة" +" "+ (str(myseriename[1]).strip())
                                print epos
                                print myimageurl
                                addLink(epos,mypageurl,31,'')
                            except IndexError:
                                print ""
                                try:
                                    mypageurl="http://www.panet.co.il"+str(str((str(items).split('&page='+str(4)+'"><img border="0" src="'))[0]).split('href="')[1]).strip()
                                    myimageurl=str((str(items).split('&page='+str(4)+'"><img border="0" src="'))[1]).strip()
                                    myimageurl=str(str(myimageurl).split('jpg"')[0]).strip()+'jpg'
                                    myseriename=str(items).split('<br/>')
                                    myseriename= myseriename[1]
                                    myseriename=myseriename[0:0]+myseriename[13+1:]
                                    myseriename=myseriename[0:53]+myseriename[65+1:]
                                    myseriename=str(myseriename).split(' ')
                                    epos="الحلقة" +" "+ (str(myseriename[1]).strip())
                                    print epos
                                    print myimageurl
                                    addLink(epos,mypageurl,31,'')
                                except IndexError:
                                    print ""
                                    try:
                                        mypageurl="http://www.panet.co.il"+str(str((str(items).split('&page='+str(5)+'"><img border="0" src="'))[0]).split('href="')[1]).strip()
                                        myimageurl=str((str(items).split('&page='+str(5)+'"><img border="0" src="'))[1]).strip()
                                        myimageurl=str(str(myimageurl).split('jpg"')[0]).strip()+'jpg'
                                        myseriename=str(items).split('<br/>')
                                        myseriename= myseriename[1]
                                        myseriename=myseriename[0:0]+myseriename[13+1:]
                                        myseriename=myseriename[0:53]+myseriename[65+1:]
                                        myseriename=str(myseriename).split(' ')
                                        epos=("الحلقة" +" "+ (str(myseriename[1]).strip()))
                                        print epos
                                        print myimageurl
                                        addLink(epos,mypageurl,31,'')
                                    except IndexError:
                                        print ""
                                        try:
                                            mypageurl="http://www.panet.co.il"+str(str((str(items).split('&page='+str(6)+'"><img border="0" src="'))[0]).split('href="')[1]).strip()
                                            myimageurl=str((str(items).split('&page='+str(6)+'"><img border="0" src="'))[1]).strip()
                                            myimageurl=str(str(myimageurl).split('jpg"')[0]).strip()+'jpg'
                                            myseriename=str(items).split('<br/>')
                                            myseriename= myseriename[1]
                                            myseriename=myseriename[0:0]+myseriename[13+1:]
                                            myseriename=myseriename[0:53]+myseriename[65+1:]
                                            myseriename=str(myseriename).split(' ')
                                            epos=("الحلقة" +" "+ (str(myseriename[1]).strip()))
                                            print epos
                                            print myimageurl
                                            addLink(epos,mypageurl,31,'')
                                        except IndexError:
                                            print ""
                                            try:
                                                mypageurl="http://www.panet.co.il"+str(str((str(items).split('&page='+str(7)+'"><img border="0" src="'))[0]).split('href="')[1]).strip()
                                                myimageurl=str((str(items).split('&page='+str(7)+'"><img border="0" src="'))[1]).strip()
                                                myimageurl=str(str(myimageurl).split('jpg"')[0]).strip()+'jpg'
                                                myseriename=str(items).split('<br/>')
                                                myseriename= myseriename[1]
                                                myseriename=myseriename[0:0]+myseriename[13+1:]
                                                myseriename=myseriename[0:53]+myseriename[65+1:]
                                                myseriename=str(myseriename).split(' ')
                                                epos=("الحلقة" +" "+ (str(myseriename[1]).strip()))
                                                print epos
                                                print myimageurl
                                                addLink(epos,mypageurl,31,'')
                                            except IndexError:
                                                print ""
                                                try:
                                                    mypageurl="http://www.panet.co.il"+str(str((str(items).split('&page='+str(8)+'"><img border="0" src="'))[0]).split('href="')[1]).strip()
                                                    myimageurl=str((str(items).split('&page='+str(8)+'"><img border="0" src="'))[1]).strip()
                                                    myimageurl=str(str(myimageurl).split('jpg"')[0]).strip()+'jpg'
                                                    myseriename=str(items).split('<br/>')
                                                    myseriename= myseriename[1]
                                                    myseriename=myseriename[0:0]+myseriename[13+1:]
                                                    myseriename=myseriename[0:53]+myseriename[65+1:]
                                                    myseriename=str(myseriename).split(' ')
                                                    epos=("الحلقة" +" "+ (str(myseriename[1]).strip()))
                                                    print epos
                                                    print myimageurl
                                                    addLink(epos,mypageurl,31,'')
                                                except IndexError:
                                                    print ""
                                                    try:
                                                        mypageurl="http://www.panet.co.il"+str(str((str(items).split('&page='+str(9)+'"><img border="0" src="'))[0]).split('href="')[1]).strip()
                                                        myimageurl=str((str(items).split('&page='+str(9)+'"><img border="0" src="'))[1]).strip()
                                                        myimageurl=str(str(myimageurl).split('jpg"')[0]).strip()+'jpg'
                                                        myseriename=str(items).split('<br/>')
                                                        myseriename= myseriename[1]
                                                        myseriename=myseriename[0:0]+myseriename[13+1:]
                                                        myseriename=myseriename[0:53]+myseriename[65+1:]
                                                        myseriename=str(myseriename).split(' ')
                                                        epos=("الحلقة" +" "+ (str(myseriename[1]).strip()))
                                                        print epos
                                                        print myimageurl
                                                        addLink(epos,mypageurl,31,'')
                                                    except IndexError:
                                                        print ""
                                                        try:
                                                            mypageurl="http://www.panet.co.il"+str(str((str(items).split('&page='+str(10)+'"><img border="0" src="'))[0]).split('href="')[1]).strip()
                                                            myimageurl=str((str(items).split('&page='+str(10)+'"><img border="0" src="'))[1]).strip()
                                                            myimageurl=str(str(myimageurl).split('jpg"')[0]).strip()+'jpg'
                                                            myseriename=str(items).split('<br/>')
                                                            myseriename= myseriename[1]
                                                            myseriename=myseriename[0:0]+myseriename[13+1:]
                                                            myseriename=myseriename[0:53]+myseriename[65+1:]
                                                            myseriename=str(myseriename).split(' ')
                                                            epos=("الحلقة" +" "+ (str(myseriename[1]).strip()))
                                                            print epos
                                                            print myimageurl
                                                            addLink(epos,mypageurl,31,'')
                                                        except IndexError:
                                                            print ""
					
	
	
def GET_VIDEO_FILE(url):
	try:
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
			
			match_url_thumb=match_url_thumb.replace("www.panet.co.il/Ext/players/flv/playern.swf?type=http&streamer=start&file=","")
			
			match_url_thumb=match_url_thumb+'|Referer=http://www.panet.co.il/Ext/players/flv5/player.swf'
			listItem = xbmcgui.ListItem(path=str(match_url_thumb))
			xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
	except:
		pass
	
def INDEX(url,start,max):
	try:
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
				addLink(name,url,2,thumbnail)
	except:
		pass
		

		
def VIDEOLINKS(url,name):
	try:
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
			
		listItem = xbmcgui.ListItem(path=str(videoPath))
		xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
	except:
		pass
			

                
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
	PanetListSeries(url)
elif mode==30:
	#print ""+url
	getEpesodes(url)
elif mode==31:
	#print ""+url
	GET_VIDEO_FILE(url)
	
	







       

xbmcplugin.endOfDirectory(int(sys.argv[1]))
