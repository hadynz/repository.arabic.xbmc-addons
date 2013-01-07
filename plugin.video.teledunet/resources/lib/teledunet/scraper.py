import cookielib
import re
import urllib2
from urllib2 import (urlopen, Request)
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup

BASE_URL = 'http://www.alqaheraalyoum.net/videos/newvideos.php'
TELEDUNET_URL = 'http://www.teledunet.com/'
TELEDUNET_TIMEPLAYER_URL = 'http://www.teledunet.com/tv/?stretching=none&file=rtmp://www.teledunet.com:1935/teledunet/%s'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def _url(path=''):
    """Returns a full url for the given path"""
    return urljoin(BASE_URL, path)

def get(url):
    """Performs a GET request for the given url and returns the response"""
    conn = urlopen(url)
    resp = conn.read()
    conn.close()
    return resp

def _html(url):
    """Downloads the resource at the given url and parses via BeautifulSoup"""
    return BeautifulSoup(get(url), convertEntities=BeautifulSoup.HTML_ENTITIES)

def _get_channel_time_player(channel_name):
    url = TELEDUNET_TIMEPLAYER_URL % channel_name
    req = Request(url)
    req.add_header('Referer', TELEDUNET_URL)    # Simulate request is coming from website
    html = get(req)

    m = re.search('time_player=(.*);', html, re.M | re.I)
    time_player_str = eval(m.group(1))

    return repr(time_player_str).rstrip('0').rstrip('.')

def get_rtmp_params(channel_name):
    time_player_id = _get_channel_time_player(channel_name)

    return {
        'rtmp_url': 'rtmp://www.teledunet.com:1935/teledunet',
        'playpath': channel_name,
        'app': 'teledunet',
        'swf_url': ('http://www.teledunet.com/tv/player.swf?'
                    'repeat=always&'
                    'autostart=true&'
                    'stretching_=none&'
                    'id0=%(time_player)s&'
                    'streamer=rtmp://www.teledunet.com:1935/teledunet&'
                    'file=%(channel_name)s&'
                    'provider=rtmp&skin=bekle/bekle.xml'
                   ) % {'time_player': time_player_id, 'channel_name': channel_name},
        'video_page_url': TELEDUNET_TIMEPLAYER_URL % channel_name,
        'swfVfy': 'true',
        'live': '1'
    }

def get_channels():
    html = _html(TELEDUNET_URL)

    items = []
    for li in html.find('ol').findAll('li'):
        onClickEl = li.find('a')['onclick']
        m = re.search('.*\'(.*)\'.*', onClickEl, re.M|re.I)
        channel_name = m.group(1)

        items.append({
            'thumbnail': TELEDUNET_URL + li.findAll('img')[1]['src'],
            'label': li.find('a').contents[1],
            'path': channel_name
        })

    return items