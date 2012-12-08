import sys
import cookielib
import json
import re
import urllib2
from BeautifulSoup import BeautifulSoup

class ModelChannel:
    def __init__(self, channelEl):
        self.id = channelEl.get('id')
        self.image_thumb = channelEl.get('thumb_url')
        self.image_fanart = channelEl.get('image_url')
        self.media_count = channelEl.get('media_count')
        self.name = channelEl.get('name').strip()
        self.series_count = channelEl.get('series_count')

class ModelProgram:
    def __init__(self, programEl):
        self.id = programEl.get('id')
        self.image_thumb = programEl.get('thumb_url')
        self.image_fanart = programEl.get('image_url')
        self.name = programEl.get('name').strip()
        self.clip_count = int(programEl.get('clip_count'))
        self.episode_count = int(programEl.get('episode_count'))

class ModelVideo:
    def __init__(self, programEl):
        self.id = programEl.get('id')
        self.image_thumb = programEl.get('thumb_url')
        self.name = programEl.get('name').strip()
        self.description = programEl.get('description')
        self.duration = programEl.get('duration')
        self.episode_number = programEl.get('episode_number')
        self.season_number = programEl.get('season_number')
        self.coming_soon = int(programEl.get('coming_soon'))

        print self.image_thumb

class Stream:
    def __init__(self, streamEl):
        self.title = streamEl.title.contents[0].strip()

        matchObj = re.search( r'/>(.*)<', str(streamEl), re.M|re.I)
        self.url = matchObj.group(1)

class ShahidUtils:

    # ATN Feeds
    urls = {}
    urls['register_device'] = "http://shahid.mbc.net/api/registerDevice?deviceID=%s"
    urls['index_pageInfo'] = "http://shahid.mbc.net/api/indexPageInfo?api_key=%s"
    urls['channel_list'] = "http://shahid.mbc.net/api/channelList?api_key=%s&offset=0&limit=60"
    urls['program_list'] = "http://shahid.mbc.net/api/programsList?api_key=%s&offset=0&limit=60&channel_id=%s"
    urls['media_list'] = "http://shahid.mbc.net/api/mediaList?api_key=%s&offset=0&limit=60&program_id=%s&sub_type=%s"

    urls['resolve_clip'] = "http://myseeon12.appspot.com/?url=http://shahid.mbc.net/media/video/%s"

    def __init__(self):
        self.settings = sys.modules["__main__"].settings
        self.language = sys.modules["__main__"].language
        self.plugin = sys.modules["__main__"].plugin

        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

    # Calls a REST Url and parses response to a JSON object automatically
    def __getData(self, url):
        response = self.opener.open(url)
        data = response.read()
        self.opener.close()

        return json.loads(data)

    # Fetches an API key for Shahid.net
    def __getAPIKey(self, deviceID):
        url = self.urls['register_device'] % deviceID
        response = self.__getData(url)

        return response['api_key']

    def getChannelList(self):
        url = self.urls['channel_list'] % self.__getAPIKey('1234')
        response = self.__getData(url)
        channelsElList = response['channels']

        list = []

        for channelEl in channelsElList:
            list.append(ModelChannel(channelEl))

        return list

    # A channel has a list of programs
    def getProgramList(self, channelID):
        url = self.urls['program_list'] % (self.__getAPIKey('1234'), channelID)
        response = self.__getData(url)
        programsElList = response['programs']

        list = []

        for programEl in programsElList:
            list.append(ModelProgram(programEl))

        return list

    # A program has a list of videos
    # videoType can be either 'episodes' or 'clips'
    def getVideoList(self, programID, videoType):
        url = self.urls['media_list'] % (self.__getAPIKey('1234'), programID, videoType)
        response = self.__getData(url)
        videosElList = response['media']

        list = []

        for videoEl in videosElList:
            list.append(ModelVideo(videoEl))

        return list

    def getPlayStreamOptions(self, programID, clipID):

        # Given the clipID, call cryptic URL to fetch path that will eventually
        # be evaluated to return the list of streams to play clip
        rssUrl = self.urls['resolve_clip'] % clipID
        response = self.opener.open(rssUrl)
        html_data = response.read();

        soup = BeautifulSoup(html_data)
        streamFindResponse = str(soup.findAll('item')[0])

        # Extracting url from example format:
        #    <item><title>Get Videos (rtmpe)</title><link />rss://myveetle12.appspot.com/?url=56a72e4d102f415dbe547fcd7dcbf64a/xxxx</item>
        matchObj = re.search( r'rss://(.*)<', streamFindResponse, re.M|re.I)
        streamFindUrl = 'http://' + matchObj.group(1)
        
        # Url to find stream has been found. Invoke and return to
        # client list of stream option to choose from
        response = self.opener.open(streamFindUrl)
        html_data = response.read();
        soup = BeautifulSoup(html_data)

        streams = []

        print "Returned Streams"
        for item in soup.findAll('item'):
            stream = Stream(item)
            print stream.title + ' ' + stream.url
            streams.append(stream)

        return streams[:1]   # Temporary convenience hack, always return one stream (the highest quality!)
