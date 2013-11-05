import os
import xbmcplugin, xbmcgui, xbmcaddon
from xbmcswift2 import Plugin
from resources.lib.shahidnet.api import ShahidNetAPI, MediaType

PLUGIN_NAME = 'Shahid.net'
PLUGIN_ID = 'plugin.video.shahid.net'
plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)

api = ShahidNetAPI()


@plugin.cached_route('/', TTL=60*24) # Cache for 24hours
def list_all_channels():
    channels = api.get_channels()
    sorted_channels = sorted(channels, key=lambda channel: channel['name'])

    items = [{
                 'label': channel['name'],
                 'path': plugin.url_for('list_channel_programs', channelID=channel['id']),
                 'thumbnail': channel['thumb_url'],
                 'properties': [
                     ('fanart_image', channel['image_url'])
                 ]
             } for channel in sorted_channels]

    return items


@plugin.cached_route('/list/channels/<channelID>', TTL=60*5) # Cache for 5hours
def list_channel_programs(channelID):
    programs = api.get_channel_programs(channelID)

    items = [{
                 'label': program['name'],
                 'path': _program_path(program),
                 'thumbnail': program['thumb_url'],
                 'properties': [
                     ('fanart_image', program['image_url'])
                 ]
             } for program in programs]

    return items


def _program_path(program):
    episodeCount = int(program['episode_count'])
    clipCount = int(program['clip_count'])

    if episodeCount > 0 and clipCount is 0:
        return plugin.url_for('list_media_items', programID=program['id'], mediaType=MediaType.EPISODE)

    if episodeCount is 0 and clipCount > 0:
        return plugin.url_for('list_media_items', programID=program['id'], mediaType=MediaType.CLIP)

    return plugin.url_for('list_episode_clip_choice', programID=program['id'], episodeCount=str(episodeCount),
                          clipsCount=str(clipCount))


@plugin.route('/list/media/program/<programID>/episode/<episodeCount>/clips/<clipsCount>')
def list_episode_clip_choice(programID, episodeCount, clipsCount):
    items = [{
                 'label': "Episodes ([COLOR blue]%s[/COLOR] episode%s)" % (
                     episodeCount, 's' if episodeCount > 1 else ''),
                 'path': plugin.url_for('list_media_items', programID=programID, mediaType=MediaType.EPISODE)
             },
             {
                 'label': "Clips ([COLOR blue]%s[/COLOR] clip%s)" % (clipsCount, 's' if clipsCount > 1 else ''),
                 'path': plugin.url_for('list_media_items', programID=programID, mediaType=MediaType.CLIP)
             }
    ]

    return plugin.finish(items)


@plugin.cached_route('/list/clips/<programID>/<mediaType>', TTL=60*2) # Cache for 2hours
def list_media_items(programID, mediaType):
    mediaItems = api.get_program_media(programID, mediaType)

    plugin.set_content('episodes')

    items = [{
                 'label': _clip_name(media),
                 'path': plugin.url_for('play_video', programID=programID, mediaType=mediaType, mediaID=media['id']),
                 'thumbnail': media['thumb_url'],
                 'info': {
                     'title': _clip_name(media),
                     'duration': media['duration'],
                     'episode': media['episode_number'],
                     'dateadded': media['tx_date'],
                     'tvshowtitle': media['series_name']
                 },
                 'is_playable': True
             } for media in reversed(mediaItems)]

    return items


def _clip_name(media):
    if media['type'] == 'clip':
        if not media['summary']:
            return media['series_name']

        return media['summary']

    return media['type'].title() + ' ' + media['episode_number']


@plugin.route('/play/<programID>/<mediaType>/<mediaID>')
def play_video(programID, mediaType, mediaID):
    quality = plugin.get_setting('quality')
    url = api.get_media_stream(quality, programID, mediaType, mediaID)

    plugin.log.info('Play Quality: %s' % quality)
    plugin.log.info('Playing url: %s' % url)

    return plugin.set_resolved_url(url)


def _art(file, *args):
    return os.path.join(plugin.addon.getAddonInfo('path'), file, *args)


if __name__ == '__main__':
    plugin.run()
