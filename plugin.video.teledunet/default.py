from operator import itemgetter
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
from xbmcswift2 import Plugin


# Setup global variables
from resources.lib.teledunet import scraper
from resources.lib.teledunet.api import TeledunetAPI


CACHE_DURATION_MINUTES = 24 * 60     # Cache for 5hrs

plugin = Plugin()


@plugin.route('/')
def list_categories():
    items = [{
                 'label': 'All',
                 'path': plugin.url_for('list_all_channels'),
                 'thumbnail': _art('art', 'all.png')

             }, {
                 'label': 'Browse by Category',
                 'path': plugin.url_for('browse_by_category'),
                 'thumbnail': _art('art', 'category.png')
             }, {
                 'label': 'Browse by Network',
                 'path': plugin.url_for('browse_by_network'),
                 'thumbnail': _art('art', 'network.png')
             }]

    return items


@plugin.route('/list/all/')
def list_all_channels():
    items = [{
                 'label': channel.display_name(),
                 'path': plugin.url_for('play_video', url=channel.path),
                 'thumbnail': channel.thumbnail,
                 'is_playable': True,
             } for channel in api.get_channels()]

    return plugin.finish(items, sort_methods=['label'])


@plugin.route('/list/browse_by_category/')
def browse_by_category():
    categories = api.get_channels_grouped_by_category()

    for category in categories:
        category['path'] = plugin.url_for('list_channels_for_category', category_name=category['category_name'])
        del category['category_name']

    return sorted(categories, key=itemgetter('label'))


@plugin.route('/list/browse_by_network/')
def browse_by_network():
    networks = api.get_channels_grouped_by_network()

    for network in networks:
        network['path'] = plugin.url_for('list_channels_for_network', network_name=network['network_name'])
        del network['network_name']

    return sorted(networks, key=itemgetter('label'))


@plugin.route('/list/category/<category_name>')
def list_channels_for_category(category_name):
    channels = api.get_channels()
    category_channels = api.get_channels_for_category(channels, category_name)

    items = [{
                 'label': channel.display_name(),
                 'path': plugin.url_for('play_video', url=channel.path),
                 'thumbnail': channel.thumbnail,
                 'is_playable': True,
             } for channel in category_channels]

    return plugin.finish(items, sort_methods=['label'])


@plugin.route('/list/network/<network_name>')
def list_channels_for_network(network_name):
    channels = api.get_channels()
    network_channels = api.get_channels_for_network(channels, network_name)

    items = [{
                 'label': channel.display_name(),
                 'path': plugin.url_for('play_video', url=channel.path),
                 'thumbnail': channel.thumbnail,
                 'is_playable': True,
             } for channel in network_channels]

    return plugin.finish(items, sort_methods=['label'])


@plugin.route('/play/<url>')
def play_video(url):
    rtmp_params = scraper.get_rtmp_params(url)

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
    cache = plugin.get_storage('teledunet_cache.txt', TTL=CACHE_DURATION_MINUTES)
    api = TeledunetAPI(cache)

    if api:
        plugin.run()
