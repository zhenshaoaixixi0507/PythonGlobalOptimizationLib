import numpy as np
import math
import ChaoticPSOAlgorithm as PSO

def GARCHNormalOptimize(ret:np.ndarray)->[float]:
    residual=ret-np.mean(ret)
    LL=np.zeros(shape=(len(residual)-1,1))
    sigmasquare=np.zeros(shape=(len(residual),1))
    sigmasquare[0]=np.var(residual[0:9])#10var seems more robust https://www.researchgate.net/publication/237530561_VARIANCE_INITIALISATION_IN_GARCH_ESTIMATION
    log=np.log
    pi=math.pi
    def loglik(parameters:[np.ndarray])->float:
        if parameters[1]+parameters[2]>1:
            return 99999999999.99
        else:
            for i in range(len(LL)):
                newsigma=parameters[0]+parameters[1]*residual[i]*residual[i]+parameters[2]*sigmasquare[i]
                sigmasquare[i+1]=newsigma
                r=residual[i+1]
                zt=r*r/newsigma
                LL[i]=0.5*log(2*pi)+0.5*log(newsigma)+0.5*log(zt)
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
    sigmasquare=np.zeros(shape=(len(residual),1))
    sigmasquare[0]=np.var(residual[0:9])
    for i in range(len(residual)-1):
         sigmasquare[i+1]=optpara[0]+optpara[1]*residual[i]*residual[i]+optpara[2]*sigmasquare[i]
    return sigmasquare