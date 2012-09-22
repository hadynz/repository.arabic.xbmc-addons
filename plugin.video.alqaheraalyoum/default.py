import urllib, urllib2, re, os, cookielib
import xbmcplugin, xbmcgui, xbmcaddon
from BeautifulSoup import BeautifulSoup
import sys

plugin = int(sys.argv[1])
settings = xbmcaddon.Addon(id='plugin.video.alqaheraalyoum')
language = settings.getLocalizedString
pluginPath = settings.getAddonInfo('path')

# Setting constants
MODE_CATEGORIES = 1
MODE_INDEX = 2
MODE_PLAYVIDEO = 3
MODE_NOVIDEOS = 4

QAHERA_NEW_VIDEOS_URL = "http://www.alqaheraalyoum.net/videos/newvideos.php"

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def getRootCategories():
    addDir("Today", QAHERA_NEW_VIDEOS_URL + "?d=today", MODE_CATEGORIES, "thumbnail_today.jpg")
    addDir("Yesterday", QAHERA_NEW_VIDEOS_URL + "?d=yesterday", MODE_CATEGORIES, "thumbnail_yesterday.jpg")
    addDir("This month", QAHERA_NEW_VIDEOS_URL + "?d=month", MODE_CATEGORIES, "thumbnail_thismonth.jpg")
    addDir("All time", QAHERA_NEW_VIDEOS_URL, MODE_CATEGORIES, "thumbnail_alltime.jpg")
    xbmcplugin.endOfDirectory(plugin)

class EpisodeClip():
    def __init__(self, el):
        self.thumbnail = el.find('img')['src']
        self.url = el.find('a')['href']
        self.name = el.findAll('td')[1].contents[0]

        # Using REGEX instead of .Replace - weird behaviour in some cases by latter
        p1 = re.compile(' hours')
        p2 = re.compile(' minutes')
        p3 = re.compile(' day')
        addedWhenContent = el.findAll('td')[3].contents[0]
        self.addedWhen = p1.sub('hrs', p2.sub('min', p3.sub('day', addedWhenContent)))

        dateRowContent = el.findAll('td')[2].find('a').contents[0]
        self.date = dateRowContent[dateRowContent.find('|') + 2:]

def extractYoutubeVid(url):
    if isinstance(url, str):
        url = [url]

    ret_list = []
    for item in url:
        item = item[item.find("v=") + 2:]
        if item.find("&") > -1:
            item = item[:item.find("&")]
        ret_list.append(item)

    return ret_list

def playVideo(thumbnailUrl):
    response = opener.open(thumbnailUrl)
    inner_data = response.read();
    opener.close()

    matchObj = re.search( r'file: \'(.*)\'', inner_data, re.M|re.I)
    url = matchObj.group(1)

    # If a youtube clip, need to play clip using the XBMC Youtube plugin
    if "youtube.com" in url:
        vid = extractYoutubeVid(url)[0]
        url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=%s" % vid

    listItem = xbmcgui.ListItem(path=url)
    return xbmcplugin.setResolvedUrl(plugin, True, listItem)

def getEpisodes(categoryUrl):
    response = opener.open(categoryUrl)
    inner_data = response.read();
    opener.close()

    soup = BeautifulSoup(inner_data)

    videoClipRowsElList = soup.find('div', { 'id': 'newvideos_results' }).findAll('tr', { 'class' : None })

    for rowEl in videoClipRowsElList:
        clip = EpisodeClip(rowEl)
        title = u'{2} | {0}'.format(clip.name, clip.date, clip.addedWhen)
        addLink(title, clip.url, MODE_PLAYVIDEO, clip.thumbnail, len(videoClipRowsElList))

    if not len(videoClipRowsElList):
        addLink("No videos have been uploaded for this category", "NOVIDEOS", MODE_NOVIDEOS, "", 1)

    xbmcplugin.endOfDirectory(plugin)

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

def addDir(name, url, mode, thumnail_filename):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode="+str(mode)

    fanart = os.path.join(pluginPath, 'fanart.jpg')
    thumbnail = os.path.join(pluginPath, 'art', thumnail_filename)

    li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    li.setInfo(type="Video", infoLabels={"Title":name})
    li.setProperty('fanart_image', fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, isFolder=True)
    return ok

def addLink(name, url, mode, iconImage, totalItems):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode)
    li = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconImage)
    li.setInfo(type="Video", infoLabels={"Title":name})
    li.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, totalItems=totalItems)
    return ok


params = get_params()
url = None
lastMode = None


try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    lastMode = int(params["mode"])
except:
    pass

if lastMode is None:
    getRootCategories()

elif lastMode == MODE_CATEGORIES:
    getEpisodes(url)

elif lastMode == MODE_PLAYVIDEO:
    playVideo(url)
