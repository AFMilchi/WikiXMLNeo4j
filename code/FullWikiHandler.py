import re
import xml.sax
import WikiHandler


class FullWikiHandler(WikiHandler.WikiHandler):

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
