import os
import xbmcplugin, xbmcgui, xbmcaddon
from xbmcswift2 import Plugin
from resources.lib.dailytube4u.api import DailyTube4uAPI

PLUGIN_NAME = 'DailyTube4U.com'
PLUGIN_ID = 'plugin.video.dailytube4u.com'
plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)

api = DailyTube4uAPI()

@plugin.cached_route('/', TTL=60*5)
def list_all_channels():
    shows = api.get_channels()

    for show in shows:
        show['path'] = plugin.url_for('list_show_clips', show_path=show['path'])
        show['properties'] = [
            ('fanart_image', _art('fanart.jpg'))
        ]

    return shows

@plugin.cached_route('/list/shows/<show_path>', TTL=60)
def list_show_clips(show_path):
    clips = api.get_clips_for_show(show_path)

    plugin.set_content('movies')

    for clip in clips:
        clip['path'] = plugin.url_for('play_video', video_id=clip['path'])

    return clips

@plugin.route('/play/<video_id>/')
def play_video(video_id):
    url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id
    plugin.log.info('Playing url: %s' % url)

    return plugin.set_resolved_url(url)

def _art(file, *args):
    return os.path.join(plugin.addon.getAddonInfo('path'), file, *args)

if __name__ == '__main__':
    plugin.run()
