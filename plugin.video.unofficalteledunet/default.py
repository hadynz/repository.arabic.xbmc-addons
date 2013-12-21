# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import urllib2,urllib
import re
import httplib,itertools
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import cookielib
import time


__settings__ = xbmcaddon.Addon(id='plugin.video.unofficalteledunet')
__icon__ = __settings__.getAddonInfo('icon')
__fanart__ = __settings__.getAddonInfo('fanart')
__language__ = __settings__.getLocalizedString
_thisPlugin = int(sys.argv[1])
_pluginName = (sys.argv[0])
globalIp=''


def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner
httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)


def CATEGORIES():
	addDir('All Channels','http://www.teledunet.com/list_chaines.php',1,'http://www.mirrorservice.org/sites/addons.superrepo.org/Frodo/.metadata/plugin.video.teledunet.png')
	
	
	
		
def index(url):
	url="http://www.teledunet.com/list_chaines.php"
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
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
	addLink('MBC','rtmp://www.teledunet.com:1935/teledunet/mbc_1',2,'https://si0.twimg.com/profile_images/1133033554/mbc-fb.JPG')
	addLink('MBC DRAMA','rtmp://www.teledunet.com:1935/teledunet/mbc_drama',2,'http://www.allied-media.com/ARABTV/images/mbc_drama.jpg')
	addLink('JSC +1','rtmp://www.teledunet.com:1935/teledunet/jsc_1',2,'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg')
	addLink('JSC +2','rtmp://www.teledunet.com:1935/teledunet/jsc_2',2,'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg')
	addLink('JSC +3','rtmp://www.teledunet.com:1935/teledunet/jsc_3',2,'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg')
	addLink('JSC +4','rtmp://www.teledunet.com:1935/teledunet/jsc_4',2,'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg')
	addLink('JSC +5','rtmp://www.teledunet.com:1935/teledunet/jsc_5',2,'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg')
	addLink('JSC +6','rtmp://www.teledunet.com:1935/teledunet/jsc_6',2,'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg')
	addLink('JSC +7','rtmp://www.teledunet.com:1935/teledunet/jsc_7',2,'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg')
	addLink('JSC +8','rtmp://www.teledunet.com:1935/teledunet/jsc_8',2,'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg')
	addLink('JSC +9','rtmp://www.teledunet.com:1935/teledunet/jsc_9',2,'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg')
	addLink('JSC +10','rtmp://www.teledunet.com:1935/teledunet/jsc_10',2,'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg')
	addLink('Abu Dhabi Al Oula','rtmp://www.teledunet.com:1935/teledunet/abu_dhabi',2,'https://www.zawya.com/pr/images/2009/ADTV_One_RGB_2009_10_08.jpg')
	addLink('Abu Dhabi Sports','rtmp://www.teledunet.com:1935/teledunet/abu_dhabi_sports_1',2,'https://si0.twimg.com/profile_images/2485587448/2121.png')
	addLink('Al Jazeera','rtmp://www.teledunet.com:1935/teledunet/aljazeera',2,'http://www.chicagonow.com/chicago-sports-media-watch/files/2013/04/Al-Jazeera.jpg')
	addLink('Al Jazeera Sport Global','rtmp://www.teledunet.com:1935/teledunet/aljazeera_sport_global',2,'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg')
	addLink('Al Jazeera Sport 1','rtmp://www.teledunet.com:1935/teledunet/aljazeera_sport_1',2,'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg')
	addLink('Al Jazeera Sport 2','rtmp://www.teledunet.com:1935/teledunet/aljazeera_sport_2',2,'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg')
	addLink('Al Jazeera Mubasher Masr','rtmp://www.teledunet.com:1935/teledunet/aljazeera_mubasher_masr',2,'http://www.chicagonow.com/chicago-sports-media-watch/files/2013/04/Al-Jazeera.jpg')
	addLink('Al Jazeera Children','rtmp://www.teledunet.com:1935/teledunet/aljazeera_children',2,'http://3.bp.blogspot.com/-UX1XBY8-02g/Uoku7OTIrFI/AAAAAAAAASk/-0eEX7fumJw/s1600/al_jazeera_children.png')
	addLink('Al Jazeera Documentation','rtmp://www.teledunet.com:1935/teledunet/aljazeera_doc',2,'http://upload.wikimedia.org/wikipedia/en/e/e6/Al_Jazeera_Doc.png')
	addLink('ART Cinema','rtmp://www.teledunet.com:1935/teledunet/art_aflam_1',2,'http://www.lyngsat-logo.com/hires/aa/art_cinema.png')
	addLink('ART Aflam 2','rtmp://www.teledunet.com:1935/teledunet/art_aflam_2',2,'http://www.invision.com.sa/en/sites/default/files/imagecache/216x216/channels/2011/10/11/1138.jpg')
	addLink('Cartoon Network','rtmp://www.teledunet.com:1935/teledunet/cartoon_network',2,'http://upload.wikimedia.org/wikipedia/commons/b/bb/Cartoon_Network_Arabic_logo.png')
	addLink('MTV Lebanon','rtmp://www.teledunet.com:1935/teledunet/mtv',2,'http://mtv.com.lb/images/mtv-social-logo1.jpg')
	addLink('NBN','rtmp://www.teledunet.com:1935/teledunet/nbn',2,'http://upload.wikimedia.org/wikipedia/en/1/14/Nbn_lebanon.png')
	addLink('Otv Lebanon','rtmp://www.teledunet.com:1935/teledunet/otv_lebanon',2,'http://www.worldmedia.com.au/Portals/0/Images/Logo_s/otv.png')
	addLink('Al Hayat','rtmp://www.teledunet.com:1935/teledunet/alhayat_1',2,'http://3.bp.blogspot.com/--uP1DsoBB7s/T4EMosYH5uI/AAAAAAAAF9E/RdbY8-E3Riw/s320/Al%2Bhayat.jpg')
	addLink('Al Hayat Cinema','rtmp://www.teledunet.com:1935/teledunet/alhayat_cinema',2,'http://www.lyngsat-logo.com/hires/aa/alhayat_cinema.png')
	addLink('Alarabiya','rtmp://www.teledunet.com:1935/teledunet/alarabiya',2,'http://www.debbieschlussel.com/archives/alarabiya2.jpg')   
	addLink('Tele Sports','rtmp://www.teledunet.com:1935/teledunet/tele_sports',2,'http://www.itwebsystems.co.uk/resources/icon.png')
	
    
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
	for items in style:
		styleItem=str( items).split('background-color:#')[1]
		styleItem=str( styleItem).replace(';"', '').strip()
		colorArray.append(styleItem) 
	for (names,images,paths,colors) in itertools.izip (nameArray,imgArray,pathArray,colorArray):
		
		addLink(names,paths,2,images)
	

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
    cj=str(cj).replace('<cookielib.CookieJar[<Cookie', '').replace('/>]>', '').replace('for www.teledunet.com', '')
    cj=str(cj).strip()
    return cj


def getId(channel):
    url="http://www.teledunet.com/tv_/?channel="+str(channel)
    req = urllib2.Request(url)
    req.add_header('Host', 'www.teledunet.com')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Referer', 'http://www.teledunet.com/')
    req.add_header('Cookie', str(getCookies(url)))
    req.add_header('Connection', 'keep-alive')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    nameUrl=(re.compile('time_player=(.+?);').findall(link))
    nameUrl=str( nameUrl).replace("['", '').replace("']", '').replace(".","").replace("E+13","00").strip()
    return nameUrl
	
                    
def PlayChannels(url):
	firstPart=str(url).split('teledunet/')[1]
	finalPayPath=url+' app=teledunet swfUrl=http://www.teledunet.com/tv/player.swf?bufferlength=5&repeat=single&autostart=true&id0='+str(getId(firstPart))+'&streamer='+str(url)+'&file='+str(firstPart)+'&provider=rtmp playpath='+str(firstPart)+' live=1 pageUrl=http://www.teledunet.com/tv/?channel='+str(firstPart)+'&no_pub'
	listItem = xbmcgui.ListItem(path=str(finalPayPath))
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
        CATEGORIES()
       
elif mode==1:
        print ""+url
        index(url)
	
elif mode==2:
        print ""+url
        PlayChannels(url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
