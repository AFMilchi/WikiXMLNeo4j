#!/usr/bin/python
import XmlStreamReader as xr
import time
import Utils


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
        self.categorieCount = 0
        self.titel = None
        self.startTime = 0

    def formatTimeElapsed(self, seconds):
        '''Formatierung von Sekunden in hh:mm:ss.ss'''
        h = int(seconds / (60 * 60))
        m = int((seconds % (60 * 60)) / 60)
        s = seconds % 60
        return f'{h}:{m:>02}:{s:>05.2f}'

    def collectData(self):
        '''Das lesen der xml erfolgt im Stream verfahren, daher muss haendisch
        mit if und lokalen Variablen verfolgt werden in welchem XML-Tag man
        sich befindet und Information direkt extrahiert werden'''
        startTime = time.time()
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
                    self.redirectCount += 1
                    # writer
                else:
                    if title is not None and 'Kategorie' in title:
                        self.categorieCount += 1
                    else:
                        self.articleCount += 1
                    # writer
                if self.totalCount % 100000 == 0:
                    print(f'Verarbeitete Artikel: {self.totalCount}')

                # if self.totalCount > 1000000000:
                #    print('safty break')
                #    break

            # hilft Garbadge Collector
            elem.clear()

        elapsedTime = self.formatTimeElapsed(time.time() - startTime)
        print(self.totalCount)
        print('Endergebnisse:       ')
        print(
            f'totalCount:{self.totalCount} templateCount:{self.templateCount} articleCount:{self.articleCount} redirectCount:{self.redirectCount}')
        print(f'Dauer: {elapsedTime}')


if __name__ == '__main__':
    test = BasicStatistics()
    print(test.collectData())
