# -*- coding: utf-8 -*-
import xbmc


class MyXBMCPlayer(xbmc.Player):
    def __init__( self, *args, **kwargs ):
        self.is_active = True
        self.urlplayed = False
        print "#XBMCPlayer#"
    
    def onPlayBackPaused( self ):
        xbmc.log("#Im paused#")
        
    def onPlayBackResumed( self ):
        xbmc.log("#Im Resumed #")
        
    def onPlayBackStarted( self ):
        print "#Playback Started#"
        try:
            print "#Im playing :: " + self.getPlayingFile()
        except:
            print "#I failed get what Im playing#"
        self.urlplayed = True
            
    def onPlayBackEnded( self ):
        print "#Playback Ended#"
        self.is_active = False
        
    def onPlayBackStopped( self ):
        print "## Playback Stopped ##"
        self.is_active = False

