#!/usr/bin/python 

#find matching Gloriam's 44 accesible residues and pars accordingly the PDB file

#import the suds client module
from suds import client
from Bio.PDB import *
import gzip
import os

#create a client from the GPCRDB WSDL
GPCRDBClient = client.Client("http://www.gpcr.org/7tm/webservice/?wsdl")
#print GPCRDBClient

adrb2 = [82,86,109,110,113,114,115,117,118,193,195,199,200,203,204,207,208,286,289,290,293,308,312,316]

g44 = ['1.39','1.42','1.46','2.53','2.57','2.58','2.61','2.62','2.64','2.65','3.28','3.29','3.32','3.33','3.36','3.37','3.39','3.40','4.56','4.57','4.60','4.61','5.38','5.39','5.42','5.43','5.46','5.47','5.50','6.44','6.47','6.48','6.51','6.52','6.55','6.58','6.59','7.35','7.36','7.39','7.42','7.43','7.45','7.46']

Nucleoside = list()
with open('Nucleoside.txt', 'r') as f:
    		for line in f:
        	    Nucleoside.append(line.strip())

#proteinname = 'adrb2_human'
proteinname = 'aa2ar_human'
pdb_file = '3EML'

def dbnumber_to_BW(proteinname):
	for inx, residue in enumerate(proteinname):
		try:
			Protein = GPCRDBClient.service.getResidue(proteinname, residue)
			print inx, residue, Protein['residueNumberFamilyAlternate']
		except:
			print "no TM region"
			continue
	print '______________________\n'

# retrieves PDBs
pdbl=PDBList()
pdbl.retrieve_pdb_file(pdb_file,obsolete=False)
parser = PDBParser(PERMISSIVE=1)
structure = parser.get_structure(pdb_file,pdb_file[1:3].lower()+"/pdb"+pdb_file.lower()+".ent")

Atyp = list()
Aid = list()

# convert BW to protein specific residue number/ID
def BW_to_res():
        print '\nconverting BW numbering to residueID..'
        for idx, i in enumerate(Nucleoside):
			bw = GPCRDBClient.service.convertBallesterosWeinsteinNumbersToGpcrdb(i)
			res = GPCRDBClient.service.getResidueByGpcrdbNumber(proteinname,bw)
			print idx+1, i + ': ' + res['residueType'], res['residueNumber']
			Atyp.append(res['residueType'])
			Aid.append(res['residueNumber'])
	print '..done..\n'

BW_to_res()
# make PDB file only with residues from Gloriam's 44 ligand accessible paper 
class select(Select):
	
	#allows to assign varables to the class
	def __init__ (self, index):
		self.index = index

	def accept_residue(self, residue):
	    	
	    	for idx,i in enumerate(Atyp):
	    		if residue.get_resname()==Atyp[idx].upper() and residue.id[1]==int(Aid[idx]):
	    			return 1
	    	else:		
		    	return 0

io = PDBIO()
io.set_structure(structure)
io.save(proteinname+'_'+pdb_file+'_ligand_accesible.pdb', select(0))
print 'PDB file with ligand accessible residues saved as: \n'+proteinname+'_ligand_accesible.pdb\n'
#BW_to_DBnumber(g44)