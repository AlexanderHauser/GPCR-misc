"""
Created in Sep 2017

@author: Alexander Hauser <alexshauser@gmail.com>

- get each segment for each GPCR into a dataframe
"""

import pandas as pd
from tqdm import *

def receptor_segments():
    ## Makes a dataframe of receptor segment amino acids

    df = pd.read_csv("/Users/vzw960/Work/GPCRdb/ID-Mapping/GPCR_Protein_Gene.csv")

    Segments = pd.DataFrame(pd.Series(df.EntryName))

    for index, protein in tqdm(enumerate(Segments.iterrows())):
        entry_name = Segments[index:index+1]['EntryName'].values[0]

        url = "http://test.gpcrdb.org/services/residues/" + entry_name
        res_data = requests.get(url).json()

        segments = {}
        if index == 0:
            agg = pd.DataFrame()

        for res in res_data:
            if not res['protein_segment'] in segments.keys():
                segments[res['protein_segment']] = res['amino_acid']
            else:
                segments[res['protein_segment']] += res['amino_acid']

        new_df = pd.DataFrame(segments, index=[index])
        agg = agg.append(new_df)
        agg.is_copy = False

    Segments = Segments.merge(agg, left_index=True, right_index=True, how='outer')

    Segments.to_csv("/Users/vzw960/Work/GPCRdb/data/GPCR_segment_sequences.csv")
