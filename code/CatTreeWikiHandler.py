import re
import DbConnector as dbc
import xml.sax
import WikiHandler


class CatTreeWikiHandler(WikiHandler.WikiHandler):

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
                    if 'Kategorie:' in self.title:
                        categoriesList = self.extractCategories(self.text)
                        self.writeAdjToCsv(
                            self.title, 'UNTERKATEGORIE_VON', categoriesList)

                if self.type == 'Artikel':
                    if 'Kategorie:' in self.title:
                        self.writeNode(self.title, self.id)
        self.current = ''

    def writeNode(self, title, id):
        ''' Wenn ein Artikel mit 'Kategorie:' beginnt ist er kein
            Typ Artikel sondern eine Kategorie. '''
        if 'Kategorie:' in title:
            nodeType = 'Kategorie'
            title = title[title.find(':')+1:]
            attributes = {'title': title, 'id': id}
            self.connector.createNode(nodeType, attributes)

    def tailCategoriesFullText(self, inhalt):
        lines = inhalt.splitlines()
        newInhalt = ''
        for line in reversed(lines):
            if '[[Kategorie:' == str(line)[:12]:
                newInhalt += str(line) + '\n'
            else:
                break
        return newInhalt

    def extractCategories(self, inhalt):
        categorieSearchString = '\[\[Kategorie:.*?\]?]'
        # Entfernt direkt Start und Endsymbohle und befüllt Liste
        categorieList = []
        inhalt = self.tailCategoriesFullText(inhalt)
        for elem in re.finditer(categorieSearchString, inhalt):
            buffer = elem.group()
            cat = buffer[buffer.find(
                ':')+1:].strip('[]').split('|')[0].strip('][').split('<')[0]
            cat = cat.replace('"', "'")
            categorieList.append(cat)
        return categorieList

    def writeAdjToCsv(self, fromNodeTitle, adjType, toNodeList):
        fromNodeTitle = fromNodeTitle[fromNodeTitle.find(':')+1:]
        for toNode in toNodeList:
            self.connector.createAdjtoCsv(
                fromNodeTitle, toNode, adjType)
