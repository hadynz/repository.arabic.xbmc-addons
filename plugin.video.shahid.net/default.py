import xbmcplugin
import xbmcgui
import xbmcaddon
from xbmcswift2 import Plugin
from resources.lib.common.utils import imagePath
from resources.lib.shahidnet.api import ShahidNetAPI
from resources.lib.shahidnet.models import MediaType


PLUGIN_NAME = 'Shahid.net'
PLUGIN_ID = 'plugin.video.shahid.net'
plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)

api = ShahidNetAPI()

SEARCH_TITLE = 'Search Shahid.net'
SEARCH_LIMIT = 10


@plugin.route('/')
def list_main_menu():
    items = [{
                 'label': 'Channels',
                 'path': plugin.url_for('list_all_channels'),
                 'thumbnail': imagePath(plugin, 'art', 'channels.png')
             },
             {
                 'label': 'Search...',
                 'path': plugin.url_for('search'),
                  'thumbnail': imagePath(plugin, 'art', 'search.png')

             },
             {
                 'label': 'Most Popular',
                 'path': plugin.url_for('list_most_popular'),
                  'thumbnail': imagePath(plugin, 'art', 'most_popular.png')

             },
             {
                 'label': 'Date released',
                 'path': plugin.url_for('list_by_date_released'),
                  'thumbnail': imagePath(plugin, 'art', 'date_released.png')

             }
    ]

    return items


@plugin.route('/list/date_released/')
def list_by_date_released():
    items = [{
                 'label': 'Latest Episodes',
                 'path': plugin.url_for('list_media_items_latest', mediaType=MediaType.EPISODE),
                 'thumbnail': imagePath(plugin, 'art', 'episodes.png')
             },
             {
                 'label': 'Latest Programs',
                 'path': plugin.url_for('list_channel_programs', channelID=' '),
                 'thumbnail': imagePath(plugin, 'art', 'programs.png')
             },
             {
                 'label': 'Latest Clips',
                 'path': plugin.url_for('list_media_items_latest', mediaType=MediaType.CLIP),
                 'thumbnail': imagePath(plugin, 'art', 'clips.png')
             }
    ]

    return plugin.finish(items)


@plugin.route('/list/most_popular/')
def list_most_popular():
    items = [{
                 'label': 'Most Popular Episodes',
                 'path': plugin.url_for('list_most_watched', programType=MediaType.EPISODE),
                 'thumbnail': imagePath(plugin, 'art', 'episodes.png')
             },
             {
                 'label': 'Most Popular Clips',
                 'path': plugin.url_for('list_most_watched', programType=MediaType.CLIP),
                 'thumbnail': imagePath(plugin, 'art', 'clips.png')
             },
    ]

    return plugin.finish(items)


@plugin.route('/search')
def search():
    search_string = plugin.keyboard(heading=SEARCH_TITLE)

    url = plugin.url_for('list_main_menu')

    if search_string:
        url = plugin.url_for('search_result', search_string=search_string)

    plugin.redirect(url)


@plugin.route('/search/<search_string>/')
def search_result(search_string):
    programs = api.search(search_term=search_string, limit=SEARCH_LIMIT)

    items = [{
                 'label': program.name,
                 'path': _program_path(program),
                 'thumbnail': program.thumbnail,
                 'properties': [
                     ('fanart_image', program.bgImage)
                 ]
             } for program in programs]

    return items


@plugin.cached_route('/list/channels', TTL=60 * 24) # Cache for 24hours
def list_all_channels():
    channels = api.get_channels()
    sorted_channels = sorted(channels, key=lambda channel: channel.name)

    items = [{
                 'label': channel.name,
                 'path': plugin.url_for('list_channel_programs', channelID=channel.id),
                 'thumbnail': channel.thumbnail,
                 'properties': [
                     ('fanart_image', channel.bgImage)
                 ]
             } for channel in sorted_channels]

    return items


@plugin.cached_route('/list/channels/<channelID>', TTL=60 * 5) # Cache for 5hours
def list_channel_programs(channelID):
    programs = api.get_channel_programs(channelID)

    if channelID.strip() is not '':
        programs = sorted(programs, key=lambda program: program.name)

    items = [{
                 'label': program.name,
                 'path': _program_path(program),
                 'thumbnail': program.thumbnail,
                 'properties': [
                     ('fanart_image', program.bgImage)
                 ]
             } for program in programs]

    return items


@plugin.cached_route('/list/most_watched/<programType>', TTL=60 * 2)
def list_most_watched(programType):
    media_list = api.get_most_watched(programType)

    items = [{
                 'label': media.displayName(),
                 'path': plugin.url_for('play_video_by_url', url=media.url),
                 'thumbnail': media.thumbnail,
                 'is_playable': True
             } for media in media_list]

    return items


def _program_path(program):
    if program.hasEpisodesOnly():
        return plugin.url_for('list_media_items', mediaType=MediaType.EPISODE, programID=program.id)

    if program.hasClipsOnly():
        return plugin.url_for('list_media_items', mediaType=MediaType.CLIP, programID=program.id)

    return plugin.url_for('list_episode_clip_choice', programID=program.id, episodeCount=str(program.episodeCount),
                          clipsCount=str(program.clipCount))


@plugin.route('/list/media/program/<programID>/episode/<episodeCount>/clips/<clipsCount>')
def list_episode_clip_choice(programID, episodeCount, clipsCount):
    items = [{
                 'label': "Episodes ([COLOR blue]%s[/COLOR] episode%s)" % (
                 episodeCount, 's' if episodeCount > 1 else ''),
                 'path': plugin.url_for('list_media_items', programID=programID, mediaType=MediaType.EPISODE),
                 'thumbnail': imagePath(plugin, 'art', 'episodes.png')
             },
             {
                 'label': "Clips ([COLOR blue]%s[/COLOR] clip%s)" % (clipsCount, 's' if clipsCount > 1 else ''),
                 'path': plugin.url_for('list_media_items', programID=programID, mediaType=MediaType.CLIP),
                 'thumbnail': imagePath(plugin, 'art', 'clips.png')
             }
    ]

    return plugin.finish(items)


@plugin.cached_route('/list/clips/<mediaType>', name='list_media_items_latest', TTL=60 * 2)
@plugin.cached_route('/list/clips/<mediaType>/<programID>', TTL=60 * 2)
def list_media_items(mediaType, programID=''):
    mediaItems = api.get_program_media(programID, mediaType)

    # When programID is not set, we are fetching latest media items; don't modify any sorting
    if programID is not '':
        mediaItems = reversed(mediaItems)

    plugin.set_content('episodes')

    items = [{
                 'label': media.displayName(),
                 'path': plugin.url_for('play_video', programID=programID if programID is not '' else media.seriesId,
                                        mediaType=mediaType,
                                        mediaID=media.id),
                 'thumbnail': media.thumbnail,
                 'info': {
                     'title': media.displayName(),
                     'duration': media.duration,
                     'episode': media.episodeNumber,
                     'dateadded': media.dateAdded,
                     'tvshowtitle': media.seriesName
                 },
                 'is_playable': True
             } for media in mediaItems]

    return items


@plugin.route('/play/<programID>/<mediaType>/<mediaID>')
def play_video(programID, mediaType, mediaID):
    quality = plugin.get_setting('quality')
    url = api.get_media_stream_by_media_id(quality, programID, mediaType, mediaID)

    plugin.log.info('Play Quality: %s' % quality)
    plugin.log.info('Playing url: %s' % url)

    return plugin.set_resolved_url(url)


@plugin.route('/play/<url>')
def play_video_by_url(url):
    '''
        This method is used to play any Shahid.Net videos that have been scraped from their website.
        We don't have the video's media_id, but only have the clip's video URL
    '''
    quality = plugin.get_setting('quality')
    url = api.get_media_stream_by_url(quality, url)

    plugin.log.info('Play Quality: %s' % quality)
    plugin.log.info('Playing url: %s' % url)

    return plugin.set_resolved_url(url)


if __name__ == '__main__':
    try:
        plugin.run()
    except Exception:
        plugin.notify('Network Error')
