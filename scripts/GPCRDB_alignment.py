"""
Created in Feb 2016

@author: Alexander Hauser <alexshauser@gmail.com>

Fetch big GPCRDB alignments
"""
import requests
import pandas as pd
import pickle

# get all GPCR identifiers and use 

def fetch_all_proteins():
    list_of_human_GPCRs = []
    for i in range(1,6):
        url_classes = "http://gpcrdb.org:80/services/proteinfamily/proteins/00" + str(i) + "/"
        protein_data = requests.get(url_classes).json()
        for protein in protein_data:
            if protein['species'].lower() == "homo sapiens":
                list_of_human_GPCRs.append(str(protein['entry_name']))
    
    return list_of_human_GPCRs

def fetch_alignment(listofgpcrs):
    lind2remove = [i for i in range(340,380)]
    listofgpcrs = [x for i,x in enumerate(listofgpcrs) if i not in lind2remove]
    all_proteins = ','.join(listofgpcrs)
    print all_proteins
    for i in range(0,1):
        try:
            url_protein = "http://gpcrdb.org:80/services/alignment/protein/" + str(all_proteins) + "/TM1%2CTM2%2CTM3%2CTM4%2CTM5%2CTM6%2CTM7/"
            # url_family = "http://gpcrdb.org/services/alignment/family/001_001/TM1%2CTM2%2CTM3%2CTM4%2CTM5%2CTM6%2CTM7/"
            alignment_data = requests.get(url_protein).json()
            break
        except:
            print i
            continue

    print alignment_data

def gpcrdb_alignment_to_fasta():
    print "d"

# list_of_human_GPCRs = fetch_all_proteins()
# with open('list_of_human_GPCRs.txt', 'wb') as f:
#     pickle.dump(list_of_human_GPCRs, f)
    # f.write(str(list_of_human_GPCRs))

with open('list_of_human_GPCRs.txt', 'rb') as f:
    list_of_human_GPCRs = pickle.load(f)

# print list_of_human_GPCRs

GPCR_alignment = fetch_alignment(list_of_human_GPCRs)
with open('GPCR_alignment.txt', 'w') as f2:
    f2.write(str(GPCR_alignment))