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
                 'label': 'All',
                 'path': plugin.url_for('list_all_channels')
             }, {
                 'label': 'Browse by Category',
                 'path': plugin.url_for('browse_by_category')
             }, {
                 'label': 'Browse by Network',
                 'path': plugin.url_for('browse_by_network')
             }]

    return items


@plugin.route('/list/all/')
def list_all_channels():
    items = [{
                 'label': channel['title'],
                 'path': plugin.url_for('play_video', url=channel['path']),
                 'is_playable': True,
                 'thumbnail': channel['thumbnail']
             } for channel in api.get_channels()]

    return plugin.finish(items, sort_methods=['label'])


@plugin.route('/list/browse_by_category/')
def browse_by_category():
    items = [{
                 'label': category['label'],
                 'path': plugin.url_for('list_channels_for_category', category_name=category['category_name']),
             } for category in api.get_channels_grouped_by_category()]

    return plugin.finish(items, sort_methods=['label'])


@plugin.route('/list/browse_by_network/')
def browse_by_network():
    items = [{
                 'label': network['label'],
                 'path': plugin.url_for('list_channels_for_network', network_name=network['network_name'])
             } for network in api.get_channels_grouped_by_network()]

    return plugin.finish(items, sort_methods=['label'])


@plugin.route('/list/category/<category_name>')
def list_channels_for_category(category_name):
    channels = api.get_channels()
    category_channels = api.get_channels_for_category(channels, category_name)

    items = [{
                 'label': channel['title'],
                 'path': plugin.url_for('play_video', url=channel['path']),
                 'is_playable': True,
                 'thumbnail': channel['thumbnail']
             } for channel in category_channels]

    return plugin.finish(items, sort_methods=['label'])


@plugin.route('/list/network/<network_name>')
def list_channels_for_network(network_name):
    channels = api.get_channels()
    network_channels = api.get_channels_for_network(channels, network_name)

    items = [{
                 'label': network['title'],
                 'path': plugin.url_for('play_video', url=network['path']),
                 'is_playable': True,
                 'thumbnail': network['thumbnail']
             } for network in network_channels]

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
