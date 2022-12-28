import re
import DbConnector as dbc
import xml.sax


class WikiHandler(xml.sax.ContentHandler):

    def __init__(self, type):
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
        for toNode in toNodeList:
            self.connector.createAdjtoCsv(
                fromNodeTitle, toNode, adjType)

    def extractInnerLinks(self, inhalt):
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
