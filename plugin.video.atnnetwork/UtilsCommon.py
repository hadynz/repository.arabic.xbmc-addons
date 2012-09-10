import sys

class UtilsCommon:
    def __init__(self):
        self.xbmc = sys.modules["__main__"].xbmc
        self.language = sys.modules["__main__"].language
        self.duration = 2000

    # Shows a more user-friendly notification
    def showMessage(self, heading, message):
        self.xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s)' % (heading, message, self.duration))

    # Standardised error handler
    def showErrorMessage(self, title="", result="", status=500):
        if title == "":
            title = self.language(30600)    # "Error"

        if result == "":
            self.showMessage(title, self.language(30601))   # "Unknown Error"
        else:
            self.showMessage(title, result)