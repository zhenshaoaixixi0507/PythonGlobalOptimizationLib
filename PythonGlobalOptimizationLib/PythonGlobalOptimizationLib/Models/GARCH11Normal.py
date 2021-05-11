import numpy as np
import math
import ChaoticPSOAlgorithm as PSO

def GARCH11NormalOptimize(ret:np.ndarray)->[float]:
    residual=ret-np.mean(ret)
    sigmasquare=np.zeros(shape=(len(residual),1))
    log=np.log
    pi=math.pi
    def loglik(parameters:[np.ndarray])->float:
        sigmasquarezero=np.mean(np.square(residual))
        residualzero=np.sqrt(np.mean(np.square(residual)))
        result=0.0
        LL=0.0
        if (parameters[1]+parameters[2])>=1:
            result= 9999999999999.999
        if (parameters[1]+parameters[2])<1:
            for i in range(len(sigmasquare)):
                newsigma=parameters[0]+parameters[1]*residualzero*residualzero+parameters[2]*sigmasquarezero
                sigmasquare[i]=newsigma
                r=residual[i]
                zt=r*r/newsigma
                #LL=0.5*log(2*pi)+0.5*log(newsigma)+0.5*log(zt)+LL
                LL=zt+log(newsigma)+LL
                sigmasquarezero=newsigma
                residualzero=residual[i]
            result=LL
        return result
    lowerbound=np.zeros((3,1))
    lowerbound[0]=0.000001
    lowerbound[1]=0.00001
    lowerbound[2]=0.6
    upperbound=np.zeros((3,1))
    upperbound[0]=4.99
    upperbound[1]=0.99
    upperbound[2]=0.99999
    tolerance=0.000000001
    numofswarms=100
    initialgusssize=1000
    maximumiteration=500
    initialguess=np.zeros((3,1))
    initialguess[0]=0.1*np.var(residual)
    initialguess[1]=0.15
    initialguess[2]=0.75
    optimizedparameters=PSO.chaoticPSOOptimize(loglik,lowerbound,upperbound,maximumiteration,initialgusssize,initialguess,numofswarms,tolerance)
    return optimizedparameters

def GetInSampleSigma(optpara:np.ndarray,ret:np.ndarray)->[np.ndarray]:
    residual=ret-np.mean(ret)
    sigmasquare=np.zeros((len(residual),1))
    sigmasquarezero=np.mean(np.square(residual))
    residualzero=np.sqrt(np.mean(np.square(residual)))
    for i in range(len(residual)):
         sigmasquare[i]=optpara[0]+optpara[1]*residualzero*residualzero+optpara[2]*sigmasquarezero
         sigmasquarezero= sigmasquare[i]
         residualzero=residual[i]
    sigmasquare=np.sqrt(sigmasquare)
    return sigmasquare

def Simulate(parameters:np.ndarray,lastsigma:float,lastresidual:float,numofsims:int,timesteps:int)->np.ndarray:
    np.random.seed(1)
    r=np.random.normal(0,1,size=(numofsims,timesteps))
    sims=np.zeros((numofsims,timesteps))
    sqrt=np.sqrt
    for t in range(timesteps):
        for i in range(numofsims):
            newsigma=parameters[0]+parameters[1]*lastresidual*lastresidual+parameters[2]*lastsigma
            sims[i,t]=sqrt(newsigma)
            lastsigma=newsigma
            lastresidual=sims[i,t]*r[i,t]
    return sims