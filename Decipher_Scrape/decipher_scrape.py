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

	#Get URL for research variants for gene
	chrome_options = Options()
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_experimental_option("detach", True)

	webdriver_service = Service("./chromedriver") #Your chromedriver path
	driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
	url = "https://www.deciphergenomics.org/gene/"+gene+"/ddd-research-variant-overlap"
	driver.get(url)
	driver.maximize_window()
	time.sleep(5)
	#accept cookie
	driver.find_element(By.XPATH,'//*[@id="onetrust-button-group-parent"]/div/button[1]').click()
	time.sleep(2)

	#Uae beautiful soup to parse the html
	soup = BeautifulSoup(driver.page_source, "lxml")
	
	print(soup.prettify())

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

