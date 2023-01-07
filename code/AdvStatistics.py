import XmlStreamReader as xr
import time
import Utils
import pprint
from BasicStatistics import BasicStatistics


class AdvStatistic(BasicStatistics):
    def __init__(self):
        super().__init__()
        self.ns = 0
        self.nsNameDic = dict()
        self.nsCountDic = dict()

    def populateNamespaceDic(self):
        for event, elem, tagName in self.reader.getNextSiteInfo():
            if event == 'start':
                if tagName == 'namespace':
                    self.nsNameDic[int(elem.attrib['key'])] = str(elem.text)
            for key in self.nsNameDic:
                self.nsCountDic[key] = 0

    def countNamespaces(self):
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

                self.nsCountDic[ns] += 1

                if self.totalCount % 100000 == 0:
                    print(f'Verarbeitete Artikel: {self.totalCount}')

            # hilft Garbadge Collector
            elem.clear()

        elapsedTime = self.formatTimeElapsed(time.time() - startTime)
        print(self.totalCount)
        print('Endergebnisse:       ')
        print(f'Dauer: {elapsedTime}')
        pprint.pprint(self.nsCountDic)
