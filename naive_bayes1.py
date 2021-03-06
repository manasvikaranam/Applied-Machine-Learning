import csv
import copy
import random
import numpy

##this function calculates the conditional probability for all features given a label 
def conditional_probability_count(data,feature,label,features):
	#considering laplacian correction we are adding one to all possible values of a feature
	conditional={f:1 for f in features}
	for line in data:
		conditional[line[(feature)]]+=1
#	print conditional 
	return conditional



##this function considers binary split for each of the labels 
def binary_classify(data,label):
#	print data
#	print "#"*40 
#	print "Binary split on label: ",label 
	#initiate two empty lists to store all the samples which have class labels 1 or 0 respectively
	label_one=[]
	label_zero=[]
	#declare a dictionary for calculating priors 
	priors={"1":0,"0":0}
	for line in data:
		#if last feature in a sample equals the label convert to 1 and add the sample to list label_one
		if line[-1]==label:
			priors["1"]+=1
			label_one.append(line[:-1]+["1"])
		else:
		#if last feature in a sample is not equal to label convert to 0 and add the sample to list label_zero
			priors["0"]+=1
			label_zero.append(line[:-1]+["0"])
	#the total number of features in an example
	num_features=len(data[0])-1
	#the total number of examples with class label 1 and 0 respectively
#	print "The number of samples with class label '1': ",len(label_one)
#	print "The number of samples with class label '0': ",len(label_zero)
#	print num_features
	#count the number of times each feature value occurs given a label : conditional probability (just the count) 
	conditional_prob_one={}
	conditional_prob_zero={}
	for i in range(num_features):
		features=sorted(set([line[i] for line in data]))
		#number of times each featue value for feature i occurs provided label is 0 or 1 
		conditional_prob_one[str(i)]=conditional_probability_count(label_one,i,"1",features)
		conditional_prob_zero[str(i)]=conditional_probability_count(label_zero,i,"0",features)
#	print conditional_prob_one
#	print conditional_prob_zero
	total=sum(priors.values())
#	print total
	#calculate prior probabilities 
	for k in priors.keys():
		priors[k]=float(priors[k]+1)/(total+2)
#	print priors 
	return conditional_prob_one,conditional_prob_zero,priors


##this funstion calculates the accuracy on tuning set for 6-Fold cross validation
def calculate_accuracy(tune_set,One,Zero,Priors,label):
#	print len(tune_set) 
	accuracy=0.0
        F_N=0
        F_P=0
        T_N=0
        T_P=0
        for line in tune_set:
                expected_class_label="1" if line[-1]==label else "0"
#                print "Expected class label: ",expected_class_label 
                prob_one=1.0
                prob_zero=1.0
                for feature_no in range(len(line)-1):
                #if there are feature values that are not already in our dictionary but are in the test set  just add them to both the dictionaries
                        if line[feature_no] not in One[str(feature_no)].keys():
                                One[str(feature_no)][line[feature_no]]=1
                        if line[feature_no] not in Zero[str(feature_no)].keys():
                                Zero[str(feature_no)][line[feature_no]]=1
#			print One
#			print Zero
                        prob_one*=float(One[str(feature_no)][line[feature_no]])/sum(One[str(feature_no)].values())
                        prob_zero*=float(Zero[str(feature_no)][line[feature_no]])/sum(Zero[str(feature_no)].values())
#               print "Probability that example has class label 1: ",float(prob_one)/(prob_one+prob_zero)
#               print "Probability that example has class label 0: ",float(prob_zero)/(prob_one+prob_zero)
                new_prob_one=float(prob_one)/(prob_one+prob_zero)
                new_prob_zero=float(prob_zero)/(prob_one+prob_zero)
                predicted_class_label="1" if new_prob_one>new_prob_zero else "0"
#              	print "Predicted class label : ",predicted_class_label 
		if expected_class_label=="0" and predicted_class_label=="0":
			T_N+=1
        	elif expected_class_label=="1" and predicted_class_label=="1":
                	T_P+=1
                elif expected_class_label=="1" and predicted_class_label=="0":
                        F_N+=1
                else:
                        F_P+=1
#	print "T_P : ",T_P
#	print "T_N : ",T_N
#	print "F_P : ",F_P	
#	print "F_N : ",F_N		
	accuracy=float(T_P+T_N)/(T_P+F_N+T_N+F_P)
#	print "Accuracy : ",accuracy
	return T_P,T_N,F_P,F_N,accuracy



##this function does validation 
def validation(lines,label):
	average_accuracy=0.0
	accuracy_list=[]
        for i in range(6):
	#	print "Tuning number : ",i
		accuracy=0.0
                tune=random.sample(range(66),11)
                tune_set=[lines[i] for i in tune]
                train_set=[lines[i] for i in range(66) if i not in tune]
  #calculate the priors,count the number of times a feature value occurs for class labels through one vs. all 
		One,Zero,Priors=binary_classify(train_set,label)
#	       	print "Conditional probability of samples with label 1 : "
#	       	print One
#	       	print "Conditional probability of sample with label 0 : "
#	       	print Zero
#	       	print "Priors : "
#	       	print Priors
#	       	print "*"*40 
		accuracy_list.append(calculate_accuracy(tune_set,One,Zero,Priors,label)[4])
	#print accuracy_list
	average_accuracy=numpy.mean(accuracy_list)
	return average_accuracy

##main
in_file=open("zoo-train.csv","r")
lines=list(csv.reader(in_file))
#print lines 
labels=sorted(set(line[-1] for line in lines))
##opening the test file 
test_file=open("zoo-test.csv","r")
lines2=list(csv.reader(test_file))


confusion_matrix=[]
max_accuracy=0.0
max_label=""
for label in labels :
	print "Splitting on label : ",label 
	Accuracy=validation(lines,label)
	print "The average accuracy for label ",label," for 6-fold cross validation is ",Accuracy
	if max_accuracy<Accuracy:
		max_accuracy=Accuracy
		max_label = label
#print max_accuracy
print max_label 
O,Z,P=binary_classify(lines2,max_label)
True_Positives,True_Negatives,False_Positives,False_Negatives,Accuracy=calculate_accuracy(lines2,O,Z,P,max_label)
print "Confusion Matrix when we split on label ",max_label," : "
print True_Positives,"\t|\t",False_Negatives
print "*"*25
print False_Positives,"\t|\t",True_Negatives






