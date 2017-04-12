#! /usr/bin/python
# time vs. crystallized GPCRs

from suds import client
import xml.etree.cElementTree as ET
import urllib2
import time

#create a client from the GPCRDB WSDL
GPCRDBClient = client.Client("http://www.gpcr.org/7tm/webservice/?wsdl")


for i in range(0,5):
		try:
			print "Connecting to GPCRDB"
			proteins = GPCRDBClient.service.getProteinsOfFamily('001_001_001')
			print "Connected!"
			break
		except:
			print "Problem connecting to GPCRDB"
			time.sleep(1)
			continue

num = 0

structures_year = {}
for i in range(1999,2014):
	b = str(i)
	structures_year[b]=structures[b]=({'Test':0})

for protein in proteins:
	ID = protein['id']
	for i in range(0,5):
		try:
			print "Fetching crystal structure data for: " + ID
			structures = GPCRDBClient.service.getProteinStructures(ID)
			break
		except:
			print "Something went wrong while fetching structures for: " + ID
			time.sleep(1)
			continue
	for structure in structures:
		if structure['structureType'] == 'X-ray':
			for line in urllib2.urlopen('http://tools.gpcr.org/crystalstructure/table'):
    					if structure['pdbId'] in line:  # look for Protein
        					num += 1
        					structures['2000'].update({'Amine':2})
        					pdblist.append(structure['pdbId'])
        					print ID, num
        					break
							
for idx, pdbid in enumerate(pdblist):
	tree = ET.ElementTree(file=urllib2.urlopen('http://www.pdb.org/pdb/rest/describePDB?structureId='+pdbid))
	root = tree.getroot()
	root.tag, root.attrib

	for date in root.iter('PDB'):
		output.append([pdbid, date.attrib['release_date'][:4]])

print output