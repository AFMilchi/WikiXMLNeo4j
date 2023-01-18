import re
import DbConnector as dbc
import xml.sax
import WikiHandler


class ArtikelTreeWikiHandler(WikiHandler.WikiHandler):
    '''Handlerfunktion zur Implementierung des SAX Parser
    Spezialisiert zum erstellen des Artikel-Graphs 
        connector(DbConnector): Interface zur Datenbank
    '''

    def endElement(self, tag):
        '''Callbackfunktion bei schließenden Tags. Hier werden die
        gesammelten Daten verarbeitet
        Parameters:
            tag(String): Name des Tags'''
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
        '''Übergibt Daten an Datenbank um Knoten zu erzeugen
        Parameters:
            title(String)
            id(String)'''
        nodeType = 'Artikel'
        attributes = {'title': title, 'id': id}
        self.connector.createNode(nodeType, attributes)
