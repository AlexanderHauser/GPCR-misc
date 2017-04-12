#! /usr/bin/python
# time vs. crystallized GPCRs

from suds import client
import xml.etree.cElementTree as ET
import urllib2
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

#====================================================
# families to be looked for X-ray structures 
families = [["Acetylecholine","001_001_001"],["Adreno","001_001_002"],["Dopamine","001_001_003"],["Histamine","001_001_004"],["Serotonine","001_001_005"],["Peptide","001_002"],["Nucleoside","001_007"],["Rhodopsin","001_004"],["Lipid","001_014"],["Secretin","002"],["Glutamate","003"]]
# Current year plus 1
currentyear = datetime.now().year+1
# save all information (year, type) in the following list
# decide whether to use file data or fetching 
inpu = raw_input("\n===========================================\nA): Fetch new GPCRDB data (continue with B)\nB): All Crystal Structures in PDB \nC): Unique Crystal Structures in PDB \nD): All New Crystal Structures in PDB \n===========================================\n\n[A/B/C/D]: ")

crystal_structures = {}
all_entries = []
for year in range (1999,currentyear):
	crystal_structures[year]={}
	for family in families:
		crystal_structures[year][family[0]] = 0

if inpu in ('a', 'A'):
	# create a client from the GPCRDB WSDL
	for i in range(0,3):
		try:
			GPCRDBClient = client.Client("http://www.gpcr.org/7tm/webservice/?wsdl")
		except:
			time.sleep(1)
			continue
	# access GPCRDBClient to retrieve crystal structure information
	for idx, family in enumerate(families):
		family_name = family[0]
		family_number = family[1]
		for i in range(0,7):
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
			for i in range(0,7):
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
		    						all_entries.append([family_name,int(date.attrib['release_date'][:4]),ID])
		    					break
	# print the amount of new structures for each year
	for x, i in enumerate(all_entries):
		print repr(i[0]).rjust(1), repr(i[1]).rjust(2),repr(i[2]).rjust(3)

# make new structures to available structures 
def new_to_available():
	for i in range(0,len(families)):
		for year in range (1999,currentyear):
    			if year >= 2000:
        			crystal_structures[year][families[i][0]] = crystal_structures[year-1][families[i][0]] + crystal_structures[year][families[i][0]]
		# print families[i][0], year, crystal_structures[year][families[i][0]]
	# print ''

if inpu in ('b', 'B'):
    with open('crystal_structures.txt', 'r') as f:
    	crystal_structures = eval(f.read())
   	p_ticks = 4
   	p_hight = 90
   	p_title = 'All Available Crystallized GPCRs by Year and Type'
   	new_to_available()
# Only all unique structures
if inpu in ('c', 'C'):
	All = []
	with open('crystal_structures_list_unique.txt', 'r') as f:
    		for line in f:
        	    All.append(line.strip().split())
   	for al in All:
   		crystal_structures[int(al[1])][al[0]]+=1
   	p_ticks = 2
   	p_hight = 20
   	p_title = 'Unique Crystallized GPCRs by Year and Type'
   	new_to_available()

if inpu in ('d', 'D'):
	with open('crystal_structures.txt', 'r') as f:
		crystal_structures = eval(f.read())
	p_ticks = 2
   	p_hight = 30
   	p_title = 'All New Crystallized GPCRs by Year and Type'
# Create the plot
def plot(plot_hight,plot_ticks,plot_title):
	N = len(range(1999,currentyear))
	ind = np.arange(N)
	width = 0.5
	opacity = 0.3
	plt.ylabel('count')
	plt.title(plot_title)
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
	plt.yticks(np.arange(0,plot_hight,plot_ticks))
	plt.tick_params(axis='y', which='both', labelleft='off', labelright='on')
	plt.xticks(ind+width/2., ["%d" % year for year in range(1999,currentyear)], rotation=45)
	plt.show()

plot(p_hight,p_ticks,p_title)