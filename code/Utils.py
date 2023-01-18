class Utils():
    '''Statische Klasse zum Auslagern von öfters genutzten Funktionen'''

    @staticmethod
    def stripTagName(elem):
        '''Simples entfernen der Nametags, die sonst wie im Beispiel ausehen
        {http://www.mediawiki.org/xml/export-0.10/}page 
        Parameters:
            elem(String): Tag Name der gestript werden soll
        Returns:
            t(String): Gestrippter Tagname'''
        t = elem.tag
        idx = t.rfind('}')
        if idx != -1:
            t = t[idx + 1:]
        return t

    @staticmethod
    def log(text):
        '''Logt den übergebenen Wert
        Parameters:
            text:(String): Der Text, der geloggt werden soll'''
        with open('../log/log.txt', 'a') as file:
            file.write(text+'\n')
