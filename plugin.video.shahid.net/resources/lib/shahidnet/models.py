from utils import isEnglish


class MediaType:
    EPISODE = 'episodes'
    CLIP = 'clips'
    PROGRAM = 'programs'


class FilterType:
    GENRE = 'genre'
    DIALECT = 'dialect'
    PROGRAM_Type = 'program'


class ChannelItem:
    def __init__(self, json):
        self.id = json['id']
        self.name = json['name'].strip()
        self.thumbnail = json['thumb_url']
        self.bgImage = json['image_url']


class ProgramItem(ChannelItem):
    def __init__(self, json):
        ChannelItem.__init__(self, json)

        self.episodeCount = int(json['episode_count'])
        self.clipCount = int(json['clip_count'])
        self.viewCount = json['total_views']

    def hasEpisodesOnly(self):
        return int(self.episodeCount) > 0 and int(self.clipCount) is 0

    def hasClipsOnly(self):
        return int(self.episodeCount) is 0 and int(self.clipCount) > 0


class MediaItem():
    def __init__(self, json):
        self.id = json.get("id", '')
        self.type = json.get("type", '').encode('utf-8')
        self.description = json.get("summary", '').strip().encode('utf-8')
        self.seriesName = json.get("series_name", '').encode("utf8")
        self.seriesId = json.get("series_id", '')
        self.episodeNumber = json.get("episode_number", '').encode('utf-8')
        self.seasonNumber = json.get("season_number", '').encode('utf-8')
        self.viewCount = json.get("total_views", '')
        self.thumbnail = json.get("thumb_url", '')
        self.duration = json.get("duration", '')
        self.dateAdded = json.get("tx_date", '')
        self.url = json.get("url", '')  # populated only for items scraped from the web

    def displayName(self):

        display_list = ['[COLOR white][B]%s[/B][/COLOR]' % self.seriesName]

        if self.description:
            if isEnglish(self.description.decode('utf-8')):
                display_list.append('-')

            if not isEnglish(self.description.decode('utf-8')):
                display_list.append('I')

            display_list.append(self.description)

        display_list.append('{start}Episode {no}{end}'.format(start='(' if self.description else '',
                                                              no=self.episodeNumber,
                                                              end=',' if self.description else ''
        ))

        display_list.append('{start}Season {no})'.format(start='' if self.description else '(', no=self.seasonNumber))

        return ' '.join(display_list)


    def isEpisode(self):
        return self.type == 'episode'

    def isClip(self):
        return self.type == 'clip'
