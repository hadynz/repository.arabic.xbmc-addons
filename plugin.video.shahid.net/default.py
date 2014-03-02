import xbmcplugin
import xbmcgui
import xbmcaddon
import copy
from xbmcswift2 import Plugin, actions
from resources.lib.shahidnet.utils import imagePath
from resources.lib.shahidnet.api import ShahidNetAPI
from resources.lib.shahidnet.models import MediaType
from resources.lib.shahidnet.scraper import FILTER_GENRE, FILTER_DIALECT, FILTER_PROGRAM_TYPE


plugin = Plugin()

SEARCH_LIMIT = 10

CACHE_NEW_FILTER = plugin.get_storage('CACHE_NEW_FILTER')

CACHE_FILTERS = plugin.get_storage('CACHE_FILTERS')
#CACHE_FILTERS.clear()

STRINGS = {
    # Root menu
    'filter': 30000,
    'channels': 30001,
    'search': 30002,
    'most_popular': 30003,
    'date_released': 30004,
    'add_filter': 30005,
    'program_type': 30006,
    'genre': 30007,
    'dialect': 30008,
    'save': 30009,
    'latest_episodes': 30010,
    'latest_programs': 30011,
    'latest_clips': 30012,
    'most_popular_episodes': 30013,
    'most_popular_clips': 30014,

    # Context menu
    'delete_filter': 30100,

    # Dialogs
    'delete_filter_head': 30110,
    'delete_filter_confirm': 30111,
    'success': 30112,
    'filter_success': 30113,
    'search_shahid': 30114,
}


@plugin.route('/')
def list_main_menu():

    # Initialise cached filters list if required
    if CACHE_FILTERS.get('list') is None:
        CACHE_FILTERS['list'] = []

    filterCount = len(CACHE_FILTERS['list'])

    items = [{
                 'label': _('filter') if filterCount == 0 else '%s ([COLOR blue]%s[/COLOR])' % (_('filter'), str(filterCount)),
                 'path': plugin.url_for('list_filters', hasSaved='False'),
                 'thumbnail': imagePath(plugin, 'art', 'filter.png')
             },
             {
                 'label': _('channels'),
                 'path': plugin.url_for('list_all_channels'),
                 'thumbnail': imagePath(plugin, 'art', 'channels.png')
             },
             {
                 'label': _('search'),
                 'path': plugin.url_for('search'),
                 'thumbnail': imagePath(plugin, 'art', 'search.png')
             },
             {
                 'label': _('most_popular'),
                 'path': plugin.url_for('list_most_popular'),
                 'thumbnail': imagePath(plugin, 'art', 'most_popular.png')
             },
             {
                 'label': _('date_released'),
                 'path': plugin.url_for('list_by_date_released'),
                 'thumbnail': imagePath(plugin, 'art', 'date_released.png')
             }
    ]

    return items


@plugin.route('/filter/remove/<indexId>')
def remove_filter_option(indexId):
    confirmed = xbmcgui.Dialog().yesno(
        _('delete_filter_head'),
        _('delete_filter_confirm')
    )

    if confirmed:
        del CACHE_FILTERS['list'][int(indexId)]

        plugin.notify(msg=_('success'))
        plugin.redirect(plugin.url_for('list_filters', hasSaved='False'))


@plugin.route('/list/filters/save', name='save_new_filter', options={'hasSaved': 'True'})
@plugin.route('/list/filters', options={'hasSaved': 'False'})
def list_filters(hasSaved='False'):
    def make_filter_ctx(filterIndex):
        return (
            _('delete_filter'),
            actions.background(plugin.url_for('remove_filter_option', indexId=filterIndex))
        )

    def filter_link(filter):
        dialectId = filter['dialect']['id'] if 'dialect' in filter else '0'
        genreId = filter['genre']['id'] if 'genre' in filter else '0'
        typeId = filter['type']['id'] if 'type' in filter else '0'

        return plugin.url_for('list_filtered_programs', dialectId=dialectId, genreId=genreId, typeId=typeId)


    def filter_name(filter):
        list = []

        for f in filter:
            list.append(filter[f]['title'])

        return ' + '.join(list)


    # Persist any new filters to the cached list of filters
    canSave = hasSaved == 'True' and len(CACHE_NEW_FILTER.keys()) > 0

    if canSave:
        newfilter = copy.deepcopy(CACHE_NEW_FILTER) # Copy new filter
        CACHE_FILTERS['list'].append(newfilter)
        CACHE_NEW_FILTER.clear()    # Clear copied filter - save to do so because we copied it before
        plugin.notify(msg=_('filter_success'))


    # Create menu items
    items = [{
                 'label': '[COLOR blue]%s...[/COLOR]' % _('add_filter'),
                 'path': plugin.url_for('add_filter')
             }
    ]

    for idx, filter in enumerate(CACHE_FILTERS.get('list')):
        items.append({
            'label': filter_name(filter),
            'path': filter_link(filter),
            'context_menu': [
                make_filter_ctx(str(idx))
            ],
            'replace_context_menu': True,
        })

    return plugin.finish(items, update_listing=canSave)


@plugin.route('/list/programs/filtered/<dialectId>/<genreId>/<typeId>')
def list_filtered_programs(dialectId, genreId, typeId):
    programs = api.get_filtered_programs(dialectId, genreId, typeId)

    items = [{
                 'label': program.name,
                 'path': _program_path(program),
                 'thumbnail': program.thumbnail
             } for program in programs]

    return items


def __filter_items():
    def display_title(title, type):
        if type in CACHE_NEW_FILTER:
            return '%s: [COLOR white][B]%s[/B][/COLOR]' % (title, CACHE_NEW_FILTER[type]['title'])

        return 'Set %s...' % title

    items = [{
                 'label': display_title(_('program_type'), 'programType'),
                 'path': plugin.url_for('add_filter_list', type='programType'),
             },
             {
                 'label': display_title(_('genre'), 'genre'),
                 'path': plugin.url_for('add_filter_list', type='genre'),
             },
             {
                 'label': display_title(_('dialect'), 'dialect'),
                 'path': plugin.url_for('add_filter_list', type='dialect'),
             },
    ]

    # User has set at least one filter option - is allowed to save
    if len(CACHE_NEW_FILTER.keys()) > 0:
        items.append({
            'label': '[COLOR blue]%s[/COLOR]' % _('save'),
            'path': plugin.url_for('save_new_filter')
        })

    return items


@plugin.route('/filters/add')
def add_filter():
    # Clear the new filter working object since user is starting again from scratch
    CACHE_NEW_FILTER.clear()

    items = __filter_items()
    return plugin.finish(items, update_listing=(len(CACHE_NEW_FILTER.keys()) > 0))


@plugin.route('/filters/add/list/<type>')
def add_filter_list(type):
    if type == 'genre':
        options = FILTER_GENRE
    elif type == 'dialect':
        options = FILTER_DIALECT
    else:
        options = FILTER_PROGRAM_TYPE

    # Show select dropdown dialog
    selected = xbmcgui.Dialog().select(
        'Choose a %s' % type,
        map(lambda x: x['title'], options)
    )

    # Add selected filter option to persistent storage
    if selected >= 0:
        CACHE_NEW_FILTER[type] = options[selected]

    # Return updated list of items after user selection
    items = __filter_items()

    return plugin.finish(items, update_listing=True)


@plugin.route('/menu/date_released/')
def list_by_date_released():
    items = [{
                 'label': _('latest_episodes'),
                 'path': plugin.url_for('list_media_items_latest', mediaType=MediaType.EPISODE),
                 'thumbnail': imagePath(plugin, 'art', 'episodes.png')
             },
             {
                 'label': _('latest_programs'),
                 'path': plugin.url_for('list_channel_programs', channelID=' '),
                 'thumbnail': imagePath(plugin, 'art', 'programs.png')
             },
             {
                 'label': _('latest_clips'),
                 'path': plugin.url_for('list_media_items_latest', mediaType=MediaType.CLIP),
                 'thumbnail': imagePath(plugin, 'art', 'clips.png')
             }
    ]

    return plugin.finish(items)


@plugin.route('/menu/most_popular/')
def list_most_popular():
    items = [{
                 'label': _('most_popular_episodes'),
                 'path': plugin.url_for('list_most_watched', programType=MediaType.EPISODE),
                 'thumbnail': imagePath(plugin, 'art', 'episodes.png')
             },
             {
                 'label': _('most_popular_clips'),
                 'path': plugin.url_for('list_most_watched', programType=MediaType.CLIP),
                 'thumbnail': imagePath(plugin, 'art', 'clips.png')
             },
    ]

    return plugin.finish(items)


@plugin.route('/search')
def search():
    search_string = plugin.keyboard(heading=_('search_shahid'))

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


@plugin.cached_route('/list/media/program/<programID>/episode/<episodeCount>/clips/<clipsCount>', TTL=60 * 5)
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


def log(text):
    plugin.log.info(text)


def _(string_id):
    if string_id in STRINGS:
        return plugin.get_string(STRINGS[string_id]).encode('utf-8')
    else:
        log('String is missing: %s' % string_id)
        return string_id


if __name__ == '__main__':
    api = ShahidNetAPI()
    if api:
        plugin.run()
