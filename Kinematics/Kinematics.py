# -*- coding: utf-8 -*-

import sys
from numpy import array,dot,zeros,ones,set_printoptions,eye
import math as m
from random import randrange

class Point:
    def __init__(self, points):
        self.coords = points

    def __repr__(self):
        res ="["
        for x in self.coords:
            res += str(x) + ","
        res +="]"
        return res
    def distance(self,target):
        res = 0
        for c1,c2 in zip(self.coords,target.coords):
            res += m.pow(c1-c2,2)
        return m.sqrt(res)


class Arm:
    def __init__(self, thetas=None,lengths=None):
        self.joints = len(thetas)
        self.thetas = thetas if thetas else []
        self.lengths = lengths
    def __repr__(self):
        res = "["
        for theta in self.thetas:
            res += str(theta) + ","
        res += "]"
        return res
class Kinematics:
    def __init__(self,target=None,pose=None):
        self.hand = Point([randrange(0,30),randrange(0,30)])
        if not pose:
            self.arm = Arm([randrange(-30,30),randrange(-30,30),randrange(-45,45)],[80,50,20])
        else:
            self.arm = pose
        self.target = target
        self.tolerence = 0.001
        self.Beta = 0.00001
        self.jointLowerBounds = [-30,-30,-45]
        self.jointUpperBounds = [30,30,45]

    def near(self):
        return True if (self.target.distance(self.hand) < self.tolerence) else False

    def getHomogenousRotMatrix(self,theta):
        return array([[m.cos(theta), -m.sin(theta),0],[m.sin(theta),m.cos(theta),0],[0,0,1]],dtype=float)

    def getHomogenousTransMatrix(self,length):
        return array([[1,0,length],[0,1,0],[0,0,1]])

    def getDifferentialOfRotMatrix(self,theta):
        return array([[-m.sin(theta), -m.cos(theta),0],[m.cos(theta),-m.sin(theta),0],[0,0,1]],dtype=float)

    def doFKSolver(self,origin):
        prod = origin.T
        r = []
        t = []
        for i in range(0,3):
            #r.append(self.getHomogenousRotMatrix(self.arm.thetas[i]))
            #t.append(self.getHomogenousTransMatrix(self.arm.lengths[i]))
            r = -self.getHomogenousRotMatrix(self.arm.thetas[i])
            t =self.getHomogenousTransMatrix(self.arm.lengths[i])
            prod  = dot(r,dot(t,prod))
        #print 'prod :',prod
        #prod = dot(r[0],dot(t[0],dot(r[1],dot(t[1],dot(r[2],dot(t[2],origin.T))))))
        self.hand = Point([prod[0,0],prod[1,0]])
        #print 'hand ',self.hand
        #print 'arm ',self.arm
        #print 'target ',self.target 

    def reset(self):
        self.hand = Point([randrange(0,30),randrange(0,30)])
        self.arm = Arm([randrange(-30,30),randrange(-30,30),randrange(-45,45)],[80,50,20])

    def crossedBoundry(self):
        for theta in self.arm.thetas:
            if theta < -30 or theta > 45:
                return True
        return False

    def doIKSolver(self):
        thetas = array([self.arm.thetas],dtype=float)
        lengths = self.arm.lengths
        #origin = array([0,0,1])
        prod = array([self.hand.coords]).T
        #e = dot(dot(dot(e,h1),h2),h3)
        jacobian = zeros((2,3))
        restart = 0
        while not self.near():
            for j in range(2,-1,-1):
                prod = array([[0],[0],[1]])
                r = []
                t = []
                for i in range(0,3):
                    '''if (j == i):
                        r.append(self.getDifferentialOfRotMatrix(self.arm.thetas[i]))
                    else:
                        r.append(self.getHomogenousRotMatrix(self.arm.thetas[i]))
                    t.append(self.getHomogenousTransMatrix(self.arm.lengths[i]))'''
                    if j == i:
                        r = -self.getDifferentialOfRotMatrix(self.arm.thetas[i])
                    else:
                        r = -self.getHomogenousRotMatrix(self.arm.thetas[i])
                    t =self.getHomogenousTransMatrix(self.arm.lengths[i])
                    prod  = dot(r,dot(t,prod))
                #prod = dot(r[0],dot(t[0],dot(r[1],dot(t[1],dot(r[2],dot(t[2],origin))))))
                jacobian[0,j] = prod[0,0]
                jacobian[1,j] = prod[1,0]
            jacobianT = jacobian.T
            deltaE  = []
            for c1,c2 in zip(self.target.coords,self.hand.coords):
                deltaE.append(c1-c2)
            deltaTheta = dot(jacobianT,dot(array(deltaE).T,self.Beta))
            #print 'deltaTheta ',deltaTheta
            thetas = thetas + deltaTheta.T
            #print 'Theta ',thetas
            self.arm.thetas = thetas.tolist()[0]
            origin = array([[0,0,1]]);
            self.doFKSolver(origin)
            #print 'Jacobian: \n',jacobian
            if self.crossedBoundry():
                restart += 1
                print '** reset ',restart
                if (restart  > 10):
                    break
                self.reset()
                jacobian = zeros((2,3))
        print 'hand ',self.hand
        print 'target ',self.target 
    def __repr__(self):
        return (" Solver with hand : %s  target: %s arm %s") % (self.hand, self.target,self.arm)

def IKSolver():
    with open("input.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            l = map(float,line.split("\t"))
            #l.append(1)
            p = Point(l)
            print '------------------------------------'
            print 'Running for Target: ',p
            solver = Kinematics(target = p)
            solver.doIKSolver()
            print solver

def FKSolver():
    solver = Kinematics(pose = Arm([45,30,30],[80,50,30]))
    origin = array([[0,0,1]]);
    solver.doFKSolver(origin)
    #print solver

def usage():
    pass

if __name__ == "__main__":
    set_printoptions(precision=3)
    set_printoptions(suppress=True)
    #FKSolver()
    IKSolver()
    

