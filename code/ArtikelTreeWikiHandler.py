import re
import DbConnector as dbc
import xml.sax
import WikiHandler


class ArtikelTreeWikiHandler(WikiHandler.WikiHandler):

    def endElement(self, tag):
        if tag == 'page':
            self.count += 1
            if self.count % 100000 == 0:
                print(self.count)
            if self.ns == 10:
                pass
            if self.redirect:
                pass

            if self.type == 'Artikel':
                if 'Kategorie:' not in self.title:
                    self.writeNode(self.title, self.id)
        self.current = ''

    def writeNode(self, title, id):
        nodeType = 'Artikel'
        attributes = {'title': title, 'id': id}
        self.connector.createNode(nodeType, attributes)
