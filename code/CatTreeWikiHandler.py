import re
import DbConnector as dbc
import xml.sax
import WikiHandler


class CatTreeWikiHandler(WikiHandler.WikiHandler):
    '''Handlerfunktion zur Implementierung des SAX Parser
    Spezialisiert zum erstellen des Kategorie-Graphs 
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
        ''' Übergibt Artikel zum schreiben an Datenbank
        Wenn ein Artikel mit 'Kategorie:' beginnt ist er kein
            Typ Artikel sondern eine Kategorie.
            Parameters:
                title(String)
                id(string)'''
        if 'Kategorie:' in title:
            nodeType = 'Kategorie'
            title = title[title.find(':')+1:]
            attributes = {'title': title, 'id': id}
            self.connector.createNode(nodeType, attributes)

    def tailCategoriesFullText(self, inhalt):
        '''Untersucht das Ende eines Artikels und schneidet alles außer Kategorien ab
        Parameters:
            inhalt(String): Volltext des Artikels
        Returns:
            newInhalt(String)'''
        lines = inhalt.splitlines()
        newInhalt = ''
        for line in reversed(lines):
            if '[[Kategorie:' == str(line)[:12]:
                newInhalt += str(line) + '\n'
            else:
                break
        return newInhalt

    def extractCategories(self, inhalt):
        '''Extrahiert alle Kategorien aus dem Volltext eines Artikels
        Parameters:
            inhalt(String)
        Returns:
            categorieList(List): Liste aller gefunden Kategorien'''
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
        '''Übergibt Daten an Datenbank zum schreiben der Beziehung in eine CSV
        Parameters:
            fromNodeTitle(String)
            adjType(String)
            toNodeList(List)'''
        fromNodeTitle = fromNodeTitle[fromNodeTitle.find(':')+1:]
        for toNode in toNodeList:
            self.connector.createAdjtoCsv(
                fromNodeTitle, toNode, adjType)
