"""
* Creation Date : 03-09-2011
* Last Modified :
* Created By :  Shreesh Ayachit (shreesh.ayachit@gmail.com)
* Description : A naive  Implementation of k Nearest Neighbour Algorithm
"""
import math

def drange(start,stop,step):
    r = start
    while r < stop:
        yield r
        r += step

def distance(item,point,dim):
    d = 0
    for i in range(0,dim):  # (x-cord,y-cord,val,distance)
        d += (item[i]-point[i]) ** 2
    return d

def knn(k,point,trainingSet):
    #nearest = [(x,distance(x,point,2)) for x in trainingSet[:k] ]
    #nearest.sort(cmp = lambda  x,y: distance(x,point,2) < distance(y,point,2))
    nearest = [] 
    for i,x  in enumerate(trainingSet):
        #if (set(x).intersection(point)): # Same point
        #    continue
        d = distance(x,point,2)
        nearest.append((d,i))
        #nearest.sort(cmp = lambda  x,y: distance(x,point,2) < distance(y,point,2))
    nearest = sorted(nearest,key = lambda x : x[0])
    print  nearest
    knear  = [ ]
    for i,val in enumerate(nearest):
        if(nearest[i][0] != nearest[i+1][0]):
            knear = nearest[:i+1] 
            break
    if(len(knear) == 0):
        knear = nearest[:k]
    return knear
    

    # print "distance bw (%g,%g) and (%g,%g) is %g" % (point[0],point[1],r,h,d)
    #print "(%g,%g,%g)" % (point[0],point[1],v)

def drawBoundry(rows,height,res,trainingSet):
    ''' gives the boundry points depending on training points
    '''
    concept = []
    for r,h in [(row,ht) for row in drange(1.0,rows,res) for ht in drange(1.0,height,res)]:
        nearest = knn(1,(r,h),trainingSet)
        argmax = 0 
        if len(nearest):
            for n in nearest:
                if(trainingSet[n[1]][2] > 0):
                    argmax = 1
                    break
                #argmax += trainingSet[n[1]][2]
            if argmax > 0 or argmax == 0: # +ve
                print "%g,%g,1" %(r,h)
            else:
                print "%g,%g,-1" %(r,h)

if __name__ == "__main__":
    tSet1 = [(1.0,4.0,-1),(1.0,1.0,1.0),(2.0,3.0,-1),(3.0,1.0,-1),(4.0,2.0,1),(4.0,5.0,1)]
    tSet2 = [(2.0,1.0,-1),(3.0,2.0,-1),(4.0,0.5,-1),(5.0,1.0,1),(3.5,3.5,1),(2.0,4.0,1),(1.0,3.0,1)]
    tSet3 = [(1.0,1.0,1),(1.0,4.0,-1),(2.0,3,-1),(3.0,1.0,-1),(4.0,2.0,1),(4.0,5.0,1)]
    tSet4 = [(1.0,3.0,1),(2.0,1.0,-1),(2.0,4,1),(3.0,2.0,-1),(4.0,0.5,-1),(3.5,3.5,1),(5.0,1.0,1)]
    
    tSet5 = [(1.0,4.0,-1),(1.0,6.0,-1),(2.0,1.0,-1),(2.0,2.0,-1),(3.0,3.0,1),(3.0,4.0,1),(4.0,1.0,-1),(4.0,3.0,1),(5.0,5.0,1),(5.0,6.0,1),(6.0,1.0,-1),(6.0,5.0,1)]
    drawBoundry(7,7,1,tSet5)

