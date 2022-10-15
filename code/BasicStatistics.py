#!/usr/bin/python
import XmlStreamReader as xr


class BasicStatistics():
    '''Wertet einen XML Datenstrom aus
    und erstellt Grundlegende Statistiken'''

    OUTPUT_FILENAME = 'output.csv'

    def __init__(self):
        self.reader = xr.XmlStreamReader()
        self.totalCount = 0
        self.articleCount = 0
        self.redirectCount = 0
        self.templateCount = 0
        self.titel = None
        self.startTime = 0

    def stripTagName(self, elem):
        '''Simples entfernen der Nametags, die sonst wie im Beispiel ausehen
        {http://www.mediawiki.org/xml/export-0.10/}page '''
        t = elem.tag
        idx = t.rfind('}')
        if idx != -1:
            t = t[idx + 1:]
        return t

    def collectData(self):
        '''Das lesen der xml erfolgt im Stream verfahren, daher muss haendisch
        mit if und lokalen Variablen verfolgt werden in welchem XML-Tag man
        sich befindet und Information direkt extrahiert werden'''
        for event, elem in self.reader.getNextArticle():
            tagName = self.stripTagName(elem)
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
                elif tagName == 'title':
                    title = elem.text
                elif tagName == 'id' and not inrevision and elem.text is not None:
                    id = int(elem.text)
                elif tagName == 'redirect':
                    redirect = elem.get('title', '')
                elif tagName == 'ns' and elem.text is not None:
                    ns = int(elem.text)

            elif tagName == 'page':
                # Statement findet closing Pagetags wie <\page>
                self.totalCount += 1

                if ns == 10:
                    # ns 10 sind immer Templates
                    self.templateCount += 1
                    # writer?
                elif redirect:
                    self.articleCount += 1
                    # writer
                else:
                    self.redirectCount += 1
                    # writer
                if self.totalCount % 10000 == 0:
                    print(f'Verarbeitete Artikel: {self.totalCount}')

                if self.totalCount > 100000:
                    print('safty break')
                    break

            # gibt etwas ram wieder frei
            elem.clear()

        print(self.totalCount)
        print(f'Endergebnisse:       ')
        print(
            f'totalCount:{self.totalCount} templateCount:{self.templateCount} articleCount:{self.articleCount} redirectCount:{self.redirectCount}')


if __name__ == '__main__':
    test = BasicStatistics()
    print(test.collectData())
