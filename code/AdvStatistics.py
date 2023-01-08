import XmlStreamReader as xr
import time
import Utils
import pprint
import os
import xml.sax
from StatisticsWikiHandler import StatisticsWikiHandler
from BasicStatistics import BasicStatistics


class AdvStatistic(BasicStatistics):
    PATH_WIKI_XML = '../wikidump/'
    FILENAME_WIKI = 'dewiki-latest-pages-articles.xml'

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

    def countImages(self):
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        handler = StatisticsWikiHandler(None)
        parser.setContentHandler(handler)
        pathWikiXml = os.path.join(self.PATH_WIKI_XML, self.FILENAME_WIKI)
        parser.parse(pathWikiXml)
        self.formatResults(handler.getResults())

    def formatResults(self, args):
        minImages, maxImages, imagesCount, artikelCount, sumTextLenght, minImageLengthRatio, maxImageLengthRatio, minRatioValues, maxRatioValues, maxImagesName = args

        print(
            f'''Minimal: {minImages}, Maximal {maxImages} Name: {maxImagesName}
            AnzahlBilder: {imagesCount}
            AnzahlArtikel: {artikelCount}
            Durchschnitt: {imagesCount/artikelCount}
            ________________________________
            Durchschnittliche Artikellänge: {sumTextLenght/artikelCount}
            Summe der Artikellänge: {sumTextLenght}
            Kleinste Ratio: {minImageLengthRatio} Bei Länge {minRatioValues[0]} {minRatioValues[1]} Bilder, Name: {minRatioValues[2]}
            Größte Ratio: {maxImageLengthRatio} Bei Länge {maxRatioValues[0]} {maxRatioValues[1]} Bilder, Name: {maxRatioValues[2]}''')

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
