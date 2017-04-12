#! /usr/bin/python
# download all ligand structures in sdf format 

import time
import urllib
import urllib2

List = [["ADRB1","2VT4","P32"],["ADRB1","2Y00","Y00"],["ADRB1","2Y01","Y01"],["ADRB1","2Y02","WHJ"],["ADRB1","2Y03","5FW"],["ADRB1","2Y04","68H"],["ADRB1","2YCW","CAU"],["ADRB1","2YCX","P32"],["ADRB1","2YCY","P32"],["ADRB1","2YCZ","I32"],["ADRB1","4AMI","G90"],["ADRB1","4AMJ","CVD"],["ADRB1","4BVN","P32"],["ADRB2","3ZPR","3WC"],["ADRB2","2RH1","CAU"],["ADRB2","3D4S","TIM"],["ADRB2","3NY8","JRZ"],["ADRB2","3NY9","JSZ"],["ADRB2","3NYA","JTZ"],["ADRB2","3P0G","P0G"],["ADRB2","3PDS","ERC"],["ADRB2","3SN6","P0G"],["ADRB2","4GBR","CAU"],["ADRB2","4LDE","P0G"],["ADRB2","4LDL","XQC"],["ADRB2","4LDO","ALE"],["CHRM2","3UON","QNB"],["CHRM2","4MQS","IXO"],["CHRM2","4MQT","2CU"],["Chrm3","4DAJ","0HK"],["DRD3","3PBL","ETQ"],["HRH1","3RZE","5EH"],["HTR1B","4IAQ","2GM"],["HTR1B","4IAR","ERM"],["HTR2B","4IB4","ERM"],["HTR2B","4NC3","ERM"],["S1PR1","3V2W","ML5"],["S1PR1","3V2Y","ML5"],["ADORA2A","2YDO","ADN"],["ADORA2A","2YDV","NEC"],["ADORA2A","3EML","ZMA"],["ADORA2A","3PWH","ZMA"],["ADORA2A","3QAK","UKA"],["ADORA2A","3REY","XAC"],["ADORA2A","3RFM","CFF"],["ADORA2A","3UZA","T4G"],["ADORA2A","3UZC","T4E"],["ADORA2A","3VG9","ZMA"],["ADORA2A","3VGA","ZMA"],["ADORA2A","4EIY","ZMA"],["P2RY12","4NTJ","AZJ"],["P2RY12","4PXZ","6AD"],["P2RY12","4PY0","6AT"],["CCR5","4MBS","MRV"],["CXCR4","3ODU","ITD"],["CXCR4","3OE0","DPR"],["CXCR4","3OE6","ITD"],["CXCR4","3OE8","ITD"],["CXCR4","3OE9","ITD"],["OPRD1","4EJ4","EJ4"],["OPRD1","4N6H","EJ4"],["OPRK1","4DJH","JDC"],["OPRL1","4EA3","0NN"],["PAR1","3VW7","VPX"],["RHO","2I35","RET"],["RHO","2X72","RET"]]

for i,a in enumerate(List):
	print "downloading "+List[i][1]
	url = 'http://pdb.org/pdb/download/downloadLigandFiles.do?ligandIdList='+List[i][2]+'&structIdList='+List[i][1]+'&instanceType=all&excludeUnobserved=false&includeHydrogens=false'
	urllib.urlretrieve(url, List[i][0]+"_"+List[i][1]+"_"+List[i][2]+".sdf")