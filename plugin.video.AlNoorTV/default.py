# -*- coding: utf-8 -*-

REMOTE_DBG = False

if REMOTE_DBG:
    try:
        sys.path.append('C:/Program Files (x86)/Kodi/system/python/Lib/site-packages/pysrc')
        import pysrc.pydevd as pydevd 
        import sys        
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")

import xbmc, xbmcgui, xbmcplugin
import urllib2, urllib, cgi, re
from HTMLParser import HTMLParser
import xbmcaddon
import traceback
import os
import sys
import json
from urlparse import urljoin

addon_id = 'plugin.video.AlNoorTV'
settings = xbmcaddon.Addon(id=addon_id)
language = settings.getLocalizedString
__addonname__ = settings.getAddonInfo('name')
__icon__ = settings.getAddonInfo('icon')
__fanart__ = settings.getAddonInfo('fanart')
addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonArt = os.path.join(addonPath, 'resources/images')
plugin = int(sys.argv[1])
msg_duration = 2000
opener = urllib2.build_opener()
# settings.setSetting('cookie','')

# Setting constants
MODE_LIST_CATEGORIES = 1
MODE_LIST_TOPICS = 2
MODE_LIST_EPISODES = 3 
MODE_EPISODE_DET = 4
MODE_PLAY_VIDEO = 5

links = {}
links['main'] = 'http://alnoortv.co/'
links['login'] = urljoin(links['main'], 'public/login/')

class myhtmlparser(HTMLParser):
    def __init__(self):
        self.reset()
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []
    def handle_starttag(self, tag, attrs):
        self.NEWTAGS.append(tag)
        self.NEWATTRS.append(attrs)
    def handle_data(self, data):
        self.HTMLDATA.append(data)
    def clean(self):
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []

        
def getSelectedLanguage():
    lang = settings.getSetting('language')
    selectedLanguage = 'ar'
    if lang == 'English':
        selectedLanguage = 'en'
    elif lang == 'Türkçe':
        selectedLanguage = 'tr'
    return selectedLanguage
    

def getRootCategories():
    url = urljoin(links['main'],'public/home/', getSelectedLanguage())
    data, current_url, code = getData(url)
    if 'error' not in current_url and code <= 302:
        allSeries = re.findall(r'<li class="has-submenu">(.*?)</li>', data, re.DOTALL)
        if allSeries:
            cat_link = ''
            allSeries= allSeries[-1]
            parser = myhtmlparser()
            parser.feed(allSeries)
            cat_name = parser.HTMLDATA[0] if len(parser.HTMLDATA)>0 else ''
            attrs = parser.NEWATTRS
            while (len(attrs) > 0 and attrs[0] != 'href'):
                attrs = attrs[0]
            else:
                if len(attrs) == 2:
                    _,cat_link = attrs
            
            addDir(cat_name, cat_link, MODE_LIST_TOPICS)

def listTopics(url):
    data, current_url, code = getData(url)
    if 'error' not in current_url and code <= 302:
        #(?:<section\sclass="category-content">)?(?:.*?(<img\s+?src.*?>).*?(<a.*?</a>).*?)(?:<span class="page-numbers current">)?
        topics = re.findall(r'(?:<section\sclass="category-content">)?(?:.*?(<img\s.+?src.*?>).*?(<a.*?</a>).*?)(?:<span class="page-numbers current">)?', data, re.DOTALL)
        
        for topic in topics:
            try:
                iconimage, name = topic
                parser = myhtmlparser()
                parser.feed(name)
                name = parser.HTMLDATA[0]
                addr = parser.NEWATTRS[0][0][-1]
                parser = myhtmlparser()
                parser.feed(iconimage)
                iconimage = parser.NEWATTRS[0][0][-1]
                name = name.replace("\t","")
                name = name.replace("\n", " ")
                addDir(name, addr, MODE_LIST_EPISODES, iconimage)
            except:
                pass

def listEpisodes(url):
    data, current_url, code = getData(url)
    if 'error' not in current_url and code <= 302:
        episodes = re.findall(r'(<img\ssrc=.*?>)(?:\s+)(<a.+?>)(?:.+?)(<a href="#">.+?>)', data, re.DOTALL)
        episodes.reverse()
        for episode in episodes:
            try:
                iconimage,addr,name = episode
                parser = myhtmlparser()
                parser.feed(name)
                name = parser.HTMLDATA[0]
                name = name.replace("\t","")
                name = name.replace("\n"," ")

                parser = myhtmlparser()
                parser.feed(addr)
                addr = parser.NEWATTRS[0][0][-1]
                parser = myhtmlparser()
                parser.feed(iconimage)
                iconimage = parser.NEWATTRS[0][0][-1]
                addDir(name, addr[1:], MODE_EPISODE_DET, iconimage, cat="DefaultVideo.png")
            except:
                pass

def episodeDetails(url):
    data, current_url, code = getData(url)
    try:
        video_id = re.findall(r'(?:https://player.vimeo.com/video/|https://player.vimeo.com/)(\d+)', data, re.DOTALL)

        uurl = 'plugin://plugin.video.vimeo/play/?video_id=%s' % video_id[0]
        addDir('Play', uurl, MODE_PLAY_VIDEO, iconimage='', cat="DefaultVideo.png")
    except:
        pass

def findStringBetween(text, start='', end=''):
    res = re.search('{0}(.*){0}'.format(start, end),text)
    return res.group(1)
def hasValidLogin():
    return settings.getSetting('validLogin') == "True"

def login():
    i = 0
    success = False
    login_url = urljoin(links['login'], getSelectedLanguage())
    while True:
        req = urllib2.Request(login_url)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        req.add_header('Host', 'alnoortv.co')
        data = prepareCredentials()
        req.add_data(data)
        req.add_header('Content-Length', str(len(data)))
        response = urllib2.urlopen(req)
        login_urlfound = ''
        try:
            login_urlfound=re.findall(r'(href="/public/login/?)', data, re.DOTALL)
        except:
            pass
        i+=1
        if (i>3 or not login_urlfound and ('error' not in response.url and response.headers.dict.get('set-cookie',''))):
            success = False
            settings.setSetting('cookie', response.headers.dict.get('set-cookie','')) 
            settings.setSetting('validLogin', str(success))
            break
        else:
            settings.openSettings()
    if not success:
        showErrorMessage("", language(30602))

def prepareCredentials():
    username = settings.getSetting('username')
    password = settings.getSetting('password')
    data = "username={username}&password={password}&submit=".format(username=username, password=password)
    return data


    # Shows a more user-friendly notification
def getData(url):       
    if settings.getSetting('cookie'):
        opener.addheaders.append(('Cookie', settings.getSetting('cookie')))
        response = opener.open(url)
        data = response.read()
        opener.close()
        login_urlfound = ''
        try:
            login_urlfound=re.findall(r'(href="/public/login/?)', data, re.DOTALL)
        except:
            pass
        if login_urlfound or 'error' in response.url or response.code  > 302:
            login()
        return data, response.url, response.code 
    else:
        login()
    pass
            
    

def showMessage(heading, message):
    xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s)' % (heading, message, msg_duration))

# Standardised error handler
def showErrorMessage(title="", result="", status=500):
    if title == "":
        title = language(30600)    # "Error"

    if result == "":
        showMessage(title, language(30601))   # "Unknown Error"
    else:
        showMessage(title, result)
            
def addDir(name,url,mode=2,iconimage='', cat="DefaultFolder.png"):
        print "IN ADD DIR"
        folder = True
        liz=xbmcgui.ListItem(name, iconImage=cat, thumbnailImage=iconimage)
        if mode != MODE_PLAY_VIDEO:
            url = urljoin(links['main'], url)
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        else:
            u = url+"&mode="+str(mode)
            liz.setProperty('IsPlayable', 'true')
            folder = False
        
        ok=True

        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok

def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


def PlayVimeo(video_id): # Ex: video_id=248894448
    uurl = 'plugin://plugin.video.vimeo/play/?video_id=%s' % video_id
    xbmc.executebuiltin("xbmc.PlayMedia(" + uurl + ")")

def PlayYoutube(url):
    uurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
    xbmc.executebuiltin("xbmc.PlayMedia(" + uurl + ")")

def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


params = get_params()
lastMode = None
lastUrl = ''

try:
    lastMode = int(params["mode"])
except:
    pass
try:
    lastUrl = urllib.unquote_plus(params["url"])
except:
    pass
#
# Controller Logic
print "Current URL: " + lastUrl

if lastMode is None:
    getRootCategories()

elif lastMode == MODE_LIST_TOPICS:
    listTopics(lastUrl)

elif lastMode == MODE_LIST_EPISODES:
    listEpisodes(lastUrl)

elif lastMode == MODE_LIST_CATEGORIES:
    listChannelsForCategory(channelName)

elif lastMode == MODE_EPISODE_DET:
    episodeDetails(lastUrl)

elif lastMode == MODE_PLAY_VIDEO:
    PlayVimeo(lastUrl)

elif lastMode == MODE_SHOW_SETTINGS:
    login()
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))