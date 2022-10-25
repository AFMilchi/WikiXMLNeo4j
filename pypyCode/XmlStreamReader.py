import xml.etree.ElementTree as et
import codecs
import csv
import time
import os
'''Anpassugnen für pypy'''


class XmlStreamReader():
    '''Kümmert sich um das Einlesen des Wikipedia Dumps als XML.
    Das Einlesen erfolgt im Streamverfahren um Arbeitsspeicher zu sparen'''

    '''Konstante Variablen zum Lesen des Databasedumps'''
    PATH_WIKI_XML = '../wikidump/'
    FILENAME_WIKI = 'dewiki-latest-pages-articles.xml'

    def __init__(self):
        '''Konstruktor'''
        self.pathWikiXml = os.path.join(self.PATH_WIKI_XML, self.FILENAME_WIKI)

    def formatTimeElapsed(self, seconds):
        '''Formatierung von Sekunden in hh:mm:ss.ss'''
        h = int(seconds / (60 * 60))
        m = int((seconds % (60 * 60)) / 60)
        s = seconds % 60
        return '{}:{:>02}:{:>05.2f}'.format(h, m, s)

    def getNextArticle(self):
        totalCount = 0
        for event, elem in et.iterparse(self.pathWikiXml, events=('start', 'end')):
            yield event, elem


if __name__ == '__main__':
    test = XmlStreamReader()
    print(test.formatTimeElapsed(1223))
