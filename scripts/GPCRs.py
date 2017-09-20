"""
Created in Sep 2017

@author: Alexander Hauser <alexshauser@gmail.com>

- Make an update of Gene and protein IDs based on the lastest GPCRdb
"""


import requests

# allGPCRs = []
df = pd.DataFrame(columns=['EntryName','Uniprot','Gene','GeneAlternative'])
for i in range(1,7):
    url = "http://www.gpcrdb.org:80/services/proteinfamily/proteins/00"+ str(i)+"/Homo sapiens"
    data = requests.get(url).json()

    for d in data:
        # content = d['accession'] + ',' + d['entry_name'] + ',' + d['genes'][0] + ',' + ';'.join(d['genes'][1:])
      # allGPCRs.append(content)
      df.loc[len(df)] = pd.Series({'Uniprot':d['accession'], 'EntryName':d['entry_name'], 'Genes': d['genes'][0], 'genesAlternative': ';'.join(d['genes'][1:])})

df.to_csv("/Users/vzw960/Work/GPCRdb/ID-Mapping/GPCR_Protein_Gene.csv")
