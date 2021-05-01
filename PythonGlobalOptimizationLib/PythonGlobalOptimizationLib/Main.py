import ChaoticPSOAlgorithm as PSO
import TestFunctions as TF
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import arch as ar
import sys
sys.path.append("./DataDownload")
import GetYahooFinanceTimeSeriesData as GD
sys.path.append("./Models")
import StatisticCalculation as SC
import GARCHNormal as GAN

# Get Yahoo Finance Data
print("Downloading data...")
adjclose=GD.GetYahooFinanceData('TSLA','2014-12-31','2019-12-31','weekly','adjclose')
print("Data downloaded, optimize parameters...")
logret=SC.LogReturnCalculation(adjclose)
#plot1 = plt.figure(1)
#plt.plot(adjclose)
#plot2 = plt.figure(2)
#plt.plot(logret)
#plt.show()

optimizedpara=GAN.GARCHNormalOptimize(logret)

# Specify GARCH model assumptions
#basic_gm = ar.arch_model(logret, p = 1, q = 1,
#                      mean = 'constant', vol = 'GARCH', dist = 'normal')
# Fit the model
#gm_result = basic_gm.fit(update_freq = 4)
#print(gm_result.summary())
print("Finished.")


