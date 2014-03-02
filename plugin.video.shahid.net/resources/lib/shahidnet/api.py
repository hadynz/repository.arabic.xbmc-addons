from scraper import get_most_watched, get_filtered_programs
from webservice import (get_channels, get_channel_programs, get_program_media, get_media_stream_by_media_id, get_media_stream_by_url, search)


class ShahidNetAPI:


    def get_channels(self):
        """
        :return: List of Channels
        :rtype : list ChannelItem
        """
        return get_channels()


    def get_channel_programs(self, channelID):
        """
        :param channelID:
        :return: List of programs for a Channel ID
        :rtype: list of ProgramItem
        """
        return get_channel_programs(channelID)


    def get_program_media(self, programID, mediaType):
        """
        :param programID: Program ID
        :param mediaType: Media type - either 'episodes' or 'clips'
        :return: List of media items for the current Program ID and media type
        :rtype: list of MediaItem
        """
        return get_program_media(programID, mediaType)


    def get_media_stream_by_media_id(self, quality, programID, mediaType, mediaID):
        '''
        Quality can be one of the following options:
            -> "360p LOW", "720p HD", "240p LOWEST", "520p HIGH"
        '''
        return get_media_stream_by_media_id(quality, programID, mediaType, mediaID)


    def get_media_stream_by_url(self, quality, video_url):
        return get_media_stream_by_url(quality, video_url)


    def get_most_watched(self, mediaType):
        return get_most_watched(mediaType)


    def search(self, search_term, limit=20):
        return search(search_term, limit)

    def get_filtered_programs(self, dialectId, genreId, typeId):
        return get_filtered_programs(dialectId, genreId, typeId)