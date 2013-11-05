from scraper import (get_channels, get_channel_programs, get_program_media, get_media_stream)

class MediaType:
    EPISODE = 'episodes'
    CLIP = 'clips'

class ShahidNetAPI():

    def get_channels(self):
        return get_channels()

    def get_channel_programs(self, channelID):
        return get_channel_programs(channelID)

    '''
        Media Type can either be "episodes" or "clips"
    '''
    def get_program_media(self, programID, mediaType):
        return get_program_media(programID, mediaType)

    '''
        Quality can be one of the following options:
            -> "360p LOW", "720p HD", "240p LOWEST", "520p HIGH"
    '''
    def get_media_stream(self, quality, programID, mediaType, mediaID):
        return get_media_stream(quality, programID, mediaType, mediaID)


