#script to query panel app API, specifically searching for a gene using a list of genes (one per line). Then returning name of all panels where gene is Green.
#usage: api_panelapp.py <gene list> <output file>

import requests
import sys

#Open file containing genes
GENE_LIST = open(sys.argv[1],"r")

#Open output file for results
OUT = open(sys.argv[2],"w")

#Go through genes one at a time
for gene in GENE_LIST:
	gene = gene.strip()
	api_request = ("https://panelapp.genomicsengland.co.uk/api/v1/genes/"+gene+"/")

	#Query API
	response = requests.get(api_request)

	#if response is OK
	if response.status_code == 200: 
		#Convert response to json
		data = response.json()

		#Empty list to store results of panels
		panels = []

		#Get the results section of the output, which is a list and then for every result, if the evidence is Green, get the name of the panel
		for i in data['results']:
			if "Expert Review Green" in (i['evidence']):
				panels.append((i['panel']['name']))
	
		#Convert list of panels to string for printing
		final_panels = (','.join(panels))

		#If no panels found, just print gene name, otherwise print gene name followed by panels
		if len(panels) == 0:
			OUT.write(gene+"\n")
		else:
			OUT.write("%s\t%s\n" % (gene,final_panels))
	
	#If response not OK
	else:
		print("No API response for "+gene)

GENE_LIST.close
OUT.close
