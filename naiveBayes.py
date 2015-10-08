import csv
import numpy
def expectedProbability(inputList,dictList,targetLabelDict):
	print "in func"
	maxProb = 0.0
	cumProb = 1.0
	prob = 1.0
	for i in range(0,len(dictList)):
		for j in range(0,len(dictList[i])):
			if(dictList[i][j].has_key(inputList[j])):
				
				print targetLabelDict.values()[i]
				prob = (float(dictList[i][j][inputList[j]])/float(targetLabelDict.values()[i]))
				cumProb *= prob
		
		if(maxProb < cumProb):
			maxProb = cumProb
	print maxProb
			
	
			
	



csvfile = open("/home/manasvi/Documents/Fall2015/Appl.ML/HW/condo.csv","r") 
reader = csv.reader(csvfile)
ncol = len(next(reader))
csvfile.seek(0)

targetAttributeIndex = ncol-1

targetLabelDict ={}
for row in reader:
	if(targetLabelDict.has_key(row[targetAttributeIndex])):
		targetLabelDict[row[targetAttributeIndex]] += 1
	else:
		targetLabelDict[row[targetAttributeIndex]] = 1

dictList = []

i = -1
csvfile.seek(0)
for val in targetLabelDict.keys():
	tempList = []
	for i in range(0,ncol-1):
		tempDict = {}
		for row in reader:
		
			if(row[targetAttributeIndex] == val):
				if(tempDict.has_key(row[i])):
				
					tempDict[row[i]] += 1
				else:
					tempDict[row[i]] = 1
				
				
		tempList.append(tempDict)
		csvfile.seek(0)
	dictList.append(tempList)

inputList = ['H','Y','M','H','Y']
print "calling"
expectedProbability(inputList,dictList,targetLabelDict)
	