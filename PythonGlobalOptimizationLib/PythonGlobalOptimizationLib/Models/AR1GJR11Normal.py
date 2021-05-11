import numpy as np
import math
import ChaoticPSOAlgorithm as PSO

def AR1GJR11NormalOptimize(ret:np.ndarray)->[float]:
    log=np.log
    pi=math.pi
    x=ret[0:(len(ret)-2)]
    y=ret[1:(len(ret)-1)]
    def loglik(parameters:[np.ndarray])->float:
        residual=ret[1:(len(ret)-1)]-(np.multiply(ret[0:(len(ret)-2)],parameters[1])+parameters[0])
        sigmasquare=np.zeros(shape=(len(residual),1))
        LL=0.0
        sigmasquarezero=np.mean(np.square(residual))
        residualzero=np.sqrt(np.mean(np.square(residual)))
        if (parameters[3]+parameters[4]*0.5+parameters[5])>1 or (parameters[3]+parameters[5])>1:
            return 99999999999.99
        if (parameters[3]+parameters[4]*0.5+parameters[5])<=1 and (parameters[3]+parameters[5])<=1:
            for i in range(len(residual)):
                newsigma=parameters[2]+parameters[3]*residualzero*residualzero+parameters[4]*residualzero*residualzero*(residualzero<0)+parameters[5]*sigmasquarezero
                sigmasquare[i]=newsigma
                r=residual[i]
                zt=r*r/newsigma
                LL=log(newsigma)+zt+LL
                sigmasquarezero=newsigma
                residualzero=residual[i]
            return LL

    lowerbound=np.zeros((6,1))
    lowerbound[0]=-4.99
    lowerbound[1]=-0.99
    lowerbound[2]=0.00001
    lowerbound[3]=0.0001
    lowerbound[4]=0.00001
    lowerbound[5]=0.6
    upperbound=np.zeros((6,1))
    upperbound[0]=4.99
    upperbound[1]=0.99
    upperbound[2]=0.99
    upperbound[3]=0.99
    lowerbound[4]=0.99
    upperbound[5]=0.99999
    tolerance=0.000000001
    numofswarms=100
    initialgusssize=1000
    maximumiteration=500
    initialguess=np.zeros((6,1))
    initialguess[0]=0.1
    initialguess[1]=0.5
    residual=ret[1:(len(ret)-1)]-(np.multiply(ret[0:(len(ret)-2)],initialguess[1])+initialguess[0])
    initialguess[2]=0.1*np.var(residual)
    initialguess[3]=0.15
    initialguess[4]=0.05
    initialguess[5]=0.75
    optimizedparameters=PSO.chaoticPSOOptimize(loglik,lowerbound,upperbound,maximumiteration,initialgusssize,initialguess,numofswarms,tolerance)
    return optimizedparameters

def GetInSampleSigma(optpara:np.ndarray,ret:np.ndarray)->[np.ndarray]:
    residual=ret[1:(len(ret)-1)]-(ret[0:(len(ret)-2)]*optpara[1]+optpara[0])
    sigmasquare=np.zeros(shape=(len(residual),1))
    sigmasquarezero=np.mean(np.square(residual))
    residualzero=np.sqrt(np.mean(np.square(residual)))
    for i in range(len(sigmasquare)):
         sigmasquare[i]=optpara[2]+optpara[3]*residualzero*residualzero+optpara[4]*residualzero*residualzero*(residualzero<0)+optpara[5]*sigmasquarezero
         sigmasquarezero=sigmasquare[i]
         residualzero=residual[i]
    return sigmasquare