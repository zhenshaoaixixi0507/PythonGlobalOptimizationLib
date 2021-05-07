import numpy as np
import math
import ChaoticPSOAlgorithm as PSO

def GARCH11NormalOptimize(ret:np.ndarray)->[float]:
    residual=ret-np.mean(ret)
    LL=np.zeros(shape=(len(residual)-1,1))
    sigmasquare=np.zeros(shape=(len(residual)-1,1))
    log=np.log
    pi=math.pi
    def loglik(parameters:[np.ndarray])->float:
        sigmasquarezero=parameters[0]/(1-parameters[1]-parameters[2])
        if parameters[1]+parameters[2]>=0.99999:
            return 99999999999.99
        else:
            for i in range(len(LL)):
                newsigma=parameters[0]+parameters[1]*residual[i]*residual[i]+parameters[2]*sigmasquarezero
                sigmasquare[i]=newsigma
                r=residual[i]
                zt=r*r/newsigma
                LL[i]=0.5*log(2*pi)+0.5*log(newsigma)+0.5*log(zt)
                sigmasquarezero=newsigma
            return sum(LL)

    lowerbound=np.zeros(shape=(3,1))
    lowerbound[0]=0.001
    lowerbound[1]=0.001
    lowerbound[2]=0.60
    upperbound=np.zeros(shape=(3,1))
    upperbound[0]=4.9999
    upperbound[1]=0.99999
    upperbound[2]=0.99999
    tolerance=0.000000001
    numofswarms=100
    initialgusssize=1000
    maximumiteration=500
    initialguess=np.zeros(shape=(3,1))
    initialguess[0]=0.01
    initialguess[1]=0.01
    initialguess[2]=0.65
    optimizedparameters=PSO.chaoticPSOOptimize(loglik,lowerbound,upperbound,maximumiteration,initialgusssize,initialguess,numofswarms,tolerance)
    return optimizedparameters

def GetInSampleSigma(optpara:np.ndarray,ret:np.ndarray)->[np.ndarray]:
    residual=ret-np.mean(ret)
    sigmasquare=np.zeros(shape=(len(residual)-1,1))
    sigmasquarezero=optpara[0]/(1-optpara[1]-optpara[2])
    for i in range(len(residual)-1):
         sigmasquare[i]=optpara[0]+optpara[1]*residual[i]*residual[i]+optpara[2]*sigmasquarezero
         sigmasquarezero= sigmasquare[i]
    return sigmasquare