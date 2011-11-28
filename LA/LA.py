"""
* Creation Date : 03-11-2011
* Last Modified : 
* Created By :  Shreesh Ayachit (shreesh.ayachit@gmail.com)
* Description : 
"""
import re
import urllib2
import json
import urlparse
import os
import sys
import pickle
import pprint
import io
from numpy import array,dot,zeros,set_printoptions
from BeautifulSoup import BeautifulSoup

class XPickler(pickle.Pickler):
  def persistent_id(self, obj):
    if obj is type(None):
      return "NoneType"
    return None

class XUnpickler(pickle.Unpickler):
  def persistent_load(self, persistent_id):
    if persistent_id == "NoneType":
      return type(None)

class Matrix(object): 
    def __init__(self, rows, cols,num=0): 
        self.data = [[num] * cols for i in xrange(rows)] 
        self.row = rows
        self.col = cols
        self._matRes = []
        self.epsilon = 0.000000001 
    def __getitem__(self, key): 
        x, y = key 
        return self.data[x][y] 
    
    def normalize(self):
        for i in range(0,self.row):
            di = 0
            for j in range(self.col):
                di += self.data[i][j]    
            if not di:
                for k in range(self.col):
                    self.data[i][k] = 1.0 / self.col
            else:
                for k in range(self.col):
                    self.data[i][k] = self.data[i][k]/ (1.0 * di)

    def __setitem__(self, key, value): 
        x, y = key 
        self.data[x][y] = value 
    
    def __add__(self,other):
        if not (self.row == other.row) and (self.col == other.col):
            return 'The number of col is not equal to the number of row'
        res = Matrix(other.row,other.col)
        for i in range(self.row):
            for j in range(self.col):
                res[(i,j)] = self.data[i][j] + other[(i,j)]
        return res
    
    def __eq__(self,other):
        if not (self.row == other.row) and (self.col == other.col):
            return 'The number of col is not equal to the number of row'
        for i in range(self.row):
            for j in range(self.col):
                diff =  abs(self.data[i][j] - other[(i,j)])
                if diff > self.epsilon:
                    return False 
        return True

    def __sub__(self,other):
        if not (self.row == other.row) and (self.col == other.col):
            return 'The number of col is not equal to the number of row'
        res = Matrix(other.row,other.col)
        for i in range(self.row):
            for j in range(self.col):
                res[(i,j)] = self.data[i][j] - other[(i,j)]
        return res

    def __mul__(self,other):
        if isinstance(other,int) or isinstance(other,float):
            res = Matrix(self.row,self.col)
            for i in range(self.row):
                for j in range(self.col):
                    res.data[i][j] = self.data[i][j] * other
            return res
                
        if self.col != other.row: return 'The number of columns of the first matrix must be equal to the number of rows of the second.'
        res = Matrix(self.row,other.col)
        for i in range(self.row):
            for j in range(other.col):
                for k in range(other.row):
                    res.data[i][j] += self.data[i][k] * other.data[k][j]               
        return res
        
    def __str__(self): 
        return '\n'.join([' '.join('%0.3f' % value for value in row) for row in self.data]) 
         

class ReadLinks:
    remotePattern = r'http://'    
    def __init__(self):
        self.patternRe  = re.compile(ReadLinks.remotePattern)

    def readRemoteFile(self,filename):
        try:
            self.indexFile= urllib2.urlopen(filename).read() 
        except Exception as  e:
            print "Can't read %s Error:%s" % (filename,e)
      
    def isRemoteFile(self,filename):
        if self.patternRe.search(filename):
            return True
        return False

    def readFile(self,filename):
        if self.isRemoteFile(filename):
            self.readRemoteFile(filename)
        else:
            f  = open(filename)
            self.indexFile = f.read().strip()
        self.links = self.indexFile.split('\n')

class LinkMatrix:
    """
    Stores the link Matrix for links in a text file
    """
    linkPattern = r'(index.html)'
    def __init__(self):
        self.linkConnect = {}
        self.dampingFactor = 0.85

    def setFiles(self,linkFile,metaData,pageRecord):
        file = ReadLinks()
        file.readFile(linkFile)
        self.links = file.indexFile.split('\n')
        self.metaData = metaData
        self.pageRecord= pageRecord

    def dump(self):
        #write dict to pickle file
        output = open('linkConnect.pkl', 'wb')
        try:
            XPickler(output).dump(self.linkConnect)
        except Exception as e:
            print e
        #str  = json.dumps(self.linkConnect)
        #m.write(str)
        output.close()
    
    def load(self):
        #write dict to pickle file
        output = open('linkConnect.pkl', 'rb')
        XUnpickler(output,self.linkConnect).load()
        #self.linkConnect = json.loads(output.read())
        output.close()



    def process(self):
        # Fetch and parse
        #self.load() 

        self.readLocalFiles()
        #self.fetchLinks()
        #m = open('temp.txt','r')
        #self.linkConnect = eval(m.read().strip('[^a-zA-Z0-9]'))
        #m.close()
        self.dump()
        # build the Matrixx
        self.buildMatrix()
        self.calcRank()
        
    def buildMatrix(self):
        self.linkArray  = [value for key,value in self.linkConnect.items()]
        self.linkKeys = self.linkConnect.keys()
        #print 'LinkKeys :',linkKeys
        self.linkMatrix = Matrix(len(self.linkKeys),len(self.linkKeys))  
        for page,values in self.linkConnect.items():
            if values.get('links',None):
                for ld in values['links']:
                    href = ld.get('href',None)
                    if  href in self.linkKeys:
                        if page != ld['href']:
                            index = self.linkKeys.index(page)
                            self.linkMatrix[(index,self.linkKeys.index(ld['href']))] = 1

    def calcRank(self):
        #close deadends
        self.linkMatrix.normalize()
        # calculate Probability matrix
        '''
        m = open('matrix.txt','w')
        print >>m,self.linkMatrix.data
        m.close()
        '''
        alpha =  1.0 - self.dampingFactor
        a = array(self.linkMatrix.data)
        a = self.dampingFactor * a
        f = alpha / len(self.linkKeys)
        identity = Matrix(self.linkMatrix.row,self.linkMatrix.col,f)
        b = array(identity.data)
        probMatrix =  a + b
        '''for r in range(probMatrix.shape[0]):
            s = 0.0
            for c in range(probMatrix.shape[1]):
                rs = 0.0
                s += probMatrix[r][c]
                #for i in range(probMatrix.shape[0]):
                    #rs += probMatrix[r][i]
                    #print 'indegree of (%d:%f)' %(c,rs)
            #print 'Alert! (%d:%f)' %(r,s)
        '''
        r = Matrix(1,len(self.linkKeys),1.0/ len(self.links))
        oldr = zeros((1,len(self.links))) #Matrix(1,len(self.links),1)
        i = 0
        pr = array(r.data)
        while(True):
            steadyState = True
            res = []
            for row in range(oldr.shape[0]):
                for col in range(oldr.shape[1]):
                    res.append(abs(oldr[row][col] - pr[row][col]))
            if max(res) <  0.0000001:
                break
            oldr = pr
            i += 1
            pr = dot(pr,probMatrix)
        self.rankVector = pr
        '''m = open('rankVector.txt','w')
        print >>m,self.rankVector
        m.close()
        s = 0
        for r in range(pr.shape[0]):
            for c in range(pr.shape[1]):
                s += pr[r][c]
        '''
        #set_printoptions(threshold='nan')
        #print 'Matrix:',probMatrix
        
    def mergeLink(self,page,link):
        ret = urlparse.urljoin(page,link)
        url = ret.split('?')[0]
        title = None
        if url.find('#') != -1:
            title  = url.split('#')[1]
            url = url.split('#')[0]
        return (url,title)

    def readLocalFiles(self):
        path = 'test3/'
        for index,link in enumerate(self.links):
            name = os.path.join(path,str(index+1)+".html")
            self.processLink(link,name)

    def fetchLinks(self):
        map(self.processLink,self.links)

    def remove_html_tags(self,data):
        p = re.compile(r'<.*?>')
        data = self.remove_space(data)
        return p.sub('', data)

    def remove_space(self,data):
        p = re.compile(r'\s+')
        return p.sub(' ', data)


    def writeMetaData(self):
        f = open('metaData.txt','w')
        for page,v in self.masterDict.items():
            a  = v.get('anchor',None)
            if a:
                a = self.remove_html_tags(a)
            if a:
                pgid = v['pageID']
                #print >>f,v.get('title',''),':',anchor
                anchor = []
                if 'http://' in a:
                    a = urlparse.urlparse(a).path
                anchor = a.split(' ')
                print >>f,pgid,':',self.rankVector[0][pgid],':',','.join(a for a in anchor)
        f.close()

    def writeIndexFile(self):
        f = open('indexRecord.txt','w')
        rec = open(self.pageRecord,'w')
        self.masterDict = {}
        for page,values in self.linkConnect.items():
            indexDict = {}
            index = self.linkKeys.index(page)
            indexDict['pageID'] = index
            indexDict['title'] = values.get('title'," ")
            indexDict['snip'] = values.get('snip', " ")
            pageID = index
            anchor = " "
            if values.get('links',None):
                for v in values['links']:
                    if v.get('anchor',None) and self.masterDict.get(v['href'],None):
                        anchor = ' '
                        if  isinstance(v['anchor'],unicode):
                           anchor = v['anchor'].decode('utf-8') 
                        else:
                            anchor = str(v['anchor'])
                        if self.masterDict.get(v['href'],None):
                            if not self.masterDict[v['href']].get('anchor',None):
                                self.masterDict[v['href']]['anchor'] = anchor
                            else:
                                self.masterDict[v['href']]['anchor'] += ' '+anchor
                    '''elif v.get('anchor',None):
                        anchor = v['anchor']
                        masterDict[v['href']]['anchor']  = anchor'''
            self.masterDict[page] = indexDict
            #f.write("%d:%s:%s\n" %(pageID,title,anchor));
        for page,v in self.masterDict.items():
            anchor  = v.get('anchor',None)
            if anchor:
                anchor = self.remove_html_tags(anchor)
            if anchor:
                print >>f,v.get('title',''),':',anchor
                print >>rec,v['pageID'],';',page,';',v['snip']
                #print >>f,v['pageID'],':',v.get('title',''),':',anchor
                #f.write("%d:%s:%r\n" %(v['pageID'],v.get('title'),v['anchor'].decode('utf-8')))
        f.close()
        rec.close()
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(masterDict)
        
    def processLink(self,pglink,name):
        try:
            #soup = BeautifulSoup(urllib2.urlopen(pglink))
            soup = BeautifulSoup(open(name).read())
            links = soup.findAll(['a'])
            patternRe  = re.compile(ReadLinks.remotePattern)
            llist = []
            #print soup.title.text
            res  = soup.findAll('div',attrs={'class':'content'})
            snip = self.remove_html_tags(str(res))
            title = " "
            frag = " "
            if soup.html and soup.html.head.title:
                title = soup.html.head.title.string
            if pglink.find('#') != -1:
                pglink = pglink.split('#')[0]
                frag = pglink.split('#')[1]
            if not title and frag:
                title = frag
            for link in links:
                ldict = {}
                ldict['page'] = pglink 
                for  t in link.attrs:
                    if t[0] == 'href':
                        ldict['href'],t = self.mergeLink(pglink,t[1])
                        if not title: title = t
                    elif t[0] == 'title' and t[1]:
                        ldict['title'] = t[1]
                if ldict.get('href',None):
                    if link.contents:
                        if  isinstance(link.contents[0],unicode):
                            ldict['anchor'] = link.contents[0].encode('utf-8')
                        else:
                            ldict['anchor'] = link.contents[0]
                    else:
                        if link.img and link.img.get('alt',None):
                            ldict['anchor'] = link.img['alt']
                    if  ldict.get('href',None):
                        llist.append(ldict)
            tdict = {}
            if llist:
                tdict['links'] = llist
            if title:
                tdict['title'] = title
            if snip:
                tdict['snip'] = self.remove_html_tags(snip)
            self.linkConnect[pglink] = tdict
            #print self.linkConnect[pglink]
        except Exception as e:
            print e

    def load_data(self):
        self.queryData = []
        with open(self.metaData,'r') as f:
            for line in f.read().split('\n'):
                ldict = {}
                ll = line.split(':')
                if len(ll) > 1:
                    ldict['pageID'] = ll[0]
                    ldict['rank'] = ll[1]
                    ldict['anchor'] = ll[2]
                    self.queryData.append(ldict)
        self.pageData = [None] * len(self.links)
        with open(self.pageRecord,'r') as f:
            for line in f.read().split('\n'):
                ll = line.split(';')
                pgid = ll[0]
                if len(ll) > 1:
                    href = ll[1]
                    snip = ll[2]
                    self.pageData[int(pgid)] = {'snip':snip[:70],'href':href}

    def search(self,term):
        result = []
        for v in self.queryData:
            if term in v['anchor']:
                res = {}
                res['id'] = int(v['pageID'])
                res['href'] = self.pageData[res['id']]['href']
                res['rank'] = float(v['rank'])
                res['snip'] = self.pageData[res['id']]['snip']
                res['anchor'] = v['anchor']
                result.append(res)

        if result:
            result = sorted(result,key=lambda k: k['rank'],reverse=True)
            print '====='
            for r in result:
                print 'Page ID :',r['id']
                print 'Page : ',r['href']
                print 'Rank : ','%f' % r['rank']
                print 'anchor :',r['anchor']
                print 'Snippet :',r['snip']
                print ' -- '
        else:
            print 'No Results Found'

    def query(self):
        string = None
        print 'Reading Data...'
        self.load_data() 
        print "[zzz: Exit, z: set K Value]"
        while(True):
            s = raw_input("Enter Query:")
            s = s.strip()
            if s == 'zzz':
                exit()
            if s is None:
                continue
            self.search(s) 
        print ''
        

if __name__ == "__main__":
    if (len(sys.argv) < 4):
        print 'Example Usage: python a3.py test3.txt metaData.txt pageRecord.txt'
        exit()
    LA = LinkMatrix()
    #LA.process()
    #LA.writeIndexFile()
    #LA.writeMetaData()
    #print LA.linkConnect
    LA.setFiles(sys.argv[1],sys.argv[2],sys.argv[3])
    LA.query()
