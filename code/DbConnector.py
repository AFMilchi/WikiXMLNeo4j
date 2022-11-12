from neo4j import GraphDatabase


class DbConnector():
    '''Sorgt für die Anbindung an das DBMS zum Einspielen, Auslesen
        und Manipulieren von Daten'''

    def __init__(self):
        self.dbConnection = GraphDatabase.driver(
            uri='bolt://localhost:7687', auth=('neo4j', 'password'))
        self.session = self.dbConnection.session()

    def createNode(self, nodeType, attributes):
        statement = f'CREATE (n:{nodeType}{{{self.convertDicString(attributes)}}})'
        print(statement)
        self.sendCommand(statement)

    def sendCommand(self, command):
        self.session.run(command)

    def convertDicString(self, dic):
        '''Konvertiert ein Dictonarie in die
            Form "key1: ’value1’, key2: 'value2'"'''
        dicString = str()
        for key, val in dic.items():
            dicString += f"{key}: '{val}', "
        # Stringmanipulation enfernt ", " am Ende
        return dicString[:-2]

    def createAdj(self, fromNode, toNode, adjType):
        '''Bei Typ Kategorie wird eine Bidirektionale beziehung Hergstellt. 
        Bei Artikeln welche auf Artikel verlinken nur Unidirektionale verbindungen'''
        reverseAdj = ''
        if adjType == 'TEIL_VON_KATEGORIE':
            toNodeType = 'Kategorie'
            reverseAdj = f'CREATE (tn)-[r2:BEINHALTET]->(fn)'
        elif adjType == 'VERLINKT_AUF_ARTIKEL':
            toNodeType = 'Artikel'
        statement = f'MATCH (fn:Artikel), (tn:{toNodeType})' + \
            f'WHERE fn.title = "{fromNode}" AND tn.title = "{toNode}"' + \
            f'CREATE (fn)-[r1:{adjType}]->(tn)' + \
            reverseAdj
        print(statement)


if __name__ == '__main__':
    testConnector = DbConnector()
    mydic = {"brand": "Ford", "model": "Mustang", "year": 1964}
    testConnector.createNode('car', mydic)
