from PIL import Image
import hashlib
import time
import os
import xbmcaddon

addonPath = xbmcaddon.Addon().getAddonInfo("path")
communityStreamPath = os.path.join(addonPath,'resources')
communityStreamPath = os.path.join(communityStreamPath,'community')
#print 'path is ',communityStreamPath
import math

class VectorCompare:
  def magnitude(self,concordance):
    total = 0
    for word,count in concordance.iteritems():
      total += count ** 2
    return math.sqrt(total)

  def relation(self,concordance1, concordance2):
    relevance = 0
    topvalue = 0
    for word, count in concordance1.iteritems():
      if concordance2.has_key(word):
        topvalue += count * concordance2[word]
    return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))



def buildvector(im):
  d1 = {}

  count = 0
  for i in im.getdata():
    d1[count] = i
    count += 1

  return d1

def getString(imgpath):
 
  v = VectorCompare()

  #iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
  iconset = ['0','1','2','3','4','5','6','7','8','9']

  imageset = []
  #print 'communityStreamPath',communityStreamPath,os.path.join( communityStreamPath,'/captchaiconset/%s/'%('0'))
  for letter in iconset:
    for img in os.listdir(communityStreamPath+'/captchaiconset/%s/'%(letter)):
      temp = []

      if img != "Thumbs.db": # windows check...
        temp.append(buildvector(Image.open( communityStreamPath+"/captchaiconset/%s/%s"%(letter,img))))
        imageset.append({letter:temp})
        #print img

  im = Image.open(imgpath)
  im2 = Image.new("P",im.size,255)
  im = im.convert("P")

  temp = {}

  for x in range(im.size[1]):
    for y in range(im.size[0]):
      pix = im.getpixel((y,x))
      #print 'imgpix',pix 
      temp[pix] = pix
      if pix==0:#pix == 220 or pix == 224: # these are the numbers to get
        im2.putpixel((y,x),0)
  #aa=im2.convert('RGB')
  #aa.save(imgpath + ".jpg", "JPEG")
  #print 'temp',temp    
  inletter = False
  foundletter=False
  start = 0
  end = 0

  letters = []

  for y in range(im2.size[0]): # slice across
    for x in range(im2.size[1]): # slice down
      pix = im2.getpixel((y,x))
      #print 'pix',pix
      if pix != 255:
        inletter = True

    if foundletter == False and inletter == True:
      foundletter = True
      start = y

    if foundletter == True and inletter == False:
      foundletter = False
      end = y
      letters.append((start,end))


    inletter=False

  count = 0
  #print 'letters',letters
  retval=""
  for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))
    #aa=im3.convert('RGB')
    #aa.save(imgpath + str(count)+".gif", "GIF")
    guess = []

    for image in imageset:
      for x,y in image.iteritems():
        if len(y) != 0:
          guess.append( ( v.relation(y[0],buildvector(im3)),x) )

    guess.sort(reverse=True)

    retval+=guess[0][1]
    #print "",guess[0]

    count += 1
  return retval
