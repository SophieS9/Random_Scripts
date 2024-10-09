"""
Script to predict PULs by extracting GH genes from the dbCAN output and then finding up to 15 genes up and downstream of this gene on the same contig
usage: predict_pul.py --dbcan <dbCAN results> --out <OUTPUT>
"""

import subprocess
import argparse

def get_candidate_gh(dbcan):
    """
    Function to get candidate GH genes based on input list
    """
    #Empty list for GH
    gh = []

    #Open file
    dbcan_file = open(dbcan,"r")

    #Get predictions with >2 tools, and within list of GHs
    for prediction in dbcan_file:

        #Skip header
        if prediction.startswith("Gene"):
            continue

        #Split line based on tab
        prediction = prediction.strip()
        prediction = prediction.split("\t")

        #More than two prediction tools
        if int(prediction[6]) < 2:
            continue 

        #If in list, add to list
        if prediction[4] == "GH3" or "GH43_" in prediction[4] or prediction[4] == "GH2" or prediction[4] == "GH13" or "GH13_" in prediction[4] or "+GH13" in prediction[4] or prediction[4] == "GH23" or prediction[4] == "GH78":
            gh.append(prediction)

    return gh

def get_pul(gh,PROKKA):
    """
    Function to get 15 genes up/downstream of GH
    """

    final_list = []

    for candidate in gh:

        gene_list = []

        #Get gene identifier
        gene_id = candidate[0].split("_")[1]

        #Get contig of candidate
        cmd = f'grep _{gene_id} {PROKKA} | cut -f 1'
        contig = subprocess.check_output(cmd, shell=True,encoding='UTF-8')

        #grep it out of the PROKKA file with 15 lines before and after
        cmd = f"cat {PROKKA} | grep -A 15 -B 15 _{gene_id}"
        hits = subprocess.check_output(cmd, shell=True, encoding='UTF-8')

        #Go over hits, and if they're the same contig, keep
        hits = hits.split("\n")

        for hit in hits:

            hit = hit.split("\t")

            if hit[0] == contig.strip():
                
                #Get gene name from info field of PROKKA file, taking product from last part
                gene_name = hit[8].split(";")[-1]

                gene_name = gene_name.replace('product=','')
                gene_name = gene_name.replace('%2C',',')

                gene_list.append(gene_name)

        #convert gene list to str
        gene_list_str = ','.join(gene_list)

        candidate.append(gene_list_str)

        final_list.append(candidate)

    return final_list

if __name__ == '__main__':

    #Get input files
    parser = argparse.ArgumentParser()
    parser.add_argument('--dbcan', required=True)
    parser.add_argument('--prokka', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    dbcan = args.dbcan
    prokka = args.prokka
    out = args.out

    gh = get_candidate_gh(dbcan)

    final_list = get_pul(gh,prokka) 

    with open(out,'w') as file:

        for line in final_list:
            file.write("\t".join(line)+"\n")
