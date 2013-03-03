from urllib2 import (urlopen )
from BeautifulSoup import BeautifulSoup
import re
from datetime import datetime, timedelta
from time import mktime, strptime

SCRAPE_SOURCE_URL = 'http://dailytube4u.com/%s'

def get(url):
    """Performs a GET request for the given url and returns the response"""
    conn = urlopen(url)
    resp = conn.read()
    conn.close()
    return resp

def _html(url):
    """Downloads the resource at the given url and parses via BeautifulSoup"""
    return BeautifulSoup(get(url), convertEntities=BeautifulSoup.HTML_ENTITIES)

def get_clips_for_show(show_path):

    # Workaround the HTML being malformed were an anchor tag has an attribute
    # that contains quotes in them e.g. <a title="Something \"in\" quotes" ..>...</a>
    content = get(SCRAPE_SOURCE_URL % show_path)
    content = content.replace("\\\"", "")
    html = BeautifulSoup(content, convertEntities=BeautifulSoup.HTML_ENTITIES)

    #html = _html(SCRAPE_SOURCE_URL % show_path)

    items = []

    for clipEl in html.find('div', { 'class' : 'maincharts' }).findAll('div', {'class' : re.compile(r'\bvideoBox\b')}):

        timespan = clipEl.find('span', { 'class' : 'timestamp' }).contents[0]

        try:
            h, m, s = map(int, timespan.split(':'))
        except :
            h = 0
            m, s = map(int, timespan.split(':'))

        duration = timedelta(hours=h, minutes=m, seconds=s)
        duration_min = duration.seconds / 60 # convert datetime to minutes

        thumbnail = clipEl.find('img')['data-src']
        title = clipEl.find('a', { 'class' : 'videotitlelink'})['title']

        # Extract youtube vid from thumbnail
        #   Wrap vid extraction in try/catch because a minority of clips use
        #   Dailymotion as a service; we are happy to ignore those at the moment
        try:
            matchObj = re.search( r'.*img.youtube.com\/vi\/(.*)/.*', thumbnail, re.M|re.I)
            video_id = matchObj.group(1)
            link = video_id

            items.append({
                'label': _parse_title(title),
                'path' : link,
                'thumbnail' : thumbnail,
                'info' : {
                    'duration' : str(duration_min)
                },
                'is_playable' : True
            })

        except Exception as ex:
            print 'Error parsing clip title and link: %s' % ex

    return items

def get_channels():
    html = _html(SCRAPE_SOURCE_URL % '')

    items = []

    for anchorEl in html.find('ul', { 'role' : 'menu' }).findAll('a'):
        items.append({
            'label': anchorEl.contents[0],
            'path' : anchorEl['href']
        })

    return items

def _parse_title(raw_title):

    try:
        # Handle Al-Qahera-Al-Youm title format
        # e.g. '2-27-02-2013 ....'
        m = re.search('(.*) ([0-9]{4}-[0-9][0-9]?-[0-9][0-9]?)-([1-9])', raw_title.encode('utf-8'), re.M|re.I)
        if m:
            title = m.group(1)
            release_date = _strptime(m.group(2))
            part = m.group(3)

            return '[[COLOR blue]Part %s[/COLOR], %s] %s ' % (part, release_date.strftime('%a %b %e'), title)

        # Handle Ibrahim Eisa, Huna Al Qahera tile format
        # e.g. '27-2-2013 ...'
        m = re.search('(.*) ([0-9]{4}-[0-9][0-9]?-[0-9][0-9]?)', raw_title.encode('utf-8'), re.M|re.I)
        if m:
            title = m.group(1)
            release_date = _strptime(m.group(2))

            return '[%s] %s ' % (release_date.strftime('%a %b %e'), title)

    except Exception as ex:
        print 'Error parsing clip title: %s' % ex

    # General cleanup
    # Replace \' with '
    return raw_title.replace("\\'", "'")

def _strptime(date_string, format='%Y-%m-%d'):
    timestamp = mktime(strptime(date_string, format))
    return datetime.fromtimestamp(timestamp)
