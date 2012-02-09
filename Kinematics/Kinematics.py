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
            res += str(x) + " "
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
            res += str(theta) + " "
            res += "]"
        return res
class Kinematics:
    def __init__(self,target=None,pose=None):
        self.hand = Point([1,1,0])
        if not pose:
            self.arm = Arm([randrange(-30,30),randrange(-30,30),randrange(-45,45)],[80,50,20])
        else:
            self.arm = pose
        self.target = target
        self.tolerence = 0.000001
        self.Beta = 0.01

    def near(self):
        return True if (self.target.distance(self.hand) < self.tolerence) else False

    def getHomogenousRotMatrix(self,theta):
        return array([[m.cos(theta), -m.sin(theta),0],[m.sin(theta),m.cos(theta),0],[0,0,1]],dtype=float)

    def getHomogenousTransMatrix(self,length):
        return array([[1,0,length],[0,1,0],[0,0,1]])

    def getDifferentialOfRotMatrix(self,theta):
        return array([[-m.sin(theta), -m.cos(theta),0],[m.cos(theta),-m.sin(theta),0],[0,0,0]],dtype=float)

    def doFKSolver(self,origin):
        prod = origin.T
        r = []
        t = []
        for i in range(0,3):
            r.append(self.getHomogenousRotMatrix(self.arm.thetas[i]))
            t.append(self.getHomogenousTransMatrix(self.arm.lengths[i]))
            #prod  = dot(r,dot(t,prod))
        prod = dot(r[2],dot(t[2],dot(r[1],dot(t[1],dot(r[0],dot(t[0],origin.T))))))
        self.hand = Point(list(prod))
        print 'hand ',self.hand
        print 'target ',self.target 

    def reset(self):
        
    def crossedBoundry(self):
        for theta in self.arm.thetas:
            if theta < -30 or theta > 30:
                return True
        return False

    def doIKSolver(self):
        thetas = array([self.arm.thetas])
        lengths = self.arm.lengths
        origin = array([0,0,1]).T
        e = array([0,0,1])
        #e = dot(dot(dot(e,h1),h2),h3)
        jacobian = zeros((3,3))
        while not self.near():
            for j in range(0,3):
                prod = ones((3,3))
                r = []
                t = []
                for i in range(0,3):
                    if (j == i):
                        r.append(self.getDifferentialOfRotMatrix(self.arm.thetas[i]))
                    else:
                        r.append(self.getHomogenousRotMatrix(self.arm.thetas[i]))
                    t.append(self.getHomogenousTransMatrix(self.arm.lengths[i]))
                prod = dot(r[2],dot(t[2],dot(r[1],dot(t[1],dot(r[0],dot(t[0],origin.T))))))
                jacobian[:j] = prod.T
            jacobianT = jacobian.T
            deltaE  = self.Beta * (array([self.target.coords]) - array([self.hand.coords]))
            deltaTheta = dot(jacobianT,deltaE.T)
            print 'deltaTheta ',deltaTheta
            thetas += deltaTheta.T
            self.doFKSolver(origin)
            self.checkBoundry()
            print 'Jacobian: \n',jacobian
    def __repr__(self):
        return (" Solver with hand : %s  target: %s arm %s") % (self.hand, self.target,self.arm)

def IKSolver():
    with open("input.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            l = map(float,line.strip().split("\t"))
            l.append(1)
            p = Point(l)
            print 'Running for Target: ',p
            solver = Kinematics(target = p)
            solver.doIKSolver()
            print solver
            print '------------------------------------'

def FKSolver():
    solver = Kinematics(pose = Arm([45,30,30],[80,50,30]))
    origin = array([0,0,1]);
    solver.doFKSolver(origin)
    print solver

def usage():
    pass

if __name__ == "__main__":
    set_printoptions(precision=3)
    #FKSolver()
    IKSolver()
    

