import re
import DbConnector as dbc
import xml.sax


class WikiHandler(xml.sax.ContentHandler):

    def __init__(self, type):
        self.text = ''
        self.title = ''
        self.current = ''
        self.connector = dbc.DbConnector()
        self.type = type

    # Gecallt bei Öffnenden Tags
    def startElement(self, tag, attr):
        self.current = tag
        if self.current == 'page':
            self.title = ''
            self.text = ''

    def characters(self, content):
        if self.current == 'title':
            self.title += content
        elif self.current == 'text':
            self.text += content

    def endElement(self, tag):
        if tag == 'page':
            if self.title != '':
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
        categorieSearchString = '\[\[Kategorie:.*[\],|]'
        # Entfernt direkt Start und Endsymbohle und befüllt Liste
        categorieList = []
        for elem in re.finditer(categorieSearchString, inhalt):
            buffer = elem.group()
            cat = buffer[buffer.find(':')+1:].strip('[]').split('|')[0]
            categorieList.append(cat)
        return categorieList

    def writeAdjToCsv(self, fromNodeTitle, adjType, toNodeList):
        for toNode in toNodeList:
            self.connector.createAdjtoCsv(
                fromNodeTitle, toNode, adjType)

    def extractInnerLinks(self, inhalt):
        linkSearchString = '\[\[.*?\]?\]'
        linkList = []
        specialLinks = ['Kategorie:', 'en:',
                        'File:', 'Datei:', 'Bild:', 'Benutzer:']
        for elem in re.finditer(linkSearchString, inhalt):
            buffer = elem.group()
            toNode = buffer.strip('[]').split('|')[0]
            if not any(word in toNode for word in specialLinks):
                linkList.append(toNode)
        return linkList
