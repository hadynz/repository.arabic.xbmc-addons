import re
from itertools import groupby
from scraper import (get_clips, get_stream_url)

'''The main API object. Useful as a starting point to get available subjects. '''
class QaheraAlYoumAPI(object):

    def __init__(self, cache):
        self.cache = cache

    def _get_clips(self):

        # cache is empty or expired, fetch from service
        if 'clips' not in self.cache:
            clips = [Clip(info) for info in get_clips()]
            self.cache['clips'] = clips

        return self.cache['clips']

    def get_clips(self):
        """Returns a list of subjects available on the website."""
        flatList = self._get_clips()

        items = []
        for key, group in groupby(flatList, lambda x: x.category):
            clipsList = list(clip for clip in group)
            items.append(Category(key, len(clipsList)))

        return items

    def get_clips_for_category(self, category):
        flatList = self._get_clips()
        return filter(lambda x: x.category == category, flatList)

    def get_stream_url(self, clip_url):
        return get_stream_url(clip_url)


class Category:

    def __init__(self, title, count):
        self.name = title
        self.count = count

class Clip(object):

    def __init__(self, el):
        self.thumbnail = el['thumbnail']
        self.url = el['url']
        self.name = el['name']

        self._addedWhen = el['addedWhen']
        self._date = el['date'][el['date'].find('|') + 2:]

        # Using REGEX instead of .Replace - weird behaviour in some cases by latter
        p1 = re.compile(' hours')
        p2 = re.compile(' minutes')
        p3 = re.compile(' day')
        self.addedWhen = p1.sub('hrs', p2.sub('min', p3.sub('day', self._addedWhen)))

        self.date = self._date.replace('/', '.')

    @property
    def category(self):
        if "day" not in self._addedWhen:
            return 'Today'
        elif "1 day" in self._addedWhen:
            return "Yesterday"
        else:
            return re.sub(r'days.*', 'days ago', self._addedWhen)
