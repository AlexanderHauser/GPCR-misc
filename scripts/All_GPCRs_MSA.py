"""
Created in Apr 2016

@author: Alexander Hauser <alexshauser@gmail.com>

- fetch an alignment of all GPCRs from GPCRdb
- create a fasta output for an alignment software
"""

import pandas as pd 
import requests
import numpy as np
import os

def alignment_fetch():

    family_slugs = ["001", "002", "003", "004", "005"]
    with open("Whole_class_alignment.fasta", "w") as fname:
        for slug in family_slugs:
            url = "http://localhost:8000/services/alignment/family/"+ slug +"/TM1,ICL1,TM2,ECL1,TM3,ICL2,TM4,ECL2,TM5,TM6,TM7/Homo sapiens/"
            alignment_data = requests.get(url).json()

            for protein in alignment_data:
                fname.write(">" + protein + "\n" + alignment_data[protein] + "\n")

alignment_fetch()
