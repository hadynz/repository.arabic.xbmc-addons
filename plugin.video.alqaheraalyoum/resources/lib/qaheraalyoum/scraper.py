import re
from urllib2 import urlopen
from urlparse import urljoin
from utils import get_redirect_flv_stream_url
from BeautifulSoup import BeautifulSoup

BASE_URL = 'http://www.alqaheraalyoum.net/videos/newvideos.php'

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

def get_stream_url(clip_url):

    # A simple rename in the clip URL can usually correctly map to the
    # correct streaming URL. Check URL after correction and return if positive
    streamUrl = re.sub('playvideo.php', 'videos.php', clip_url)
    flvUrl = get_redirect_flv_stream_url(streamUrl)

    if not flvUrl is '':
        return flvUrl

    # Do an expensive fetch to the clip's page, and extract stream link from there
    html = get(clip_url)
    matchObj = re.search( r'file: \'(.*)\'', html, re.M|re.I)
    return matchObj.group(1)

def get_clips():
    """Returns a list of subjects for the website. Each subject is a dict with keys of 'name' and 'url'."""
    url = _url()
    html = _html(url)

    clips = html.find('div', { 'id': 'newvideos_results' }).findAll('tr', { 'class' : None })
    return [_get_clip(clip) for clip in clips]

def _get_clip(el):
    return {
        'thumbnail': el.find('img')['src'],
        'url': el.find('a')['href'],
        'name': el.findAll('td')[1].contents[0],
        'addedWhen': el.findAll('td')[3].contents[0],
        'date': el.findAll('td')[2].find('a').contents[0]
    }