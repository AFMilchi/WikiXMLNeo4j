#!/usr/bin/python
import XmlStreamReader as xr


class DebugXml():
    '''Klasse speziell zur Analyse und Troubleshooting
    von Großen XML Dateien die zu groß für RAM sind'''

    def __init__(self):
        self.reader = xr.XmlStreamReader()


if __name__ == '__main__':
    test = DebugXml()
    print('test')
    print(test.reader.getNextLine())
    test.reader.test()
