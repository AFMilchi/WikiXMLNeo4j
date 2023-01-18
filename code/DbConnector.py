from neo4j import GraphDatabase
from Utils import Utils


class DbConnector():
    '''Sorgt für die Anbindung an das DBMS zum Einspielen, Auslesen
        und Manipulieren von Daten
        Parameters:
            dbConnection = GraphDatabase.driver
            session = dbConnection.session'''

    def __init__(self):
        '''Konstruktor'''
        self.dbConnection = GraphDatabase.driver(
            uri='bolt://localhost:7687', auth=('neo4j', 'password'))
        self.session = self.dbConnection.session()

    def createNode(self, nodeType, attributes):
        '''Schreibe Knoten in Datenbank
        Parameters:
            nodeType(String): Art des Knotens, Arikel/Kategorie
            attributes(List): Liste aller Attribute'''
        statement = f'CREATE (n:{nodeType}{{{self.convertDicString(attributes)}}}) return n'
        # print(statement)
        if '' == attributes['title']:
            Utils.log('Ungültige Attributwerte: '+statement)
        else:
            self.sendCommand(statement)

    def sendCommand(self, command):
        '''Sendet ein Commando an die Neo4j Datenbank
        Parameters:
            command(String)'''
        returnValue = self.session.run(command)
        # Wenn es keinen Returnwert gibt, wurde der Knoten / Die Kanten nicht erstellt
        if returnValue.single() is None:
            Utils.log(command)

    def convertDicString(self, dic):
        '''Konvertiert ein Dictonarie in die
            Form "key1: ’value1’, key2: 'value2'"'''
        dicString = str()
        for key, val in dic.items():
            dicString += f'{key}: "{val}", '
        # Stringmanipulation enfernt ", " am Ende
        return dicString[:-2]

    def createAdj(self, fromNodeTitle, toNodeTitle, adjType):
        '''Bei Typ Kategorie wird eine Bidirektionale beziehung Hergstellt. 
        Bei Artikeln welche auf Artikel verlinken nur Unidirektionale verbindungen
        Parameters:
            fromNodeTitle(String)
            toNodeTitle(String)
            adjType(String)'''
        reverseAdj = ''
        toNodeType = ''
        if adjType == 'TEIL_VON_KATEGORIE':
            toNodeType = 'Kategorie'
            reverseAdj = 'CREATE (tn)-[r2:BEINHALTET]->(fn) '
        elif adjType == 'VERLINKT_AUF_ARTIKEL':
            toNodeType = 'Artikel'

        statement = f'MATCH (fn:Artikel), (tn:{toNodeType}) ' + \
            f'WHERE fn.title = "{fromNodeTitle}" AND tn.title = "{toNodeTitle}" ' + \
            f'CREATE (fn)-[r1:{adjType}]->(tn) ' + \
            reverseAdj + \
            f'return r1'
        self.sendCommand(statement)
        # print(statement)

    def createAdjtoCsv(self, fromNodeTitle, toNodeTitle, adjType):
        '''Analog zu createAdj, jedoch wird nicht in die Datenbank sonder in eine CSV Datei geschrieben'''
        with open(f'../csvData/{adjType}.csv', 'a') as file:
            file.write(f'{fromNodeTitle}|{toNodeTitle}\n')


if __name__ == '__main__':
    testConnector = DbConnector()
    mydic = {"brand": "Ford", "model": "Mustang", "year": 1964}
    testConnector.createNode('car', mydic)
