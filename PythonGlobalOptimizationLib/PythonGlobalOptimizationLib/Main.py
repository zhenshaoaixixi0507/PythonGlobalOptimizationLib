import ChaoticPSOAlgorithm as PSO
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import TestFunctions as ts
import sys
sys.path.append("./DataDownload")
import GetYahooFinanceTimeSeriesData as GD
sys.path.append("./Models")
import StatisticCalculation as SC
import GARCH11Normal as GA11N
import GJR11Normal as GJR11N
import AR1GARCH11Normal as AR1GA11N

# Get Yahoo Finance Data
print("Downloading data...")
adjclose=GD.GetYahooFinanceData('^GSPC','2015-12-31','2018-12-31','daily','adjclose')
print("Data downloaded, optimize parameters...")
logret=SC.LogReturnCalculation(adjclose)
DF_logret = pd.DataFrame(logret)
DF_logret.to_csv("DataDownload/return.csv",index=False)

optimizedpara1=GA11N.GARCH11NormalOptimize(logret)
sigmainsmaple1=GA11N.GetInSampleSigma(optimizedpara1,logret)
optimizedpara2=AR1GA11N.AR1GARCH11NormalOptimize(logret)
sigmainsmaple2=AR1GA11N.GetInSampleSigma(optimizedpara2,logret)
print(optimizedpara1)
print(optimizedpara2)
plot1 = plt.figure(1)
plt.plot(sigmainsmaple1)
plot2 = plt.figure(2)
plt.plot(sigmainsmaple2)
plt.show()
#optimizedpara=GJR11N.GJR11NormalOptimize(logret)
#sigmainsmaple=GJR11N.GetInSampleSigma(optimizedpara,logret)
#print(optimizedpara)
#plt.plot(sigmainsmaple)
#plt.show()

