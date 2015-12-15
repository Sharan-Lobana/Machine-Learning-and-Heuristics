from numpy import *
import time
def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def gradAscent(dataMatIn,classLabels):
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()
    m,n=shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = ones((n,1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix*weights)
        error = (labelMat - h)
        weights = weights + alpha * dataMatrix.transpose()*error
    return weights

def stocGradAscent(dataMat,classLabels):
    m,n = shape(dataMat)
    weights = ones((n,1))
    alpha = 0.01
    for i in range(m):
        h = sigmoid(sum(dataMat[i]*weights))
        error = classLabels[i] - h
        weights = weights + alpha*error*mat(dataMat[i]).transpose()
    return weights

def stocGradAscent1(dataMat,classLabels,numIter=150):
    m,n = shape(dataMat)
    weights = ones((n,1))
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0+j+i) + 0.01
            randIndex = int(random.uniform(0,len(dataIndex)))
            h = sigmoid(sum(dataMat[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha*error*mat(dataMat[randIndex]).transpose()
            del(dataIndex[randIndex])
    return weights

def plotBestFit(wei):
    import matplotlib.pyplot as plt
    weights = wei.getA()
    dataMat,labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0] #number of rows in dataArr
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if (int(labelMat[i]) == 1):
            xcord1.append(dataArr[i,1])
            ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1])
            ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1,ycord1,s=30,c='red',marker='s')
    ax.scatter(xcord2,ycord2,s=30,c='green',marker='s')
    x = arange(-3.0,3.0,0.05)
    y = (-weights[0] - weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()
    # plt.close()
def classifyVector(inX,weights):
    prob = sigmoid(sum(inX*weights))
    if prob>0.5:
        return 1.0
    return 0.0

def colicTest(fTrain,fTest):
    frTrain = open(fTrain)
    frTest = open(fTest)
    trainingSet = []
    trainingLabels = []
    for line in frTrain.readlines():
        currline = line.strip.split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(flaot(currline[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(currline[21])
    trainWeights = stocGradAscent1(array(trainingSet),trainingLabels,500)
    errorCount = 0
    numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currline = line.strip().split('\t')
        lineArr =[]
        for i in range(21):
            lineArr.append(float(currline[i]))
        if int(classifyVector(array(lineArr),trainWeights)) != int(currline[21])
                errorCount += 1
    errorRate = float(errorCount)/numTestVec
    print "The error rate of this test is: %f" % errorRate
    return errorRate

def multiTest():
    numTests = 10
    errorSum = 0.0
    for k in range(numTests):
        errorSum += colicTest()
    print "After %d iterations the average error rate is: %f "\
     %(numTests,errorSum/float(numTests))
