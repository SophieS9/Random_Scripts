#!/usr/bin/env python

"""
Script to filter SpliceAI annotation files for only variants with a score of >0.2 in either DS_AG, DS_AL, DS_DG, DS_DL. If any of these metrics have a score >0.2, the variant is kept and the highest score is added to INFO as MaxSpliceAI. 
"""

from pysam import VariantFile
import argparse

#Setting up argument parser so that the VCF file can be passed as --vcf and output file as --out
parser = argparse.ArgumentParser(description='Filtering of SpliceAI VCF files based on DS_AG, DS_AL, DS_DG or DS_DL < 0.2')
parser.add_argument('--vcf', type=str, nargs=1, required=True,
				help='vcf file location')
parser.add_argument('--out', type=str,nargs=1, required=True,
				help='output file name')
args = parser.parse_args()

vcf = args.vcf[0]

#Use VariantFile to process the VCF
myvcf = VariantFile(vcf)

#Modify INFO to also include the MaxSpliceAI value
myvcf.header.info.add('MaxSpliceAI','.','Float','Maximum SpliceAI value')

#Set up output file
OUT = VariantFile(args.out[0], 'w', header=myvcf.header)

#Loop through VCF file, taking the SpliceAI value from INFO and then splitting based on | separator. 
for variant in myvcf:
	spliceai = variant.info['SpliceAI']
	
	#Create empty list for all of the values for DS_AG, DS_AL, DS_DG, DS_DL
	variant_values = []
	
	#Loop over spliceai, taking the values and adding them to variant_values
	for gene in spliceai:
		gene_values=gene.split('|')
		variant_values.append(gene_values[2])
		variant_values.append(gene_values[3])
		variant_values.append(gene_values[4])
		variant_values.append(gene_values[5])
	
	max_splice_ai = max(variant_values)
	
	variant.info['MaxSpliceAI'] = float(max_splice_ai)
	
	if float(max_splice_ai) >= 0.2:
		OUT.write(variant)	

