# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Plugin Tools v1.0.2
#---------------------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube, parsedom and pelisalacarta addons
# Author: 
# Jesús
# tvalacarta@gmail.com
# http://www.mimediacenter.info/plugintools
#---------------------------------------------------------------------------
# Changelog:
# 1.0.0
# - First release
# 1.0.1
# - If find_single_match can't find anything, it returns an empty string
# - Remove addon id from this module, so it remains clean
# 1.0.2
# - Added parameter on "add_item" to say that item is playable
# 1.0.3
# - Added direct play
# - Fixed bug when video isPlayable=True
# 1.0.4
# - Added get_temp_path, get_runtime_path, get_data_path
# - Added get_setting, set_setting, open_settings_dialog and get_localized_string
# - Added keyboard_input
# - Added message
#---------------------------------------------------------------------------

import xbmc
import xbmcplugin
import xbmcaddon
import xbmcgui
import urllib
import urllib2
import re
import sys
import os

module_log_enabled = False

# Write something on XBMC log
def log(message):
    xbmc.log(message)

# Write this module messages on XBMC log
def _log(message):
    if module_log_enabled:
        xbmc.log("plugintools."+message)

# Parse XBMC params - based on script.module.parsedom addon    
def get_params():
    _log("get_params")
    
    param_string = sys.argv[2]
    
    _log("get_params "+str(param_string))
    
    commands = {}

    if param_string:
        split_commands = param_string[param_string.find('?') + 1:].split('&')
    
        for command in split_commands:
            _log("get_params command="+str(command))
            if len(command) > 0:
                if "=" in command:
                    split_command = command.split('=')
                    key = split_command[0]
                    value = urllib.unquote_plus(split_command[1])
                    commands[key] = value
                else:
                    commands[command] = ""
    
    _log("get_params "+repr(commands))
    return commands

# Fetch text content from an URL
def read(url):
    _log("read "+url)

    f = urllib2.urlopen(url)
    data = f.read()
    f.close()
    
    return data

# Parse string and extracts multiple matches using regular expressions
def find_multiple_matches(text,pattern):
    _log("find_multiple_matches pattern="+pattern)
    
    matches = re.findall(pattern,text,re.DOTALL)

    return matches

# Parse string and extracts first match as a string
def find_single_match(text,pattern):
    _log("find_single_match pattern="+pattern)

    result = ""
    try:    
        matches = re.findall(pattern,text, flags=re.DOTALL)
        result = matches[0]
    except:
        result = ""

    return result

def add_item( action="" , title="" , plot="" , url="" ,thumbnail="" , isPlayable = False, folder=True ):
    _log("add_item action=["+action+"] title=["+title+"] url=["+url+"] thumbnail=["+thumbnail+"] isPlayable=["+str(isPlayable)+"] folder=["+str(folder)+"]")

    listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
    listitem.setInfo( "video", { "Title" : title, "FileName" : title, "Plot" : plot } )
    
    if url.startswith("plugin://"):
        itemurl = url
        listitem.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)
    elif isPlayable:
        listitem.setProperty("Video", "true")
        listitem.setProperty('IsPlayable', 'true')
        itemurl = '%s?action=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , action , urllib.quote_plus( title ) , urllib.quote_plus(url) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ))
        xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)
    else:
        itemurl = '%s?action=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , action , urllib.quote_plus( title ) , urllib.quote_plus(url) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ))
        xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)

def close_item_list():
    _log("close_item_list")

    xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)

def play_resolved_url(url):
    _log("play_resolved_url ["+url+"]")

    listitem = xbmcgui.ListItem(path=url)
    listitem.setProperty('IsPlayable', 'true')
    return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def direct_play(url):
    _log("direct_play ["+url+"]")

    title = ""

    try:
        xlistitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", path=url)
    except:
        xlistitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", )
    xlistitem.setInfo( "video", { "Title": title } )

    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    playlist.clear()
    playlist.add( url, xlistitem )

    player_type = xbmc.PLAYER_CORE_AUTO
    xbmcPlayer = xbmc.Player( player_type )
    xbmcPlayer.play(playlist)

def get_temp_path():
    _log("get_temp_path")

    dev = xbmc.translatePath( "special://temp/" )
    _log("get_temp_path ->'"+str(dev)+"'")

    return dev

def get_runtime_path():
    _log("get_runtime_path")

    dev = xbmc.translatePath( __settings__.getAddonInfo('Path') )
    _log("get_runtime_path ->'"+str(dev)+"'")

    return dev

def get_data_path():
    _log("get_data_path")

    dev = xbmc.translatePath( __settings__.getAddonInfo('Profile') )
    
    # Parche para XBMC4XBOX
    if not os.path.exists(dev):
        os.makedirs(dev)

    _log("get_data_path ->'"+str(dev)+"'")

    return dev

def get_setting(name):
    _log("get_setting name='"+name+"'")

    dev = __settings__.getSetting( name )

    _log("get_setting ->'"+str(dev)+"'")

    return dev

def set_setting(name,value):
    _log("set_setting name='"+name+"','"+value+"'")

    __settings__.setSetting( name,value )

def open_settings_dialog():
    _log("open_settings_dialog")

    __settings__.openSettings()

def get_localized_string(code):
    _log("get_localized_string code="+str(code))

    dev = __language__(code)

    try:
        dev = dev.encode("utf-8")
    except:
        pass

    _log("get_localized_string ->'"+dev+"'")

    return dev

def keyboard_input(default_text=""):
    _log("keyboard_input default_text='"+default_text+"'")

    keyboard = xbmc.Keyboard(default_text)
    keyboard.doModal()
    
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
    else:
        tecleado = ""

    _log("keyboard_input ->'"+tecleado+"'")

    return tecleado

def message(text1, text2="", text3=""):
    if text3=="":
        xbmcgui.Dialog().ok( text1 , text2 )
    elif text2=="":
        xbmcgui.Dialog().ok( "" , text1 )
    else:
        xbmcgui.Dialog().ok( text1 , text2 , text3 )

f = open( os.path.join( os.path.dirname(__file__) , "addon.xml") )
data = f.read()
f.close()

addon_id = find_single_match(data,'id="([^"]+)"')
if addon_id=="":
    addon_id = find_single_match(data,"id='([^']+)'")

__settings__ = xbmcaddon.Addon(id=addon_id)
__language__ = __settings__.getLocalizedString
