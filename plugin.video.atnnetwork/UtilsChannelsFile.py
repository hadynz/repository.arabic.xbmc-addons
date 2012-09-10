import sys
from BeautifulSoup import BeautifulSoup

class Category:
    def __init__(self, categoryEl):
        self.title = categoryEl['title']

class Channel:
    def __init__(self, channelEl):
        self.id = channelEl['id']
        self.title = channelEl['title']
        self.thumbnail = channelEl['thumbnail']

class UtilsChannelsFile:

    _channelsXmlFile = "\\resources\\data\\channels.xml"

    def __init__(self):
        self.pluginPath = sys.modules["__main__"].pluginPath

    def readChannelsFileAsSoup(self):
        handler = open(self.pluginPath + self._channelsXmlFile).read()
        return BeautifulSoup(handler)

    def getCategories(self):
        soup = self.readChannelsFileAsSoup()
        categoryListEl = soup.findAll('category')

        list = []

        for categoryEl in categoryListEl:
            list.append(Category(categoryEl))

        return list

    def getChannelsByCategoryTitle(self, categoryTitle):
        soup = self.readChannelsFileAsSoup()
        channelListEl = soup.find('category', {'title' : categoryTitle}).findAll('channel')

        list = []

        for channelEl in channelListEl:
            list.append(Channel(channelEl))

        return list