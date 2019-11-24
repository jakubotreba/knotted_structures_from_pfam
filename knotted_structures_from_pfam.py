from urllib import request
import argparse
import re

parser=argparse.ArgumentParser()

parser.add_argument("-A", help='Clan structures overview file from pfam')
parser.add_argument("-B", help='KnotProt Raw Data text file')

args=parser.parse_args()

knotteds=open(args.A).read()

knotteds=knotteds.split("<!-- start structures block -->")[-1]
knotteds=knotteds.split("<!-- end structures block -->")[0]
knotteds=knotteds.split("<tr>")

knotprot=open(args.B).readlines()

hrefs=[]
good={}

ofile=open(args.A.split('_')[0]+".txt","w")

for i in range(len(knotteds)):
	if "<a href=" in knotteds[i]:
		href=re.findall('<a href=(.*)?',knotteds[i])
		hrefs.append(href)
		if '"/family/' in href[0]:
			good[href[0].split('>')[1].split('<')[0]]=[]
			good[href[0].split('>')[1].split('<')[0]].append(href[2].split('/')[2].split('"')[0])
			family=href[0].split('>')[1].split('<')[0]
			ofile.write('#'+str(family)+'\n')
		elif '"/protein/' in href[0]:
			if href[1].split('/')[2].split('>')[0] not in good[family]:
				good[family].append(href[1].split('/')[2].split('"')[0])
				ofile.write(str(href[1].split('/')[2].split('"')[0].lower()))
				for j in range(len(knotprot)):
					if href[1].split('/')[2].split('"')[0].lower() in knotprot[j]:
						knots=knotprot[j].split(';')[-1]
						typ=knotprot[j].split(';')[-2]
						ofile.write('\t'+typ+'\t'+knots+'\n')
				ofile.write('\n')		
		elif '"/structure/viewer' in href[0]:
			if href[0].split('id=')[1].split('"')[0] not in good[family]:
				good[family].append(href[0].split('id=')[1].split('"')[0])
				ofile.write(str(href[0].split('id=')[1].split('"')[0].lower()))
				for j in range(len(knotprot)):
					if href[0].split('id=')[1].split('"')[0].lower() in knotprot[j]:
						knots=knotprot[j].split(';')[-1]
						typ=knotprot[j].split(';')[-2]
						ofile.write('\t'+typ+'\t'+knots+'\n')
				ofile.write('\n')		
		elif '"/structure/viewer' in href[1]:
			if href[1].split('id=')[1].split('"')[0] not in good[family]:
				good[family].append(href[1].split('id=')[1].split('"')[0])
				ofile.write(str(href[1].split('id=')[1].split('"')[0].lower()))
				for j in range(len(knotprot)):
					if href[1].split('id=')[1].split('"')[0].lower() in knotprot[j]:
						knots=knotprot[j].split(';')[-1]
						typ=knotprot[j].split(';')[-2]
						ofile.write('\t'+typ+'\t'+knots+'\n')
				ofile.write('\n')		
			
ofile.close()
