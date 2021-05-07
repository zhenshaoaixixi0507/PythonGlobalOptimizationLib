import numpy as np
import math
import ChaoticPSOAlgorithm as PSO

def AR1GARCH11NormalOptimize(ret:np.ndarray)->[float]:
    LL=np.zeros(shape=(len(ret)-2,1))
    sigmasquare=np.zeros(shape=(len(ret)-2,1))
    log=np.log
    pi=math.pi
    def loglik(parameters:[np.ndarray])->float:
        residual=ret[1:(len(ret)-1)]-ret[0:(len(ret)-2)]*parameters[0]
        sigmasquarezero=parameters[1]/(1-parameters[2]-parameters[3])
        if parameters[2]+parameters[3]>1:
            return 99999999999.99
        else:
            for i in range(len(LL)):
                newsigma=parameters[1]+parameters[2]*residual[i]*residual[i]+parameters[3]*sigmasquarezero
                sigmasquare[i]=newsigma
                r=residual[i]
                zt=r*r/newsigma
                LL[i]=0.5*log(2*pi)+0.5*log(newsigma)+0.5*log(zt)
                sigmasquarezero=newsigma
            return sum(LL)

    lowerbound=np.zeros(shape=(4,1))
    lowerbound[0]=-0.99
    lowerbound[1]=0.001
    lowerbound[2]=0.001
    lowerbound[3]=0.60
    upperbound=np.zeros(shape=(4,1))
    upperbound[0]=0.99
    upperbound[1]=4.9999
    upperbound[2]=0.99999
    upperbound[3]=0.99999
    tolerance=0.000000001
    numofswarms=100
    initialgusssize=1000
    maximumiteration=500
    initialguess=np.zeros(shape=(4,1))
    initialguess[0]=0.5
    initialguess[1]=0.01
    initialguess[2]=0.01
    initialguess[3]=0.65
    optimizedparameters=PSO.chaoticPSOOptimize(loglik,lowerbound,upperbound,maximumiteration,initialgusssize,initialguess,numofswarms,tolerance)
    return optimizedparameters

def GetInSampleSigma(optpara:np.ndarray,ret:np.ndarray)->[np.ndarray]:
    sigmasquare=np.zeros(shape=(len(ret)-2,1))
    residual=ret[1:(len(ret)-1)]-ret[0:(len(ret)-2)]*optpara[0]
    sigmasquarezero=optpara[1]/(1-optpara[2]-optpara[3])
    for i in range(len(sigmasquare)):
         sigmasquare[i]=optpara[1]+optpara[2]*residual[i]*residual[i]+optpara[3]*sigmasquarezero
         sigmasquarezero=sigmasquare[i]
    return sigmasquare