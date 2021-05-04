import ChaoticPSOAlgorithm as PSO
import TestFunctions as TF
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import sys
sys.path.append("./DataDownload")
import GetYahooFinanceTimeSeriesData as GD
sys.path.append("./Models")
import StatisticCalculation as SC
import GARCHNormal as GAN

# Get Yahoo Finance Data
print("Downloading data...")
adjclose=GD.GetYahooFinanceData('^GSPC','2014-12-31','2019-12-31','weekly','adjclose')
print("Data downloaded, optimize parameters...")
logret=SC.LogReturnCalculation(adjclose)
DF_logret = pd.DataFrame(logret)
DF_logret.to_csv("DataDownload/return.csv",index=False)
#plot1 = plt.figure(1)
#plt.plot(adjclose)
#plot2 = plt.figure(2)
#plt.plot(logret)
#plt.show()

optimizedpara=GAN.GARCHNormalOptimize(logret)
print(optimizedpara)
sigmainsmaple=GAN.GetInSampleSigma(optimizedpara,logret)
plt.plot(sigmainsmaple)
plt.show()

