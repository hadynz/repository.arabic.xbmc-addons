import re
from models import MediaType
from resources.lib.common.utils import html
from webservice import MediaItem


MAX_LIMIT = 25


URL_MOST_WATCHED = "http://shahid.mbc.net/Ajax/popular?operation={operation}&time_period=month&&offset={offset}&limit={maxLimit}"
URL_LATEST = "http://shahid.mbc.net/Ajax/recent/{operation}/0/0/0/4?offset={offset}&limit={maxLimit}"


MOST_WATCHED_MAP = {
    MediaType.PROGRAM: 'load_popular_programs',
    MediaType.EPISODE: 'load_popular_episodes',
    MediaType.CLIP: 'load_popular_clips'
}

LATEST_MAP = {
    MediaType.PROGRAM: 'load_recent_series',
    MediaType.EPISODE: 'load_recent_episodes',
    MediaType.CLIP: 'load_recent_clips'
}

MEDIA_TYPE = {
    MediaType.EPISODE: 'episode',
    MediaType.CLIP: 'clip',
    MediaType.PROGRAM: 'program',
}


def get_most_watched(programType):
    url = URL_MOST_WATCHED.format(operation=MOST_WATCHED_MAP[programType], offset='0', maxLimit=MAX_LIMIT)
    html_response = html(url)

    items = html_response.find('ul').findAll('a', {'class': 'tip_anchor'})
    return [_get_item(clip, programType) for clip in items]


def _get_item(el, mediaType):
    span_list = el.findAll('span', {'class': re.compile(r"\b.*title.*\b")})
    description = el.find('span', {'class': 'title_minor'})
    season_episode_str = span_list[2].contents[0].strip()

    # Extract Season and Episode no from a mixed string (e.g. "Season 1, Episode 3) in Arabic
    digits_list = re.findall(r'\d{1,5}', season_episode_str)

    json = {
        'type': MEDIA_TYPE[mediaType],
        'summary': '' if len(description.contents) == 0 else description.contents[0].strip(),
        'series_name': span_list[0].contents[0].strip(' -'),
        'episode_number': digits_list[1] if len(digits_list) > 1 else '',
        'season_number': digits_list[0],
        'thumb_url': el.find('img')['src'],
        'url': re.sub('(.*[0-9]\/).*', r'\g<1>', el['href']), # strip out troublesome ascii characters
    }

    return MediaItem(json)


def get_latest(mediaType):
    '''
    Deprecated. Using Shahid.Net API to fetch the latest media items by different media types
    '''
    url = URL_LATEST.format(operation=LATEST_MAP[mediaType], offset='0', maxLimit=MAX_LIMIT)
    response = html(url)
    return response


def debug():
    for item in get_most_watched(MediaType.CLIP):
        print item.description
        #print get_latest(MediaType.PROGRAM)


if __name__ == '__main__':
    debug()


