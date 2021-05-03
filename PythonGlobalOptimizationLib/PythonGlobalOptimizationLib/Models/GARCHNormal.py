import numpy as np
import math
import ChaoticPSOAlgorithm as PSO

def GARCHNormalOptimize(ret:np.ndarray)->[float]:
    residual=ret-np.mean(ret)
    LL=np.zeros(shape=(len(residual)-1,1))
    sigmasquare=np.zeros(shape=(len(residual),1))
    sigmasquare[0]=residual[0]*residual[0]
    log=math.log
    
    pi=math.pi
    def loglik(parameters:[np.ndarray])->float:
        if parameters[1]+parameters[2]>=1:
            return 99999999999.99
        else:
            for i in range(len(LL)):
                newsigma=parameters[0]+parameters[1]*residual[i]*residual[i]+parameters[2]*sigmasquare[i]*sigmasquare[i]
                sigmasquare[i+1]=newsigma
                r=residual[i+1]
                zt=r*r/newsigma
                LL[i]=0.5*log(2*pi)+0.5*log(min(newsigma,999999))+0.5*log(zt+0.0000000001)
            return sum(LL)

    lowerbound=np.zeros(shape=(3,1))
    lowerbound[0]=0.000000001
    lowerbound[1]=0.000000001
    lowerbound[2]=0.65
    upperbound=np.zeros(shape=(3,1))
    upperbound[0]=0.9999
    upperbound[1]=0.9999
    upperbound[2]=0.9999
    tolerance=0.000000001
    numofswarms=100
    initialgusssize=1000
    maximumiteration=500
    optimizedparameters=PSO.chaoticPSOOptimize(loglik,lowerbound,upperbound,maximumiteration,initialgusssize,numofswarms,tolerance)
    return optimizedparameters