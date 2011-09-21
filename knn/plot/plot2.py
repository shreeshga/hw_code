"""
* Creation Date : 05-09-2011
* Last Modified : 
* Created By :  Shreesh Ayachit (shreesh.ayachit@gmail.com)
* Description : 
"""
from matplotlib import pyplot
import math
if __name__ == "__main__":
    N = 30
    x1 = [2,3,4] 
    y1 = [1,2,0.5]
    x2 = [1,2,3.5,5] 
    y2 = [3,4,3.5,1] 
    #area = pi*(10 * rand(N))**2 # 0 to 10 point radiuses
    pyplot.scatter(x1,y1,s=25,c='r',marker="o")
    pyplot.scatter(x2,y2,s =25 ,c='g',marker="d")
    #pyplot.legend([line1],["Normalized-k10"])
    #x = [0.5,1,1.5,2,2.5]
    #y = [2.5,2.5,2.5,2,0]
    x = [0.5,1,1.5,2,2.5,3,3.5,4,4.5]
    y = [1.5,2,2,2.5,3,3,3,3,1]
    pyplot.plot(x,y)
    pyplot.text(1.5, 3, "P")
    pyplot.text(3.5, 2, "N")
    pyplot.text(4.5, 3, "P")
    #x1 = [3,3.5,4]
    #y1 = [4.5,2,1.5]
    #pyplot.plot(x1,y1)
    pyplot.grid(True)
    pyplot.show()

