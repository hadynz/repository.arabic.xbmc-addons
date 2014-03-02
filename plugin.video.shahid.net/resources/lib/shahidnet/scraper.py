import re
from models import MediaType
from utils import html
from models import ChannelItem, ProgramItem, MediaItem


MAX_LIMIT = 25

URL_MOST_WATCHED = "http://shahid.mbc.net/Ajax/popular?operation={operation}&time_period=month&&offset={offset}&limit={maxLimit}"
URL_LATEST = "http://shahid.mbc.net/Ajax/recent/{operation}/0/0/0/4?offset={offset}&limit={maxLimit}"
URL_FILTER = "http://shahid.mbc.net/Ajax/seriesFilter?year=0&dialect={dialect}&title=0&genre={genre}&channel=0&prog_type={type}&media_type=0&airing=0&sort=latest&series_id=0&offset=0&sub_type=0&limit={limit}"

FILTER_PROGRAM_TYPE = [
    {'id': '22', 'title': 'Cartoon'},
    {'id': '21', 'title': 'Documentary'},
    {'id': '20', 'title': 'Programs'},
    {'id': '19', 'title': 'Series'},
]

FILTER_GENRE = [
    {'id': '24', 'title': 'Comedy'},
    {'id': '2', 'title': 'Drama'},
    {'id': '22', 'title': 'Educational'},
    {'id': '3', 'title': 'Entertainment'},
    {'id': '4', 'title': 'Game Show'},
    {'id': '14', 'title': 'Health'},
    {'id': '5', 'title': 'History'},
    {'id': '6', 'title': 'Horror'},
    {'id': '11', 'title': 'Lifestyle'},
    {'id': '8', 'title': 'Music'},
    {'id': '19', 'title': 'News'},
    {'id': '10', 'title': 'Politics'},
    {'id': '15', 'title': 'Reality TV'},
    {'id': '9', 'title': 'Religious'},
    {'id': '7', 'title': 'Romance'},
    {'id': '17', 'title': 'Social'},
    {'id': '21', 'title': 'Sports'},
    {'id': '18', 'title': 'Talk Show'},
    {'id': '13', 'title': 'Tourism'},
    {'id': '25', 'title': 'Wrestling'}
]

FILTER_DIALECT = [
    {'id': '2', 'title': 'Arabic'},
    {'id': '12', 'title': 'Bedouin'},
    {'id': '8', 'title': 'Dubbed Indian'},
    {'id': '15', 'title': 'Dubbed Korean'},
    {'id': '7', 'title': 'Dubbed Latin'},
    {'id': '6', 'title': 'Dubbed Turkish'},
    {'id': '3', 'title': 'Egyptian'},
    {'id': '13', 'title': 'English'},
    {'id': '1', 'title': 'Gulf'},
    {'id': '14', 'title': 'Iraqi'},
    {'id': '5', 'title': 'Jordanian'},
    {'id': '11', 'title': 'Lebanese'},
    {'id': '4', 'title': 'Syrian'},
]

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


def _get_program_item(el):
    span_list = el.find('a', {'class': 'tip_anchor'}).findAll('span', {'class': re.compile(r"\b.*title.*\b")})
    season_episode_str = span_list[-1].contents[0].strip()
    digits_list = re.findall(r'\d{1,5}', season_episode_str)

    json = {
        'id': el['class'].replace('ser_', ''),
        'name': span_list[0].contents[0].strip(' -'),
        'thumb_url': el.find('img')['src'],
        'image_url': '',
        'episode_count': digits_list[0],
        'clip_count': '0',
        'total_views': '',
    }

    return ProgramItem(json)


def get_filtered_programs(dialectId, genreId, typeId):
    url = URL_FILTER.format(dialect=dialectId, genre=genreId, type=typeId, limit=MAX_LIMIT)
    html_response = html(url)

    items = html_response.find('ul').findAll('a', {'class': 'tip_anchor'})
    items = html_response.findAll('li')
    return [_get_program_item(clip) for clip in items]


def debug():
    #for item in get_most_watched(MediaType.CLIP):
    #    print item.description
    #    print get_latest(MediaType.PROGRAM)

    #print get_most_watched(MediaType.CLIP)
    print get_filtered_programs('6', '4', '0')


if __name__ == '__main__':
    debug()


