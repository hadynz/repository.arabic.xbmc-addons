import urllib, urllib2, re, os, cookielib
import xbmcplugin, xbmcgui, xbmcaddon
from BeautifulSoup import BeautifulSoup
import sys

thisPlugin = int(sys.argv[1])

# Setting constants
MODE_CATEGORIES = 1
MODE_INDEX = 2
MODE_PLAYVIDEO = 3
MODE_NOVIDEOS = 4

NUM_SOCKETS = 5
NUM_WORKERS = 8

QAHERA_NEW_VIDEOS_URL = "http://www.alqaheraalyoum.net/videos/newvideos.php"

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def getRootCategories():
    qaheraUrl = QAHERA_NEW_VIDEOS_URL
    addDir("Today", qaheraUrl + "?d=today", MODE_CATEGORIES)
    addDir("Yesterday", qaheraUrl + "?d=yesterday", MODE_CATEGORIES)
    addDir("This month", qaheraUrl + "?d=month", MODE_CATEGORIES)
    addDir("All time", qaheraUrl, MODE_CATEGORIES)
    xbmcplugin.endOfDirectory(thisPlugin)

class EpisodeClip():
    def __init__(self, el):
        self.thumbnail = el.find('img')['src']
        self.url = el.find('a')['href']
        self.name = el.findAll('td')[1].contents[0]

        addedWhenContent = el.findAll('td')[3].contents[0]
        self.addedWhen = addedWhenContent.replace(' hours,', 'hrs').replace(' minutes', 'min')

        dateRowContent = el.findAll('td')[2].find('a').contents[0]
        self.date = dateRowContent[dateRowContent.find('|') + 2:]

def playVideo(thumbnailUrl):
    response = opener.open(thumbnailUrl)
    inner_data = response.read();
    opener.close()

    matchObj = re.search( r'file: \'(.*)\'', inner_data, re.M|re.I)

    clipStreamingUrl = matchObj.group(1)
    listItem = xbmcgui.ListItem(path=clipStreamingUrl)
    return xbmcplugin.setResolvedUrl(thisPlugin, True, listItem)

def getEpisodes(categoryUrl):
    response = opener.open(categoryUrl)
    inner_data = response.read();
    opener.close()

    soup = BeautifulSoup(inner_data)

    videoClipRowsElList = soup.find('div', { 'id': 'newvideos_results' }).findAll('tr', { 'class' : None })

    for rowEl in videoClipRowsElList:
        clip = EpisodeClip(rowEl)
        title = u'{1} ({2}) | {0}'.format(clip.name, clip.date, clip.addedWhen)
        addLink(title, clip.url, MODE_PLAYVIDEO, clip.thumbnail, len(videoClipRowsElList))

    if not len(videoClipRowsElList):
        addLink("No videos have been uploaded for this category", "NOVIDEOS", MODE_NOVIDEOS, "", 1)

    xbmcplugin.endOfDirectory(thisPlugin)

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

def addDir(name, url, mode):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode="+str(mode)
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
    liz.setInfo(type="Video", infoLabels={"Title":name})
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

def addLink(name, url, mode, iconImage, totalItems):
    u = sys.argv[0] + "?url="+urllib.quote_plus(url) + "&mode=" + str(mode)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconImage)
    liz.setInfo(type="Video", infoLabels={"Title":name})
    liz.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, totalItems=totalItems)
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
