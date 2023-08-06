##check if the index exists
-- DELIMITER $$
-- DROP PROCEDURE IF EXISTS drop_index_if_exists $$
-- CREATE PROCEDURE drop_index_if_exists(in theTable varchar(128), in theIndexName varchar(128) )
-- BEGIN
--  IF((SELECT COUNT(*) AS index_exists FROM information_schema.statistics WHERE TABLE_SCHEMA = DATABASE() and table_name =
-- theTable AND index_name = theIndexName) > 0) THEN
--    SET @s = CONCAT('DROP INDEX ' , theIndexName , ' ON ' , theTable);
--    PREPARE stmt FROM @s;
--    EXECUTE stmt;
--  END IF;
-- END $$

-- DELIMITER ;
-- call drop_index_if_exists('gene_product','genesymbolindex');
DELETE FROM term where term.is_obsolete = 1 and term_type = "biological_process";
CREATE INDEX genesymbolindex ON gene_product(symbol);

DROP VIEW IF EXISTS NCBIsymbol;
CREATE VIEW NCBIsymbol AS SELECT DISTINCT(symbol) FROM symbol_synonym;
DROP VIEW IF EXISTS symbolonly_term;
CREATE VIEW symbolonly_term AS SELECT A.id AS accid,A.term_id,A.gene_product_id,T.name,T.term_type, T.acc,G.full_name,G.species_id,G.symbol,NS.symbol AS offsymbol FROM association AS A, term AS T, gene_product AS G,NCBIsymbol AS NS, species as S WHERE G.id=A.gene_product_id AND T.term_type="biological_process" AND T.id=A.term_id AND G.symbol=NS.symbol AND G.species_id=S.id AND S.genus = "Homo" AND S.species = "sapiens";
DROP VIEW IF EXISTS temp_symbol_term;
CREATE VIEW temp_symbol_term AS SELECT offsymbol,acc FROM symbolonly_term;
DROP VIEW IF EXISTS pure_symbol_term;
CREATE VIEW pure_symbol_term AS SELECT * FROM temp_symbol_term group by offsymbol,acc having count(*)>1;
DROP VIEW IF EXISTS synonym;
CREATE VIEW synonym AS SELECT synonym FROM symbol_synonym;
DROP VIEW IF EXISTS synonym_term;
CREATE VIEW synonym_term AS SELECT A.id AS accid,A.term_id,A.gene_product_id,T.name,T.term_type, T.acc,G.full_name,G.species_id,G.symbol,S.synonym FROM association AS A, term AS T, gene_product AS G , synonym AS S, species as SP WHERE G.id=A.gene_product_id AND T.term_type="biological_process" AND T.id=A.term_id AND G.symbol=S.synonym AND G.species_id=SP.id AND SP.genus = "Homo" AND SP.species = "sapiens";
DROP VIEW IF EXISTS  synonym_term_symbol;
CREATE VIEW synonym_term_symbol AS SELECT ST.accid,ST.term_id,ST.gene_product_id,ST.name,ST.term_type,ST.acc,ST.full_name,ST.species_id,ST.symbol,ST.synonym,SS.symbol AS offcialsymbol,SS.synonym AS synonym1 FROM synonym_term AS ST, symbol_synonym AS SS WHERE ST.synonym=SS.synonym;
DROP VIEW IF EXISTS temp_synonym_term;
CREATE VIEW temp_synonym_term AS SELECT offcialsymbol,acc FROM synonym_term_symbol;
DROP VIEW IF EXISTS pure_symbol_term;
CREATE VIEW pure_symbol_term AS SELECT * FROM temp_symbol_term GROUP BY offsymbol,acc HAVING count(*)>1;
DROP VIEW IF EXISTS pure_synonym_term;
CREATE VIEW pure_synonym_term AS SELECT * FROM temp_synonym_term GROUP BY offcialsymbol,acc HAVING count(*)>1;
DROP TABLE IF EXISTS final_symbol_term;
CREATE TABLE final_symbol_term AS SELECT * FROM pure_symbol_term UNION SELECT * FROM pure_synonym_term;

#####Evidence table
DROP TABLE IF EXISTS term_evidence;
CREATE TABLE term_evidence AS SELECT D.xref_key,T.id AS termid FROM dbxref AS D, association AS A, gene_product AS G,term AS T, evidence AS E, species as S WHERE A.id=E.association_id AND A.gene_product_id=G.id AND G.species_id=S.id AND S.genus = "Homo" AND S.species = "sapiens" AND A.term_id=T.id AND T.term_type= "biological_process" AND E.dbxref_id=D.id AND D.xref_dbname IN ("PMID","PubMed") ORDER BY termid;
DROP TABLE IF EXISTS distinct_term_evidence;
CREATE TABLE distinct_term_evidence AS SELECT xref_key,termid FROM term_evidence GROUP BY xref_key,termid;
DROP TABLE IF EXISTS term_parent;
CREATE TABLE term_parent AS SELECT * FROM distinct_term_evidence AS TE, term2term AS TT WHERE TE.termid=TT.term2_id AND TT.relationship_type_id=1;
DROP TABLE IF EXISTS term_parent2;
CREATE TABLE term_parent2 AS SELECT TP.xref_key,TP.term1_id FROM term_parent AS TP;
DROP TABLE IF EXISTS distinct_term_parent2;
CREATE TABLE distinct_term_parent2 AS SELECT xref_key,term1_id FROM term_parent2 group by xref_key,term1_id;
DROP TABLE IF EXISTS totalterm_evidence;
CREATE TABLE totalterm_evidence AS SELECT * FROM distinct_term_parent2 UNION SELECT * FROM distinct_term_evidence;
DROP TABLE IF EXISTS final_term_evidence;
CREATE TABLE final_term_evidence AS SELECT TE.term1_id AS termid, TE.xref_key AS pmid, T.acc AS acc FROM totalterm_evidence as TE, term AS T where T.id=TE.term1_id;


CREATE INDEX termname on term(acc);
DROP TABLE IF EXISTS term_n;
CREATE TABLE term_n AS SELECT acc, count(*) AS n FROM final_symbol_term group by acc;

#term graph table, filter out term of type "biological process"
DROP TABLE IF EXISTS termgraph;
CREATE TABLE termgraph AS SELECT temp.relationship_type_id,temp.term1_id,temp.term2_id,temp.term1_type,temp.term1_acc,term.acc AS term2_acc,term.term_type AS term2_type FROM term, (SELECT relationship_type_id,term1_id,term2_id,T.term_type AS term1_type,T.acc AS term1_acc FROM term2term AS TT, term AS T WHERE T.id= TT.term1_id AND T.term_type="biological_process") AS temp WHERE temp.term2_id=term.id AND term.term_type="biological_process" and temp.relationship_type_id=1;

#clean up
DROP VIEW NCBIsymbol
DROP VIEW symbolonly_term
DROP VIEW temp_symbol_term
DROP VIEW pure_symbol_term
DROP VIEW synonym
DROP VIEW synonym_term
DROP VIEW synonym_term_symbol
DROP VIEW temp_synonym_term
DROP VIEW pure_symbol_term
DROP VIEW pure_synonym_term