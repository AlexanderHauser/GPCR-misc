"""
Created in Jul 2016

@author: Alexander Hauser <alexshauser@gmail.com>

visualise the similarity/ identity within a receptor family
"""

import os
import requests
import pandas as pd
from collections import OrderedDict
from ast import literal_eval
import seaborn as sns
import matplotlib.pyplot as plt

def get_proteins_of_slug(slug):
    # get ligand_type specific GPCRdb reesidue numbers
    list_of_proteins = {}
    url_protein = 'http://test.gpcrdb.org/services/proteinfamily/proteins/' + slug + '/Homo sapiens'
    ProteinsInFamily_data = requests.get(url_protein).json()

    for protein in ProteinsInFamily_data:
        # print protein['entry_name']
        list_of_proteins[protein['entry_name']] = protein['family'][4:-8]

    return list_of_proteins

def get_families_of_slug(slug):
    # get ligand_type specific GPCRdb reesidue numbers
    list_of_families = {}

    def get_families(slug):
        url_protein = 'http://test.gpcrdb.org:80/services/proteinfamily/children/' + slug
        family_slugs = requests.get(url_protein).json()

        return family_slugs

    if len(slug) <= 3:
    	ligandtype_slugs= {}
        ligandtype_slugs_raw = get_families(slug)

        for LT in ligandtype_slugs_raw:
            ligandtype_slugs[LT['slug']] = LT['name']

    else:
    	ligandtype_slugs = {slug:slug}

    for slug in ligandtype_slugs.keys():

        family_slugs = igandtype_slugs = get_families(slug)

        for family in family_slugs:
            list_of_families[family['slug']] = family['name']


    return list_of_families

def similarity_search(list_of_proteins, search_protein, segments=['TM1','TM2','TM3','TM4','TM5','TM6','TM7'], top=5):

    segments = ','.join(segments)

    url_protein = 'http://test.gpcrdb.org/services/alignment/similarity/'+search_protein + ',' + ','.join(list_of_proteins) + '/' + segments

    similarity_data = requests.get(url_protein).json()
    
    similarity_data = OrderedDict(sorted(similarity_data.items(), key=lambda x: (x[1]['similarity'], x[1]['identity']), reverse=True))

    return similarity_data

def similarity_within_family(slug): 

    proteins = get_proteins_of_slug(slug).keys()
    list_of_compares = list(proteins)
    list_sim = []
    list_ide = []

    for i, search_protein in enumerate(proteins):

        sim_data = similarity_search(list_of_compares, search_protein,['TM1','TM2','TM3','TM4','TM5','TM6','TM7'], len(proteins))
        list_of_compares.remove(search_protein)

        sim_data_list = [x for x in sim_data.keys() if x != search_protein]

        for name in sim_data_list:
            # print search_protein, name, sim_data[name]['similarity'], sim_data[name]['identity']
            list_sim.append(int(sim_data[name]['similarity']))
            list_ide.append(int(sim_data[name]['identity']))
            # df.loc[len(df)] = pd.Series({'Family': slug,'LigandType': slug,'Similarities': int(sim_data[name]['similarity']),'Identities': int(sim_data[name]['identity'])})
            df.loc[len(df)] = pd.Series({'Family': list_of_families[slug].replace("receptors",""),'LigandType': familyID_translation[slug[:-4]],'Value': int(sim_data[name]['similarity']),'Category': 'Similarity'})
            df.loc[len(df)] = pd.Series({'Family': list_of_families[slug].replace("receptors",""),'LigandType': familyID_translation[slug[:-4]],'Value': int(sim_data[name]['identity']),'Category': 'Identify'})

    # print df

familyID_translation = {"001_001": "aminergic",
                        "001_002": "peptide",
                        "001_003": "protein",
                        "001_004": "lipid",
                        "001_005": "melatonin",
                        "001_006": "nucleotide",
                        "001_007": "steroid",
                        "001_008": "alicarboxylic",
                        "001_009": "sensory",
                        "001_010": "orphan",
                        "002_001": "peptide",
                        "003_001": "orphan",
                        "004_001": "ion",
                        "004_002": "amino acid",
                        "004_003": "sensory",
                        "004_004": "orphan"}

# ==================
# ====== DATA ======
# ==================

# df = pd.DataFrame(columns=['Family','LigandType','Value','Category'])

# list_of_families = get_families_of_slug("001")
# slugs = list_of_families.keys()

# for slug in slugs:
#     print "Load " + list_of_families[slug]
#     similarity_within_family(slug)

# df.to_csv("/Users/vzw960/Work/GPCRdb/similarities_of_families/sims_classC.csv")

# =================
# ====== VIS ======
# =================
df = pd.read_csv("/Users/vzw960/Work/GPCRdb/similarities_of_families/sims_classA.csv")

sns.set(style="whitegrid", color_codes=True)
f, ax = plt.subplots(figsize=(15, 10))
ax.set(ylim=(0, 100))


# Simlarity or Identity ? 
df = df[df['Category']=='Similarity']
# Specific family or ligandtype?
df = df[df['LigandType']=='lipid']
# df = df[df['Family']=='Vasopressin and oxytocin ']

sort_value = "Family"

sns.violinplot(x = sort_value, y = "Value", data=df, bw=0.5, cut=0, palette="muted", linewidth=1, split=True)
# sns.violinplot(x="Family", y="Value", hue='Category', data=df, bw=.4, cut=0, linewidth=1, split=True)
# sns.boxplot(x="Family", y="Value", hue='Category', data=df, )
sns.swarmplot(x=sort_value, y="Value", hue="Category", data=df, color = 'white', edgecolor="white", size=4)
sns.despine(left=True
	)
# plt.plot((len(df.Family.unique())+1) * [0], (len(df.Family.unique())+1) * [df.Value.min()], 'k--', linewidth=1)
plt.axhline(y=df.Value.min(), xmin=0, xmax=1, linewidth=1, color = 'k', linestyle = '--')
plt.axhline(y=df.Value.max(), xmin=0, xmax=1, linewidth=1, color = 'k', linestyle = '--')

plt.title("Receptorsimilarities of GPCR Families", fontsize=16)
plt.xticks(rotation=45)
plt.gcf().subplots_adjust(bottom=0.20)
# plt.gca().tight_layout()
plt.show()









