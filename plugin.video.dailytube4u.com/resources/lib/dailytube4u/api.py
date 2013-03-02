from scraper import (get_clips_for_show, get_channels)

'''The main API object. Useful as a starting point to get available subjects. '''
class DailyTube4uAPI():

    def get_channels(self):
        return get_channels()

    def get_clips_for_show(self, show_path):
        return get_clips_for_show(show_path)

