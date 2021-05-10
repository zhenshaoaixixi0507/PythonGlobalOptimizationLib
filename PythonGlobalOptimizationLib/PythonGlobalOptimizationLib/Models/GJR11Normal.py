import numpy as np
import math
import ChaoticPSOAlgorithm as PSO

def GJR11NormalOptimize(ret:np.ndarray)->[float]:
    residual=ret-np.mean(ret)
    sigmasquare=np.zeros(shape=(len(residual),1))
    log=np.log
    pi=math.pi
    def loglik(parameters:[np.ndarray])->float:
        sigmasquarezero=np.mean(np.square(residual))
        residualzero=np.sqrt(np.mean(np.square(residual)))
        result=0.0
        LL=0.0
        if (parameters[1]+parameters[2]*0.5+parameters[3])>1 or (parameters[1]+parameters[3])>1:
            result= 9999999999999.999
        if (parameters[1]+parameters[2]*0.5+parameters[3])<=1 and (parameters[1]+parameters[3])<=1:
            for i in range(len(sigmasquare)):
                newsigma=parameters[0]+parameters[1]*residualzero*residualzero+parameters[2]*residualzero*residualzero*(residualzero<0)+parameters[3]*sigmasquarezero
                sigmasquare[i]=newsigma
                r=residual[i]
                zt=r*r/newsigma
                LL=0.5*log(2*pi)+0.5*log(newsigma)+0.5*log(zt)+LL
                sigmasquarezero=newsigma
                residualzero=residual[i]
            result=LL
        return result
    lowerbound=np.zeros((4,1))
    lowerbound[0]=0.001
    lowerbound[1]=0.1
    lowerbound[2]=0.001
    lowerbound[3]=0.49
    upperbound=np.zeros((4,1))
    upperbound[0]=0.49
    upperbound[1]=0.49
    lowerbound[2]=0.99
    upperbound[3]=0.99999
    tolerance=0.000000001
    numofswarms=100
    initialgusssize=1000
    maximumiteration=500
    initialguess=np.zeros((4,1))
    initialguess[0]=0.1*np.var(residual)
    initialguess[1]=0.15
    initialguess[2]=-0.5
    initialguess[3]=0.75
    optimizedparameters=PSO.chaoticPSOOptimize(loglik,lowerbound,upperbound,maximumiteration,initialgusssize,initialguess,numofswarms,tolerance)
    return optimizedparameters

def GetInSampleSigma(optpara:np.ndarray,ret:np.ndarray)->[np.ndarray]:
    residual=ret-np.mean(ret)
    sigmasquare=np.zeros((len(residual),1))
    sigmasquarezero=np.mean(np.square(residual))
    residualzero=np.sqrt(np.mean(np.square(residual)))
    for i in range(len(residual)):
         sigmasquare[i]=np.sqrt(optpara[0]+optpara[1]*residualzero*residualzero+optpara[2]*residualzero*residualzero*(residualzero<0)+optpara[3]*sigmasquarezero)
         sigmasquarezero= sigmasquare[i]
         residualzero=residual[i]
    return sigmasquare