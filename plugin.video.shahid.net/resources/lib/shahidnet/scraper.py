import json
import re
from urllib2 import (urlopen )
from BeautifulSoup import BeautifulSoup

API_KEY = '4cd216240b9e47c3d97450b9b4866d3f'

URL_CHANNEL_LIST = "http://shahid.mbc.net/api/channelList?api_key={apiKey}&offset=0&limit=60"
URL_PROGRAMS_LIST = "http://shahid.mbc.net/api/programsList?api_key={apiKey}&offset=0&limit=60&channel_id={channelID}"
URL_MEDIA_LIST = "http://shahid.mbc.net/api/mediaList?api_key={apiKey}&offset=0&limit=60&program_id={programID}&sub_type={mediaType}"
URL_MEDIA_INFO = "http://shahid.mbc.net/api/mediaInfoList?api_key={apiKey}&media_id={mediaID}&offset=0&limit=60&program_id={programID}&sub_type={mediaType}"

URL_MEDIA_STREAM = "http://hadynz-shahid.appspot.com/scrape?m={mediaHash}"

def get(url):
    """Performs a GET request for the given url and returns the response"""
    conn = urlopen(url)
    resp = conn.read()
    conn.close()
    return resp


def _html(url):
    """Downloads the resource at the given url and parses via BeautifulSoup"""
    return BeautifulSoup(get(url), convertEntities=BeautifulSoup.HTML_ENTITIES)


def _json(url):
    print 'Fetching JSON from: ' + url
    response = get(url).decode("utf-8-sig")
    return json.loads(response)


def get_channels():
    response = _json(URL_CHANNEL_LIST.format(apiKey=API_KEY))
    return response['channels']

def get_channel_programs(channelID):
    response = _json(URL_PROGRAMS_LIST.format(apiKey=API_KEY, channelID=channelID))
    return response['programs']

def get_program_media(programID, mediaType):
    response = _json(URL_MEDIA_LIST.format(apiKey=API_KEY, programID=programID, mediaType=mediaType))
    return response['media']

def _get_media_info(programID, mediaType, mediaID):
    response = _json(URL_MEDIA_INFO.format(apiKey=API_KEY, programID=programID, mediaType=mediaType, mediaID=mediaID))
    return response['media']

def _get_media_id_hash(programID, mediaType, mediaID):
    mediaInfo = _get_media_info(programID, mediaType, mediaID)
    mediaUrl = mediaInfo['media_url']

    try:
        matchObj = re.search(r'media\/(.*)\.m3u8', mediaUrl, re.M|re.I)
        mediaHash = matchObj.group(1)

        return mediaHash

    except Exception as ex:
        print 'Error parsing media hash from media url: %s' % ex

    return None

def get_media_stream(quality, programID, mediaType, mediaID):
    mediaHash = _get_media_id_hash(programID, mediaType, mediaID)
    streams = _json(URL_MEDIA_STREAM.format(apiKey=API_KEY, mediaHash=mediaHash))

    for stream in streams:
        if quality == stream['Quality']:
            return stream['URL']

    return None

def debug():
    for program in get_channel_programs('8'):
        print program['mobile_image_url'] + ' id=' + program['id'] + ' clip_count=' + program['clip_count'] + ' episode_count=' +  program['episode_count'] + ' item_type=' + program['item_type']

    for media in get_program_media('1559', 'episodes'):
        print media

    print get_media_stream('360p LOW', '1559', 'episodes', '53899')


# debug()


