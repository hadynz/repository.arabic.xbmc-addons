import urllib, urllib2, re, cookielib
import xbmcplugin, xbmcgui, xbmcaddon
from BeautifulSoup import BeautifulSoup
import sys

thisPlugin = int(sys.argv[1])

# Setting constants
MODE_MOVIE_LISTING_PAGE = 1
MODE_PLAYVIDEO = 2
MODE_NOVIDEOS = 3

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

START_PAGINATION_INDEX = 1
MOVIES_URL = "http://www.sotwesoora.tv/categories"

def getRootCategories():
    addDir("Movies", MOVIES_URL, MODE_MOVIE_LISTING_PAGE, 1)
    xbmcplugin.endOfDirectory(thisPlugin)


class VideoClipRow():
    def __init__(self, el):
        imgEl = el.find('img')
        self.thumbnail = imgEl['src']
        self.name = imgEl['alt']
        self.url = el.find('a')['href'].encode('utf-8')

def playVideo(thumbnailUrl):
    m = re.search('.*\/(\d+)\/.*', thumbnailUrl, re.M|re.I)
    videoID = m.group(1)
    playerConfigUrl = 'http://www.sotwesoora.tv/flv_player/data/playerConfig/{0}.xml'.format(videoID)

    response = opener.open(playerConfigUrl)
    html_data = response.read()
    opener.close()

    soup = BeautifulSoup(html_data)
    clipStreamingUrl = soup.find('video')['sd']

    listItem = xbmcgui.ListItem(path=clipStreamingUrl)
    return xbmcplugin.setResolvedUrl(thisPlugin, True, listItem)

def getMovieLinks(websiteUrl, currentIndex):
    response = opener.open(websiteUrl)
    inner_data = response.read();
    opener.close()

    soup = BeautifulSoup(inner_data)

    boxRowElList = soup.findAll('div', {'class': 'box'})
    resultsCount = len(boxRowElList)

    for boxRowEl in boxRowElList:
        clip = VideoClipRow(boxRowEl)
        addLink(clip.name, clip.url, MODE_PLAYVIDEO, clip.thumbnail, resultsCount)

    addDir("Next Page >>", MOVIES_URL, MODE_MOVIE_LISTING_PAGE, currentIndex + 1)

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

def addDir(name, url, mode, pageIndex):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url + "&p=" + str(pageIndex)) + "&mode=" + str(mode) + "&pageindex=" + str(pageIndex)
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

def addLink(name, url, mode, iconImage, totalItems):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode)
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconImage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, totalItems=totalItems)
    return ok

params = get_params()
url = None
lastMode = None
pageIndex = 1

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    lastMode = int(params["mode"])
except:
    pass
try:
    pageIndex = int(params["pagendex"])
except:
    pass

if lastMode is None:
    getRootCategories()

elif lastMode == MODE_MOVIE_LISTING_PAGE:
    getMovieLinks(url, pageIndex)

elif lastMode == MODE_PLAYVIDEO:
    playVideo(url)
