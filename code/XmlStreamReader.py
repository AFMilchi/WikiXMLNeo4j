import xml.etree.ElementTree as et

import codecs
import csv
import time
import Utils

import os


class XmlStreamReader():
    '''Kümmert sich um das Einlesen des Wikipedia Dumps als XML.
    Das Einlesen erfolgt im Streamverfahren um Arbeitsspeicher zu sparen'''

    '''Konstante Variablen zum Lesen des Databasedumps'''
    PATH_WIKI_XML = '../wikidump/'
    FILENAME_WIKI = 'dewiki-latest-pages-articles.xml'

    def __init__(self):
        '''Konstruktor'''
        self.pathWikiXml = os.path.join(self.PATH_WIKI_XML, self.FILENAME_WIKI)

    def getNextArticle(self):
        '''Generatorfunktion zum Einslesen des XML-Dumps alle Pages
        yield: Tupel des Events und des Etree Elements
        ytype: (String, Etree.Element)'''
        for event, elem in et.iterparse(self.pathWikiXml, events=('start', 'end')):
            yield event, elem

    def getNextSiteInfo(self):
        '''Generatorfunktion zum Einslesen des XML-Dumps nur Siteinfo
        yield: Tupel des Events und des Etree Elements und Tag Name
        ytype: (String, Etree.Element, String)'''
        for event, elem in et.iterparse(self.pathWikiXml, events=('start', 'end')):
            tagName = Utils.Utils.stripTagName(elem)
            if event == 'start' and tagName == 'page':
                return 0
            yield event, elem, tagName

    def getNextLine(self):
        '''Generatorfunktion zum Zeilenweisen Einlesen des XML-Dumps
        yield: Die aktuelle Zeile der XML
        ytype: String'''
        with open(self.pathWikiXml, 'r') as file:
            for line in file:
                yield line

        return 'return Value'


if __name__ == '__main__':
    test = XmlStreamReader()
    print(test.formatTimeElapsed(1223))
