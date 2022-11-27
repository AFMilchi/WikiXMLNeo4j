class Utils():

    @staticmethod
    def stripTagName(elem):
        '''Simples entfernen der Nametags, die sonst wie im Beispiel ausehen
        {http://www.mediawiki.org/xml/export-0.10/}page '''
        t = elem.tag
        idx = t.rfind('}')
        if idx != -1:
            t = t[idx + 1:]
        return t

    @staticmethod
    def log(text):
        with open('../log/log.txt', 'a') as file:
            file.write(text+'\n')
