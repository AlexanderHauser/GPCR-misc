"""
Created in May 2016

@author: Alexander Hauser <alexshauser@gmail.com>

exchange uniprot accession with entry_names
"""

import os

with open("newick_file.nwk") as f:
    newick = str(f.readlines()[0])
    with open("GPCRs_translate.txt") as t:
        for line in t.readlines():
            line = line.strip().split(",")
            newick = newick.replace(str(line[0]),line[1].upper().split("_")[0])

print newick