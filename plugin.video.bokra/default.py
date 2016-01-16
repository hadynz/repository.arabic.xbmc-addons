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
import xbmcgui
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import cookielib
import datetime




__settings__ = xbmcaddon.Addon(id='plugin.video.bokra')
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

def get_categories(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()

    target= re.findall(r' <ul class="hidden-xs">(.*?)\s(.*?) </ul>', link, re.DOTALL)
    mylist= [items for i in  target for items in i if items !='']
    final_catergories = [it for itr in mylist for it in itr.split('/a></li>') if '="' in str(it)  ]
    for itr in  final_catergories:
        my_data =itr.split('="')[1]
        path =  'http://shahidlive.com'+my_data.split('">')[0]
        title =  my_data.split('">')[1]
        title = title.replace('<','')
	if 'مسلسلات' in str(title):
		addDir(title,path,1,'')
	elif 'افلام' in str(title):
		addDir(title,path,2,'')

def list_cat_content(url):
    max_nr = int(get_max_page(url))
    for iter in range(1,max_nr):
        try:
            url = url.split('-')[0] +'-'+ url.split('-')[1]+'-'+str(iter)
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req,timeout=1)
            link=response.read()
	    target= re.findall(r'<div class="col-(.*?)\s(.*?)</h4></div>', link, re.DOTALL)
            counter = 0
            for itr in  target:
                counter =counter +1
                if counter > 1:
                  for item in  itr:

                      item= item.split('">')
                      try:
                        path =  'http://shahidlive.com'+item[1].replace('<a href="','').strip()
                        img =  item[3].split('="')[1].split('"')[0].strip()
                        title = item[6].replace('<h4>','').strip()
			addDir(title,path,3,img)
			
                      except:
                          pass
        except:

            print 'Nothing ti view'

		
def get_max_page(url):
    my_nr_list = []
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    target= re.findall(r'<ul class="pagination">(.*?)\s(.*?)</div>', link, re.DOTALL)
    for item in target:
        for itr in item:
            for i in  itr.split('class="page"'):
                try:
                    my_list_item= i.split('</a></li><li class=')[0].split('">')[1]
                    if my_list_item.isdigit():
                        my_nr_list.append(my_list_item)
                except:
                    pass

    return max (my_nr_list)

def get_episodes(url):

    max_nr = int(get_max_page(url))
    try:

        for iter in range(0,max_nr):
            url = url.split('-')[0] +'-'+ url.split('-')[1]+'-'+str(iter)
            print url
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link=response.read()
            target= re.findall(r' <a href="(.*?)\s(.*?)<img src="(.*?)\s(.*?)class(.*?)\s(.*?)<div class="title"><h4>(.*?)\s(.*?)</h4></div>', link, re.DOTALL)
            counter = 0
            for itr in  target:
                counter =counter +1
                if counter > 1:
                    video = 'http://shahidlive.com'+ itr[0].replace('">','').strip()
                    img =   itr[2].replace('"','').strip()
                    name = itr[6]+' '+ itr[7]
                    name= name.strip()
		    addLink(name,video,4,img)
                    
    except:
        pass
      
def get_video_file(url):
    url = 'http://shahidlive.com/Play/'+url.split('Video-')[1]+'-681-382'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    target= re.findall(r'<iframe src="(.*?)\s(.*?)"', link, re.DOTALL)
    target= target[0]
    target = target[0].replace('"','').strip()

    req_target = urllib2.Request(target)
    req_target.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response_target = urllib2.urlopen(req_target)
    link_target=response_target.read()
    link_file= re.findall(r'"file":(.*?)\s(.*?)",', link_target, re.DOTALL)
    final_video_url= str(link_file[0][1]).replace('"','').strip()
    #link_streamer= re.findall(r'"streamer":(.*?)\s(.*?)",', link_target, re.DOTALL)
    #link_flash= re.findall(r'"flashplayer":(.*?)\s(.*?)",', link_target, re.DOTALL)
    #link_flash= link_flash[0]
    #link_flash= 'http://nadstream.shahidlive.com'+link_flash[1].replace('"','').strip()
    #link_file= link_file[0]
    #link_file= link_file[1]
    #link_streamer= link_streamer[0]
    #link_streamer= link_streamer[1]
    #final_video_url = link_streamer.replace('"','').strip()+' playpath='+link_file.replace('"','').strip()+' swfUrl='+link_flash+ ' timeout=20'
    listItem = xbmcgui.ListItem(path=str(final_video_url))
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
        get_categories('http://shahidlive.com/')
       
elif mode==1:
        print ""+url
        list_cat_content(url)
	
elif mode==2:
	print ""+url
	get_episodes(url)

elif mode==3:
	print ""+url
	get_episodes(url)
elif mode==4:
	print ""+url
	get_video_file(url)
			

xbmcplugin.endOfDirectory(int(sys.argv[1]))
