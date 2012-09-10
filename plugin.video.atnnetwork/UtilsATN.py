import cookielib
import hashlib
import json
import sys
import urllib2

URL_LOGIN_TOKEN = "email={email}&password={password}"
URL_GET_PACKAGES = "http://api.arabtvnet.tv/get_packages?{loginTicket}"
URL_GET_CHANNEL = "http://api.arabtvnet.tv/channel?{loginTicket}&package={packageNo}&channel={channelID}"
URL_GET_CHANNELS = "http://api.arabtvnet.tv/channels?{loginTicket}&package={packageNo}"

class UtilsATN:

    # ATN Feeds
    urls = {}
    urls['login_querystring'] = "email={email}&password={password}"
    urls['get_packages'] = "http://api.arabtvnet.tv/get_packages?{loginTicket}"
    urls['get_channel'] = "http://api.arabtvnet.tv/channel?{loginTicket}&package={packageNo}&channel={channelID}"
    urls['get_channels'] = "http://api.arabtvnet.tv/channels?{loginTicket}&package={packageNo}"

    def __init__(self):
        self.settings = sys.modules["__main__"].settings
        self.language = sys.modules["__main__"].language
        self.plugin = sys.modules["__main__"].plugin

        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

    def loginTicket(self):
        username = self.settings.getSetting('username')
        password = self.settings.getSetting('password')
        md5Password = hashlib.md5(password).hexdigest()

        return self.urls['login_querystring'].format(email=username, password=md5Password)

    def hasValidLogin(self):
        return self.settings.getSetting('validLogin') == "True"

    def getData(self, url):
        response = self.opener.open(url)
        data = response.read()
        self.opener.close()

        return json.loads(data)

    def login(self):
        url = self.urls['get_packages'].format(loginTicket=self.loginTicket())
        atnPackageData = self.getData(url)

        success = False

        # User has 1 or more ATN package subscriptions
        if len(atnPackageData) > 0:
            success = atnPackageData[0]['Expiry'] is not None

        # Mark that the user has a successful login credential
        self.settings.setSetting('validLogin', str(success))

        return success

    def getAllChannels(self):
        url = self.urls['get_channels'].format(loginTicket=self.loginTicket(), packageNo="15")
        return self.getData(url)

    def getChannelStreamUrl(self, channelID):
        url = self.urls['get_channel'].format(loginTicket=self.loginTicket(), packageNo="15", channelID=channelID)
        channelData = self.getData(url)
        return channelData["Message"]