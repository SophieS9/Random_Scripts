from pyvariantfilter.family import Family
from pyvariantfilter.family_member import FamilyMember
from pyvariantfilter.variant_set import VariantSet

import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


#variable set up
basepath='/data/output/results/210816_A00748_0135_BHVYF5DMXX/IlluminaPCRFree/'
run_id='210816_A00748_0135_BHVYF5DMXX'

print("Calculating CNV metrics")

#Get list of samples
#List all of the folders in the run that aren't post_processing or vc
sample_list = []
for x in os.listdir(basepath):
	path = os.path.join(basepath,x)
	if os.path.isdir(path) and "post_processing" not in x and "vc" not in x:
		sample_list.append(x)

#For every sample, set a family, and make the sample the effected proband
for count,id in enumerate(sample_list):
	
	print("Processing Sample "+id)
	
	my_family = Family('FAM'+str(count))
	proband = FamilyMember(id,str(my_family),2,True)
	my_family.add_family_member(proband)
	my_family.set_proband(proband.get_id())

	#Load SV VCF for "proband" from family
	
	my_variant_set = VariantSet()
	my_variant_set.add_family(my_family)
	my_variant_set.read_variants_from_sv_vcf(basepath+'post_processing/results/sv_cnv/'+run_id+'.sv.cnv.vep.vcf.gz', proband_variants_only = True)	
	
	print('variants loaded')
	print(len(my_variant_set.variant_dict))
	
	master_dict = my_variant_set.to_dict()
	
	#Get some info!
	#output file set up and opening
	outfile = run_id+"_"+id+"_cnv.log"
	OUT = open(outfile,"w")
	
	OUT.write("CNV Summary Metrics \n")
	OUT.write("===================================================================\n\n")
		
	#Count the CNVs
	OUT.write("Total Number of SV/CNVs = "+str(len(master_dict['variants']))+"\n")
	
	#Create lists of possible metrics
	cnv_type=[]	
	callers = []
	pss = 0
	list_fails = []
	chromosomes = []
	consequences = []
	inheritance_modes = []
	quals = []
	for var in master_dict['variants']:
		#Quality scores
		if var['quality']:
			quals.append(int(var['quality']))	
		#SV/CNV types
		if var['info_annotations']['SVTYPE'] not in cnv_type:
			cnv_type.append(var['info_annotations']['SVTYPE'])
		#Callers
		if var['info_annotations']['caller'] not in callers:
                        callers.append(var['info_annotations']['caller'])
		#Pass/fail
		if var['filter_status'] == "PASS":
			pss = pss + 1
		else:
			if var['filter_status'] not in list_fails:
				list_fails.append(var['filter_status'])
		#Chromosomes
		if var['chromosome'] not in chromosomes:
			chromosomes.append(var['chromosome'])
		#Consequences
		if var['worst_consequence'] not in consequences:
			consequences.append(var['worst_consequence'])
		#Inheritance
		if var['inheritance_models'] not in inheritance_modes:
			inheritance_modes.append(var['inheritance_models'])
	
	#Count the type of each SV/CNV with a histogram of lengths
	OUT.write("Types of SV/CNVs:\n")
	for type in cnv_type:
		total=0
		lengths = []
		for var in master_dict['variants']:
			if var['info_annotations']['SVTYPE'] == type:
				total += 1
				lengths.append(var['info_annotations']['sv_length'])
		OUT.write("Total Number of "+type+" = "+str(total)+"\n")
		
		#Histogram of lengths saving to separate png for each type
		plt.hist(lengths,100)
		plt.title('Distribution of '+type+' Lengths in Sample '+id)
		plt.xlabel('Lengths')
		plt.ylabel('Count')
	
		plt.savefig(id+"_"+type+".png")
		plt.close()

	OUT.write("===================================================================\n\n")
	
	#Count the number of CNVs by caller
	OUT.write("CNV caller\n")
	for caller in callers:
		total=0
		for var in master_dict['variants']:
			if var['info_annotations']['caller'] == caller:
				total += 1
		OUT.write(caller+" = "+str(total)+"\n")

	OUT.write("===================================================================\n\n")

	#Count the number of pass/fail
	OUT.write("Total Number PASS = "+str(pss)+"\n")
	#for each fail reason, count the number of occurrences
	for i in list_fails:
		total=0
		for var in master_dict['variants']:
			if var['filter_status'] == i:
				total += 1		
		OUT.write("Total Number FAIL for "+i+" = "+str(total)+"\n")
	
	OUT.write("===================================================================\n\n")

	#Quality Score distribution
	OUT.write("Quality Scores Distributions (Manta calls only)\n")
	#skipping if no quality scores (usually NTC) as crashes calculations
	if len(quals) > 0:
		OUT.write("Number of SV/CNVs with quality score = "+str(len(quals))+"\n")
		OUT.write("Minimum Quality = "+str(min(quals))+"\n")
		OUT.write("Maximum Quality = "+str(max(quals))+"\n")
		OUT.write("Average Quality = "+str(sum(quals)/len(quals))+"\n")
	
	OUT.write("===================================================================\n\n")

	#Count per chromosome
	OUT.write("Total Number Per Chromosome\n")
	#for each chromosome, count the number of occurrences
	for chrm in chromosomes:
		total=0
		for var in master_dict['variants']:
			if var['chromosome'] == chrm:
				total +=1
		OUT.write("Chromosome "+chrm+" = "+str(total)+"\n")
	
	OUT.write("===================================================================\n\n")

	#Number overlapping coding regions and consequences
	OUT.write("Number of Worst Consequences:\n")
	for cons in consequences:
		total=0
		for var in master_dict['variants']:
			if var['worst_consequence'] == cons:
				total += 1
		OUT.write(cons+" = "+str(total)+"\n")

	OUT.write("===================================================================\n\n")

	#Inheritance models
	OUT.write("Inheritance models:\n")
	for inher in inheritance_modes:
		total = 0
		for var in master_dict['variants']:
			if var['inheritance_models'] == inher:
				total +=1
		OUT.write(inher+" = "+str(total)+"\n")

	OUT.close() 

