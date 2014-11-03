import cookielib
import re
import urllib2,urllib
from BeautifulSoup import BeautifulSoup
from models import ChannelItem
from hardcode import HARDCODED_STREAMS
import xbmcaddon
#addon_id = 'plugin.video.shahidmbcnet'
selfAddon = xbmcaddon.Addon()

#HEADER_REFERER = 'http://www.teledunet.com/'
#HEADER_REFERER = 'http://www.teledunet.com/list_chaines.php'
HEADER_REFERER = 'http://www.teledunet.com/'
TELEDUNET_CHANNEL_PAGE = 'http://www.teledunet.com/mobile/?con'

HEADER_HOST = 'www.teledunet.com'
HEADER_USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
TELEDUNET_TIMEPLAYER_URL = 'http://www.teledunet.com/mobile/?con'
PPV_CHANNEL_URL='rtmp://5.135.134.110:1935/teledunet/'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))


def _get(request,post=None):
    """Performs a GET request for the given url and returns the response"""
    return opener.open(request,post).read()

def _html(url, rheaders=None):
    """Downloads the resource at the given url and parses via BeautifulSoup"""
    headers = { "User-Agent": HEADER_USER_AGENT  }
    if rheaders:
        headers.update(rheaders);
    request = urllib2.Request (url , headers = headers)
    return BeautifulSoup(_get(request), convertEntities=BeautifulSoup.HTML_ENTITIES)


def __get_cookie_session():
    # Fetch the main Teledunet website to be given a Session ID
    _html('http://www.teledunet.com/')

    for cookie in cj:
        if cookie.name == 'PHPSESSID':
            return 'PHPSESSID=%s' % cookie.value

    raise Exception('Cannot find PHP session from Teledunet')

def performLogin():
    print 'performing login'
    userName=selfAddon.getSetting( "teledunetTvLogin" )
    password=selfAddon.getSetting( "teledunetTvPassword" )
    req = urllib2.Request('http://www.teledunet.com/boutique/connexion.php')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    post={'login_user':userName,'pass_user':password}
    post = urllib.urlencode(post)
    link = _get(req,post)

    req = urllib2.Request('http://www.teledunet.com/')#access main page too
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    _get(req,post)


def __get_channel_time_player(channel_name):
    loginname=selfAddon.getSetting( "teledunetTvLogin" )
    
    if not (loginname==None or loginname==""):
        performLogin()
        
    url = TELEDUNET_TIMEPLAYER_URL# % channel_name
    print url
    # Set custom header parameters to simulate request is coming from website
    req = urllib2.Request(url)
    req.add_header('Referer', HEADER_REFERER)
    req.add_header('Host', HEADER_HOST)
    req.add_header('User-agent', HEADER_USER_AGENT)
    req.add_header('Cookie', __get_cookie_session())

    html = _get(req)
    #m = re.search('aut=\'\?id0=(.*?)\'', html, re.M | re.I)
    #time_player_str = eval(m.group(1))
    match =re.findall('aut=\'\?id0=(.*?)\'', html)
    time_player_str=str(long(float(match[0])))
    
    #print 'set_favoris\(\''+channel_name+'\'.*?rtmp://(.*?)\''
    m = re.search('rtmp://(.*?)/%s\''%channel_name, html, re.M | re.I)
    if  m ==None:
        print 'geting from backup file'
        req = urllib2.Request("http://www.pastebin.com/download.php?i=fKh4gG5s")
        html = _get(req)
        m = re.search('rtmp://(.*?)/%s\''%channel_name, html, re.M | re.I)

    if  m ==None:
        rtmp_url=PPV_CHANNEL_URL+channel_name        
    else:
        rtmp_url = m.group(1)
        rtmp_url='rtmp://%s/%s'%(rtmp_url,channel_name)
    play_path = rtmp_url[rtmp_url.rfind("/") + 1:]
    return rtmp_url, play_path,time_player_str# repr(time_player_str).rstrip('0').rstrip('.')


def get_rtmp_params(channel_name):
    rtmp_url, play_path, time_player_id = __get_channel_time_player(channel_name)

    return {
        'rtmp_url': rtmp_url,
        'playpath': play_path,
        'app': 'teledunet',
        'swf_url': ('http://www.teledunet.com/mobile/player.swf?'
                    'id0=%(time_player)s&channel=%(channel_name)s'
                   ) % {'time_player': str(time_player_id), 'channel_name': channel_name, 'rtmp_url': rtmp_url},
        'video_page_url': 'http://www.teledunet.com/mobile/ flashVer=WIN\\2014,0,0,145 swfVfy=true  timeout=20',
        'live': '1'
    }

def get_channels():
    loginname=selfAddon.getSetting( "teledunetTvLogin" )

    _html(HEADER_REFERER)

    headers = { "Referer": HEADER_REFERER  }
    html = _html(TELEDUNET_CHANNEL_PAGE,headers)
#    channel_divs = lambda soup : soup.findAll("div", { "class" : re.compile("div_channel") })
    #print html
    channel_divs = lambda soup : soup.findAll("tr")
    #print channel_divs
    channels = [ChannelItem(el=el) for el in channel_divs(html)]

    # Extend Teledunet list with custom hardcoded list created by community
    channels.extend(__get_hardcoded_streams())
    return channels


def __get_hardcoded_streams():
    return [ChannelItem(json=json) for json in HARDCODED_STREAMS]


def debug():
    print len(get_channels())
    #print __get_channel_time_player('2m')
    #print get_rtmp_params('2m')
    pass


if __name__ == '__main__':
    debug()