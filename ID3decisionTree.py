import sys
import csv
import math
import numpy
import itertools
import operator

#Entropy Calculation
def entropy(input_data, target_attribute):
    val_freq = {}
    data_entropy = 0.0
    for data in input_data:
        if (val_freq.has_key(data[target_attribute])):
            val_freq[data[target_attribute]] += 1.0
        else:
            val_freq[data[target_attribute]] = 1.0

    for freq in val_freq.values():
        data_entropy += (-freq / len(input_data)) * math.log(freq / len(input_data), 2)

    return data_entropy

#Information Gain Calculation
def gain(data, attr, target_attr):
    val_freq = {}
    subset_entropy = 0.0

    for record in data:
        if (val_freq.has_key(record[attr])):
            val_freq[record[attr]] += 1.0
        else:
            val_freq[record[attr]] = 1.0

    for val in val_freq.keys():
        val_prob = val_freq[val] / sum(val_freq.values())
        data_subset = [record for record in data if record[attr] == val]
        subset_entropy += val_prob * entropy(data_subset, target_attr)


    return (entropy(data, target_attr) - subset_entropy)

#Building tree
def buildTree(matrix, attributes, target_attribute,depth):
    data = matrix[:]
    vals = [eachRow[target_attribute] for eachRow in data]  
    depth = depth - 1
    if len(data) == 0 :
        return -1
    elif (len(attributes) <= 1):
        return get_labels(data,target_attribute)
    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        maxGainAttri = selectAttribute(data, attributes, target_attribute)
        tree = {maxGainAttri:{}}
        nextVals = set()
        for row in data:
            nextVals.add(row[maxGainAttri])
        for val in nextVals:
            if depth==0:
                subTree = buildTree(getData(data,maxGainAttri,val),[],target_attribute,depth)
            else:
                subTree = buildTree(getData(data,maxGainAttri,val),[att for att in attributes if att!=maxGainAttri],target_attribute,depth)
            tree[maxGainAttri][val] = subTree
    return tree

#Return label that appears the most in the examples
def get_labels(data,target_attribute):
    vals = [eachRow[target_attribute] for eachRow in data]
    val_freq = {}
    for record in vals:
        if (val_freq.has_key(record)):
            val_freq[record] += 1.0
        else:
            val_freq[record] = 1.0
    return max(val_freq.iteritems(), key=operator.itemgetter(1))[0]

#Creating the new data matrix after forming new node
def getData(data,maxGainAttri,val):
    subData = []
    for row in data:
        if(row[maxGainAttri] == val):
            subData.append(row)
    return subData

maxGain = -999999

#Select the best attribute; The attribute with maximum info gain
def selectAttribute(data, attributes, target_attribute):
    bestAttri = attributes[0]
    global maxGain

    for attri in attributes:
        g = gain(data, attri, target_attribute)
        if (g > maxGain):
            maxGain = g
            bestAttri = attri
    return bestAttri

#Test the tree on test set
def predict(tree,data,target_attribute,attributes):
    data_matrix = data[:]
    row = []
    results = []
    i = 0
    for row in data_matrix:
        results.append(mypredict(tree,row,attributes))
    confusionMatrix(results,data,target_attribute)
    #print results    

#Confusion Matrix Calculation
def confusionMatrix(predicted,data,target_attribute):
    data_matrix = data[:]
    actual = []
    values = []
    for row in data_matrix: 
        actual.append(row[target_attribute])
    for i in actual:
        if i not in values:
            values.append(i)
    n = len(values)
    matrix = numpy.zeros((n,n))        
    for i in range(len(actual)):
        matrix[actual[i]-1][predicted[i]-1]+=1
    print "Confusion matrix = "
    print matrix
    true_pos = []
    true_neg = []
    false_pos = []
    false_neg = []
    temp = 0
    for i in range(n):
        true_pos.append(matrix[i][i])
    for i in range(n):
        for j in range(n):
            if(i!=j):
                temp+=matrix[i][j] 
        false_neg.append(temp)
        temp = 0
    for i in range(n):
        for j in range(n):
            if(i!=j):
                temp+=matrix[j][i]
        false_pos.append(temp)
        temp = 0
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if(i!=j and k!=i):
                    temp+=matrix[j][k]
        true_neg.append(temp)
        temp = 0
    print "true positives = ",true_pos
    print "true negatives = ",true_neg
    print "false positives = ",false_pos
    print "false negatives  = ",false_neg

    total_truepos = 0
    total_trueneg = 0
    total_falseneg = 0
    total_falsepos = 0
    for i in range(n):
        total_truepos+=true_pos[i]
    for i in range(n):
        total_trueneg+=true_neg[i]
    for i in range(n):
        total_falseneg+=false_neg[i]
    for i in range(n):
        total_falsepos+=false_pos[i]
    print "total true pos = ",total_truepos
    print "total true neg = ",total_trueneg
    accuracy = (total_truepos+total_trueneg)/(total_truepos+total_trueneg+total_falsepos+total_falseneg)    
    print "Number of misclassifications = ", len(data_matrix) - total_truepos
    print "Accuracy = ",accuracy
 
#Prediction function
def mypredict(tree,row,attributes):
    d={}
    for k, v in tree.iteritems():
        for attr in attributes:
            if attr==k:
                if row[k] in v and type(v[row[attr]])==type(d):
                    return mypredict(v[row[attr]],row,attributes)
                else:   
                    if row[k] in v:
                        return v[row[k]]                    
                    else:
                        return 1

#Main Function
def main():
    trainfilename = sys.argv[1]
    depth = int(sys.argv[2])
    testfilename = sys.argv[3]
    d = ','
    f = open(trainfilename, 'r')
    reader = csv.reader(f, delimiter=d)
    ncol = len(next(reader))  # Read first line and count columns
    f.seek(0)
    matrix = numpy.loadtxt(open(trainfilename, "rb"), delimiter=",")

    target = len(matrix[0]) - 1

    #Attributes list
    attributes = [i for i in range(1,target)]

    t = buildTree(matrix,attributes,target,depth)

    print "Decision Tree = ",t

    f_test = open(testfilename, 'r')
    reader_test = csv.reader(f_test, delimiter=d)

    #Read columns
    #ncol_test = len(next(reader_test)) 
    f_test.seek(0)

    matrix_test = numpy.loadtxt(open(testfilename, "rb"), delimiter=",")

    predict(t,matrix_test,target,attributes)


if __name__ == "__main__": main()
