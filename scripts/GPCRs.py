"""
Created in Sep 2017

@author: Alexander Hauser <alexshauser@gmail.com>

- Make an update of Gene and protein IDs based on the lastest GPCRdb
- includes all Family and Ligandtypes
"""

import requests
import json
import pandas as pd

def get_all_slugs():
    url = 'http://gpcrdb.org/services/proteinfamily/?page=000'
    all_data = requests.get(url).json()
    df = pd.read_json(json.dumps(all_data))

    ## Remove parent column, parent slug, Gproteins and arrestin proteins
    df = df[~df.slug.isin(['000','100','200'])]
    df = df.drop('parent', 1)

    ## Assign target levels
    df['level'] = df.slug.apply(lambda x: 'Class' if len(x.split('_')) == 1 else 'Ligandtype' if len(x.split('_')) == 2 else 'Family' if len(x.split('_')) == 3 else 'Receptor' if len(x.split('_')) == 4 else None)

    return df

info_df = get_all_slugs()

gpcrs = pd.DataFrame(columns=['EntryName','Uniprot','Gene','GeneAlternative','Class','Ligandtype','Family'])

classslugs = info_df[info_df['level']=='Class'].slug.unique()

for slug in classslugs:
    url = "http://www.gpcrdb.org:80/services/proteinfamily/proteins/"+ str(slug)+"/Homo sapiens"
    data = requests.get(url).json()

    for d in data:
      slug = d['family']
      classlevel = info_df[info_df.slug==slug[:-12]].name.values[0]
      ligandtype = info_df[info_df.slug==slug[:-8]].name.values[0]
      family = info_df[info_df.slug==slug[:-4]].name.values[0]

      gpcrs.loc[len(gpcrs)] = pd.Series({'Uniprot':d['accession'], 'EntryName':d['entry_name'], 'Gene': d['genes'][0], 'GeneAlternative': ';'.join(d['genes'][1:]), 'Class':classlevel, 'Ligandtype':ligandtype, 'Family':family})

gpcrs.to_csv("/Users/vzw960/Work/GPCRdb/ID-Mapping/GPCR_Protein_Gene.csv")
