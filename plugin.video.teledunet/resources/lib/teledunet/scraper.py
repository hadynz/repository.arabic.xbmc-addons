import cookielib
import re
import urllib2
import os.path
from urllib2 import (urlopen, Request)
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup

TELEDUNET_URL = 'http://www.teledunet.com/'
TELEDUNET_TIMEPLAYER_URL = 'http://www.teledunet.com/tv/?channel=%s&no_pub'
HTML_FALLBACK = 'htmlfallback.html'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def _url(path=''):
    """Returns a full url for the given path"""
    return urljoin(BASE_URL, path)


def get(url):
    """Performs a GET request for the given url and returns the response"""
    try:
        conn = urlopen(url)
        resp = conn.read()
        conn.close()
        return resp
    except IOError:
        pass
    return ""


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
    

    m = re.search('curent_media=\'(.*)\';', html, re.M | re.I)
    rtmp_url = m.group(1)
    play_path= rtmp_url[rtmp_url.rfind("/")+1:] 
    return rtmp_url, play_path, repr(time_player_str).rstrip('0').rstrip('.')


def get_rtmp_params(channel_name):
    rtmp_url, play_path, time_player_id = _get_channel_time_player(channel_name)

    return {
        'rtmp_url': rtmp_url,
        'playpath': play_path,
        'app': 'teledunet',
        'swf_url': ('http://www.teledunet.com/tv/player.swf?'
                    'bufferlength=5&'
                    'repeat=single&'
                    'autostart=true&'
                    'id0=%(time_player)s&'
                    'streamer=%(rtmp_url)s&'
                    'file=%(channel_name)s&'
                    'provider=rtmp'
                       ) % {'time_player': time_player_id, 'channel_name': play_path, 'rtmp_url': rtmp_url},
        'video_page_url': 'http://www.teledunet.com/tv/?channel=%s&no_pub' % play_path,
        'live': '1'
    }


def get_channels():
    html = _html(TELEDUNET_URL)
    items = _parse_channels_from_html_dom(html)

    '''
    If no channels are returned from Teledunet service, fall back to returning
    channels from an offline HTML fallback file.
    '''
    if not items:
        path = os.path.join(os.path.dirname(__file__), HTML_FALLBACK)
        html = BeautifulSoup(''.join(open(path).readlines()), convertEntities=BeautifulSoup.HTML_ENTITIES)
        items = _parse_channels_from_html_dom(html)

    return items


def _parse_channels_from_html_dom(html):
    items = []

    for div in html.findAll("div", {"class": "div_channel"}):
        is_working = '#009900' in div['style']
        is_hd = '#0099ff' in div['style']
        if is_working:
           label_pattern = '[COLOR green]%s[/COLOR]'
        elif is_hd:
           label_pattern = '[COLOR blue]%s   [/COLOR][COLOR red]HD[/COLOR]'
        else:
           label_pattern = '%s'
        path = re.sub('^.*\=', '', div.findAll('a')[1]['href'])
        items.append({
            'title': label_pattern % div.find('span').contents[0],
            'thumbnail': div.findAll('img')[0]['src'],
            'path': path
        })

    return items