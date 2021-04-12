from PSOAlgorithm import PSOOptimization
from TestFunctions import TestFunctions

test=TestFunctions()
numofpara=10
lowerbound=[0]*numofpara
upperbound=[0]*numofpara
for i in range(numofpara):
  lowerbound[i]=-29.99
  upperbound[i]=29.99
tolerance=0.000001
numofswarms=200
initialgusssize=1000
maximumiteration=5000
PSO=PSOOptimization(lowerbound,upperbound,tolerance,numofswarms,initialgusssize,maximumiteration,test)
PSO.optimize()


