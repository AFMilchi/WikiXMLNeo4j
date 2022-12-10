#!/usr/bin/python
import os
import XmlStreamReader as xr
import xml.sax
from DebugWikiHandler import DebugWikiHandler


class DebugXml():
    '''Klasse speziell zur Analyse und Troubleshooting
    von Großen XML Dateien die zu groß für RAM sind'''
    PATH_WIKI_XML = '../wikidump/'
    FILENAME_WIKI = 'dewiki-latest-pages-articles.xml'

    def __init__(self):
        self.reader = xr.XmlStreamReader()

    def printNLine(self, searchedLine):
        count = 1
        for line in self.reader.getNextLine():
            if count >= searchedLine:
                print(count, line)
                break
            count += 1

    def printNLinesBlock(self, searchedLine, plus):
        count = 1
        for line in self.reader.getNextLine():
            if count in range(searchedLine-plus, searchedLine+1+plus):
                print(count, line)
            if count >= searchedLine+plus+10:
                break
            count += 1

    def printArtikel(self, ArtikelName):
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        handler = DebugWikiHandler(ArtikelName)
        parser.setContentHandler(handler)
        pathWikiXml = os.path.join(self.PATH_WIKI_XML, self.FILENAME_WIKI)
        parser.parse(pathWikiXml)


if __name__ == '__main__':
    debugger = DebugXml()
    # searchedLine = int(input('Gesuchte Zeile:'))
    # plus = int(input('Plus/Minus wie viel?: '))
    # debugger.printNLinesBlock(searchedLine, plus)
    debugger.printArtikel('Böhmwind')
