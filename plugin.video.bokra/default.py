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

def list_cats(url):
    all_cats ={}
    req = urllib2.Request(url)
    response = urllib2.urlopen(req,timeout=15)
    link = response.read()

    target = re.findall(r'<ul class="hidden-xs">(.*?)\s(.*?)</ul>', link, re.DOTALL)
    for items in target:
        for itr in items:
            if itr !='':
                for val in itr.split('</a></li>'):
                    if val !='':
                        try:
							my_path = 'http://shahidlive.com'+val.strip().split('href="')[1].split('">')[0]
							my_name = val.strip().split('href="')[1].split('">')[1]
							if 'مسلسلات' in my_name:
								addDir(my_name,my_path,1,'')
							else :
								addDir(my_name,my_path,2,'')
							all_cats[my_name]=my_path
                        except:
                            pass
    return all_cats
    

def list_epos(url):
	
    all_cats = {}
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link = response.read()
    target = re.findall(r'<div class="col-xs-5 no-pd-left ">(.*?)\s(.*?)<script>', link, re.DOTALL)
    for epo in target:
        for it in epo:
            for my_con in it.split('</div>'):
                if 'href' in my_con:
                    target = re.findall(r'<a href="(.*?)\s(.*?)" class="center-block">', my_con, re.DOTALL)
                    for i in target:
						name=str( i[1]).split('=')[1].replace('"',"").strip()
						path= 'http://shahidlive.com'+i[0].replace('"',"").strip()
						addLink(name,path,3,'')

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
	print link_target
    #RTMPVideoURL(url=RTMP_URL, clip=PLAYPATH, swf_url=swf_url, args=(dict()))
	video_url= str(link_target).split('<source src="')[1].split('" type=')[0].strip().split('vod')

	video_url_1 = ''.join(video_url)
	sep = '"'
	rest = video_url_1.split(sep,1)[0]
	listItem = xbmcgui.ListItem(path=str(rest))
	xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
   
 

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
						addDir(title,path,2,img)
						print path
						print img
						print title



                      except:
                          pass
        except:

            print 'Nothing ti view'

def get_episodes(url):

    max_nr = int(get_max_page(url))
    try:

        for iter in range(0,max_nr):
            url = url.split('-')[0] +'-'+ url.split('-')[1]+'-'+str(iter)
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link=response.read()
            sum_target = str(link).split(' <meta name="description" content="')[1].split('" />')[0]
            print sum_target
            target= re.findall(r' <a href="(.*?)\s(.*?)<img src="(.*?)\s(.*?)class(.*?)\s(.*?)<div class="title"><h4>(.*?)\s(.*?)</h4></div>', link, re.DOTALL)
            counter = 0
            for itr in  target:
                counter =counter +1
                if counter > 1:
					video = 'http://shahidlive.com'+ itr[0].replace('">','').strip()
					img =   itr[2].replace('"','').strip()+' '+itr[3].strip().replace('"','').replace(' ', '%20' )
					name = itr[6]+' '+ itr[7]
					name= name.strip()
					addLink(name,video,3,img)
                    #print name
                    #print img
                    #print video




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
        list_cats('http://shahidlive.com/')
       
elif mode==1:
        print ""+url
        list_cat_content(url)
elif mode==2:
        print ""+url
        get_episodes(url)
	
elif mode==3:
	print ""+url
	get_video_file(url)
	

xbmcplugin.endOfDirectory(int(sys.argv[1]))
