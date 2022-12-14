# Lade alle Kategorien aus CSV und baue Relations in beide Richtungen 
:auto using periodic commit 100000
load csv from 'file:///categories.csv' as row FIELDTERMINATOR ';'
match(f:Artikel{title:row[0]})
match(t:Kategorie{title:row[1]})
create (f)-[r2:TEIL_VON_Kategorie]->(t)
create (t)-[r1:BEINHALTET]->(f)



:auto using periodic commit 10000
load csv from 'file:///VERLINKT_AUF.csv' as row FIELDTERMINATOR '|'
match(f:Artikel{title:row[0]})
match(t:Artikel{title:row[1]})
create (f)-[r1:VERLINKT_AUF]->(t)


:auto using periodic commit 10000
load csv from 'file:///UNTERKATEGORIE_VON.csv' as row FIELDTERMINATOR '|'
match(f:Artikel{title:row[0]})
match(t:Artikel{title:row[1]})
create (f)-[r1:HAT_OBERKATEGORIE]->(t)
create (t)-[r2:BEINHALTET_UNTERKATEGORIE]->(f)




call apoc.meta.stats() yield nodeCount, relCount as totalRelCount
match(n:Artikel)
with n, size((n)--()) as relCount, nodeCount, totalRelCount
return avg(relCount) as averageRelCount, nodeCount, totalRelCount:wq

