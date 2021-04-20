from ChaoticPSOAlgorithm import ChaoticPSOOptimization
from TestFunctions import TestFunctions
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn

msft = yf.Ticker("MSFT")

# get stock info
print(msft.info)

# get historical market data
hist = msft.history(period="5d")
hist['Close'].plot(figsize=(16, 9))
#test=TestFunctions()
#numofpara=20
#lowerbound=[0]*numofpara
#upperbound=[0]*numofpara
#for i in range(numofpara):
#  lowerbound[i]=-29.99
#  upperbound[i]=29.99
#tolerance=0.000001
#numofswarms=100
#initialgusssize=1000
#maximumiteration=5000
#ChaoticPSO=ChaoticPSOOptimization(lowerbound,upperbound,tolerance,numofswarms,initialgusssize,maximumiteration,test)
#optimizedparameters=ChaoticPSO.optimize()


