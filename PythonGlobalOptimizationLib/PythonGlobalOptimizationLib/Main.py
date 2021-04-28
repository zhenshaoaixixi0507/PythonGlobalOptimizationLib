import ChaoticPSOAlgorithm as PSO
import TestFunctions as TF
#import yfinance as yf
#import matplotlib.pyplot as plt
#import seaborn

#msft = yf.Ticker("MSFT")

## get stock info
#print(msft.info)

## get historical market data
#hist = msft.history(period="5d")
#hist['Close'].plot(figsize=(16, 9))

numofpara=20
lowerbound=[0]*numofpara
upperbound=[0]*numofpara
for i in range(numofpara):
  lowerbound[i]=-29.99
  upperbound[i]=29.99
tolerance=0.000001
numofswarms=100
initialgusssize=1000
maximumiteration=5000
optimizedparameters=PSO.chaoticPSOOptimize(TF.function1,lowerbound,upperbound,maximumiteration,initialgusssize,numofswarms,tolerance)


