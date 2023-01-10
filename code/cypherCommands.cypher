# Lade alle Kategorien aus CSV und baue Relations in beide Richtungen 

:auto using periodic commit 10000
load csv from 'file:///VERLINKT_AUF.csv' as row FIELDTERMINATOR '|'
match(f:Artikel{title:row[0]})
match(t:Artikel{title:row[1]})
create (f)-[r1:VERLINKT_AUF]->(t)


:auto using periodic commit 10000
load csv from 'file:///UNTERKATEGORIE_VON.csv' as row FIELDTERMINATOR '|'
match(f:Kategorie{title:row[0]})
match(t:Kategorie{title:row[1]})
create (t)-[r2:BEINHALTET_UNTERKATEGORIE]->(f)
create (f)-[r1:HAT_OBERKATEGORIE]->(t)




call apoc.meta.stats() yield nodeCount, relCount as totalRelCount
match(n:Artikel)
with n, size((n)--()) as relCount, nodeCount, totalRelCount
return avg(relCount) as averageRelCount, nodeCount, totalRelCount


#delete am besten mit
:auto match ()-[r:HAT_OBERKATEGORIE]->() call {with r delete r} in transactions of 1000 rows;

# create in memory graph Kategories
call gds.graph.project('graph', 'Kategorie', {BEINHALTET_UNTERKATEGORIE:{orientation:'UNDIRECTED'}})
# delete in memory graph
call gds.graph.drop('graph')
# Zyklen
match (m1:Kategorie) with collect(m1) as nodes call apoc.nodes.cycles(nodes) yield path return path
# check ob zusammenhängend
CALL gds.wcc.stream('graph')
YIELD nodeId, componentId
RETURN gds.util.asNode(nodeId).title AS title, componentId
ORDER BY componentId, title

#anzahl Komponenten
CALL gds.wcc.stats('graph')
YIELD componentCount

#anzahl Knoten in Komponenten
CALL gds.wcc.stream('graph')
YIELD nodeId, componentId
RETURN count(gds.util.asNode(nodeId).title) AS titleCount, componentId
order by titleCount desc

# Anzahl Isolierter Knoten
match(N) where not (N)-[*]-() return count(N)
# Erste 10 Isolierte Knoten
match(N) where not (N)-[*]-() return N limit 10
# Liste aller Komponenten, außer Hauptkomponente
CALL gds.wcc.stream('graph')
YIELD nodeId, componentId
where componentId <> 0
with gds.util.asNode(nodeId).title AS title 
match(n) where n.title = title
return n
# Löschen
CALL gds.wcc.stream('graph')
YIELD nodeId, componentId
where componentId <> 0
with gds.util.asNode(nodeId).title AS title 
match(n) where n.title = title
detach delete n
#Anzahl Paths zu allen Knoten von Wurzel aus Zählen
match path = (n:Kategorie{title:'!Hauptkategorie'})-[:BEINHALTET_UNTERKATEGORIE*]->(c)
return c.title, count(*)
# Anzahl der Anzahl Paths zu allen Knoten von Wurzel aus
match path = (n:Kategorie{title:'!Hauptkategorie'})-[:BEINHALTET_UNTERKATEGORIE*]->(c)
with c.title as title, count(*) as numberOfPaths
return numberOfPaths, count(numberOfPaths)
# Längster Pfad im Graph
match path = (n:Kategorie{title:'!Hauptkategorie'})-[:BEINHALTET_UNTERKATEGORIE*]->(c)
return c.title, max(length(path)) as len
order by len desc
# Längster Pfad, wenn stehts der Kürzeste Pfad zu einem Knoten genutzt wird
match path = (n:Kategorie{title:'!Hauptkategorie'})-[:BEINHALTET_UNTERKATEGORIE*]->(c)
return c.title, min(length(path)) as len
order by len desc
#Durchschnittliche Pfadlänge des Graphens
match path = (n:Kategorie{title:'!Hauptkategorie'})-[:BEINHALTET_UNTERKATEGORIE*]->(c)
return avg(length(path)) 
#Durschnittliche Tiefe bei kürzestem Pfad
match path = (n:Kategorie{title:'!Hauptkategorie'})-[:BEINHALTET_UNTERKATEGORIE*]->(c)
with c.title as title, min(length(path)) as len
return avg(len)
# ___________________________
# Artikelgraph spezifische Befehle
# Bestimmung der Anzahl der Dreiecke im Graph
call gds.triangleCount.stats('graph') 
yield globalTriangleCount, nodeCount
