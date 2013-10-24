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
    print html

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
    channels from an offline HTML fallback file
    Hady: Unsure in what scenario is this useful given that RTMP stream might also be down as well?!
    '''
    if not items:
        path = os.path.join(os.path.dirname(__file__), HTML_FALLBACK)
        html = BeautifulSoup(''.join(open(path).readlines()), convertEntities=BeautifulSoup.HTML_ENTITIES)
        items = _parse_channels_from_html_dom(html)

    return items


def _parse_channels_from_html_dom(html):
    items = []

    for div in html.findAll("div", {"class": "div_channel"}):
        match2=re.compile('''onclick="go_c2.?'(.+?)'.+?'rtmp.+?style=".+?<img onerror=".+?" src="(.+?)" height=.+? style=.+?><font style=".+?"> <span id=.+?">(.+?)</span>.+?<font style=".+?">(.+?)</font>''').findall(str(div))
        match=re.compile('''onclick="go_c2.?'(.+?)'.+?'rtmp.+?style=".+?<img onerror=".+?" src="(.+?)" height=.+? style=.+?><font style=".+?"> <span id=.+?">(.+?)</span>''').findall(str(div))
        for url,thumb,name in match:
            for url2,thumb2,name2,hd in match2:
                if name==name2:
                    name=name+' [COLOR red]HD[/COLOR]'
        items.append({
            'title': name,
            'thumbnail': thumb,
            'path': url
        })
    items.append({
            'title': 'MBC',
            'thumbnail': 'https://si0.twimg.com/profile_images/1133033554/mbc-fb.JPG',
            'path': 'mbc_1'})
    items.append({
            'title': 'JSC +1',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_1'})
    items.append({
            'title': 'JSC +2',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_2'})
    items.append({
            'title': 'JSC +3',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_3'})
    items.append({
            'title': 'JSC +4',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_4'})
    items.append({
            'title': 'JSC +5',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_5'})
    items.append({
            'title': 'JSC +6',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_6'})
    items.append({
            'title': 'JSC +7',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_7'})
    items.append({
            'title': 'JSC +8',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_8'})
    items.append({
            'title': 'JSC +9',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_9'})
    items.append({
            'title': 'JSC +10',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_10'})
    items.append({
            'title': 'Abu Dhabi Al Oula',
            'thumbnail': 'https://www.zawya.com/pr/images/2009/ADTV_One_RGB_2009_10_08.jpg',
            'path': 'abu_dhabi'})
    items.append({
            'title': 'Abu Dhabi Sports',
            'thumbnail': 'https://si0.twimg.com/profile_images/2485587448/2121.png',
            'path': 'abu_dhabi_sports_1'})
    items.append({
            'title': 'Al Jazeera',
            'thumbnail': 'http://www.chicagonow.com/chicago-sports-media-watch/files/2013/04/Al-Jazeera.jpg',
            'path': 'aljazeera'})
    items.append({
            'title': 'Al Jazeera Sport 1',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'aljazeera_sport_1'})
    items.append({
            'title': 'Al Jazeera Sport 2',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'aljazeera_sport_2'})
    items.append({
            'title': 'Al Jazeera Mubasher Masr',
            'thumbnail': 'http://www.chicagonow.com/chicago-sports-media-watch/files/2013/04/Al-Jazeera.jpg',
            'path': 'aljazeera_mubasher_masr'})
    items.append({
            'title': 'ART Aflam 2',
            'thumbnail': 'http://www.invision.com.sa/en/sites/default/files/imagecache/216x216/channels/2011/10/11/1138.jpg',
            'path': 'art_aflam_2'})
    items.append({
            'title': 'Al Jazeera Children',
            'thumbnail': 'http://www.chicagonow.com/chicago-sports-media-watch/files/2013/04/Al-Jazeera.jpg',
            'path': 'aljazeera_children'})
    items.append({
            'title': 'ART Cinema',
            'thumbnail': 'http://www.lyngsat-logo.com/hires/aa/art_cinema.png',
            'path': 'art_aflam_1'})
    items.append({
            'title': 'Cartoon Network',
            'thumbnail': 'http://upload.wikimedia.org/wikipedia/commons/b/bb/Cartoon_Network_Arabic_logo.png',
            'path': 'cartoon_network'})
    return items
