#! /usr/bin/python
# time vs. crystallized GPCRs

from suds import client
import xml.etree.cElementTree as ET
import urllib2
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# create a client from the GPCRDB WSDL
GPCRDBClient = client.Client("http://www.gpcr.org/7tm/webservice/?wsdl")
# families to be looked for X-ray structures 
families = [["Acetylecholine","001_001_001"],["Adreno","001_001_002"],["Dopamine","001_001_003"],["Histamine","001_001_004"],["Serotonine","001_001_005"],["Peptide","001_002"],["Nucleoside","001_007"],["Rhodopsin","001_004"],["Lipid","001_014"],["Secretin","002"],["Glutamate","003"]]
# Current year plus 1
currentyear = datetime.now().year+1
# save all information (year, type) in the following list
crystal_structures = {}
for year in range (1999,currentyear):
	crystal_structures[year]={}
	for family in families:
		crystal_structures[year][family[0]] = 0
# access GPCRDBClient to retrieve crystal structure information
for idx, family in enumerate(families):
	family_name = family[0]
	family_number = family[1]
	for i in range(0,6):
			try:
				print "Connecting to GPCRDB for "+family_name
				proteins = GPCRDBClient.service.getProteinsOfFamily(family_number)
				print "Connected!"
				break
			except:
				print "Problem connecting to GPCRDB for "+family_name
				time.sleep(2)
				continue
	for protein in proteins:
		ID = protein['id']
		for i in range(0,6):
			try:
				print "Fetching crystal structure data for: " + ID
				structures = GPCRDBClient.service.getProteinStructures(ID)
				break
			except:
				print "Something went wrong while fetching structures for: " + ID
				time.sleep(2)
				continue
		for structure in structures:
			# only include X-ray structures
			if structure['structureType'] == 'X-ray':
				# only include fullm 7tm structures (now only based on GPCRtools table)
				for line in urllib2.urlopen('http://tools.gpcr.org/crystalstructure/table'):
	    				if structure['pdbId'] in line:  
						# retrieve the PDB release date from RESTful pdb.org
						tree = ET.ElementTree(file=urllib2.urlopen('http://www.pdb.org/pdb/rest/describePDB?structureId='+structure['pdbId']))
						root = tree.getroot()
						root.tag, root.attrib
	    					for date in root.iter('PDB'):
	    						crystal_structures[int(date.attrib['release_date'][:4])][family_name]+=1
	    					break
# print the amount of new structures for each year
for i in range(0,len(families)):
	for year in range (1999,currentyear):
		print families[i][0], year, crystal_structures[year][families[i][0]]
	print ''
# Create the plot
N = len(range(1999,currentyear))
ind = np.arange(N)
width = 0.5
opacity = 0.3
plt.ylabel('count')
plt.title('Crystallized receptors by year and type')
data = []
for i in range(len(families)):
	vars()['count' + str(i)]=list()
	for year in range(1999,currentyear):
		vars()['count' + str(i)].append(crystal_structures[year][families[i][0]])
	data.append(vars()['count' + str(i)])

n_rows = len(data)
colors = ('DarkGreen','SeaGreen','ForestGreen','Lime','Olive','DimGray','DarkViolet', 'Maroon', 'DarkOrange', 'Turquoise', 'SpringGreen')
y_offset = np.array([0.0] * N)
for row in range(n_rows):
    plt.bar(ind, data[row], width, bottom= y_offset,color=colors[row],label=families[row][0])
    y_offset = y_offset + data[row]
plt.legend(loc=2 )
plt.yticks(np.arange(0,30,4))
plt.xticks(ind+width/2., ["%d" % year for year in range(1999,currentyear)], rotation=45)
plt.show()
print crystal_structures