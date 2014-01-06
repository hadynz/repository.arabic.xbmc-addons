# -*- coding: utf8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import urllib2,urllib
import re
import httplib
import time,itertools

__settings__ = xbmcaddon.Addon(id='plugin.video.dardarkom')
__icon__ = __settings__.getAddonInfo('icon')
__fanart__ = __settings__.getAddonInfo('fanart')
__language__ = __settings__.getLocalizedString
_thisPlugin = int(sys.argv[1])
_pluginName = (sys.argv[0])



def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner
httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)

def getCategories():
	addDir('أفلام اجنبية اون لاين','http://www.dardarkom.com/filme-enline/filme-gharbi',1,'http://www.theonestopfunshop.com/product_images/uploaded_images/movie-night.jpg',1,7,'DESCRIPTION','0.0',"N/A","N/A","N/A","N/A","N/A","N/A")
	addDir('أفلام هندية اون لاين','http://www.dardarkom.com/hindi-movies',4,'http://www.theonestopfunshop.com/product_images/uploaded_images/movie-night.jpg',1,7,'DESCRIPTION','0.0',"N/A","N/A","N/A","N/A","N/A","N/A")
	addDir('افلام اسيوية','http://www.dardarkom.com/watch-asian-movies-on-line',3,'http://www.theonestopfunshop.com/product_images/uploaded_images/movie-night.jpg',1,30,'DESCRIPTION','0.0',"N/A","N/A","N/A","N/A","N/A","N/A")
	addDir('أفلام اوروبية عالمية','http://www.dardarkom.com/watch-european-movies',1,'http://www.theonestopfunshop.com/product_images/uploaded_images/movie-night.jpg',1,7,'DESCRIPTION','0.0',"N/A","N/A","N/A","N/A","N/A","N/A")
	addDir('أفلام انمي كرتون اون لاين','http://www.dardarkom.com/anime',1,'http://www.theonestopfunshop.com/product_images/uploaded_images/movie-night.jpg',1,7,'DESCRIPTION','0.0',"N/A","N/A","N/A","N/A","N/A","N/A")
	addDir('أفلام وثائقية اون لاين','http://www.dardarkom.com/documentary-films',5,'http://www.theonestopfunshop.com/product_images/uploaded_images/movie-night.jpg',1,10,'DESCRIPTION','0.0',"N/A","N/A","N/A","N/A","N/A","N/A")
	addDir('أفلام مصرية أون لاين','http://www.dardarkom.com/filme-enline/filme-egypt',3,'http://www.theonestopfunshop.com/product_images/uploaded_images/movie-night.jpg',1,30,'DESCRIPTION','0.0',"N/A","N/A","N/A","N/A","N/A","N/A")
	addDir('أفلام مصرية قديمة أون لاين','http://www.dardarkom.com/filme-enline/classic',5,'http://www.theonestopfunshop.com/product_images/uploaded_images/movie-night.jpg',1,10,'DESCRIPTION','0.0',"N/A","N/A","N/A","N/A","N/A","N/A")
	addDir('أفلام مغربية اون لاين','http://www.dardarkom.com/filme-enline/filme-maroc',5,'http://www.theonestopfunshop.com/product_images/uploaded_images/movie-night.jpg',1,7,'DESCRIPTION','0.0',"N/A","N/A","N/A","N/A","N/A","N/A")
	addDir('أفلام عربية اون لاين','http://www.dardarkom.com/filme-enline/arabic',5,'http://www.theonestopfunshop.com/product_images/uploaded_images/movie-night.jpg',1,10,'DESCRIPTION','0.0',"N/A","N/A","N/A","N/A","N/A","N/A")

def removeArabicCharsFromString(myString):
    finalString=''
    allowedChars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz- "
    for chars in myString:
        if chars in allowedChars:
            
            finalString= finalString+chars
            
    return str(finalString).strip()
	
	
def getImdbCred(movieName):
    
    movieName=str(movieName).replace(" ", "%20")
    url='http://www.omdbapi.com/?t='+str(movieName)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    myImdbArray={"Year":"","Genre":"","Poster":"", "Plot":"","imdbRating":"","Actors":"","Runtime":"","Writer":"","Director":""}
    
    if 'Response":"False"' in str(link):
		myImdbArray["Year"]="No Year found"
		myImdbArray["Genre"]="No Genre found"
		myImdbArray["Poster"]="No Poster found"
		myImdbArray["Plot"]="No Plot found"
		myImdbArray["imdbRating"]="No Rating found"
		myImdbArray["Actors"]="No Actors found"
		myImdbArray["Runtime"]="No Runtime found"
		myImdbArray["Writer"]="No Writer found"
		myImdbArray["Director"]="No Director found"
		 
        
    if 'Response":"True"' in str(link):
        try:
            Year=(re.compile('"Year":"(.+?)",').findall(link))
            Year=str(Year).replace("['", "").replace("']", "").strip()
            myImdbArray["Year"]=Year
        except:
            myImdbArray["Year"]="No Year found"
            pass
        
        try:
            Genre=(re.compile('"Genre":"(.+?)",').findall(link))
            Genre=str(Genre).replace("['", "").replace("']", "").strip()
            myImdbArray["Genre"]=Genre
        except:
            myImdbArray["Genre"]="No Genre found"
            pass
        
        try:
            Poster=(re.compile('"Poster":"(.+?)",').findall(link))
            Poster=str(Poster).replace("['", "").replace("']", "").strip()
            myImdbArray["Poster"]=Poster
           
        except:
            myImdbArray["Poster"]="No Poster found"
            pass
        
        try:
            Plot=(re.compile('"Plot":"(.+?)",').findall(link))
            Plot=str(Plot).replace("['", "").replace("']", "").strip()
            myImdbArray["Plot"]=Plot
           
        except:
            myImdbArray["Plot"]="No Plot found"
            pass
        
        try:
            imdbRating=(re.compile('"imdbRating":"(.+?)",').findall(link))
            imdbRating=str(imdbRating).replace("['", "").replace("']", "").strip()
            myImdbArray["imdbRating"]=imdbRating
            
        except:
            myImdbArray["imdbRating"]="No Rating found"
            pass
        
        try:
            Actors=(re.compile('"Actors":"(.+?)",').findall(link))
            Actors=str(Actors).replace("['", "").replace("']", "").strip()
            myImdbArray["Actors"]=Actors
            
        except:
            myImdbArray["Actors"]="No Actors found"
            pass
        
        try:
            Writer=(re.compile('"Writer":"(.+?)",').findall(link))
            Writer=str(Writer).replace("['", "").replace("']", "").strip()
            myImdbArray["Writer"]=Writer
            
        except:
            myImdbArray["Writer"]="No Writer found"
            pass
        
        try:
            Director=(re.compile('"Director":"(.+?)",').findall(link))
            Director=str(Director).replace("['", "").replace("']", "").strip()
            myImdbArray["Director"]=Director
            
        except:
            myImdbArray["Director"]="No Director found"
            pass
        
        try:
            
            Runtime=(re.compile('"Runtime":"(.+?)",').findall(link))
            Runtime=str(Runtime).replace("['", "").replace("']", "").strip()
            
            if 'h' not in Runtime:
                Runtime=str(Runtime).replace("min", "").strip()
                myImdbArray["Runtime"]=Runtime 
                            
            elif 'h' and 'min' in Runtime:
                
                Runtime=str(Runtime).split("h")
                hours= 60*int(Runtime[0])
                minutes=str(Runtime[1]).replace("min", "")
                Runtime=int(minutes)+ hours
                myImdbArray["Runtime"]=Runtime
                        
            elif 'h' in Runtime and not "min" in Runtime:
                Runtime=str(Runtime).replace("h", "").strip()
                Runtime=60*int(Runtime)
                myImdbArray["Runtime"]=Runtime
                
        except:
            myImdbArray["Runtime"]="No Runtime found"
            pass
    return myImdbArray
	
def indexIndian(url,initial,max,plot,rating,genre,cast,year,duration,writer,director):
	try:
		for counter in range(initial,max):
			dlg = xbmcgui.DialogProgress()
			line1 = 'Getting the movies...'
			dlg.create('In progress, Please wait...', line1)
			percent = int((counter * 100) / max)
			label = str(counter)+" out of "+str(max)+" pages"
			dlg.update(percent, line1, label)
			
			req = urllib2.Request(url+'/page/'+str(counter)+'/')
			response = urllib2.urlopen(req)
			link=response.read()
			url_target=(re.compile('<a href="(.+?)"><font color="(.+?)">(.+?)</font>   </a>').findall(link))
			url_2=(re.compile('<a href="(.+?)" onclick="return hs.expand').findall(link))
			target= re.findall(r'<div  style="font-family:Tahoma;font-size:9pt;color: #5C7287;;text-align:right;padding:10px; margin-right:10px;">(.*?)\s(.*?)</div>', link, re.DOTALL)
			name=''
			
			for (itr,items,it) in itertools.izip  (url_target,url_2,target):
				name=str( itr[2]).strip()
				path =str(itr[0]).strip()
				image=str(items).strip()
				plot=str( it[1]).strip()
				name2=removeArabicCharsFromString(name)
				myResult=(getImdbCred(name2))
				myFanart=str(myResult["Poster"]).strip()
				rating=str(myResult["imdbRating"]).strip()
				genre=str(myResult["Genre"]).strip()
				cast=str(myResult["Actors"]).strip()
				year=str(myResult["Year"]).strip()
				duration=str(myResult["Runtime"]).strip()
				writer=str(myResult["Writer"]).strip()
				director=str(myResult["Director"]).strip()
				if  myResult["Plot"]=="No Plot found" and myResult["Poster"]=="No Poster found" and rating=="No Rating found" and genre=="No Genre found" and year=="No Year found" and cast=="No Actors found" and duration=="No Runtime found" and writer=="No Writer found" and director=="No Director found":
					addLink(name+"\n"+genre+": "+year,path,2,image,image,plot,' ',"N/A","N/A","N/A","N/A","N/A","N/A")
				else:
					plot2= getImdbCred(name2)["Plot"]
					combinedPlot=str(plot)+"\n"+"\n"+str(plot2)+"\n"+"Actors: "+str(cast)
					addLink(name+"\n"+genre+": "+year,path,2,image,myFanart,combinedPlot,rating,genre,cast,year,duration,writer,director)
					
			if len(str(name))<2:
				url_target2=(re.compile('<a href="(.+?)">(.+?)</a></center>').findall(link))
				url_2=(re.compile('<center><div class="boxshort"> <img src="(.+?)" alt="').findall(link))
				for (itr,items) in itertools.izip  (url_target2,url_2):
					path=str( itr[0]).strip()
					name=str( itr[1]).strip()
					image=str(items).strip()
					name2=removeArabicCharsFromString(name)
					myResult=(getImdbCred(name2))
					myFanart=str(myResult["Poster"]).strip()
					rating=str(myResult["imdbRating"]).strip()
					genre=str(myResult["Genre"]).strip()
					cast=str(myResult["Actors"]).strip()
					year=str(myResult["Year"]).strip()
					duration=str(myResult["Runtime"]).strip()
					writer=str(myResult["Writer"]).strip()
					director=str(myResult["Director"]).strip()
					if  myResult["Plot"]=="No Plot found" and myResult["Poster"]=="No Poster found" and rating=="No Rating found" and genre=="No Genre found" and year=="No Year found" and cast=="No Actors found" and duration=="No Runtime found" and writer=="No Writer found" and director=="No Director found":
						addLink(name+"\n"+genre+": "+year,path,2,image,image,plot,' ',"N/A","N/A","N/A","N/A","N/A","N/A")
					else:
						plot2= getImdbCred(name2)["Plot"]
						combinedPlot=str(plot)+"\n"+"\n"+str(plot2)+"\n"+"Actors: "+str(cast)
						addLink(name+"\n"+genre+": "+year,path,2,image,myFanart,combinedPlot,rating,genre,cast,year,duration,writer,director)
	except:
		pass
				
	initial=initial+10
	max=max + 10
	
	addDir('<<<< اضهار افلام جديدة',url,4,'http://www.theonestopfunshop.com/product_images/uploaded_images/movie-night.jpg',initial,max,'DESCRIPTION','0.0')

	
def indexOldEgyptian(url,initial,max,plot,rating,genre,cast,year,duration,writer,director):
	try:
		for counter in range(initial,max):
			dlg = xbmcgui.DialogProgress()
			line1 = 'Getting the movies...'
			dlg.create('In progress, Please wait...', line1)
			percent = int((counter * 100) / max)
			label = str(counter)+" out of "+str(max)+" pages"
			dlg.update(percent, line1, label)
			
			req = urllib2.Request(url+'/page/'+str(counter)+'/')
			response = urllib2.urlopen(req)
			link=response.read()
			url_target=(re.compile('<a href="(.+?)"><font color="(.+?)">(.+?)</font>   </a>').findall(link))
			url_2=(re.compile('<a href="(.+?)" onclick="return hs.expand').findall(link))
			target= re.findall(r'<div  style="font-family:Tahoma;font-size:9pt;color: #5C7287;;text-align:right;padding:10px; margin-right:10px;">(.*?)\s(.*?)</div>', link, re.DOTALL)
			name=''
			
			for (itr,items,it) in itertools.izip  (url_target,url_2,target):
				name=str( itr[2]).strip()
				path =str(itr[0]).strip()
				image=str(items).strip()
				plot=str( it[1]).strip()
				name2=removeArabicCharsFromString(name)
				myResult=(getImdbCred(name2))
				myFanart=str(myResult["Poster"]).strip()
				rating=str(myResult["imdbRating"]).strip()
				genre=str(myResult["Genre"]).strip()
				cast=str(myResult["Actors"]).strip()
				year=str(myResult["Year"]).strip()
				duration=str(myResult["Runtime"]).strip()
				writer=str(myResult["Writer"]).strip()
				director=str(myResult["Director"]).strip()
				if  myResult["Plot"]=="No Plot found" and myResult["Poster"]=="No Poster found" and rating=="No Rating found" and genre=="No Genre found" and year=="No Year found" and cast=="No Actors found" and duration=="No Runtime found" and writer=="No Writer found" and director=="No Director found":
					addLink(name,path,2,image,image,plot,' ',"N/A","N/A","N/A","N/A","N/A","N/A")
				else:
					plot2= getImdbCred(name2)["Plot"]
					combinedPlot=str(plot)+"\n"+"\n"+str(plot2)+"\n"+"Actors: "+str(cast)
					addLink(name,path,2,image,myFanart,combinedPlot,rating,genre,cast,year,duration,writer,director)
					
			if len(str(name))<2:
				url_target2=(re.compile('<a href="(.+?)">(.+?)</a></center>').findall(link))
				url_2=(re.compile('<center><div class="boxshort"> <img src="(.+?)" alt="').findall(link))
				for (itr,items) in itertools.izip  (url_target2,url_2):
					path=str( itr[0]).strip()
					name=str( itr[1]).strip()
					image=str(items).strip()
					name2=removeArabicCharsFromString(name)
					myResult=(getImdbCred(name2))
					myFanart=str(myResult["Poster"]).strip()
					rating=str(myResult["imdbRating"]).strip()
					genre=str(myResult["Genre"]).strip()
					cast=str(myResult["Actors"]).strip()
					year=str(myResult["Year"]).strip()
					duration=str(myResult["Runtime"]).strip()
					writer=str(myResult["Writer"]).strip()
					director=str(myResult["Director"]).strip()
					if  myResult["Plot"]=="No Plot found" and myResult["Poster"]=="No Poster found" and rating=="No Rating found" and genre=="No Genre found" and year=="No Year found" and cast=="No Actors found" and duration=="No Runtime found" and writer=="No Writer found" and director=="No Director found":
						addLink(name,path,2,image,image,plot,' ',"N/A","N/A","N/A","N/A","N/A","N/A")
					else:
						plot2= getImdbCred(name2)["Plot"]
						combinedPlot=str(plot)+"\n"+"\n"+str(plot2)+"\n"+"Actors: "+str(cast)
						addLink(name,path,2,image,myFanart,combinedPlot,rating,genre,cast,year,duration,writer,director)
	except:
		pass
	initial=initial+10
	max=max + 10
	addDir('<<<< اضهار افلام جديدة',url,5,'http://www.theonestopfunshop.com/product_images/uploaded_images/movie-night.jpg',initial,max,'DESCRIPTION','0.0')

	
def indexSeries(url,initial,max,plot,rating,genre,cast,year,duration,writer,director):
	try:
	
		for counter in range(initial,max):
			url_target=""
			url_2=""
			target=""
			name=''
			fanart=''
			link=""
			
			dlg = xbmcgui.DialogProgress()
			line1 = 'Getting the movies...'
			dlg.create('In progress, Please wait...', line1)
			percent = int((counter * 100) / max)
			label = str(counter)+" out of "+str(max)+" pages"
			dlg.update(percent, line1, label)
			
			try:
				req = urllib2.Request(url+'/page/'+str(counter)+'/')
				response = urllib2.urlopen(req)
				link=response.read()
				url_target=(re.compile('<a href="(.+?)"><font color="(.+?)">(.+?)</font>   </a>').findall(link))
				url_2=(re.compile('<a href="(.+?)" onclick="return hs.expand').findall(link))
				target= re.findall(r'<div  style="font-family:Tahoma;font-size:9pt;color: #5C7287;;text-align:right;padding:10px; margin-right:10px;">(.*?)\s(.*?)</div>', link, re.DOTALL)
				
				
			except:
				pass
				
			
			for (itr,items,it) in itertools.izip  (url_target,url_2,target):
				name=str( itr[2]).strip()
				
				path =str(itr[0]).strip()
				image=str(items).strip()
				plot=str( it[1]).strip()
				name2=removeArabicCharsFromString(name)
				myResult=(getImdbCred(name2))
				myFanart=str(myResult["Poster"]).strip()
				rating=str(myResult["imdbRating"]).strip()
				genre=str(myResult["Genre"]).strip()
				cast=str(myResult["Actors"]).strip()
				year=str(myResult["Year"]).strip()
				duration=str(myResult["Runtime"]).strip()
				writer=str(myResult["Writer"]).strip()
				director=str(myResult["Director"]).strip()
				if  myResult["Plot"]=="No Plot found" and myResult["Poster"]=="No Poster found" and rating=="No Rating found" and genre=="No Genre found" and year=="No Year found" and cast=="No Actors found" and duration=="No Runtime found" and writer=="No Writer found" and director=="No Director found":
					addLink(name2+"\n"+genre+": "+year,path,2,image,image,plot,'N/A','N/A','N/A','N/A','N/A')
				else:
					plot2= getImdbCred(name2)["Plot"]
					combinedPlot=str(plot)+"\n"+"\n"+str(plot2)+"\n"+"Actors: "+str(cast)
					addLink(name2+"\n"+genre+": "+year,path,2,image,myFanart,combinedPlot,rating,genre,cast,year,duration,writer,director)
							
			if len(str(name))<2:
				url_target2=(re.compile('<a href="(.+?)">(.+?)</a></center>').findall(link))
				url_2=(re.compile('<center><div class="boxshort"> <img src="(.+?)" alt="').findall(link))
				for (itr,items) in itertools.izip  (url_target2,url_2):
					path=str( itr[0]).strip()
					name=str( itr[1]).strip()
					image=str(items).strip()
					name2=removeArabicCharsFromString(name)
					myResult=(getImdbCred(name2))
					if  myResult["Plot"]=="No Plot found" and myResult["Poster"]=="No Poster found" and rating=="No Rating found" and genre=="No Genre found" and year=="No Year found" and cast=="No Actors found" and duration=="No Runtime found" and writer=="No Writer found" and director=="No Director found":
						addLink(name2+"\n"+genre+": "+year,path,2,image,image," ","N/A","N/A","N/A","N/A")
					else:
						myFanart=str(myResult["Poster"]).strip()
						plot2= getImdbCred(name2)["Plot"]
						rating=str(myResult["imdbRating"]).strip()
						genre=str(myResult["Genre"]).strip()
						cast=str(myResult["Actors"]).strip()
						plot2=str(plot2)+"\n"+"\n"+"Actors: "+str(cast)
						year=str(myResult["Year"]).strip()
						duration=str(myResult["Runtime"]).strip()
						writer=str(myResult["Writer"]).strip()
						director=str(myResult["Director"]).strip()
						addLink(name2+"\n"+genre+": "+year,path,2,image,myFanart,plot2,rating,genre,cast,year,duration,writer,director)
			
					
	except:
		pass
	initial=initial+7
	max=max + 7
	addDir(' <<<< اضهار افلام جديدة',url,1,'http://www.theonestopfunshop.com/product_images/uploaded_images/movie-night.jpg',initial,max,'DESCRIPTION','0.0',"N/A","N/A","N/A","N/A","N/A")
		

def indexEgyptian(url,initial,max,plot,rating,genre,cast,year,duration,writer,director):
	try:
		for counter in range(initial,max):
			
			dlg = xbmcgui.DialogProgress()
			line1 = 'Getting the movies...'
			dlg.create('In progress, Please wait...', line1)
			percent = int((counter * 100) / max)
			label = str(counter)+" out of "+str(max)+" pages"
			dlg.update(percent, line1, label)
			req = urllib2.Request(url+'/page/'+str(counter)+'/')
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			link=response.read()
			url_target=(re.compile('<a href="(.+?)" onclick="(.+?)title="(.+?)"').findall(link))
			url_path=(re.compile('<a href="(.+?)">شاهد الأن</a>').findall(link))
			targetPlot= re.findall(r'<div  style="font-family:Tahoma;font-size:9pt;color: #5C7287;;text-align:right;padding:10px; margin-right:10px;" dir="rtl">(.*?)\s(.*?)</div>', link, re.DOTALL)
			
			for (itr,i,trpl) in itertools.izip  (url_target,url_path,targetPlot):
				image=str( itr[0]).strip()
				name=str( itr[2]).strip()
				path=str(i).strip()
				plot=str( trpl[1]).strip()
				addLink(name,path,2,image,image,plot," ","N/A","N/A","N/A","N/A","N/A","N/A")
	
	except:
		pass
		
	initial=initial+30
	max=max + 30
	addDir(' <<<< اضهار افلام جديدة',url,3,'http://www.theonestopfunshop.com/product_images/uploaded_images/movie-night.jpg',initial,max,'DESCRIPTION','0.0',"N/A","N/A","N/A","N/A","N/A")	
	
			
def playDarDar(url):
	try:
		req1 = urllib2.Request(url)
		response1 = urllib2.urlopen(req1)
		link1=response1.read()
		url_target1=(re.compile('<a href="(.+?)" target="_blank"><img src=').findall(link1))
		myurl=str( url_target1[0]).strip()
		print myurl
		req2 = urllib2.Request(myurl)
		response2 = urllib2.urlopen(req2)
		link2=response2.read()
		url_target2=(re.compile('<div id="(.+?)src="(.+?)" width=').findall(link2))
		url_target2=str( url_target2).split(',')[1]
		url_target2=str( url_target2).replace("'", '').replace("')]", "").replace(')]','').strip()
		print url_target2
		req3 = urllib2.Request(url_target2)
		response3 = urllib2.urlopen(req3)
		link3=response3.read()
		url_target3=(re.compile('<param name="flashvars" value="(.+?)"></param>').findall(link3))
		final= str(url_target3).split('&amp;')
		for mp4 in final:
			if 'url360=' in str(mp4):
				playpath=str( mp4).replace('url360=', '')
				listItem = xbmcgui.ListItem(path=str(playpath))
				xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
	except:
		pass
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('Info','This film could not be played!!!',4000, 'http://blog.spamfighter.com/wp-content/uploads/g1-error-768519.png'))
	            
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




def addLink(name,url,mode,iconimage,fanart,plot='',rating="",genre="",cast="",year="",duration="",writer="",director=""):
	ok=True
	u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
	
	liz=xbmcgui.ListItem(name,iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot":plot,"rating":rating,"genre":genre,"Cast":cast,"year":year,"duration":duration,"writer":writer,"director":director})
	liz.setProperty( "Fanart_Image", fanart )
	liz.setProperty("IsPlayable","true");
	ok=xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=False)
	return ok


def addDir(name,url,mode,iconimage,initial,max,plot='',rating="",genre="",cast="",year="",duration="",writer="",director=""):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&initial="+str(initial)+"&max="+str(max)+"&rating="+str(rating)+"&genre="+str(genre)+"&Cast="+str(cast)+"&year="+str(year)+"&duration="+str(duration)+"&writer="+str(writer)+"&director="+str(director)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":plot,"rating":rating,"genre":genre,"Cast":cast,"year":year,"duration":duration,"writer":writer,"director":director} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

              
params=get_params()
url=None
name=None
mode=None
initial=None
max=None
rating=None
cast=None
year=None
genre=None
duration=None
writer=None
director=None

	
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
try:
        initial=int(params["initial"])
except:
        pass
try:
        max=int(params["max"])
except:
        pass
try:
        plot=urllib.unquote_plus(params["plot"])
except:
        plot=''
try:
        rating=urllib.unquote_plus(params["rating"])
except:
        rating=''

try:
        year=urllib.unquote_plus(params["year"])
except:
        year=''
try:
        cast=urllib.unquote_plus(params["cast"])
except:
        pass
try:
        genre=urllib.unquote_plus(params["genre"])
except:
        genre=''
		
try:
        duration=urllib.unquote_plus(params["duration"])
except:
        duration=''
		
try:
        writer=urllib.unquote_plus(params["writer"])
except:
        writer=''

try:
        director=urllib.unquote_plus(params["director"])
except:
        director=''
		


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "initial: "+str(initial)
print "max: "+str(max)
print "plot: "+str(plot)
if mode==None or url==None or len(url)<1:
        print ""
        getCategories()
       
elif mode==1:
        print ""+url
        indexSeries(url,initial,max,plot,rating,genre,cast,year,duration,writer,director)
elif mode==2:
        print ""+url
        playDarDar(url)
		
elif mode==3:
        print ""+url
        indexEgyptian(url,initial,max,plot,rating,genre,cast,year,duration,writer,director)

elif mode==4:
        print ""+url
        indexIndian(url,initial,max,plot,rating,genre,cast,year,duration,writer,director)
		
elif mode==5:
        print ""+url
        indexOldEgyptian(url,initial,max,plot,rating,genre,cast,year,duration,writer,director)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
