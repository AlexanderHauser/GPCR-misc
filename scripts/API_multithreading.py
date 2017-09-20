from urlparse import urlparse
from threading import Thread
from Queue import Queue
import httplib, sys
import pandas as pd 
import requests
from Bio import Entrez

max_queue = 10

def doWork():
    while True:
        index = q.get()
        update_family(index)
        q.task_done()

def update_family(index):

    exceptions = {'pd2r2_human': 'Prostaglandin D2 receptor', 'p2ry4_human': "P2Y4", "s1pr4_human":"S1P4"}


    def search(query):
        Entrez.email = 'alexshauser@gmail.com'
        handle = Entrez.esearch(db='pubmed', 
                                sort='relevance',
                                retmax='20000', # more than 10000 possible?
                                retmode='xml', 
                                term=query)
        results = Entrez.read(handle)
        return results

    try:
        gene_term = table[index:index+1]['Gene names  (primary )'].values[0]
        protein_term = table[index:index+1]['Entry name'].values[0]
        protein_name = table[index:index+1]['Protein names'].values[0].split('(')[0]
        chembl = table[index:index+1]['Chembl_compounds'].values[0]

        if protein_term in exceptions:
            protein_term = exceptions[protein_term]

        terms = [gene_term, protein_term]

        results = []

        for term in terms:

            results += search(term)['IdList']

        if len(results)==0 or chembl/len(set(results)) > 20:
            results += search(protein_name)['IdList']

        temp[index] = len(set(results))

    except:
        temp[index] = 0

table = pd.read_csv("/Users/vzw960/Work/Drugtarget_review/data/161020_combined_data.tsv", sep='\t', header = 0)

temp = {}

q = Queue(max_queue * 2)
for i in range(max_queue):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    for index in range(0,table.shape[0]+1):
        q.put(index)
    q.join()
except KeyboardInterrupt:
    sys.exit(1)

table['Pubmed entries'] = pd.DataFrame.from_dict(temp, orient='index')

print table.head(n=10)