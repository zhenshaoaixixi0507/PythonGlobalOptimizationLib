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
import GJR11Normal as GJR11N
import AR1GARCH11Normal as AR1GA11N
import AR1GJR11Normal as AR1GJR11N
# Get Yahoo Finance Data
print("Downloading data...")
adjclose=GD.GetYahooFinanceData('^HSI','2018-12-31','2020-12-31','daily','adjclose')
print("Data downloaded, optimize parameters...")
logret=SC.LogReturnCalculation(adjclose)
unconditionalvol=SC.UnconditionalVolCalculation(logret)
DF_logret = pd.DataFrame(logret)
DF_logret.to_csv("DataDownload/return.csv",index=False)

optimizedpara1=GA11N.GARCH11NormalOptimize(logret)
sigmainsmaple1=GA11N.GetInSampleSigma(optimizedpara1,logret)
optimizedpara2=AR1GA11N.AR1GARCH11NormalOptimize(logret)
sigmainsmaple2=AR1GA11N.GetInSampleSigma(optimizedpara2,logret)
print(optimizedpara1)
print(optimizedpara2)

plot1 = plt.figure(1)
plt.plot(unconditionalvol[1:],'k--',label=r'$\sigma$')
plt.plot(sigmainsmaple1,'k',label=r'$\sigma_{t}$')
plt.legend()
plt.title('GARCH(1,1)-Normal Volatility Estimation', fontsize=10)
plt.ylabel('Volatility (%)')
plot2 = plt.figure(2)
plt.plot(unconditionalvol[1:],'k--',label=r'$\sigma$')
plt.plot(sigmainsmaple2,'k',label=r'$\sigma_{t}$')
plt.legend()
plt.title('AR(1)-GARCH(1,1)-Normal Volatility Estimation', fontsize=10)
plt.ylabel('Volatility (%)')
plt.show()

#GJR model
#optimizedpara=GJR11N.GJR11NormalOptimize(logret)
#sigmainsmaple=GJR11N.GetInSampleSigma(optimizedpara,logret)
#print(optimizedpara)
#plt.plot(sigmainsmaple)
#plt.show()
#AR1GJR11 model
#optimizedpara=AR1GJR11N.AR1GJR11NormalOptimize(logret)
#sigmainsmaple=AR1GJR11N.GetInSampleSigma(optimizedpara,logret)
#print(optimizedpara)
#plt.plot(sigmainsmaple)
#plt.show()

