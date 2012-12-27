import os
from xbmcswift2 import Plugin
from resources.lib.qaheraalyoum.api import QaheraAlYoumAPI
from resources.lib.qaheraalyoum.utils import extract_youtube_vid

PLUGIN_NAME = 'Al Qahera Al Youm'
PLUGIN_ID = 'plugin.video.alqaheraalyoum'
plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)

CACHE_DURATION_MINUTES = 7
cache = plugin.get_storage('clips_cache.txt', TTL=CACHE_DURATION_MINUTES)
api = QaheraAlYoumAPI(cache)

@plugin.route('/')
def list_categories():
    categories = api.get_clips()

    items = [{
        'label': "%s ([COLOR blue]%s[/COLOR] clip%s)" % (category.name, category.count, 's' if category.count > 1 else ''),
        'path': plugin.url_for('list_category_clips', category=category.name),
        'thumbnail': _art('art', '%s.jpg' % category.name.lower()),
        'properties': [
            ('fanart_image', _art('fanart.jpg'))
        ]
    } for category in categories]

    return items

@plugin.route('/clips/<category>/')
def list_category_clips(category):
    plugin.log.info('Listing category: %s' % category)
    clips = api.get_clips_for_category(category)

    items = [{
        'label': u'%s | [B]%s[/B]' % (clip.addedWhen, clip.name),
        'path': plugin.url_for('play_clip', url=clip.url),
        'is_playable': True,
        'thumbnail': clip.thumbnail,
        'properties': [
            ('fanart_image', _art('fanart.jpg'))
        ]
    } for clip in reversed(clips)]

    return plugin.finish(items)

@plugin.route('/play/<url>/')
def play_clip(url):
    plugin.log.info('Playing clip in url: %s' % url)
    stream_url = api.get_stream_url(url)

    # If a YouTube clip, need to play clip using the XBMC YouTube plugin
    if "youtube.com" in stream_url:
        vid = extract_youtube_vid(stream_url)[0]
        stream_url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=%s" % vid
        plugin.log.info('Playing YouTube clip at [vid=%s]' % vid)
    else:
        plugin.log.info('Extracted stream url: %s' % stream_url)

    return plugin.set_resolved_url(stream_url)

def _art(file, *args):
    return os.path.join(plugin.addon.getAddonInfo('path'), file, *args)

if __name__ == '__main__':
    plugin.run()
