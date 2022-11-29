import DbConnector as dbc
import XmlStreamReader as xr
import Utils
import re


class DataProcessor():

    def __init__(self):
        self.reader = xr.XmlStreamReader()
        self.connector = dbc.DbConnector()

    def traverseData(self, kind):
        totalCount = 0
        for event, elem in self.reader.getNextArticle():
            tagName = Utils.Utils.stripTagName(elem)
            # event == start bei oeffnenden tags e.g. <page>
            if event == 'start':
                if tagName == 'page':
                    title = ''
                    id = -1
                    redirect = ''
                    inrevision = False
                    ns = 0
                elif tagName == 'revision':
                    inrevision = True
                elif tagName == 'title' and elem.text is not None:
                    title = elem.text.replace('"', "'")
                elif tagName == 'id' and not inrevision and elem.text is not None:
                    id = int(elem.text)
                elif tagName == 'redirect':
                    redirect = elem.get('title', '')
                elif tagName == 'ns' and elem.text is not None:
                    ns = int(elem.text)
                elif tagName == 'text':
                    inhalt = str(elem.text)

            elif tagName == 'page':
                # Statement findet closing Pagetags wie <\page>
                totalCount += 1

                if ns == 10:
                    # Template
                    pass
                elif redirect:
                    # Redirect
                    pass
                elif title is not None:
                    # Artikel
                    if kind == 'Artikel':
                        self.writeNode(title, id)
                    elif kind == 'Kategorie':
                        if 'Kategorie:' not in title:
                            categoriesList = self.extractCategories(inhalt)
                            self.writeAdj(
                                title, 'TEIL_VON_KATEGORIE', categoriesList)
                if totalCount % 100000 == 0:
                    print(f'Verarbeitete Artikel: {totalCount}')

                # if totalCount >= 0:
                #    print('safty break')
                #    break

            # hilft Garbadge Collector
            elem.clear()

    def extractCategories(self, inhalt):
        categorieSearchString = '\[\[Kategorie:[\w*-,\s]*[\],|]'
        # Entfernt direkt Start und Endsymbohle und befüllt Liste
        categorieList = []
        for elem in re.finditer(categorieSearchString, inhalt):
            buffer = elem.group()
            cat = buffer[buffer.find(':')+1:-1]
            categorieList.append(cat)
            if 'Kategorie:' in cat:
                print(buffer)
        return categorieList

    def writeNode(self, title, id):
        ''' Wenn ein Artikel mit 'Kategorie:' beginnt ist er kein
            Typ Artikel sondern eine Kategorie. '''
        if 'Kategorie:' in title:
            nodeType = 'Kategorie'
            title = title[title.find(':')+1:]
        else:
            nodeType = 'Artikel'
        attributes = {'title': title, 'id': id}
        self.connector.createNode(nodeType, attributes)

    def writeAdj(self, fromNodeTitle, adjType, toNodeList):
        for toNode in toNodeList:
            # self.connector.createAdj(fromNodeTitle, toNode, adjType)
            self.connector.createCategorieAdjtoCsv(
                fromNodeTitle, toNode, adjType)

    def extractInnerLinks(self, inhalt):
        pass


if __name__ == '__main__':
    processor = DataProcessor()
    # processor.traverseData('Artikel')
    processor.traverseData('Kategorie')
