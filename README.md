# WikiXMLNeo4j
Diese Repo ist Teil der BA "Kleine-Welt-Wikipedia - Eine Erhebung und Analyse der internen Verlinkungsstruktur der deutschsprachigen Wikipedia"
Author: Andreas Faaß

Im Repository ist eine Ansammlung an Klassen zum Einlesen, Verarbeiten, Analysieren eines Wikipedia Dumps im XML Format.
Der Wikipedia dump ist im Ordner Wikipdump als xml zu hinterlegen.
Herunterzuladen unter: https://dumps.wikimedia.org/dewiki/latest/dewiki-latest-pages-articles.xml.bz2

Datenbank:
Der DbConnector erwartet eine Neo4j Instanz unter bolt://localhost:7687 mit U/P neo4j/password

Genutzt wird die main.py zum Starten. Wenn unterschiedliche Funktionalität benötigt werden, muss die main händisch angepasst werden.
Weiterhin wird das Repo zur Archivierung von Daten, Texten und Bildern genutzt, welche nicht im Overleaf liegen.
Es finden sich die Klassendiagramme, Transkripte der Klassendiagramme und die QualCoder Daten aus der qualitativen Auswertung.

Benötigte Packages:


Datenbank:
Neo4j - pip install neo4j
bs4 - pip install bs4




