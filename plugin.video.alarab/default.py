# -*- coding: utf8 -*-
import urllib,urllib2,xbmcplugin,xbmcgui,xbmcaddon
import re

__settings__ = xbmcaddon.Addon(id='plugin.video.alarab')
__icon__ = __settings__.getAddonInfo('icon')
__fanart__ = __settings__.getAddonInfo('fanart')
__language__ = __settings__.getLocalizedString
_thisPlugin = int(sys.argv[1])
_pluginName = (sys.argv[0])




def CATEGORIES():
	addDir("RAMADAN MORROCAN SERIES","/ramadan2016/مغربية",2,"http://wadeni.com/images/icons/0alarab-net.jpg")
	addDir("RAMADAN SYRIAN SERIES","http://tv1.alarab.com/ramadan2016/سورية",2,"http://wadeni.com/images/icons/0alarab-net.jpg")
	addDir("RAMADAN EGYPTIAN SERIES","http://tv1.alarab.net/ramadan2016/مصرية",2,"http://wadeni.com/images/icons/0alarab-net.jpg")
	addDir("RAMADAN KHALIJI SERIES","http://tv1.alarab.net/ramadan2016/خليجية",2,"http://wadeni.com/images/icons/0alarab-net.jpg")
	addDir("RAMADAN LEBANESE SERIES","http://tv1.alarab.net/ramadan2016/لبانينة",2,"http://wadeni.com/images/icons/0alarab-net.jpg")
	addDir("RAMADAN KUWAITI SERIES","http://tv1.alarab.net/ramadan2016/كويتية",2,"http://wadeni.com/images/icons/0alarab-net.jpg")
	addDir("RAMADAN SAUDI SERIES","http://tv1.alarab.net/ramadan2016/سعودية",2,"http://wadeni.com/images/icons/0alarab-net.jpg")
	addDir("RAMADAN JORDANIAN SERIES","http://tv1.alarab.net/ramadan2016/اردنية",2,"http://wadeni.com/images/icons/0alarab-net.jpg")
	addDir("RAMADAN BAHRAINI SERIES","http://tv1.alarab.net/ramadan2016/بحرينية",2,"http://wadeni.com/images/icons/0alarab-net.jpg")
	addDir("RAMADAN EMARATI SERIES","http://tv1.alarab.net/ramadan2016/اماراتية",2,"http://wadeni.com/images/icons/0alarab-net.jpg")

def getMovie(url):
	openerx = urllib2.build_opener()
	sockx = openerx.open(url)
	contentx = sockx.read()
	sockx.close()
	wieviele = contentx.count('<div class="video-box">')
	teilen = contentx.split('<div class="video-box">')
	for i in range(1,wieviele+1):
		linkjetzt = teilen[i].split('"')
		imgjetzt = linkjetzt[3]
		urljetzt = "http://tv1.alarab.net/"+linkjetzt[1]
		namejetzt = linkjetzt[5]
		addLink(namejetzt,urljetzt,4,imgjetzt)
	seitenzahl1 = contentx.split('<div class="pages"><center>')
	seitenzahl2 = seitenzahl1[1].split("</div></center></div>")
	seitenzahl3 = seitenzahl2[0].split('tsc_3d_button blue"')
	seitenzahl4 = seitenzahl3[1].split(">")
	seitenzahl5 = seitenzahl4[1].split("<")
	seitenzahlselected = seitenzahl5[0]
	seitenwieviel = seitenzahl2[0].count("href")
	if int(seitenzahlselected) < seitenwieviel:
		nextpagelink1 = seitenzahl3[1].split('"')
		nextpagelink = "http://tv1.alarab.net" + nextpagelink1[7]
		addDir("("+seitenzahlselected+"/"+str(seitenwieviel)+") Next Page",nextpagelink,1,"http://wadeni.com/images/icons/0alarab-net.jpg")

def getSerie(url):
	openerx = urllib2.build_opener()
	sockx = openerx.open(url)
	contentx = sockx.read()
	sockx.close()
	wieviele = contentx.count('<div class="video-box">')
	teilen = contentx.split('<div class="video-box">')
	for i in range(1,wieviele+1):
		linkjetzt = teilen[i].split('"')
		imgjetzt = linkjetzt[3]
		urljetzt = "http://tv1.alarab.net/"+linkjetzt[1]
		namejetzt = linkjetzt[5]
		addDir(namejetzt,urljetzt,3,imgjetzt)
	seitenzahl1 = contentx.split('<div class="pages"><center>')
	seitenzahl2 = seitenzahl1[1].split("</div></center></div>")
	seitenzahl3 = seitenzahl2[0].split('tsc_3d_button blue"')
	seitenzahl4 = seitenzahl3[1].split(">")
	seitenzahl5 = seitenzahl4[1].split("<")
	seitenzahlselected = seitenzahl5[0]
	seitenwieviel = seitenzahl2[0].count("href")
	if int(seitenzahlselected) < seitenwieviel:
		nextpagelink1 = seitenzahl3[1].split('"')
		nextpagelink = "http://tv1.alarab.net" + nextpagelink1[7]
		addDir("("+seitenzahlselected+"/"+str(seitenwieviel)+") Next Page",nextpagelink,2,"http://wadeni.com/images/icons/0alarab-net.jpg")

def getSerieFolge(url):
	openerx = urllib2.build_opener()
	sockx = openerx.open(url)
	contentx = sockx.read()
	sockx.close()
	wieviele = contentx.count('<div class="video-box">')
	teilen = contentx.split('<div class="video-box">')
	for i in range(1,wieviele+1):
		linkjetzt = teilen[i].split('"')
		imgjetzt = linkjetzt[3]
		urljetzt = "http://tv1.alarab.net/"+linkjetzt[1]
		namejetzt = linkjetzt[5]
		addLink(namejetzt,urljetzt,4,imgjetzt)
	seitenzahl1 = contentx.split('<div class="pages"><center>')
	seitenzahl2 = seitenzahl1[1].split("</div></center></div>")
	seitenzahl3 = seitenzahl2[0].split('tsc_3d_button blue"')
	seitenzahl4 = seitenzahl3[1].split(">")
	seitenzahl5 = seitenzahl4[1].split("<")
	seitenzahlselected = seitenzahl5[0]
	seitenwieviel = seitenzahl2[0].count("href")
	if int(seitenzahlselected) < seitenwieviel:
		nextpagelink1 = seitenzahl3[1].split('"')
		nextpagelink = "http://tv1.alarab.net" + nextpagelink1[7]
		addDir("("+seitenzahlselected+"/"+str(seitenwieviel)+") Next Page",nextpagelink,3,"http://wadeni.com/images/icons/0alarab-net.jpg")

def PlayMovie(url):
		opener = urllib2.build_opener()
		sock = opener.open(url)
		content = sock.read()
		sock.close()
		source1 = content.split('http://alarabplayers.alarab.net')
		fileright = getFlvAddress(source1[0])
		print 'Used Url is:', fileright		
		listItem = xbmcgui.ListItem(path=str(fileright))
		xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)

def getFlvAddress(par_sHtmlContent):
		# search for the .flv address and change the flv. prefix to flv2.	
		sFlvAddress = re.search(r'file=.*?\.flv', par_sHtmlContent, re.DOTALL)
		
		sFlvAddress = sFlvAddress.group()

		iHttpStartIndex = sFlvAddress.find('=') 

		sFinalAndCorrectedFlvAddress = sFlvAddress[iHttpStartIndex+1:].replace('flv.', 'flv2.')
		sFinalAndCorrectedFlvAddress = sFinalAndCorrectedFlvAddress.replace('/flv/','/new/flv/')
		
		return sFinalAndCorrectedFlvAddress

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param



def addLink(name,url,mode,iconimage):
    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty("IsPlayable","true");
    ok=xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=False)
    return ok



def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


params=get_params()
url=None
name=None
mode=None



try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
elif mode==1:
	print ""+url
	getMovie(url)
elif mode==2:
	print ""+url
	getSerie(url)
elif mode==3:
	print ""+url
	getSerieFolge(url)
elif mode==4:
	print ""+url
	PlayMovie(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
