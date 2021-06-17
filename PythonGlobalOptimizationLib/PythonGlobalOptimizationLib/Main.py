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
#print("Downloading data...")
#adjclose=GD.GetYahooFinanceData('^GSPC','2019-12-31','2021-05-10','daily','adjclose')
#print("Data downloaded, optimize parameters...")
#logret=SC.LogReturnCalculation(adjclose)
#DF_logret = pd.DataFrame(logret)
#DF_logret.to_csv("DataDownload/return.csv",index=False)
#Test optimization algorithm
GA11N.TestOptimizationAlgorithm()
#optimizedpara1=GA11N.GARCH11NormalOptimize(logret)
#sigmainsmaple1=GA11N.GetInSampleSigma(optimizedpara1,logret)
#optimizedpara2=AR1GA11N.AR1GARCH11NormalOptimize(logret)
#sigmainsmaple2=AR1GA11N.GetInSampleSigma(optimizedpara2,logret)
#print(optimizedpara1)
#print(optimizedpara2)

#plot1 = plt.figure(1)
#unconditionalvol1=np.sqrt(np.var(logret-np.mean(logret)))*np.ones((len(logret)-1,1))
#plt.plot(unconditionalvol1,'k--',label=r'$\sigma$')
#plt.plot(sigmainsmaple1,'k',label=r'$\sigma_{t}$')
#plt.legend()
#plt.title('GARCH(1,1)-Normal Volatility Estimation', fontsize=10)
#plt.ylabel('Volatility (%)')
#plot2 = plt.figure(2)
#unconditionalvol2=np.sqrt(np.var(logret[1:(len(logret)-1)]-(np.multiply(logret[0:(len(logret)-2)],optimizedpara2[1])+optimizedpara2[0])))*np.ones((len(logret)-2,1))
#plt.plot(unconditionalvol2,'k--',label=r'$\sigma$')
#plt.plot(sigmainsmaple2,'k',label=r'$\sigma_{t}$')
#plt.legend()
#plt.title('AR(1)-GARCH(1,1)-Normal Volatility Estimation', fontsize=10)
#plt.ylabel('Volatility (%)')
#plt.show()

#GARCH11Normal Simulation
#print("Simulate...")
#mu=np.mean(logret)
#residual=logret-mu
#lastsigma=sigmainsmaple1[len(sigmainsmaple1)-1]**2
#numofsims=10000
#timesteps=10
#sims=GA11N.Simulate(optimizedpara1,lastsigma,residual[len(residual)-1],numofsims,timesteps)
#column_means = sims.mean(axis=0)
#plot3=plt.figure(3)
#plt.plot(column_means)
#plt.title('10-Day GARCH(1,1)-Normal Volatility Forecasting', fontsize=10)
#plt.ylabel('Volatility (%)')
#plt.show()

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

