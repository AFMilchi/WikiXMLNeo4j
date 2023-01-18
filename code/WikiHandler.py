import re
import DbConnector as dbc
import xml.sax


class WikiHandler(xml.sax.ContentHandler):
    '''Handlerfunktion zur Implementierung des SAX Parser
    Parameters:
        text, title, current, redirect (String)
        id, ns, count (int)
        connector(DbConnector): Interface zur Datenbank
        inrevision(bool)
    '''

    def __init__(self, type):
        '''Konsturktor
        Parameters:
            type(String): Art des Parsmodus
        '''
        self.text = ''
        self.title = ''
        self.id = -1
        self.current = ''
        self.connector = dbc.DbConnector()
        self.type = type
        self.ns = 0
        self.redirect = ''
        self.inrevision = False
        self.count = 0

    # Gecallt bei Öffnenden Tags
    def startElement(self, tag, attr):
        '''Callbackfunktion bei öffnenden Tags
        Parameters:
            tag(String): Name des Tags
            attr(String): Attribute des Tags'''
        self.current = tag
        if self.current == 'page':
            self.title = ''
            self.ns = 0
            self.redirect = ''
            self.inrevision = False
            self.text = ''

    def characters(self, content):
        '''Callbackfunktion während dem Inhalt eines Tags
        Parameters:
            content(String): Inhalt des Tags'''
        if self.current == 'title':
            self.title = content.replace('"', "'")
        elif self.current == 'text':
            self.text += content
        elif self.current == 'redirect':
            self.redirect += content
        elif self.current == 'ns' and content is not None:
            self.ns = int(content)

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
            elif self.title != '':
                if self.type == 'Kategorie':
                    if 'Kategorie:' not in self.title:
                        categoriesList = self.extractCategories(self.text)
                        self.writeAdjToCsv(
                            self.title, 'TEIL_VON_KATEGORIE', categoriesList)
                if self.type == 'Verlinkung':
                    if 'Kategorie:' not in self.title:
                        linkList = self.extractInnerLinks(self.text)
                        self.writeAdjToCsv(
                            self.title, 'VERLINKT_AUF', linkList)

                if self.type == 'Artikel':
                    pass
        self.current = ''

    def extractCategories(self, inhalt):
        '''Extrahiert alle Kategorien aus dem Volltext eines Artikels
        Parameters:
            inhalt(String):Volltext eines Artikels
        Returns:
            categorieList(List):Alle gefunden Kategorien'''
        categorieSearchString = '\[\[Kategorie:.*?\]?]'
        # Entfernt direkt Start und Endsymbohle und befüllt Liste
        categorieList = []
        for elem in re.finditer(categorieSearchString, inhalt):
            buffer = elem.group()
            cat = buffer[buffer.find(
                ':')+1:].strip('[]').split('|')[0].strip('][').split('<')[0]
            cat = cat.replace('"', "'")
            categorieList.append(cat)
        return categorieList

    def writeAdjToCsv(self, fromNodeTitle, adjType, toNodeList):
        '''Datenbankinterface um Daten in eine CSV Datei zu schreiben
        Parameters:
            fromNodeTitle(String)
            adjType(String)
            toNodeList(List)'''
        for toNode in toNodeList:
            self.connector.createAdjtoCsv(
                fromNodeTitle, toNode, adjType)

    def extractInnerLinks(self, inhalt):
        '''Extrahiert alle Artikelverlinkungen aus dem Volltext eines Artikels
        Parameters:
            inhalt(String):Volltext eines Artikels'''
        linkSearchString = '\[\[.*?\]?\]'
        linkList = []
        specialLinks = ['Kategorie:', 'en:',
                        'File:', 'Datei:', 'Bild:', 'Benutzer:', 'Image:', 'doi:']
        for elem in re.finditer(linkSearchString, inhalt):
            buffer = elem.group()
            toNode = buffer.strip('[]').split('|')[0].strip('][').split('<')[0]
            toNode = toNode.replace('"', "'")
            if not any(word in toNode for word in specialLinks):
                linkList.append(toNode)
        return linkList
