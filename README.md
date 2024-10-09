# Random_Scripts
Collection of random scripts with no other home!

CNV Metrics
------
A python script to produce metrics on CNV calls from a VEP annotated VCF file. This script utilises the pyvariantfilter package to parse the VCF and matplotlib for plots.


SpliceAI Filter
------
A python script to filter the [SpliceAI](https://github.com/Illumina/SpliceAI) VCF file for genome build 38. Includes bash script for submitting this as a job on a SLURM scheduler. 


Coverage
------
A python script to take the output from [CoverageCalculatorPy](https://github.com/AWGL/CoverageCalculatorPy) when split at exon level and produce average for each gene.


JSON Convert
------
A python script to take a JSON file supplied by GOSH containing variant information and convert this to a csv file format containing just the key information on variant location, ref/alt allele, type and subtype.  


PanelApp API Query
-----
A python script to query the PanelApp API for genes and to then parse the information to retrieve information on panels where the genes are reviewed as green. 


Decipher Scrape
-----
A python script to get all patient and research variant for a given gene from decipher. Has it's own conda environment yml with necessary packages. 


PUL Prediction
-----
A python script to take an output from dbCAN and use this to predict PULs based on 15 genes up and downstream of a key class of GHs. 
