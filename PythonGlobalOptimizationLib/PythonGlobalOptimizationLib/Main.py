import ChaoticPSOAlgorithm as PSO
import TestFunctions as TF
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
sys.path.append("./DataDownload")
import GetYahooFinanceTimeSeriesData as GD
sys.path.append("./Models")
import StatisticCalculation as SC
# Get Yahoo Finance Data
adjclose=GD.GetYahooFinanceData('TSLA','2000-01-01','2019-12-31','weekly','adjclose')
logret=SC.LogReturnCalculation(adjclose)
plot1 = plt.figure(1)
plt.plot(adjclose)
plot2 = plt.figure(2)
plt.plot(logret)
plt.show()

#numofpara=30
#lowerbound=np.zeros(shape=(numofpara,1))
#upperbound=np.zeros(shape=(numofpara,1))
#for i in range(numofpara):
#  lowerbound[i]=-29.99
#  upperbound[i]=29.99
#tolerance=0.000000001
#numofswarms=100
#initialgusssize=1000
#maximumiteration=500
#optimizedparameters=PSO.chaoticPSOOptimize(TF.function1,lowerbound,upperbound,maximumiteration,initialgusssize,numofswarms,tolerance)


