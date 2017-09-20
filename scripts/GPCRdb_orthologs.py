"""
Created in Feb 2017

@ Daniel and Alex

Get all GPCR information for GPCRdb
"""
import pandas as pd 
import requests
from tqdm import *
import json

def get_all_GPCRs():
    url = "http://gpcrdb.org/services/proteinfamily/?page=000"
    res_data = requests.get(url).json()
    df = pd.read_json(json.dumps(res_data))
    df = df[df.slug.str.len()==15]
    df.drop(['parent'], inplace=True, axis=1)
    df = df.reset_index()

    return df

def enrich_information(slug):

    url_fam = "http://test.gpcrdb.org/services/proteinfamily/"+ slug[:11] 
    fam_data = requests.get(url_fam).json()
    Family = fam_data['name']

    url_ligand = "http://test.gpcrdb.org/services/proteinfamily/"+ slug[:7] 
    ltype_data = requests.get(url_ligand).json()
    Ltype = ltype_data['name'].replace(' receptors','')

    url_class = "http://test.gpcrdb.org/services/proteinfamily/"+ slug[:3]
    class_data = requests.get(url_class).json() 
    Class = class_data['name']

    return Class, Ltype, Family

def get_orthologs(slug):
    url = "http://gpcrdb.org/services/alignment/family/" + slug
    orthologs = requests.get(url).json()
    orthologlist = []
    for i in orthologs:
        if i != 'CONSENSUS' and i != 'false':
            orthologlist.append(i)

    return orthologlist

def get_protein_residues(EntryName):

    url = "http://test.gpcrdb.org/services/residues/" + EntryName
    res_data = requests.get(url).json()

    return res_data

## Starts from here
all_GPCRs = get_all_GPCRs()
all_GPCRs_orthos = pd.DataFrame(columns=['name','slug','Class','Ltype','Family'])

print "Generate all GPCR entries including orthologs:"
for index, res in tqdm(enumerate(all_GPCRs.iterrows())):
    slug = all_GPCRs[index:index+1]['slug'].values[0]
    
    try:
        orthos = get_orthologs(slug)
        Class, Ltype, Family = enrich_information(slug)
        all_GPCRs.loc[index,'Class'] = Class
        all_GPCRs.loc[index,'Ltype'] = Ltype
        all_GPCRs.loc[index,'Family'] = Family

        orthodf = all_GPCRs[index:index+1].reset_index()
        sub_index = 0
        for ortho in orthos:
            orthodf.loc[sub_index,'EntryName'] = ortho
            orthodf.loc[sub_index,'name'] = orthodf.loc[0,'name']
            orthodf.loc[sub_index,'slug'] = orthodf.loc[0,'slug']
            orthodf.loc[sub_index,'Class'] = orthodf.loc[0,'Class']
            orthodf.loc[sub_index,'Ltype'] = orthodf.loc[0,'Ltype']
            orthodf.loc[sub_index,'Family'] = orthodf.loc[0,'Family']
            sub_index += 1

        all_GPCRs_orthos = pd.concat([all_GPCRs_orthos, orthodf])
    except:
        print slug

all_GPCRs_orthos.reset_index(drop=True, level=0, inplace=True)
all_GPCRs_orthos.to_csv("saveItSomewhere.csv")

## Fill in Alignment elements
print "\nFill in Alignment elements:"
for index, res in tqdm(enumerate(all_GPCRs_orthos.iterrows())):
    EntryName = all_GPCRs_orthos[index:index+1]['EntryName'].values[0]
    residue_data = get_protein_residues(EntryName)

    for residue in residue_data:
        if residue['display_generic_number']:
            all_GPCRs_orthos.loc[index, residue['display_generic_number']] = residue['amino_acid']

all_GPCRs_orthos.to_csv("thewholething.csv")

