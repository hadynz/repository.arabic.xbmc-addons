import sys
import urllib
import xbmcplugin
import xbmcgui
import xbmcaddon

import ShahidUtils

plugin = int(sys.argv[1])
settings = xbmcaddon.Addon(id='plugin.video.shahid.net')
language = settings.getLocalizedString
pluginPath = settings.getAddonInfo('path')

ShahidUtils = ShahidUtils.ShahidUtils()

# Setting constants
MODE_LIST_CHANNELS = 1
MODE_LIST_PROGRAMS = 2
MODE_LIST_VIDEOS = 3
MODE_PLAY_VIDEO = 4
MODE_LIST_STREAMS = 5

def getRootCategories():
    addLink("Channels", MODE_LIST_CHANNELS)
    #addLink("Programs", MODE_LIST_CATEGORY_CHANNELS)
    #addLink("Episodes", MODE_LIST_CATEGORY_CHANNELS)
    #addLink("Clips",    MODE_LIST_CATEGORY_CHANNELS)
    xbmcplugin.endOfDirectory(plugin)

def listChannels():
    modelChannels = ShahidUtils.getChannelList()
    for channel in sorted(modelChannels, key=lambda c: c.name):
        params = "channelID={0}".format(channel.id)
        addLink(channel.name, MODE_LIST_PROGRAMS, params, channel.image_thumb, channel.image_fanart)

    xbmcplugin.endOfDirectory(plugin)

def listPrograms(channelID):
    modelPrograms = ShahidUtils.getProgramList(channelID)

    for program in sorted(modelPrograms, key=lambda p: p.name):
        params = "programID={0}&episodesCount={1}&clipsCount={2}".format(program.id, str(program.episode_count), str(program.clip_count))

        # Append videoType if possible
        if program.episode_count > 0 and program.clip_count == 0:
            params += "&videoType=%s" % "episodes"

        if program.episode_count == 0 and program.clip_count > 0:
            params += "&videoType=%s" % "clips"

        addLink(program.name, MODE_LIST_VIDEOS, params, program.image_thumb, program.image_fanart)

    xbmcplugin.endOfDirectory(plugin)

def showEpisodeClipFolders(programID, episodesCount, clipsCount):
    paramsPattern = "programID={0}&videoType={1}"

    addLink("Episodes (%s)" % episodesCount, MODE_LIST_VIDEOS, paramsPattern.format(programID, "episodes"))
    addLink("Clips (%s)" % clipsCount, MODE_LIST_VIDEOS, paramsPattern.format(programID, "clips"))

    xbmcplugin.endOfDirectory(plugin)

def listVideos(programID, videoType):
    paramsPattern = "programID={0}&videoType={1}&clipID={2}"
    list = ShahidUtils.getVideoList(programID, videoType)

    for item in filter(lambda x: x.coming_soon == 0 , list):
        addLink(item.name, MODE_LIST_STREAMS, paramsPattern.format(programID, videoType, item.id, item.name), item.image_thumb, isFolder=False)

    xbmcplugin.endOfDirectory(plugin)

def listStreams(programID, clipID):
    paramsPattern = "playUrl={0}"
    streamList = ShahidUtils.getPlayStreamOptions(programID, clipID)

    # If only one stream is returned, just simply play it by default for user
    if len(streamList) == 1:
        url = urllib.quote_plus(streamList[0].url)
        return playVideo(url)

    # Many options are returned, list them to our dear user
    else:
        for item in streamList:
            url = urllib.quote_plus(item.url)
            addLink(item.title, MODE_PLAY_VIDEO, paramsPattern.format(url), None, isFolder=False)

        xbmcplugin.endOfDirectory(plugin)

def playVideo(playUrl):
    playUrl = urllib.unquote_plus(playUrl)

    item = xbmcgui.ListItem(path=playUrl)
    item.setInfo(type = 'video', infoLabels = {'Title': None})
    return xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=item)

def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param

def addLink(name, mode, params=None, thumbnailImage="DefaultVideo.png", fanArtImage=None, isFolder=True):
    if params is None:
        params = ''

    u = sys.argv[0] + "?mode={0}&{1}".format(str(mode), params)

    li = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnailImage)
    li.setInfo(type="Video", infoLabels={"Title": name})

    if mode == MODE_PLAY_VIDEO or \
       mode == MODE_LIST_STREAMS:   # Temporary hack; we are currently always returning one stream to play
        li.setProperty('IsPlayable', 'true')

    if fanArtImage is not None:
        li.setProperty('fanart_image', fanArtImage)

    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, isFolder=isFolder)
    return ok

def tryParse(array, key):
    value = None

    try:
        value = array[key]
    except:
        pass

    return value

# ---------------------------------------------------------------------------------

#
# Parse query string parameters
params = get_params()
lastMode = None

try:
    lastMode = int(params["mode"])
except:
    pass

channelID       = tryParse(params, "channelID")
programID       = tryParse(params, "programID")
episodesCount   = tryParse(params, "episodesCount")
clipsCount      = tryParse(params, "clipsCount")
videoType       = tryParse(params, "videoType")
clipID          = tryParse(params, "clipID")
playUrl         = tryParse(params, "playUrl")

#
# Controller Logic
print "Current URL: " + sys.argv[2]

if lastMode is None:
    getRootCategories()

elif lastMode == MODE_LIST_CHANNELS:
    listChannels()

elif lastMode == MODE_LIST_PROGRAMS:
    listPrograms(channelID)

elif lastMode == MODE_LIST_VIDEOS:
    if videoType is not None:
        listVideos(programID, videoType)
    else:
        showEpisodeClipFolders(programID, episodesCount, clipsCount)

elif lastMode == MODE_LIST_STREAMS:
    listStreams(programID, clipID)

elif lastMode == MODE_PLAY_VIDEO:
    playVideo(playUrl)
