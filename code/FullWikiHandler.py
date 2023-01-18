import re
import xml.sax
import WikiHandler


class FullWikiHandler(WikiHandler.WikiHandler):
    '''Handlerfunktion zur Implementierung des SAX Parser
    Spezialisiert zum erstellen des Full-Graphs 
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

    def extractInnerLinks(self, inhalt):
        '''Extrahiert alle Verlinkungen von Artikeln auf Andere aus dem Volltext
        Parameters:
            inhalt(String)
        Returns:
            linkList(List):Liste aller Zielverlinkungen'''
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
