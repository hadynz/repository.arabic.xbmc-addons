# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import httplib
import zlib,gzip



__settings__ = xbmcaddon.Addon(id='plugin.video.cartoonarabi')
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



def GetCartoonArabiSeries(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    myNames=[]
    url_target=(re.compile('<li class=""><a href="(.+?)" class="">(.+?)</a>').findall(link))

    for items in url_target:
        path=str( items[0]).strip()
        name=str( items[1]).strip()
        addDir(name,path,1,'')

def GetCartoonArabiEpos(url):
	for itr in range(1,6):
		req = urllib2.Request(url+'&page='+str(itr))
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		url_target=(re.compile('<a href="(.+?)" class="(.+?)class="pm-thumb-fix-clip"><img src="(.+?)" alt="(.+?)"').findall(link))
		for items in url_target:
			path=str( items[0]).strip()
			name=str( items[3]).strip()
			img=str( items[2]).strip()
			addLink(name,path,2,img)

def decode (page):
    encoding = page.info().get("Content-Encoding")
    if encoding in ('gzip', 'x-gzip', 'deflate'):
        content = page.read()
        if encoding == 'deflate':
            data = StringIO.StringIO(zlib.decompress(content))
        else:
            data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(content))
        page = data.read()

    return page


def playContent(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	link2=link
	response.close()
	url_target=(re.compile('<iframe frameborder=(.+?)src="(.+?)"></iframe>').findall(link))
	if 'syndication' in str( url_target):
		videoId=str( url_target[0]).split(',')
		videoId=str( videoId[1]).split('?syndication=')
		videoId=str( videoId[0] ).replace("'http://www.dailymotion.com/embed/video/", '').strip()
		playback_url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url='+ str(videoId)
		listItem = xbmcgui.ListItem(path=str(playback_url))
		xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
	else:
		url_target=(re.compile('<embed src="(.+?)"(.+?)autostart="').findall(link))
		url2=str( url_target[0]).split(("',"))
		url2=url2[0]
		url2=str(url2).replace("('", '').strip()
		opener = urllib2.build_opener()
		opener.addheaders = [('Referer', 'http://www.4shared.com'),('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'), ('Accept-Encoding', 'gzip,deflate,sdch')]
		usock = opener.open(url2)
		url2 = usock.geturl()
		usock.close()
		videoFile=str( url2).split('&streamer=')[0]
		videoFile=str( videoFile).split('fileId=')[1]
		videoFile=str(videoFile).split('&image=')[0]
		videoFile=str(videoFile).split('&apiURL=')[0]
		videoFile=str( videoFile).strip()
		restUrl = str ('http://www.4shared.com/web/rest/files/' + videoFile + '/embed/meta.xml')
		req = urllib2.Request(restUrl)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		videoLink=response.read()
		response.close()
		videoLink = str( videoLink ).split('</previewUrl>')[0]
		videoLink = str( videoLink ).split('<previewUrl>')[1]
		playback_url = urllib.unquote ( videoLink )
		listItem = xbmcgui.ListItem(path=str(playback_url))
		xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)


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
        GetCartoonArabiSeries('http://www.cartoonarabi.com/newvideos.php?&page=1')

elif mode==1:
        print ""+url
        GetCartoonArabiEpos(url)

elif mode==2:
		print ""+url
		playContent(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))