This package is for gene ontology analysis. It has 2 main functions: 1. It receives a gene list, and give back the enrichment and merge result. 2. It can update to the newest gene ontology database.

1. ############################Analysis############################
How to do gene ontology term analysis?

(1). ######enrichment######
create an instance for enrichment class, then call the function:

1. inputfile is genelists in a csv file: every row is a list, the first column is drivers of this gene list.  
2. outputfile_path is the directory to store the enrichment result. The number of outputfiles is same with the numbers of genelists in input file. Each output file is named by the driver of each genelist.
3. threshold is the significant p-value threshold
2. top is an optional parameter for picking up the top number of enrichment result (e.g. top 5 or top 10), by default is none. 

Example of how to use this class:

tool = enrichment.Enrichment("localhost", "fanyu", "hellowork", "assocdb", "MLL2-MLL3.targetgenes.v9.csv", "", 0.01)
tool.enrich_csv()

(2) ######merge######
Create an instance of GoGraph class:

#Data of Go Ontology structure and gene_Goterm association
weightGographData = "weightedGoGraph.xml"
genelist = GeneList_csv_directory
output = output_directory
p_value = 0.05
subGenelistNo = 3

#Create a GoGraph object (Note: every time you use the gotermSummarization(), you need to create a new object)
gograph = merge.GoGraph("weightedGraph.xml", "MLL2-MLL3.targetgenes.v9.csv", "", 0.01, 3, "localhost", "fanyu", "hellowork", "assocdb")
gograph.gotermSummarization()

Result is in the output directory

2. ############################Update#############################
How to update?

(1). #################update database##################
Before update database, user must complete the following steps: 
a. download the newest database dump: http://archive.geneontology.org/latest-lite/
b. add .sql to current database dump file, for example: change "go_20151003-assocdb-data" to "go_20151003-assocdb-data.sql"
c. log into database on server and type the following command:
	DROP DATABASE IF EXISTS assocdb
	CREATE DATABASE IF EXISTS assocdb
	quit
d. type the following command: 
        mysql -h localhost -u username -p assocdb <dbdump
   for example: 
        mysql -h localhost -u username -p assocdb <go_20151003-assocdb-data.sql
e. download 

Then update database as following: 
create an instance for updating database, then call the function:
mydb = updateDB.UpdateDB("localhost", "fanyu", "hellowork", "assocdb", "gene_ontology/util/originalData/Homo_sapiens.gene_info.gene_info.txt")
mydb.update()


(2) #################update pubmeds##################

###download and parse###

example of using download and parse pubmed
pubmed_directory is the directory that user wants to store the pubmed articles 
tool = downloadPubMed.DownloadPubMed("localhost", "fanyu", "hellowork", "assocdb")
tool.parse()

###Name entity recognition process###

The name entity recognition process this package using is ABNER. It was developed by  Burr Settles, Department of Computer Sciences, University of Wisconsin-Madison. It was written in Java. For more information, you can go to: http://pages.cs.wisc.edu/~bsettles/abner/

Step of use ABNER.
a. find these 3 files: abner.jar, Tagging.java, Tagging.class. They are wrapping up as extra file in the package. 
b. when you find it and locate in the path, enter the following command in terminal:
java -cp .:abner.jar Tagging  inputpath  outputpath
input path indicates where you pubmeds are, outeutpath indicates where you want to store the pubmeds after ABNER analysis

An example of using ABNER:

java -cp .:abner.jar Tagging  /Users/YUFAN/Desktop/parsedPubMeds  /Users/YUFAN/Desktop/files.xml

3. #################update weights##################
This part builds a GOterm graph structure, and calculate the new weights in this structure

The input file is parsed pubmeds with ABNER
The output file is a GO term graph structure
Stopwords is a txt file contains NLP stop words

The input file path is where the parsed pubmeds are stored 
The output file path is the directory where user want to store the output GO term graph structure

input_filepath = "../taggedAbstracts/files.xml"
output_filepath = "weightedGoGraph.xml"

Example of how to update weights:
g=goStructure.GoStructure("localhost", "fanyu", "hellowork", "assocdb", "files.xml", "")
g.updateWeights()


