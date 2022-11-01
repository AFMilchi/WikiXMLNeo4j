#!/usr/bin/python
import XmlStreamReader as xr


class DebugXml():
    '''Klasse speziell zur Analyse und Troubleshooting
    von Großen XML Dateien die zu groß für RAM sind'''

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


if __name__ == '__main__':
    debugger = DebugXml()
    searchedLine = int(input('Gesuchte Zeile:'))
    plus = int(input('Plus/Minus wie viel?: '))
    debugger.printNLinesBlock(searchedLine, plus)
