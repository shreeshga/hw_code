"""
* Creation Date : 05-10-2011
* Last Modified : 
* Created By :  Shreesh Ayachit (shreesh.ayachit@gmail.com)
* Description : 
"""
from scipy import linalg,array,dot,mat,zeros,nonzero,set_printoptions
from operator import itemgetter
from math import * 
from pprint import pprint
from collections import defaultdict
import string
import os
import re
import urllib2 

class PostItem:
    """
    Stores the term occurrance statistic
    """
    def __init__(self,word):
        self.word = word
        self.tfd = 0.0
        self.idf = 0.0
        self.tfidf = 0.0
        self.offset = -1

    def __repr__(self):
        return " (word=%s,offset=%dtfd=%f,idf=%f,tfidf=%f)\n " % (self.word,self.offset,self.tfd,self.idf,self.tfidf)

class WordItem:
    def __init__(self,word):
        self.word = ""
        self.df = 0
        self.isStopWord = False

class LSA:
    """ 
    Find out Latent relationships between terms and documents
    """

    remotePattern = r'http://'    
    def __init__(self):
        self.patternRe  = re.compile(LSA.remotePattern)
        self.files = [] 
        self.wordList = {} 
        self.stopList = open("stopList.txt").read().split(' ')
        self.k = 4;
        self.numResults = 4
    
    def printMatrix(self,CM):
        """ Make the matrix look pretty """
        stringRepresentation=""
        rows,cols = CM.shape
        for row in xrange(0,rows):
            stringRepresentation += "["
            for col in xrange(0,cols):
                stringRepresentation+= ("%+0.2f " ) % (CM[row][col])
            stringRepresentation += "]\n"
        return stringRepresentation
            
    def isRemoteFile(self,filename):
        if self.patternRe.search(filename):
            return True
        return False

    def readFile(self,filename,index):
        if self.isRemoteFile(filename):
            self.readRemoteFile(filename)
        else:
            f  = open(filename)
            self.file = f.read()
        self.files.append({'index':index,'name':filename,'data':self.file})
        self.readTokens(self.file,index)
  
    def normalizeTokens(self,tokens):
        ts = []
        for t in tokens:
            t = t.lower()
            t = t.strip()
            if t in self.stopList or not t:
                continue
            if re.search("^[a-z]+",t):
                ts.append(t)
        return ts

    def doTFIDF(self):
        i = 0
        self.TM = zeros((len(self.wordList),len(self.files)),float)
        self.CM = zeros((len(self.wordList),len(self.files)),float)
        for w,plist in self.wordList.items():
            tf = 0
            df = len(plist)
            for index,post in plist.items():
                post.idf = log10(len(self.files)/ df * 1.0) 
                post.tfidf = (1 + log10(post.tfd) ) * post.idf * 1.0
                self.TM[i][index] = post.tfidf
            i+=1
        
        #print self.wordList
        #print 'WordList:',len(self.wordList)
        #self.wordList = sorted(self.wordList)

    def validateQuery(self,s):
        qWords  = s.strip().split(' ')
        if qWords is None:
           return None 
        for w in qWords:
            w = w.lower()
            w = w.strip()
            if w in lsa.stopList:
                qWords.remove(w)
        if not qWords:
            return None
        return qWords

    def makeVector(self,query):
        keys = self.wordList.keys()
        queryVector = zeros(len(self.wordList))
        for q in query:
            try:
                index = keys.index(q)
                queryVector[index] += 1
            except ValueError as e:
                continue
        return queryVector

    def cosine(self,vector1, vector2):
            return float(dot(vector1,vector2) / (linalg.norm(vector1) * linalg.norm(vector2)))
 
    def searchQuery(self,queryStr):
        qwords = self.validateQuery(queryStr)
        if  qwords is None:
            return None
        qVector = self.makeVector(qwords)
        if  not any(qVector):
            print 'No results Found\n'
            return None
        #convert query vector to concept space: but no required though
        #print "Shapes: q,U,sigma",qVector.shape,self.U.transpose().shape,linalg.inv(self.sigma).shape
        #qStar = dot(dot(qVector,self.U),linalg.inv(self.sigma))
    
        #calculate similarity
        results = [] 
        for i in range(0,self.CM.shape[1]):
            docVector = array(self.CM[:,i])
            j = 0
            #normalize
            #docVector /= linalg.norm(docVector) 
            results.append({'index':i,'val':self.cosine(qVector.transpose(),docVector)})
        results = sorted(results,key = itemgetter('val'),reverse=True)
        print "Results:"
        res = self.numResults
        for e in results[:res]:
            findex = e['index']
            print '\n' 
            print "Document:",e['index']
            print "Score:",e['val']
            for word in qwords:
                offset = -1
                done = False
                if self.wordList[word].get(e['index']):
                    offset = self.wordList[word][e['index']].offset 
                if offset >= 0:
                    done = True
                    print "Text:",self.files[findex]['data'][offset - 10 :offset+200]
                    break
                else:
                    for word in self.wordList.keys():
                        if self.wordList[word].get(e['index']):
                            done = True
                            offset = self.wordList[word][e['index']].offset 
                            print "Text:",self.files[findex]['data'][offset:offset+200]
                            break
                if done:
                    break

                    

    def readTokens(self,string,fileIndx):
        tokens = self.normalizeTokens(string.split(' '))
        tDict = defaultdict(int) 
        for t in tokens:
            tDict[t] += 1
        for k,v in tDict.items():
            if  not self.wordList.get(k):
                self.wordList[k] = {} 
            if self.wordList[k].get(fileIndx):
                pass
            else:
                self.wordList[k][fileIndx] = PostItem(k)
                self.wordList[k][fileIndx].df = 1
                i = self.files[fileIndx]['data'].find(k)
                self.wordList[k][fileIndx].offset = i
            self.wordList[k][fileIndx].tfd = v 

    def readRemoteFile(self,filename):
        try:
            self.file = urllib2.urlopen(filename).read() 
        except Exception as  e:
            print "Can't read %s Error:%s" % (filename,e)

    def doLSA(self):
        self.U,s,self.Vt = linalg.svd(self.TM) 
        #print 'Eigen Values : ',s 
        #self.U, self.Vt = array(self.U),array(self.Vt)
        # Reduce Sig
        for i in range(self.k,len(s)):
           s[i] = 0 
        #for i in range(0,self.k):
        #    print s[i]
        r,c = self.U.shape
        l,z = self.Vt.shape
        self.sigma = array(linalg.diagsvd(s,r,z))
        self.CM = dot(dot(self.U ,self.sigma), self.Vt)
        #for i in range(0,r):
        #    print self.CM[i],'\n'
        #self.printMatrix(self.CM)

if __name__ == "__main__":
    lsa = LSA()
    filename = ''
    remote = 'http://www.infosci.cornell.edu/Courses/info4300/2011fa/test/file%02d.txt'
    local = './test/file%02d.txt'
    #set_printoptions(precision=2, linewidth=150,suppress = True,threshold = 1000000)
    if os.path.isfile(local % (1)):
        filename = local
    else:
        filename = remote

    print 'Processing Files...'
    for i in range(0,40):
        s = filename % i
        lsa.readFile(s,i)

    lsa.doTFIDF() 
    while True:
        k = raw_input("Enter K:")
        try:
            lsa.k = int(k)
        except ValueError as e:
            print 'Enter an integer'
            continue
        print 'Hardcore LSA Action...'
        lsa.doLSA()
        #f = open('matrix.txt','w')
        #print >>f,lsa.TM
        print "[zzz: Exit, z: set K Value]"
        while(True):
            s = raw_input("Enter Query:")
            if s == 'zzz':
                exit()
            if s == 'z':
                break
            if s is None:
                continue
            lsa.searchQuery(s)
        print ''
