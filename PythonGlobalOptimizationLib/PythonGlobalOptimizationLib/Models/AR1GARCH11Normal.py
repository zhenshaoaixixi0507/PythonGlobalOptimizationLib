import numpy as np
import math
import ChaoticPSOAlgorithm as PSO

def AR1GARCH11NormalOptimize(ret:np.ndarray)->[float]:
    log=np.log
    pi=math.pi
    def loglik(parameters:[np.ndarray])->float:
        residual=ret[1:(len(ret)-1)]-ret[0:(len(ret)-2)]*parameters[0]
        sigmasquare=np.zeros(shape=(len(residual),1))
        LL=np.zeros(shape=(len(residual),1))
        sigmasquarezero=np.var(residual)
        residualzero=np.mean(residual)
        if (parameters[2]+parameters[3])>=1:
            return 99999999999.99
        if parameters[2]+parameters[3]<1:
            for i in range(len(LL)):
                newsigma=parameters[1]+parameters[2]*residualzero*residualzero+parameters[3]*sigmasquarezero
                sigmasquare[i]=newsigma
                r=residual[i]
                zt=r*r/newsigma
                LL[i]=0.5*log(2*pi)+0.5*log(newsigma)+0.5*log(zt)
                sigmasquarezero=newsigma
                residualzero=residual[i]
            return sum(LL)

    lowerbound=np.zeros((4,1))
    lowerbound[0]=-0.99
    lowerbound[1]=0.0001
    lowerbound[2]=0.0001
    lowerbound[3]=0.7
    upperbound=np.zeros((4,1))
    upperbound[0]=0.99
    upperbound[1]=0.99
    upperbound[2]=0.99
    upperbound[3]=0.99999
    tolerance=0.000000001
    numofswarms=100
    initialgusssize=1000
    maximumiteration=500
    initialguess=np.zeros((4,1))
    initialguess[0]=0.5
    initialguess[1]=0.01
    initialguess[2]=0.15
    initialguess[3]=0.75
    optimizedparameters=PSO.chaoticPSOOptimize(loglik,lowerbound,upperbound,maximumiteration,initialgusssize,initialguess,numofswarms,tolerance)
    return optimizedparameters

def GetInSampleSigma(optpara:np.ndarray,ret:np.ndarray)->[np.ndarray]:
    residual=ret[1:(len(ret)-1)]-ret[0:(len(ret)-2)]*optpara[0]
    sigmasquare=np.zeros(shape=(len(residual),1))
    sigmasquarezero=np.var(residual)
    residualzero=np.mean(residual)
    for i in range(len(sigmasquare)):
         sigmasquare[i]=optpara[1]+optpara[2]*residualzero*residualzero+optpara[3]*sigmasquarezero
         sigmasquarezero=sigmasquare[i]
         residualzero=residual[i]
    return sigmasquare