import ChaoticPSOAlgorithm as PSO
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import sys
sys.path.append("./DataDownload")
import GetYahooFinanceTimeSeriesData as GD
sys.path.append("./Models")
import StatisticCalculation as SC
import GARCH11Normal as GA11N
import AR1GARCH11Normal as AR1GA11N
# Get Yahoo Finance Data
print("Downloading data...")
adjclose=GD.GetYahooFinanceData('^DJI','2019-12-31','2020-12-31','daily','adjclose')
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

