"""
* Creation Date : 05-09-2011
* Last Modified : 
* Created By :  Shreesh Ayachit (shreesh.ayachit@gmail.com)
* Description : 
"""
from matplotlib import pyplot
import math
if __name__ == "__main__":
    k = [1,3,5,11,21,51,101,201,501,1001]
    RMSE1 = [131666,106961,101392,98620,98195,100310,102480,104439,107911,111033] # Unnormalized,UnWeighted
    RMSE2 = [91302.3,79168,75973.7,74720.4,75790.3,78823.9,82302.7,86840.6,94915.1,103652]        # Normalized,Unweighted
    #RMSEN = [82445.68210672728,77593.48084942155,72576.80019886539,69506.95602087707,67918.94286228428,63603.71178167287,62177.73470865206]
    RMSEN = [82445.68210672728,77593.48084942155,72576.80019886539,69506.95602087707,67918.94286228428,63603.71178167287,62177.73470865206]
    N = [185,371,928,1857,3715,9288,18576]
    #line1 = pyplot.semilogx(k,RMSE1,'r--o')
    #line2 = pyplot.semilogx(k,RMSE2,'b-s')
    line = pyplot.semilogx(N,RMSEN,'b-s')
    #pyplot.legend([line1,line2],["UnNornmalized","Normalized"])
    #pyplot.legend([line1],["Normalized-k10"])
    pyplot.ylabel('RMSE')
    pyplot.xlabel('N')
    pyplot.title('N vs RMSE')
    pyplot.show()
