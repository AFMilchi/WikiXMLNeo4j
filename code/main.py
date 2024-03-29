from FullWikiHandler import FullWikiHandler
from CatTreeWikiHandler import CatTreeWikiHandler
from ArtikelTreeWikiHandler import ArtikelTreeWikiHandler
from DataProcessor import DataProcessor
import os
import xml.sax
from AdvStatistics import AdvStatistic

PATH_WIKI_XML = '../wikidump/'
FILENAME_WIKI = 'dewiki-latest-pages-articles.xml'


def main():
    '''Einstiegspunkt zum Starten der Module'''
    # processData('Kategorie')
    # processFullData('Verlinkung')
    # processCatTreeData('Artikel')
    # processCatTreeData('Kategorie')

    advStatisticer = AdvStatistic()
    # advStatisticer.populateNamespaceDic()
    # advStatisticer.countNamespaces()
    advStatisticer.countImages()
    # advStatisticer.countInfoBoxes()


def processFullData(parseType):
    '''Starterfunktion zum Parsen und Erstellen des Full-Graphs
    Parameters:
        parseType(String): Gibt Art des Parsens an'''
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = FullWikiHandler(parseType)
    parser.setContentHandler(handler)
    pathWikiXml = os.path.join(PATH_WIKI_XML, FILENAME_WIKI)
    parser.parse(pathWikiXml)


def processCatTreeData(parseType):
     '''Starterfunktion zum Parsen und Erstellen des Kategorie-Graphs
    Parameters:
        parseType(String): Gibt Art des Parsens an'''
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = CatTreeWikiHandler(parseType)
    parser.setContentHandler(handler)
    pathWikiXml = os.path.join(PATH_WIKI_XML, FILENAME_WIKI)
    parser.parse(pathWikiXml)


def processArtikleData(parseType):
      '''Starterfunktion zum Parsen und Erstellen des Artikel-Graphs
    Parameters:
        parseType(String): Gibt Art des Parsens an'''
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = ArtikelTreeWikiHandler(parseType)
    parser.setContentHandler(handler)
    pathWikiXml = os.path.join(PATH_WIKI_XML, FILENAME_WIKI)
    parser.parse(pathWikiXml)


if __name__ == '__main__':
    main()
