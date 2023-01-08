import re
import xml.sax
import WikiHandler


class StatisticsWikiHandler(WikiHandler.WikiHandler):

    def __init__(self, type):
        super().__init__(type)
        self.minImages = 0
        self.maxImages = 0
        self.maxImagesName = ''
        self.imagesCount = 0
        self.artikelCount = 0
        self.minImageLengthRatio = 1
        self.maxImageLengthRatio = 0
        self.sumTextLenght = 0
        self.maxRatioValues = (0, 0, '')
        self.minRatioValues = (0, 0, '')

    def startElement(self, tag, attr):
        self.current = tag
        if self.current == 'page':
            self.title = ''
            self.ns = 0
            self.redirect = ''
            self.inrevision = False
            self.text = ''
            self.textLenght = 1
        if self.current == 'text':
            self.textLenght = int(attr['bytes'])

    def endElement(self, tag):
        if tag == 'page':
            self.count += 1
            if self.count % 100000 == 0:
                print(self.count)
            if self.ns == 0 and not self.redirect:
                self.artikelCount += 1
                if self.title != '':
                    imCount = self.extractImagesCount(self.text)
                    self.imagesCount += imCount
                    self.sumTextLenght += self.textLenght
                    ratio = imCount / self.textLenght

                    if ratio > self.maxImageLengthRatio:
                        self.maxImageLengthRatio = ratio
                        self.maxRatioValues = self.textLenght, imCount, self.title
                    if ratio != 0 and ratio < self.minImageLengthRatio:
                        self.minImageLengthRatio = ratio
                        self.minRatioValues = self.textLenght, imCount, self.title
                    if imCount > self.maxImages:
                        self.maxImages = imCount
                        self.maxImagesName = self.title
                    elif imCount < self.minImages:
                        self.minImages = imCount
        self.current = ''

    def getResults(self):
        return self.minImages, self.maxImages, self.imagesCount, self.artikelCount, self.sumTextLenght, self.minImageLengthRatio, self.maxImageLengthRatio, self.minRatioValues, self.maxRatioValues, self.maxImagesName

    def extractImagesCount(self, inhalt):
        imageSearchString = '(Datei:|Bild:|File:|Image:).*?\.'
        allList = re.findall(imageSearchString, inhalt)
        return (len(allList))

    def extractCategories(self, inhalt):
        categorieSearchString = '\[\[Kategorie:.*?\]?]'
        # Entfernt direkt Start und Endsymbohle und befüllt Liste
        categorieList = []
        for elem in re.finditer(categorieSearchString, inhalt):
            buffer = elem.group()
            cat = buffer[buffer.find(
                ':')+1:].strip('[]').split('|')[0].strip('][').split('<')[0]
            cat = cat.replace('"', "'")
            categorieList.append(cat)
        return categorieList
