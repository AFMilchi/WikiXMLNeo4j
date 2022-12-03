from WikiHandler import WikiHandler
import os
import xml.sax

PATH_WIKI_XML = '../wikidump/'
FILENAME_WIKI = 'dewiki-latest-pages-articles.xml'


def main():
    # processData('Kategorie')
    processData('Verlinkung')


def processData(parseType):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = WikiHandler(parseType)
    parser.setContentHandler(handler)
    pathWikiXml = os.path.join(PATH_WIKI_XML, FILENAME_WIKI)
    parser.parse(pathWikiXml)


if __name__ == '__main__':
    main()
