#A Naive Bayes based classifier to classify
# whether a line is abusive or not based
# on common occurence of some abusive words in these lines
from numpy import *

#Utility function to load DataSet from a file
def loadDataSet(fileName,splitcharacter = ' '):
	#Each line of the file should contain a sentence
	#whose last character is the class (1 if abusive 0 if not abusive)
	fname = open(fileName)
	postingList = []
	classVec = []
	for line in fname.readlines():
		line = ''.join(e for e in line if isalnum(e))
		dataExample = line.strip().split(splitcharacter)
		postingList.append(dataExample[:-1])
		classVec.append(int(dataExample[-1]))
	return postingList,classVec

def createVocabList(dataSet):
	vocabSet = set([])
	for document in dataSet:
		vocabSet = vocabSet | set(document)
	return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):
	returnVec = [0]*len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] =  1
		else:
			print "The word: %s is not in my Vocabulary!" %word
	return returnVec

def trainNB0(trainMatrix,trainCategory):
	numtrainDocs = len(trainMatrix)
	numWords = len(trainMatrix[0])
	pAbusive = sum(trainCategory)/float(numtrainDocs)
	p0Num = ones(numWords)
	p1Num = ones(numWords)
	p0Denom = 2.0
	p1Denom = 2.0
	for i in range(numtrainDocs):
		if trainCategory[i] == 1:
			p1Num += trainMatrix[i]
			p1Denom += sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += sum(trainMatrix[i])
	p1Vect = log(p1Num/p1Denom) # Taking the log to avoid underflow
	p0Vect = log(p0Num/p0Denom) # Taking the log to avoid underflow
	return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
	p1 = sum(vec2Classify*p1Vec) + log(pClass1)
	p0 = sum(vec2Classify*p0Vec) + log(1.0 - pClass1)
	if p1>p0:
		return 1
	else:
		return 0

def testingNB():
	listOPosts,listClasses = loadDataSet()
	myVocabList = createVocabList(listOPosts)
	trainMat = []
	for postinDoc in listOPosts:
		trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
	p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses))
	testEntry = ['my','garbage','dalmation']
	thisDoc = array(setOfWords2Vec(myVocabList,testEntry))
	print testEntry,'classfied as: ',classifyNB(thisDoc,p0V,p1V,pAb)
	testEntry = ['love','stupid']
	thisDoc = array(setOfWords2Vec(myVocabList,testEntry))
	print testEntry,'classfied as: ',classifyNB(thisDoc,p0V,p1V,pAb)
