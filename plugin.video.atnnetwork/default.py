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
MODE_LIST_ATN_PACKAGES = 2
MODE_LIST_ATN_PACKAGE_CHANNELS = 3
MODE_PLAY_VIDEO = 4
MODE_SHOW_SETTINGS = 5

ATN_ARABIC_PACKAGE_NO = 15

def getRootCategories():
    if not(utilsATN.hasValidLogin()):
        addDir(language(30500), MODE_SHOW_SETTINGS, '')

    else:
        addDir(language(30501), MODE_LIST_ATN_PACKAGES, '')
        for category in utilsChannelsFile.getCategories():
            addDir(category.title, MODE_LIST_CATEGORY_CHANNELS, ATN_ARABIC_PACKAGE_NO)

    xbmcplugin.endOfDirectory(plugin)

def listChannelsForCategory(categoryTitle):
    channelsList = utilsChannelsFile.getChannelsByCategoryTitle(categoryTitle)
    for channel in channelsList:
        addLink(channel.title, channel.id, MODE_PLAY_VIDEO, ATN_ARABIC_PACKAGE_NO, channel.thumbnail, len(channelsList))

    xbmcplugin.endOfDirectory(plugin)

def listATNPackages():
    packages = utilsATN.getATNSubscriptionPackages()

    for package in packages:
        print package['Name'] + ', ' + package['ID']
        addDir(package['Name'], MODE_LIST_ATN_PACKAGE_CHANNELS, package['ID'])

    xbmcplugin.endOfDirectory(plugin)

def listChannelsForATNPackage(packageNo):
    channels_json = utilsATN.getAllChannels(packageNo)
    resultsCount = len(channels_json)

    for channel in channels_json:
        addLink(channel['Name'], channel['ID'], MODE_PLAY_VIDEO, packageNo, channel['Logo'], resultsCount)

    xbmcplugin.endOfDirectory(plugin)

def playVideo(channelID, packageNo):
    clipStreamingUrl = utilsATN.getChannelStreamUrl(channelID, packageNo)
    listItem = xbmcgui.ListItem(path=clipStreamingUrl)

    # Check if user's current subscription is upto date and valid
    if utilsATN.login() is False:
        dialog = xbmcgui.Dialog()
        dialog.ok(language(30603), language(30604), '', language(30605))
        return

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

def addDir(name, mode, packageNo):
    u = sys.argv[0] + "?mode=" + str(mode) + "&packageNo=" + str(packageNo) + "&channelName=" + str(name)

    thumbnail = os.path.join(pluginPath, 'art', name.lower() + '.jpg')

    li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    li.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, isFolder=True)
    return ok

def addLink(name, channelID, mode, packageNo, iconImage, totalItems):
    u = sys.argv[0] + "?channelID=" + str(channelID) + "&packageNo=" + str(packageNo) + "&mode=" + str(mode)
    li = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconImage)
    li.setInfo(type="Video", infoLabels={"Title": name})
    li.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, totalItems=totalItems)
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

channelID   = tryParse(params, "channelID")
channelName = tryParse(params, "channelName")
packageNo   = tryParse(params, "packageNo")

#
# Controller Logic
print "Current URL: " + sys.argv[2]

if lastMode is None:
    getRootCategories()

elif lastMode == MODE_LIST_ATN_PACKAGES:
    listATNPackages()

elif lastMode == MODE_LIST_ATN_PACKAGE_CHANNELS:
    listChannelsForATNPackage(packageNo)

elif lastMode == MODE_LIST_CATEGORY_CHANNELS:
    listChannelsForCategory(channelName)

elif lastMode == MODE_PLAY_VIDEO:
    playVideo(channelID, packageNo)

elif lastMode == MODE_SHOW_SETTINGS:
    login()