import re
from scraper import (get_rtmp_params, get_channels)

'''The main API object. Useful as a starting point to get available subjects. '''

class TeledunetAPI(object):
    def __init__(self, cache):
        self.cache = cache

    def get_rtmp_params(self, channel_name):
        return get_rtmp_params(channel_name)

    def get_channels(self):
        if 'data' not in self.cache:
            self.cache['data'] = get_channels()

        return self.cache.get('data')