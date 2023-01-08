from FullWikiHandler import FullWikiHandler
from CatTreeWikiHandler import CatTreeWikiHandler
import os
import xml.sax
from AdvStatistics import AdvStatistic

PATH_WIKI_XML = '../wikidump/'
FILENAME_WIKI = 'dewiki-latest-pages-articles.xml'


def main():
    # processData('Kategorie')
    # processFullData('Verlinkung')
    # processCatTreeData('Artikel')
    # processCatTreeData('Kategorie')
    advStatisticer = AdvStatistic()
    # advStatisticer.populateNamespaceDic()
    # advStatisticer.countNamespaces()
    advStatisticer.countImages()


def processFullData(parseType):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = FullWikiHandler(parseType)
    parser.setContentHandler(handler)
    pathWikiXml = os.path.join(PATH_WIKI_XML, FILENAME_WIKI)
    parser.parse(pathWikiXml)


def processCatTreeData(parseType):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = CatTreeWikiHandler(parseType)
    parser.setContentHandler(handler)
    pathWikiXml = os.path.join(PATH_WIKI_XML, FILENAME_WIKI)
    parser.parse(pathWikiXml)


if __name__ == '__main__':
    main()
