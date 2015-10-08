import csv
import numpy
def expectedProbability(inputList,dictList,targetLabelDict):
	
	maxProb = 0.0
	cumProb = 1.0
	prob = 1.0
	probDict={}
	for i in range(0,len(dictList)):
		for j in range(0,len(dictList[i])):
			if(dictList[i][j].has_key(inputList[j])):
				
				
				prob = (float(dictList[i][j][inputList[j]])/float(targetLabelDict.values()[i]))
				cumProb *= prob
		
		probDict[targetLabelDict.keys()[i]] = cumProb
			
	print probDict
			
	
#Reading input file		
csvfile = open("/home/manasvi/Documents/Fall2015/Appl.ML/code/condo.csv","r") 
reader = csv.reader(csvfile)
ncol = len(next(reader))
csvfile.seek(0)

#Storing the index for target label
targetAttributeIndex = ncol-1

targetLabelDict ={}
#Creating a dictionary for target label; It will store each possible value and count
for row in reader:
	if(targetLabelDict.has_key(row[targetAttributeIndex])):
		targetLabelDict[row[targetAttributeIndex]] += 1
	else:
		targetLabelDict[row[targetAttributeIndex]] = 1

dictList = []

i = -1
csvfile.seek(0)
#Creating list of dictionaries.
#For example if target label has values Y and N. 
#Then for each of the values of remaining attributes, it stores the corresponding count of Y and N
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

#Sample test case
inputList = ['H','Y','M','H','Y']

expectedProbability(inputList,dictList,targetLabelDict)
	
