# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin
import urllib2, urllib, cgi, re
import HTMLParser
import xbmcaddon
import traceback
import os
import sys
import json

addon_id = 'plugin.video.albernameg'
__settings__ = xbmcaddon.Addon(id=addon_id)
__addonname__ = __settings__.getAddonInfo('name')
__icon__ = __settings__.getAddonInfo('icon')
__fanart__ = __settings__.getAddonInfo('fanart')

selfAddon = xbmcaddon.Addon(id=addon_id)
addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonArt = os.path.join(addonPath, 'resources/images')
communityStreamPath = os.path.join(addonPath, 'resources/community')

mainurl = 'http://www.albernameg.com/'
apikey = 'AIzaSyBI4me7Tk-7MU5AwLEXUqJXoB24TvUtRcU'




def addDir(name, url, mode, iconimage, showContext=False, isItFolder=True, pageNumber="", isHTML=True,
           addIconForPlaylist=False):
    #	print name
    #	name=name.decode('utf-8','replace')
    if isHTML:
        h = HTMLParser.HTMLParser()
        name = h.unescape(name).decode("utf-8")
        rname = name.encode("utf-8")
    else:
        #h = HTMLParser.HTMLParser()
        #name =h.unescape(name).decode("utf-8")
        rname = name.encode("utf-8")
    #		url=  url.encode("utf-8")
    #	url= url.encode('ascii','ignore')
    #print rname
    #print iconimage
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(rname)
    if len(pageNumber):
        u += "&pagenum=" + pageNumber
    if addIconForPlaylist:
        u += "&addIconForPlaylist=yes"
    ok = True
    #	print iconimage
    liz = xbmcgui.ListItem(rname, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    #liz.setInfo( type="Video", infoLabels={ "Title": name } )
    if showContext == True:
        cmd1 = "XBMC.RunPlugin(%s&cdnType=%s)" % (u, "l3")
        cmd2 = "XBMC.RunPlugin(%s&cdnType=%s)" % (u, "xdn")
        cmd3 = "XBMC.RunPlugin(%s&cdnType=%s)" % (u, "ak")
        liz.addContextMenuItems(
            [('Play using L3 Cdn', cmd1), ('Play using XDN Cdn', cmd2), ('Play using AK Cdn', cmd3)])

    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isItFolder)
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




def PlayYoutube(url):
    uurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
    xbmc.executebuiltin("xbmc.PlayMedia(" + uurl + ")")


def AddYoutubePlaylists(channelId):
    print 'in AddYoutubePlaylists(channelId)'
    #if not username.startswith('https://www.googleapis'):
    #	channelId=getChannelIdByUserName(username)#passusername
    #else:
    #	channelId=username
    #channelId=username
    playlists, next_page = getYouTubePlayList(channelId);
    for playList in playlists:
        print playList
        addDir(playList[0], playList[1], 3, playList[2], isItFolder=True, isHTML=False)  #name,url,mode,icon
    if next_page:
        addDir('Next', next_page, 2, addonArt + '/next.png', isItFolder=True)  #name,url,mode,icon


def getYouTubePlayList(channelId):
    print 'in getYouTubePlayList(channelId)'
    if not channelId.startswith('https://www.googleapis'):
        u_url = 'https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=%s&maxResults=50&key=%s' % (
            channelId, apikey)
    else:
        u_url = channelId
    doc = getJson(u_url)
    ret = []
    for playlist_item in doc['items']:
        title = playlist_item["snippet"]["title"]
        id = playlist_item["id"]
        if not title == 'Private video' and type(title) != type(object) and str(title.encode('utf8', 'ignore')).__contains__('كامل'):
            imgurl = ''
            try:
                imgurl = playlist_item["snippet"]["thumbnails"]["high"]["url"]
            except:
                pass
            if imgurl == '':
                try:
                    imgurl = playlist_item["snippet"]["thumbnails"]["default"]["url"]
                except:
                    pass
            ret.append([title, id, imgurl])
    nextItem = None
    if 'nextPageToken' in doc:
        nextItem = doc["nextPageToken"]
    else:
        nextItem = None

    nextUrl = None
    if nextItem:
        if not '&pageToken' in u_url:
            nextUrl = u_url + '&pageToken=' + nextItem
        else:
            nextUrl = u_url.split('&pageToken=')[0] + '&pageToken=' + nextItem

    return ret, nextUrl;


def AddYoutubeVideosByPlaylist(playListId, AddPlayListIcon=False, channelid=None):
    print 'AddYoutube', url
    videos, next_page = getYoutubeVideosByPlaylist(playListId);
    if AddPlayListIcon:
        addDir('Playists', channelid, 2, addonArt + '/playlist.png', isHTML=False)

    for video in videos:
        #print chName
        print video
        addDir(video[0], video[1], 1, video[2], isItFolder=False, isHTML=False)  #name,url,mode,icon
    if next_page:
        addDir('Next', next_page, 3, addonArt + '/next.png', isItFolder=True)  #name,url,mode,icon


def getJson(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    response = urllib2.urlopen(req)
    #link=response.read()
    #response.close()
    decoded = json.load(response)
    return decoded


def getChannelIdByUserName(username):
    u_url = 'https://www.googleapis.com/youtube/v3/channels?part=id&forUsername=%s&key=%s' % (username, apikey)
    channelData = getJson(u_url)
    return channelData['items'][0]['id']


def getYoutubeVideosByPlaylist(playlistId):
    if playlistId.startswith('https://www'):
        #nextpage
        u_url = playlistId
    else:
        u_url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=%s&key=%s' % (
            playlistId, apikey)
    videos = getJson(u_url)
    return prepareYoutubeVideoItems(videos, u_url)


def prepareYoutubeVideoItems(videos, urlUsed):
    print 'urlUsed', urlUsed
    if 'nextPageToken' in videos:
        nextItem = videos["nextPageToken"]
    else:
        nextItem = None
    ret = []
    for playlist_item in videos["items"]:
        title = playlist_item["snippet"]["title"]
        print 'urlUsed', urlUsed
        if not 'search?part=snippet' in urlUsed:
            video_id = playlist_item["snippet"]["resourceId"]["videoId"]
        else:
            video_id = playlist_item["id"]["videoId"]
        if not title == 'Private video':
            imgurl = ''
            try:
                imgurl = playlist_item["snippet"]["thumbnails"]["high"]["url"]
            except:
                pass
            if imgurl == '':
                try:
                    imgurl = playlist_item["snippet"]["thumbnails"]["default"]["url"]
                except:
                    pass
            #print "%s (%s)" % (title, video_id)
            ret.append([title, video_id, imgurl])
    nextUrl = None
    if nextItem:
        if not '&pageToken' in urlUsed:
            nextUrl = urlUsed + '&pageToken=' + nextItem
        else:
            nextUrl = urlUsed.split('&pageToken=')[0] + '&pageToken=' + nextItem
    return ret, nextUrl;

#print "i am here"
params = get_params()
url = None
name = None
mode = None
linkType = None
pageNumber = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass

try:
    pageNumber = params["pagenum"]
except:
    pageNumber = "";

args = cgi.parse_qs(sys.argv[2][1:])
cdnType = ''
try:
    cdnType = args.get('cdnType', '')[0]
except:
    pass

addIconForPlaylist = ""
try:
    addIconForPlaylist = args.get('addIconForPlaylist', '')[0]
except:
    pass

print    mode, pageNumber

try:
    if mode == None or url == None or len(url) < 1:
        print "Entered Get channel and add playlists"
        chId = getChannelIdByUserName('albernameg')
        AddYoutubePlaylists(chId)
    elif mode == 1:  #add communutycats
        print "play youtube url is " + url, mode
        PlayYoutube(url);
    elif mode == 2:  #add communutycats
        print "play youtube url is " + url, mode
        AddYoutubePlaylists(url);
    elif mode == 3:  #add communutycats
        print "play youtube url is " + url, mode
        AddYoutubeVideosByPlaylist(url);
except:
    print 'somethingwrong'
    traceback.print_exc(file=sys.stdout)


xbmcplugin.endOfDirectory(int(sys.argv[1]))

