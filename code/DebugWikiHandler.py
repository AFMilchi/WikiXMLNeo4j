import DbConnector as dbc
import xml.sax


class DebugWikiHandler(xml.sax.ContentHandler):

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

    # Gecallt bei Öffnenden Tags
    def startElement(self, tag, attr):
        self.current = tag
        if self.current == 'page':
            self.title = ''
            self.ns = 0
            self.redirect = ''
            self.inrevision = False
            self.text = ''

    def characters(self, content):
        if self.current == 'title':
            self.title = content.replace('"', "'")
        elif self.current == 'text':
            self.text += content
        elif self.current == 'redirect':
            self.redirect += content
        elif self.current == 'ns' and content is not None:
            self.ns = int(content)

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
