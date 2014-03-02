import re
from models import ChannelItem, ProgramItem, MediaItem
from utils import json


API_KEY = '4cd216240b9e47c3d97450b9b4866d3f'


URL_CHANNEL_LIST = "http://shahid.mbc.net/api/channelList?api_key={apiKey}&offset=0&limit=60"
URL_PROGRAMS_LIST = "http://shahid.mbc.net/api/programsList?api_key={apiKey}&offset=0&limit=60&channel_id={channelID}"
URL_MEDIA_LIST = "http://shahid.mbc.net/api/mediaList?api_key={apiKey}&offset=0&limit=60&program_id={programID}&sub_type={mediaType}"
URL_MEDIA_INFO = "http://shahid.mbc.net/api/mediaInfoList?api_key={apiKey}&media_id={mediaID}&offset=0&limit=60&program_id={programID}&sub_type={mediaType}"

URL_MEDIA_STREAM_BY_MEDIA_ID = "http://hadynz-shahid.appspot.com/scrape?m={mediaHash}"
URL_MEDIA_STREAM_BY_VIDEO_ID = "http://hadynz-shahid.appspot.com/scrape?v={videoId}"

URL_SEARCH = "http://shahid.mbc.net/api/programsList?api_key={apiKey}&offset=0&limit={limit}&keyword={keyword}"


def get_channels():
    """
    :return: Returns list of all Channels
    :rtype : list of ChannelItem
    """
    response = json(URL_CHANNEL_LIST.format(apiKey=API_KEY))
    return [ChannelItem(channelJson) for channelJson in response['channels']]


def get_channel_programs(channelID):
    """
    :param channelID: Channel ID
    :return: list of programs for th current Channel ID
    :rtype: list of ProgramItem
    """
    response = json(URL_PROGRAMS_LIST.format(apiKey=API_KEY, channelID=channelID))
    programs = [ProgramItem(programJson) for programJson in response['programs']]

    # Only return programs with one or more episodes/clips
    return filter(lambda x: (x.episodeCount + x.clipCount) > 0, programs)


def get_program_media(programID, mediaType):
    response = json(URL_MEDIA_LIST.format(apiKey=API_KEY, programID=programID, mediaType=mediaType))
    return [MediaItem(mediaJson) for mediaJson in response['media']]


def _get_media_info(programID, mediaType, mediaID):
    response = json(URL_MEDIA_INFO.format(apiKey=API_KEY, programID=programID, mediaType=mediaType, mediaID=mediaID))
    return response['media']


def _get_media_id_hash(programID, mediaType, mediaID):
    mediaInfo = _get_media_info(programID, mediaType, mediaID)
    mediaUrl = mediaInfo['media_url']

    try:
        matchObj = re.search(r'media\/(.*)\.m3u8', mediaUrl, re.M | re.I)
        mediaHash = matchObj.group(1)

        return mediaHash

    except Exception as ex:
        print 'Error parsing media hash from media url: %s' % ex

    return None


def get_media_stream_by_media_id(quality, programID, mediaType, mediaID):
    mediaHash = _get_media_id_hash(programID, mediaType, mediaID)

    streams = json(URL_MEDIA_STREAM_BY_MEDIA_ID.format(mediaHash=mediaHash))
    return _get_matching_stream_quality(quality, streams)


def get_media_stream_by_url(quality, url):
    match_obj = re.search(r'.*video\/(.*)\/.*', url, re.M | re.I)
    video_id = match_obj.group(1)

    streams = json(URL_MEDIA_STREAM_BY_VIDEO_ID.format(videoId=video_id))
    return _get_matching_stream_quality(quality, streams)


def _get_matching_stream_quality(quality, streams):
    for stream in streams:
        if quality == stream['Quality']:
            return stream['URL']

    return None


def search(search_term, limit=20):
    response = json(URL_SEARCH.format(apiKey=API_KEY, keyword=search_term, limit=limit))
    programs = [ProgramItem(programJson) for programJson in response['programs']]
    return programs


def debug():
    '''
    for program in get_channel_programs('8'):
        print program['mobile_image_url'] + ' id=' + program['id'] + ' clip_count=' + program['clip_count'] + ' episode_count=' +  program['episode_count'] + ' item_type=' + program['item_type']

    for media in get_program_media('1559', 'episodes'):
        print media

    print get_media_stream('360p LOW', '1559', 'episodes', '53899')
    '''

    #url = 'http://shahid.mbc.net/media/video/46534/Arabs_got_talent_%D8%A7%D9%84%D8%AD%D9%84%D9%82%D8%A9_7'
    #print get_media_stream_by_url('360p LOW', url)

    print search('Ar')


if __name__ == '__main__':
    debug()
