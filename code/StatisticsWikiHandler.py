import re
import xml.sax
import WikiHandler


class StatisticsWikiHandler(WikiHandler.WikiHandler):
    '''Handlerfunktion zur Implementierung des SAX Parser
    Spezialisiert zum Sammel von Statistiken
    Parameters:
        maxImagesname, maxBoxName (string)
        minImages, maxImages, imagesCount, artikelCount, sumTextlengt
            boxFirstLinecount, maxBoxInlineCount, zeroBoxCount, totalboxcount (int)
        connector(DbConnector): Interface zur Datenbank
    '''

    def __init__(self, type):
        '''Konstruktor
        Parameters:
            type(String): Art des Parsmodus'''
        super().__init__(type)
        self.minImages = 0
        self.maxImages = 0
        self.maxImagesName = ''
        self.imagesCount = 0
        self.artikelCount = 0

        self.minImageLengthRatio = 1.0
        self.maxImageLengthRatio = 0.0
        self.sumTextLenght = 0
        self.maxRatioValues = (0, 0, '')
        self.minRatioValues = (0, 0, '')
        self.zeroImageCount = 0

        self.boxFirstLineCount = 0
        self.boxInlineCount = 0
        self.maxBoxInlineCount = 0
        self.maxBoxName = ''
        self.zeroBoxCount = 0
        self.totalBoxCount = 0

    def startElement(self, tag, attr):
        '''Callbackfunktion bei öffnenden Tags
        Parameters:
            tag(String): Name des Tags
            attr(String): Attribute des Tags'''
        self.current = tag
        if self.current == 'page':
            self.title = ''
            self.ns = -1
            self.redirect = ''
            self.inrevision = False
            self.text = ''
            self.textLenght = 1
        if self.current == 'text':
            self.textLenght = int(attr['bytes'])

    def endElement(self, tag):
        '''Callbackfunktion bei schließenden Tags. Hier werden die
        gesammelten Daten verarbeitet
        Parameters:
            tag(String): Name des Tags'''
        if tag == 'page':
            self.count += 1
            if self.count % 100000 == 0:
                print(self.count)
            if self.ns == 0 and not self.redirect:
                if self.title != '':
                    self.artikelCount += 1

                    if self.type == 'Image':
                        self.processImages(self.text)
                    elif self.type == 'Box':
                        self.processBoxes(self.text)
        self.current = ''

    def processBoxes(self, inhalt):
        '''Extrahiert Statistische Infos über die Infoboxen im Volltext
        Parameters:
            inhalt(string): Volltext des Artikels
        '''
        lines = inhalt.splitlines()
        firstLine = lines[0]
        inLine = ' '.join(
            [str(elem) if i > 0 else '' for i, elem in enumerate(lines)])
        firstLineCount = self.extractBoxCount(firstLine)
        self.boxFirstLineCount += firstLineCount
        inLineCount = self.extractBoxCount(inLine)
        self.totalBoxCount += inLineCount + firstLineCount
        if inLineCount > 0:
            self.boxInlineCount += 1
        elif firstLineCount == 0:
            self.zeroBoxCount += 1
        if inLineCount > self.maxBoxInlineCount:
            self.maxBoxInlineCount = inLineCount
            self.maxBoxName = self.title

    def extractBoxCount(self, inhalt):
        '''Extrahiert die Anzahl von Inforboxen im Text
        Parmeters:
            inhalt(String):Volltext oder Ausschnitt von Artikel
        Returns:
            (int):Anzahl an Boxen'''
        boxSearchString = '{{Infobox'
        allList = re.findall(boxSearchString, inhalt)
        return (len(allList))

    def processImages(self, inhalt):
        '''Extrahiert Statistische Infos über Verwendung von Bildern
        Parameters:
            inhalt(String):Volltext'''
        imCount = self.extractImagesCount(inhalt)
        self.imagesCount += imCount
        self.sumTextLenght += self.textLenght
        ratio = imCount / self.textLenght

        if imCount == 0:
            self.zeroImageCount += 1
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

    def extractImagesCount(self, inhalt):
        '''Extrahiert Anzahl Bilder aus String
        Parameters:
            inhalt(String)'''
        imageSearchString = '(Datei:|Bild:|File:|Image:).*?\.'
        allList = re.findall(imageSearchString, inhalt)
        return (len(allList))

    def getResultsImages(self):
        '''Get Funktion um Alle Attribute der Bilder zu bekommen'''
        return self.minImages, self.maxImages, self.imagesCount, self.artikelCount, self.sumTextLenght, self.minImageLengthRatio, self.maxImageLengthRatio, self.minRatioValues, self.maxRatioValues, self.maxImagesName, self.zeroImageCount

    def getResultsBoxes(self):
        '''Getter Funktion um alle Attribute der Boxen zu bekommen'''
        return self.artikelCount, self.boxFirstLineCount, self.boxInlineCount, self.maxBoxInlineCount, self.maxBoxName, self.zeroBoxCount, self.totalBoxCount
