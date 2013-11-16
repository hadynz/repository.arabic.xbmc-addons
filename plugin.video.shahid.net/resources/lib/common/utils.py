import json as j
import os
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
import unicodedata


latin_letters= {}


def get(url):
    """Performs a GET request for the given url and returns the response"""
    conn = urlopen(url)
    resp = conn.read()
    conn.close()
    return resp


def html(url):
    """Downloads the resource at the given url and parses via BeautifulSoup"""
    return BeautifulSoup(get(url), convertEntities=BeautifulSoup.HTML_ENTITIES)


def json(url):
    print 'Fetching JSON from: ' + url
    response = get(url).decode("utf-8-sig")
    return j.loads(response)


def isEnglish(unistr):
    return all(_is_latin(uchr)
           for uchr in unistr
           if uchr.isalpha()) # isalpha suggested by John Machin


def _is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
         return latin_letters.setdefault(uchr, 'LATIN' in unicodedata.name(uchr))


def imagePath(plugin, folder, *args):
    return os.path.join(plugin.addon.getAddonInfo('path'), folder, *args)