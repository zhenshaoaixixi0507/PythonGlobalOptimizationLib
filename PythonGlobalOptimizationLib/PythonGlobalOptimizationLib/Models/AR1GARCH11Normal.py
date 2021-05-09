import numpy as np
import math
import ChaoticPSOAlgorithm as PSO

def AR1GARCH11NormalOptimize(ret:np.ndarray)->[float]:
    log=np.log
    pi=math.pi
    x=ret[0:(len(ret)-2)]
    y=ret[1:(len(ret)-1)]
    A=np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    def loglik(parameters:[np.ndarray])->float:
        residual=ret[1:(len(ret)-1)]-(np.multiply(ret[0:(len(ret)-2)],m)+c)
        sigmasquare=np.zeros(shape=(len(residual),1))
        LL=np.zeros(shape=(len(residual),1))
        sigmasquarezero=np.mean(np.square(residual))
        residualzero=np.sqrt(np.mean(np.square(residual)))
        if (parameters[1]+parameters[2])>=1:
            return 99999999999.99
        if parameters[1]+parameters[2]<1:
            for i in range(len(LL)):
                newsigma=parameters[0]+parameters[1]*residualzero*residualzero+parameters[2]*sigmasquarezero
                sigmasquare[i]=newsigma
                r=residual[i]
                zt=r*r/newsigma
                LL[i]=0.5*log(2*pi)+0.5*log(newsigma)+0.5*log(zt)
                sigmasquarezero=newsigma
                residualzero=residual[i]
            return sum(LL)

    lowerbound=np.zeros((3,1))
    lowerbound[0]=0.001
    lowerbound[1]=0.1
    lowerbound[2]=0.7
    upperbound=np.zeros((3,1))
    upperbound[0]=0.49
    upperbound[1]=0.99
    upperbound[2]=0.99999
    tolerance=0.000000001
    numofswarms=100
    initialgusssize=1000
    maximumiteration=500
    initialguess=np.zeros((3,1))
    initialguess[0]=0.01
    initialguess[1]=0.05
    initialguess[2]=0.85
    optimizedparameters=np.zeros((5,1))
    optimizedparameters[0]=c
    optimizedparameters[1]=m
    optimizedpara=PSO.chaoticPSOOptimize(loglik,lowerbound,upperbound,maximumiteration,initialgusssize,initialguess,numofswarms,tolerance)
    optimizedparameters[2]=optimizedpara[0]
    optimizedparameters[3]=optimizedpara[1]
    optimizedparameters[4]=optimizedpara[2]
    return optimizedparameters

def GetInSampleSigma(optpara:np.ndarray,ret:np.ndarray)->[np.ndarray]:
    residual=ret[1:(len(ret)-1)]-(ret[0:(len(ret)-2)]*optpara[1]+optpara[0])
    sigmasquare=np.zeros(shape=(len(residual),1))
    sigmasquarezero=np.mean(np.square(residual))
    residualzero=np.sqrt(np.mean(np.square(residual)))
    for i in range(len(sigmasquare)):
         sigmasquare[i]=optpara[2]+optpara[3]*residualzero*residualzero+optpara[4]*sigmasquarezero
         sigmasquarezero=sigmasquare[i]
         residualzero=residual[i]
    return sigmasquare