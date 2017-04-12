import requests

allGPCRs = []
for i in range(1,7):
	url = "http://www.gpcrdb.org:80/services/proteinfamily/proteins/00"+ str(i)+"/Homo sapiens"
	data = requests.get(url).json()

	for d in data:
		content = d['accession'] + ',' + d['entry_name']
		allGPCRs.append(content)

for GPCR in allGPCRs:
	print GPCR