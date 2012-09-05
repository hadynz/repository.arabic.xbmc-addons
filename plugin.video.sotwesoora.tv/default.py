import urllib, urllib2, re, cookielib
import xbmcplugin, xbmcgui, xbmcaddon
from BeautifulSoup import BeautifulSoup
import sys

thisPlugin = int(sys.argv[1])

# Setting constants
MODE_GOTO_MOVIE_CATEGORIES = 1
MODE_GOTO_MOVIE_LISTINGS = 2
MODE_PLAYVIDEO = 3
MODE_NOVIDEOS = 4

LISTING_MOST_RECENT = "mr";
LISTING_MOST_VIEWED = "mv";
LISTING_TOP_RATED = "tr";
LISTING_RECENTLY_FEATURED = "rf";
LISTING_RECENTLY_VIEWED = "rv";
LISTING_RANDOM = "ran";

URL_PATTERN_MOVIES = "http://www.sotwesoora.tv/categories&cid=1&c=Movies&lo=detailed&s={listingType}&t=a&p={pageNo}"
URL_PATTERN_XML_CONFIG = "http://www.sotwesoora.tv/flv_player/data/playerConfig/{videoId}.xml"

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

class VideoClipRow():
    def __init__(self, el):
        imgEl = el.find('img')
        self.thumbnail = imgEl['src']
        self.name = imgEl['alt']
        self.url = el.find('a')['href'].encode('utf-8')

def getRootCategories():
    addDir("Movies", MODE_GOTO_MOVIE_CATEGORIES)
    xbmcplugin.endOfDirectory(thisPlugin)

def getMovieCategories():
    addDir("Recently Featured", MODE_GOTO_MOVIE_LISTINGS, LISTING_RECENTLY_FEATURED)
    addDir("Recently Viewed", MODE_GOTO_MOVIE_LISTINGS, LISTING_RECENTLY_VIEWED)
    addDir("Most Recent", MODE_GOTO_MOVIE_LISTINGS, LISTING_MOST_RECENT)
    addDir("Most Viewed", MODE_GOTO_MOVIE_LISTINGS, LISTING_MOST_VIEWED)
    addDir("Top Rated", MODE_GOTO_MOVIE_LISTINGS, LISTING_TOP_RATED)
    addDir("Random", MODE_GOTO_MOVIE_LISTINGS, LISTING_RANDOM)
    xbmcplugin.endOfDirectory(thisPlugin)

def getMovieLinks(listingType, pageNo):
    pageUrl = URL_PATTERN_MOVIES.format(listingType=listingType, pageNo=pageNo)

    response = opener.open(pageUrl)
    inner_data = response.read();
    opener.close()

    soup = BeautifulSoup(inner_data)

    boxRowElList = soup.findAll('div', {'class': 'box'})
    resultsCount = len(boxRowElList)

    for boxRowEl in boxRowElList:
        clip = VideoClipRow(boxRowEl)
        addLink(clip.name, clip.url, MODE_PLAYVIDEO, clip.thumbnail, resultsCount)

    addDir("Next Page >>", MODE_GOTO_MOVIE_LISTINGS, listingType, pageNo + 1)

    xbmcplugin.endOfDirectory(thisPlugin)

def playVideo(thumbnailUrl):
    m = re.search('.*\/(\d+)\/.*', thumbnailUrl, re.M|re.I)
    videoId = m.group(1)
    playerConfigUrl = URL_PATTERN_XML_CONFIG.format(videoId=videoId)

    response = opener.open(playerConfigUrl)
    html_data = response.read()
    opener.close()

    soup = BeautifulSoup(html_data)
    clipStreamingUrl = soup.find('video')['sd']

    listItem = xbmcgui.ListItem(path=clipStreamingUrl)
    return xbmcplugin.setResolvedUrl(thisPlugin, True, listItem)

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

def addDir(name, mode, listingType=None, pageIndex=None):
    u = sys.argv[0] + "?mode=" + str(mode) + "&listingType=" + str(listingType) + "&pageIndex=" + str(pageIndex)
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
listingType = None
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
    listingType = params["listingType"]
except:
    pass
try:
    pageIndex = int(params["pageIndex"])
except:
    pass

if lastMode is None:
    getRootCategories()

elif lastMode == MODE_GOTO_MOVIE_CATEGORIES:
    getMovieCategories()

elif lastMode == MODE_GOTO_MOVIE_LISTINGS:
    getMovieLinks(listingType, pageIndex)

elif lastMode == MODE_PLAYVIDEO:
    playVideo(url)
