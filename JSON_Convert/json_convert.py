#script to convert json variant file from GOSH to readable format
#usage: json_convert.py <JSON input file> 

import json
import os
import sys

#Open and load json file
with open(sys.argv[1],"r") as read_file:
	data = json.load(read_file)

read_file.close

#Get sample identifier, which is the only key value in the samples value of the initial dictionary
sampleID = list(data['samples'].keys())[0]

#Extract a list of variants (each one is a dictionary)
variants = data['samples'][sampleID]['FetalAnomalies1_92']['variants']

#Print how many variants we have
print(len(variants))

output_name = sampleID+"_variants.csv"

#Open output file for writing
OUT = open(output_name,"w")

#Write headers to output
OUT.write("Chromosome,Position,Ref,Alt,Type,Subtype\n")

#scroll through each variant which is a dictionary, go to the 'variant' value, this is another dictionary - make a list of the values from this and output to file 
for i in variants:
	value_list = []
	for key, value in i['variant'].items():
		value_list.append(value)
	OUT.write("%s,%s,%s,%s,%s,%s\n" % (value_list[0],value_list[1],value_list[2],value_list[3],value_list[4],value_list[5]))

OUT.close
