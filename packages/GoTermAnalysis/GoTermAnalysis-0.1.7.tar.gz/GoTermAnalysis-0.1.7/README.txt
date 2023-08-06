This package is for gene ontology analysis. It has 2 main functions: 1. It receives a gene list, and give back the enrichment and merge result. 2. It can update to the newest gene ontology database.

First import this package: 

from gotermanalysis import *

1. ############################Update#############################
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
e. download newest NCBI homo gene file: http://www.ncbi.nlm.nih.gov/gene/
click Download/FTP on left column, directory is Data —> GENE_INFO —> Mammalia —> Homo_sapiens.gene_info.gz, after download it, change file type to .txt

Then Create an instance for updating database and call function to update.
Parameters:
a. homo_gene_directory is the directory that of the previous downloaded NCBI homo gene txt file. 
 
Example of updating database: 
mydb = updateDB.UpdateDB(host, username, password, "assocdb”, homo_gene_directory)
mydb.update()


(2) #################update pubmeds##################

###download and parse###
Parameters:
a. pubmed_directory is the directory that user wants to store the pubmed articles 
b. parsed_pubmed_directory is the directory that user wants to store the parsed pubmed articles 

Example of updating pubmeds:
tool = downloadPubMed.DownloadPubMed(host, username, password, "assocdb”, pubmed_directory, parsed_pubmed_directory)
tool.parse()

###Name entity recognition process###

The name entity recognition process this package using is ABNER. It was developed by  Burr Settles, Department of Computer Sciences, University of Wisconsin-Madison. It was written in Java. For more information, you can go to: http://pages.cs.wisc.edu/~bsettles/abner/

Step of use ABNER.
a. find these 3 files: abner.jar, Tagging.java, Tagging.class. They are wrapping up as extra file in the package. 
b. when you find it and locate in the path, enter the following command in terminal:
java -cp .:abner.jar Tagging  inputpath  outputpath
input path indicates where you pubmeds are, outputpath indicates where you want to store the pubmeds after ABNER analysis

An example of using ABNER:

java -cp .:abner.jar Tagging  /Users/YUFAN/Desktop/parsedPubMeds  /Users/YUFAN/Desktop/files.xml

(3). #################update weights##################
This part builds a GOterm graph structure, and calculate the new weights in this structure

Parameters:
a. input_filepath: parsed pubmeds with ABNER
b. output_filepath: directory to store the output file,  output file is a GO term graph structure

Example of how to update weights:
g=goStructure.GoStructure(host, username, password, "assocdb”, input_filepath, output_filepath)
g.updateWeights()


3. ############################Analysis############################
How to do gene ontology term analysis?

(1). ######enrichment######

Parameters: 
a. inputfile: genelists in a csv file: every row is a list, the first column is drivers of this gene list.  
b. outputfile_path: directory to store the enrichment result. The number of outputfiles is same with the numbers of genelists in input file. Each output file is named by the driver of each genelist.
c. p_value: minimum p-value required for go terms to be enriched
d. top: is an optional parameter for picking up the top number of enrichment result (e.g. top 5 or top 10), by default is none. 

create an instance for enrichment class, then call the function. Example of how to use this class:

tool = enrichment.Enrichment(host, username, password, "assocdb", inputfile, outputfile_path, 0.01)
tool.enrich_csv(top = none)

(2) ######merge######

Parameters: 
a. weightGographData: a xml file which represents Gene Ontology structure, for example “weightedGoGraph.xml"
b. genelist: a csv file contains a genelist (Each input cvs file must contain only one genelist, which means it only has one row!!)
c. output: output_directory
d. p_value: minimum p-value required for go terms to be enriched
e. subGenelistNo: minimum number of genes required for go terms to be enriched

#Create a GoGraph object (Note: every time you use the gotermSummarization(), you need to create a new object)

gograph = merge.GoGraph(weightGographData, genelist, output, p_value, subGenelistNo, host, username, password, "assocdb")
gograph.gotermSummarization()

Result is in the output directory



