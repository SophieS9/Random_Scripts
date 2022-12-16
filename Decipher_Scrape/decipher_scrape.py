"""
Script to scrape decipher patient variants and research variants from a set gene. Outputs a list of variants

Usage: decipher_scrape.py --gene <GENE_ID> --out <OUT FILE NAME>
"""

import argparse
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

###############################
###        Functions        ###
###############################

def get_patient_variants(gene):
	"""
	Function to web scrape patient variants from Decipher for a given gene
	"""
	
	#Empty list to store variants
	patient_variants=[]

	#Get URL for patient variants for gene
	URL = "https://www.deciphergenomics.org/gene/"+gene+"/patient-overlap/snvs"
	page = requests.get(URL)

	#Use beautiful soup to parse the html
	soup = BeautifulSoup(page.content, "html.parser")

#	print(soup.body.div.prettify())

	return(patient_variants)


def get_research_variants(gene):
	"""
	Function to web scrape research variants from Decipher for a given gene
	"""

	#Empty list to store variants
	research_variants=[]

	#Get URL for research variants for gene - had to use selenium to run the js to get all info
	chrome_options = Options()
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_experimental_option("detach", True)
	chrome_options.add_argument("--headless")

	webdriver_service = Service("./chromedriver") #Your chromedriver path
	driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
	url = "https://www.deciphergenomics.org/gene/"+gene+"/ddd-research-variant-overlap"
	driver.get(url)
	driver.maximize_window()
	time.sleep(5)

	#Use beautiful soup to parse the html
	soup = BeautifulSoup(driver.page_source, "html.parser")
	
	#Markers to use to bring the variant information together as they're in sequential tags in the html
	got_chr = False
	got_pos = False
	got_ref = False
	got_alt = False

	#The information we want is within span tags, specifically those with classes
	for tag in soup.find_all('span'):
	
		#If it has a class label
		if tag.has_attr('class'):
				
			#Chromosome
			if 'chr' in tag['class']:
				chrm = tag.contents[0]
				got_chr = True
				
			#Position
			if 'start' in tag['class']:
				position = tag.contents[0]
				got_pos = True
				
			#Ref - this might be a list if multiple bases, so need to loop
			if 'allele-ref' in tag['class']:
				ref = ''
				for base in tag.contents:
					#Only take the bases
					if 'allele-replace' not in base['class']:
						ref += base.contents[0]
				got_ref = True
				
			#Alt - as above, might be a list
			if 'allele-alt' in tag['class']:
				alt = ''
				for base in tag.contents:
					alt += base.contents[0]
				got_alt = True
			
			#Put together into a variant when all elements got, then reset
			if got_chr and got_pos and got_ref and got_alt:
				
				var = chrm+":"+position+ref+">"+alt
				
				got_chr = False
				got_pos = False
				got_ref = False
				got_alt = False
				
				research_variants.append(var)

	return(research_variants)

###############################
###        Programme        ###
###############################

if __name__ == '__main__':

        ##arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--gene', '-g', help = 'Gene ID')
        parser.add_argument('--out', '-o', help = 'path to output file')
        args = parser.parse_args()

#Get patient variants
patient_variants = get_patient_variants(args.gene)

#Get research variants
research_variants = get_research_variants(args.gene)

#Print out
with open(args.out,'w') as out:
	for var in research_variants:
		out.write(var+"\n")
		
