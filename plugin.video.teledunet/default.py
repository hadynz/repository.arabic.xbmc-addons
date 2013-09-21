import os
import xbmcplugin, xbmcgui, xbmcaddon
from operator import itemgetter
from xbmcswift2 import Plugin
from resources.lib.teledunet.api import TeledunetAPI

# Setup global variables
PLUGIN_NAME = 'Teledunet.com'
PLUGIN_ID = 'plugin.video.teledunet'
CACHE_DURATION_MINUTES = 20

# Create Plugin object
plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)

# Instantiate API object
cache = plugin.get_storage('channels_cache.txt', TTL=CACHE_DURATION_MINUTES)
api = TeledunetAPI(cache)

@plugin.route('/')
def list_categories():
    items = [{
                 'label': channel['title'],
                 'path': plugin.url_for('play_video', url=channel['path']),
                 'is_playable': True,
                 'thumbnail': channel['thumbnail']
             } for channel in api.get_channels()]

    return plugin.finish(items, sort_methods=['label'])




@plugin.route('/play/<url>')
def play_video(url):
    rtmp_params = api.get_rtmp_params(url)

    def rtmpdump_output(rtmp_params):
        return (
                   'rtmpdump.exe '
                   '--rtmp "%(rtmp_url)s" '
                   '--app "%(app)s" '
                   '--swfUrl "%(swf_url)s" '
                   '--playpath "%(playpath)s" '
                   '-o test.flv'
                   ) % rtmp_params

    def xbmc_output(rtmp_params):
        return (
                   '%(rtmp_url)s '
                   'app=%(app)s '
                   'swfUrl=%(swf_url)s '
                   'playpath=%(playpath)s '
                   'live=%(live)s '
                   'pageUrl=%(video_page_url)s '
                   ) % rtmp_params

    playback_url = xbmc_output(rtmp_params)
    plugin.log.info('RTMP cmd: %s' % rtmpdump_output(rtmp_params))
    plugin.log.info('XBMC cmd: %s' % xbmc_output(rtmp_params))
    return plugin.set_resolved_url(playback_url)


def _art(file, *args):
    return os.path.join(plugin.addon.getAddonInfo('path'), file, *args)

if __name__ == '__main__':
    plugin.run()
