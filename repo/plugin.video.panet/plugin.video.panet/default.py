# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
from httplib import HTTP
from urlparse import urlparse



def CATEGORIES():
	addDir('Arab films','http://www.panet.co.il/online/video/movies/movie/',1,'http://reggiebibbs.files.wordpress.com/2007/12/the-movies360-crop.jpg')
	addDir( 'Turkish drama','',1,'')
	addDir( 'Egyptian drama','',1,'')
	addDir( 'Syrian drama','',1,'')
	addDir( 'Lebanese drama','',1,'')
	addDir( 'Golf drama','',1,'')
		
def checkURL(url):
    p = urlparse(url)
    h = HTTP(p[1])
    h.putrequest('HEAD', p[2])
    h.endheaders()
    if h.getreply()[0] == 200: return 1
    else: return 0

                       
def INDEX(url,start,max):
    film=start
	
	
    while film<max :
        film=film+1
        filmo=str(film)
        programurl=[str('http://www.panet.co.il/online/video/movies/movie/'+filmo+'.html')]
        for currurl in programurl:
            url=programurl.pop(0)
            
            if checkURL(url):
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                
                match=(re.compile('name="title" content=(.+?)/>').findall(link))
                
                if len(match) :
                    
                        name= ''.join(match).replace('"', '')
                        
                match2=re.compile('"video_src" href="(.+?)"/>').findall(link)
                if len(match2) :
                        VideoImg= (''.join(match2).replace('"', '').split('&image='))
                        temp=VideoImg.pop(0).strip(' ')
                        thumbnail=VideoImg.pop(0).strip(' ')
		addDir(name,url,2,thumbnail)
		

		
def VIDEOLINKS(url,name):
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match2=re.compile('"video_src" href="(.+?)"/>').findall(link)
                
                if len(match2) :
                        VideoImg= (''.join(match2).replace('"', '').split('&image='))
                        videoPath=VideoImg.pop(0).strip('')
                        videoPath=videoPath[81:]
                        videoPath=videoPath.replace('%3A',':')
                        videoPath=videoPath.replace('%2F','/')
		addLink(name,videoPath,'')
        

                
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




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
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
        INDEX(url,0,10)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',3,'')
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name) 
elif mode==3:
	print ""+url
	INDEX(url,10,20)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',4,'')
elif mode==4:
	print ""+url
	INDEX(url,20,30)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',5,'')
	
elif mode==5:
	print ""+url
	INDEX(url,30,40)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',6,'')
elif mode==6:
	print ""+url
	INDEX(url,40,50)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',7,'')
elif mode==7:
	print ""+url
	INDEX(url,50,60)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',8,'')
	
elif mode==8:
	print ""+url
	INDEX(url,60,70)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',9,'')
elif mode==9:
	print ""+url
	INDEX(url,70,80)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',10,'')
elif mode==10:
	print ""+url
	INDEX(url,80,90)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',11,'')
	
elif mode==11:
	print ""+url
	INDEX(url,90,100)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',12,'')
elif mode==12:
	print ""+url
	INDEX(url,100,110)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',13,'')
elif mode==13:
	print ""+url
	INDEX(url,110,120)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',14,'')
	
elif mode==14:
	print ""+url
	INDEX(url,120,130)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',15,'')

elif mode==15:
	print ""+url
	INDEX(url,130,140)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',16,'')
elif mode==16:
	print ""+url
	INDEX(url,140,150)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',17,'')
	
elif mode==17:
	print ""+url
	INDEX(url,150,160)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',18,'')
	
elif mode==18:
	print ""+url
	INDEX(url,160,170)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',19,'')
elif mode==19:
	print ""+url
	INDEX(url,170,180)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',20,'')
	
elif mode==20:
	print ""+url
	INDEX(url,180,190)
	addDir('View more films >>','http://www.panet.co.il/online/video/movies/movie/',21,'')
elif mode==21:
	print ""+url
	INDEX(url,190,200)
	







xbmcplugin.endOfDirectory(int(sys.argv[1]))
