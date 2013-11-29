import re


class ChannelItem:
    def __init__(self, el=None, json=None):
        if json is None:
            self.__parseElement(el)
        else:
            self.__parseJSON(json)

    def __parseElement(self, el):
        anchorEl = el.find('a')
        match_channel_name = re.match(r'.*\(\'(.*?)\'.*', anchorEl['onclick'], re.M | re.I)

        self.title = str(anchorEl.findAll('span')[-1].contents[0])  # Copy out channel name, and not reference
        self.thumbnail = anchorEl.find('img')['src']
        self.path = match_channel_name.group(1)
        self.isHD = len(anchorEl.findAll('font')) > 2

    def __parseJSON(self, json):
        self.title = json['title']
        self.thumbnail = json['thumbnail']
        self.path = json['path']
        self.isHD = False

    def display_name(self):
        if self.isHD:
            return '%s [COLOR red]HD[/COLOR]' % self.title

        return self.title

