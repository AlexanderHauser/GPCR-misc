"""
Created in Apr 2016

@author: Alexander Hauser <alexshauser@gmail.com>

- fetch residue information for a given receptor
- translate GPCRdb numbers into amino acid numbers
- pregenerate a pymol input string for certain highlighting
- focused on Gprotein interactions, bt adaptable to generic
	pymol inputs
"""

import requests
import pandas as pd

def Res_to_GPCRdb(identifier):
    url = 'http://test.gpcrdb.org:80/services/residues/' + identifier + '/' 
    response = requests.get(url)
    residue_data = response.json()

    return residue_data

# returns dictionary
residue_data = Res_to_GPCRdb("adrb2_human")

# load into pandas df
rd_df = pd.DataFrame.from_dict(residue_data, orient='columns', dtype=None)
# rename generic numbers into GPCRdb numbers only
rd_df['display_generic_number'] = rd_df[rd_df['display_generic_number'].notnull()]['display_generic_number'].apply(lambda x: str(x).split('.')[0] + "x" + str(x).split('x')[1])

def bw_to_res(BWs, subtype):
	residue_numers = []
	for BW in BWs:
	    residue_numers.append(str(rd_df[rd_df['display_generic_number']==str(BW)]['sequence_number'].values[0]))

	color = {'Gia': "red", 'Gio': "red", 'Gsa': "blue", 'Gqv': "black"}
	atom = "CA"

	print "select resi " + '+'.join(residue_numers) + " and name " + atom
	print "color " + color[subtype] + ", sele and name " + atom
	print "show spheres, sele and name " + atom + "\n"


Gia = ['5x64', '34x53', '5x62', '8x50', '34x53', '5x62', '8x50', '3x55', '34x53', '34x56', '34x57', '5x60', '5x62', '5x66', '5x67', '8x49', '34x53', '5x64', '6x33', '34x52', '8x49', '34x56', '34x57', '5x60', '5x66']
Gio = ['5x62', '6x37', '7x55', '7x55', '5x64', '8x49', '6x37', '5x64']
Gsa = ['5x64', '5x65', '5x62', '8x50', '5x62', '8x50', '3x55', '5x60', '5x66', '5x67', '6x37', '5x64', '5x65', '8x49', '5x60', '5x66', '5x67', '7x55']
Gqv = ['3x53', '3x55', '34x53', '34x57', '5x60', '5x65', '7x55', '5x64', '3x53', '3x55', '34x57', '5x60', '5x65', '34x54']

subtypes = {'Gia': Gia, 'Gio': Gio, 'Gsa': Gsa, 'Gqv': Gqv}

for subtype in subtypes:
	bw_to_res(subtypes[subtype], subtype)







