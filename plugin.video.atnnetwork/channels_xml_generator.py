from itertools import groupby

class Channel:
    def __init__(self, channelArr):
        self.channelID = channelArr[0]
        self.title = channelArr[1]
        self.thumbnail = channelArr[2]
        self.categoryName = channelArr[3]

class Generator:
    """
        Generates a new channels.xml file from channels.csv file that
        can be used by the ATN Network XBMC plugin. Must be run from the
        root of the checked-out repo. Only handles single depth folder structure.
    """
    def __init__( self ):
        # generate files
        self._generate_addons_file()
        # notify user
        print "Finished creating ATN channels xml file"

    def _generate_addons_file( self ):
        # final addons text
        channels_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<categories>\n"

        try:
            _path = ".\\resources\\data\\channels.csv"
            csv_lines = open(_path, "r" ).read().splitlines()

            channels_list = []

            for line in csv_lines[1:]:  # skip header row: [1:]
                channel = Channel(line.split(","))
                channels_list.append(channel)

            channels_list.sort(key=lambda c: c.categoryName)

            for key, group in groupby(channels_list, lambda  x: x.categoryName):
                channels_xml += "<category title='%s'>\n" % key
                for thing in group:
                    channels_xml += "<channel id='%s' title='%s' thumbnail='%s' />\n" % (thing.channelID, thing.title, thing.thumbnail)
                channels_xml += "</category>\n"

        except Exception, e:
            # missing or poorly formatted addon.xml
            print "Excluding %s for %s" % ( _path, e, )
            # clean and add closing tag

        channels_xml = channels_xml.strip() + u"\n</categories>\n"

        # save file
        self._save_file( channels_xml.encode( "utf-8" ), file=".\\resources\\data\\channels.xml" )

    def _save_file( self, data, file ):
        try:
            # write data to the file
            open( file, "w" ).write( data )
        except Exception, e:
            # oops
            print "An error occurred saving %s file!\n%s" % ( file, e, )


if ( __name__ == "__main__" ):
    # start
    Generator()