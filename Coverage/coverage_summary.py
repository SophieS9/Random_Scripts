#Script to take output from CoverageCalculator.py (at exon level, sorted by exon name) and collapse to gene level
#usage: coverage_summary.py <coverage file> <output>

import os 
import sys

from collections import defaultdict

COV = open(sys.argv[1],"r")

#Make dictionary containing all genes and their average coverage value (use column index 4) or PCT20 (use column ndex5)
genes = defaultdict(list)

for entry in COV:
	if "START" not in entry:
		entry = entry.strip()
		entry = entry.split()
		gene_id = entry[3].split("(")[0]
		genes[gene_id].append(entry[5])

COV.close

OUT = open(sys.argv[2],"w")	
for key in genes:
	#Get values for a gene
	vals = genes[key]
	#Convert to int
	vals_int = [int(float(i)) for i in vals]
	#get average
	av_cov = (sum(vals_int)/len(vals_int))
	OUT.write("%s\t%.2f\n" % (key, av_cov))
