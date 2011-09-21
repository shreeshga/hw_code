"""
* Creation Date : 03-09-2011
* Last Modified : 
* Created By :  Shreesh Ayachit (shreesh.ayachit@gmail.com)
* Description : Measure knn using Root Mean Squared Error method 
"""
import math
import operator
from time import clock,time
def distance(item,point,dim):
    d = 0
    for i in range(0,dim):  # ((label,(x-cord,y-cord,...)),similarity)
        d += (item[1][i] -point[1][i]) ** 2
    return d

def similarity(item,neighbour,dim,):

    dis = math.sqrt(distance(item,neighbour,dim))
    #K = 1.0 / math.sqrt(distance(item,neighbour,dim))
    K = math.exp(-dis) 
    return K
def normalize(trainingSet,test,features):
    testN = len(test)
    trainN= len(trainingSet)
    for j in xrange(0,len(features)):
        trainSum = sum(t[1][j] for t in trainingSet)
        testSum = sum(t[1][j] for t in test)  
        trainmu = trainSum / trainN 
        testmu = testSum / testN

        trainSTD= math.sqrt((trainSum ** 2 / trainN) - (trainmu ** 2)) 
        testSTD= math.sqrt((testSum ** 2 / testN) - (testmu** 2)) 
        for t in test: 
            t[1][j] = (t[1][j] - testmu ) / testSTD 
        for t in trainingSet: 
            t[1][j] = (t[1][j] - trainmu ) / trainSTD 

def knn(k,point,trainingSet,dim):
    #nearest = [(x,similarity(x,point,dim)) for x in trainingSet[:k] ]
    #nearest.sort(cmp = lambda  x,y: x[1] > y[1] ) # Sort by decreasing distance
    nearest = []
    for x  in trainingSet[k:]:
        #print x,point
        if (set(x[1]).intersection(point[1])): # Same point
            continue
        K = similarity(point,x,dim)
        nearest.append((K,x))
        """ if( K >  nearest[0][1]):
            for i in range(0,len(nearest)):
                if( K == nearest[i][1]):
                    nearest.append((x,K))
                else:
                    nearest[0] = (x,K)
        """
    nearest.sort(key = lambda x : x[0],reverse=1)
    return nearest[:k]

def getRMSE(trainFile=None,testFile=None,k=1,isWeighted=0,isNormalized=0):
    training = []  # tuples of (label,(feat1,feat2,...))
    test  = [] # same as above
    # Load up training data
    with open(trainFile,'r') as f:
        for line in f:
           tuples = line.split(' ') 
           label = float(tuples[0])
           feats = [float(i.split(':')[1]) for i  in tuples[1:-3]]
           training.append((label,feats))
    #print training
    # Load up test data
    with open(testFile,'r') as f:
        for line in f:
           tuples = line.split(' ') 
           label = float(tuples[0])
           feats = [float(i.split(':')[1]) for i  in tuples[1:-3]]
           test.append((label,feats))
    
    if(isNormalized):
        normalize(training,test,feats)
    
    sumSq = 0
    start = time() 
    for item in test:
        nearest = knn(k,item,training,len(feats))
        #print nearest
        Ypred = 0
        if(not isWeighted):
            tsum = sum(n[1][0] for n in nearest)
            Ypred  = tsum  / k
        else:
            weightSum = sum((n[1][0] * n[0]) for n in nearest) 
            kSum = sum(n[0] for n in nearest) 
            Ypred = weightSum / kSum
        sumSq += (item[0] - Ypred) ** 2
    #print time() - start
    RMSE = math.sqrt(sumSq / len(test))
    print "k = %d N = %d RMSE = %g" % (k,len(training),RMSE)
    return RMSE 
    

if __name__ == "__main__":
    kVals = [1,3,5,11,21,51,101,201,501,1001]
    testCases = ["../Cal/cal.train01","../Cal/cal.train05","../Cal/cal.train02","../Cal/cal.train","../Cal/cal.train2","../Cal/cal.train5","../Cal/cal.train10"]
    for t in testCases: 
        #start = time() 
        #RMSE  = getRMSE("../Cal/cal.train","../Cal/cal.test",k,1,1)
        RMSE  = getRMSE(t,"../Cal/cal.test",10,0,1)
        #print time() - start
