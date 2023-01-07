import DbConnector as dbc
import xml.sax
import WikiHandler


class DebugWikiHandler(WikiHandler.WikiHandler):

    def __init__(self, searchedArtikel):
        self.text = ''
        self.title = ''
        self.current = ''
        self.connector = dbc.DbConnector()
        self.type = type
        self.ns = 0
        self.redirect = ''
        self.inrevision = False
        self.searchedArtikel = searchedArtikel
        self.count = 0

    def endElement(self, tag):
        if tag == 'page':
            self.count += 1
            if self.count % 100000 == 0:
                print(self.count)
            if self.ns == 10:
                pass
            if self.redirect:
                pass
            elif self.title != '':
                if self.title == self.searchedArtikel:
                    print(self.title)
                    print(self.text)
                    quit()
        self.current = ''
