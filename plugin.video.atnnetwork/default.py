import os
import sys
import xbmcplugin
import xbmcgui
import xbmcaddon

from UtilsCommon import UtilsCommon
from UtilsATN import UtilsATN
from UtilsChannelsFile import UtilsChannelsFile

plugin = int(sys.argv[1])
settings = xbmcaddon.Addon(id='plugin.video.atnnetwork')
language = settings.getLocalizedString
pluginPath = settings.getAddonInfo('path')

utilsATN = UtilsATN()
utilsCommon = UtilsCommon()
utilsChannelsFile = UtilsChannelsFile()

# Setting constants
MODE_LIST_CATEGORY_CHANNELS = 1
MODE_LIST_CHANNELS_FROM_ATN = 2
MODE_PLAY_VIDEO = 3
MODE_SHOW_SETTINGS = 4

def getRootCategories():
    if not(utilsATN.hasValidLogin()):
        addDir(language(30500), MODE_SHOW_SETTINGS)

    else:
        addDir(language(30501), MODE_LIST_CHANNELS_FROM_ATN)
        for category in utilsChannelsFile.getCategories():
            addDir(category.title, MODE_LIST_CATEGORY_CHANNELS, category.title)

    xbmcplugin.endOfDirectory(plugin)

def getCategoryChannels(categoryTitle):
    channelsList = utilsChannelsFile.getChannelsByCategoryTitle(categoryTitle)
    for channel in channelsList:
        addLink(channel.title, channel.id, MODE_PLAY_VIDEO, channel.thumbnail, len(channelsList))

    xbmcplugin.endOfDirectory(plugin)

def getAllATNChannels():
    channels_json = utilsATN.getAllChannels()
    resultsCount = len(channels_json)

    for channel in channels_json:
        addLink(channel['Name'], channel['ID'], MODE_PLAY_VIDEO, channel['Logo'], resultsCount)

    xbmcplugin.endOfDirectory(plugin)

def playVideo(channelID):
    clipStreamingUrl = utilsATN.getChannelStreamUrl(channelID)
    listItem = xbmcgui.ListItem(path=clipStreamingUrl)
    return xbmcplugin.setResolvedUrl(plugin, True, listItem)

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

def login():
    xbmcaddon.Addon(id='plugin.video.atnnetwork').openSettings()
    success = utilsATN.login()

    if not success:
        utilsCommon.showErrorMessage("", language(30602))

def addDir(name, mode, channelName=None):
    u = sys.argv[0] + "?mode=" + str(mode) + "&channelName=" + str(channelName)

    thumbnail = os.path.join(pluginPath, 'art', name.lower() + '.jpg')

    li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    li.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, isFolder=True)
    return ok

def addLink(name, channelID, mode, iconImage, totalItems):
    u = sys.argv[0] + "?channelID=" + str(channelID) + "&mode=" + str(mode)
    li = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconImage)
    li.setInfo(type="Video", infoLabels={"Title": name})
    li.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, totalItems=totalItems)
    return ok

params = get_params()
channelID = None
lastMode = None
channelName = None

try:
    channelID = str(params["channelID"])
except:
    pass
try:
    lastMode = int(params["mode"])
except:
    pass
try:
    channelName = params["channelName"]
except:
    pass

# Controller Logic
if lastMode is None:
    getRootCategories()

elif lastMode == MODE_LIST_CHANNELS_FROM_ATN:
    getAllATNChannels()

elif lastMode == MODE_LIST_CATEGORY_CHANNELS:
    getCategoryChannels(channelName)

elif lastMode == MODE_PLAY_VIDEO:
    playVideo(channelID)

elif lastMode == MODE_SHOW_SETTINGS:
    login()