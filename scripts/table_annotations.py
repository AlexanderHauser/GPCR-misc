"""
Created in Apr 2016

@author: Alexander Hauser <alexshauser@gmail.com>

- fetch all 50 positions and align them into a table for David
- check whether a following segment annotation has a higher residue
number than the previsous (could cause alignment problems)
"""

import pandas as pd 
import os, glob
import requests
import re
import itertools

def class_label(receptor):

    table = pd.read_csv("/Users/vzw960/Work/Drugtarget_review/pubmed_search/pubmed_GPCRs_chembl.tsv", sep='\t', header = 0)

    family_trans = {"001": "Class A (Rhodopsin)", "002": "Class B1 (Secretin)", "003": "Class B2 (Adhesion)", "004": "Class C (Glutamate)", "005": "Class F (Frizzled)", "006": "Other"}
    
    try:
        classname = table[table['Entry name']==receptor]['Class'].values[0]
    except:
        classname = 'None'

    if classname == 'None':
        
        try: 
        # fetch Class from latest GPCRdb
            url = "http://test.gpcrdb.org:80/services/protein/" + receptor
            class_data = requests.get(url).json()
            classname = family_trans[class_data['family'][:-12]]
        except:
            print receptor
            classname = 'None'
        
    df.loc[receptor]['Class'] = classname

    return classname

def validation(receptor):
    # check whether a following segment annotation has a higher residue
    # number than the previsous
    # print df.columns
    segments = list(df.columns)
    segments.pop(0)

    seg_trans = {'TM1': 1, 'ICL1': 12, 'TM2': 2, 'ECL1': 23, 'TM3': 3, 'ICL2': 34, 'TM4': 4, 'ECL2': 45, 'TM5': 5, 'TM6': 6, 'TM7': 7, 'H8':8}

    compare = 0 
    print receptor
    for index, seg in enumerate(segments):
        print seg
        try:
            if (df.loc[receptor][segments[index]] == int) == True:
                compare1 = int(df.loc[receptor][segments[index]])
            else:
                compare1 = int(re.search('\d+', df.loc[receptor][segments[index]]).group())

            if compare1 < int(compare):
                print receptor, seg, compare, df.loc[receptor][segments[index]]
        except:
            print receptor, seg, index

        compare = int(re.search('\d+', df.loc[receptor][segments[index]]).group())

    # vlaidation for, whether x50 positions are within the assigned segment borders
    for crystal in crystals:
        if crystal.split("_")[1] == 'human':
            for ind in seg_trans:
                if (int(df.loc[receptor][str(seg_trans[ind])+'x50']) >= int(re.search('\d+', df.loc[receptor][str(seg_trans[ind])+'b']).group())) and (int(df.loc[receptor][str(seg_trans[ind])+'x50']) <= int(re.search('\d+', df.loc[receptor][str(seg_trans[ind])+'e']).group())) == False:
                    print "Bug in", crystal, ind

def structure_annotations():
    
    seg_trans = {'TM1': 1, 'ICL1': 12, 'TM2': 2, 'ECL1': 23, 'TM3': 3, 'ICL2': 34, 'TM4': 4, 'ECL2': 45, 'TM5': 5, 'TM6': 6, 'TM7': 7, 'H8':8}

    struc_anno = pd.read_excel("/Users/vzw960/Work/GPCRdb/structure_annotation/Structural_Annotation.xlsx")
    struc_anno['!Title'] = struc_anno['!Title'].str.split('_').str.get(0)+"_"+struc_anno['!Title'].str.split('_').str.get(1)

    struc_anno_sub = struc_anno[['!Title', 'Seg', 'x50' , '!bAlP', '!eAlP']].drop_duplicates()
    crystals = struc_anno_sub['!Title'].unique()

    for crystal in crystals:
        if crystal.split("_")[1] == 'human':
            temp_df = struc_anno_sub[struc_anno_sub['!Title']==crystal]
            for index, x in enumerate(temp_df.iterrows()):
                # print temp_df[index:index+1]['Seg']
                segID = str(seg_trans[temp_df[index:index+1]['Seg'].values[0]])
                df.ix[crystal.lower(), segID+'b'] = temp_df[index:index+1]['!bAlP'].values[0]
                df.ix[crystal.lower(), segID+'e'] = temp_df[index:index+1]['!eAlP'].values[0]
                # df.loc[crystal.lower()][segID+'b'] = temp_df[index:index+1]['!bAlP'].values[0]
                # df.loc[crystal.lower()][segID+'e'] = temp_df[index:index+1]['!eAlP'].values[0]

def load_files(filename):

    receptor = filename.split("/")[-1][:-5]
    df.loc[receptor] = " "
    df.loc[receptor][['Class','1x50', '12x50', '2x50', '23x50', '3x50', '34x50', '4x50', '45x50', '5x50', '6x50', '7x50', '8x50']] = "None"

    with open(filename) as fname:

        for line in fname.readlines():
            line = line.strip()

            TM = line.split(":")[0]
            index = list(df.columns).index(TM)
            df.loc[receptor][index] = line.split(":")[1].replace(" ", "")

    return receptor

# df = pd.DataFrame(columns=('Class','1x50', '12x50', '2x50', '23x50', '3x50', '34x50', '4x50', '45x50', '5x50', '6x50', '7x50', '8x50'))
df = pd.DataFrame(columns=('Class', '1b','1x50', '1e', '12b','12x50', '12e', '2b','2x50', '2e', '23b', '23x50', '23e', '3b','3x50', '3e', '34b', '34x50', '34e', '4b', '4x50', '4e', '45b', '45x50', '45e', '5b', '5x50', '5e' , '6b', '6x50', '6e', '7b', '7x50', '7e', '8b', '8x50', '8e'))

path = '/Users/vzw960/protwis_vagrant/shared/data/protwis/gpcr/residue_data/reference_positions/*'
filenames = glob.glob(path + '.yaml')

for filename in filenames:

    receptor = load_files(filename)
    classname = class_label(receptor)
    structure_annotations()

    # validation(receptor)

print df

df.to_csv("/Users/vzw960/Downloads/reference_positions.csv")
df = pd.read_csv("/Users/vzw960/Downloads/reference_positions.csv", index_col=0)

# df = df[~df['1e'].str.contains(" ")]
# for receptor in list(df.index):
#     validation(receptor)


