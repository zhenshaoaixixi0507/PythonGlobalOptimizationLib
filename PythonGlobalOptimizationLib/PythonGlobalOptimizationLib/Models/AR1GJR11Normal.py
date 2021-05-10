import numpy as np
import math
import ChaoticPSOAlgorithm as PSO

def AR1GJR11NormalOptimize(ret:np.ndarray)->[float]:
    log=np.log
    pi=math.pi
    x=ret[0:(len(ret)-2)]
    y=ret[1:(len(ret)-1)]
    A=np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    def loglik(parameters:[np.ndarray])->float:
        residual=ret[1:(len(ret)-1)]-(np.multiply(ret[0:(len(ret)-2)],m)+c)
        sigmasquare=np.zeros(shape=(len(residual),1))
        LL=0.0
        sigmasquarezero=np.mean(np.square(residual))
        residualzero=np.sqrt(np.mean(np.square(residual)))
        if (parameters[1]+parameters[2]*0.5+parameters[3])>1 or (parameters[1]+parameters[3])>1:
            return 99999999999.99
        if (parameters[1]+parameters[2]*0.5+parameters[3])<=1 and (parameters[1]+parameters[3])<=1:
            for i in range(len(residual)):
                newsigma=parameters[0]+parameters[1]*residualzero*residualzero+parameters[2]*residualzero*residualzero*(residualzero<0)+parameters[3]*sigmasquarezero
                sigmasquare[i]=newsigma
                r=residual[i]
                zt=r*r/newsigma
                LL=0.5*log(2*pi)+0.5*log(newsigma)+0.5*log(zt)+LL
                if np.isnan(LL):
                    LL=9999999999999.999
                    break;
                sigmasquarezero=newsigma
                residualzero=residual[i]
            return LL

    lowerbound=np.zeros((4,1))
    lowerbound[0]=0.001
    lowerbound[1]=0.1
    lowerbound[2]=0.001
    lowerbound[3]=0.6
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
    residual=ret[1:(len(ret)-1)]-(np.multiply(ret[0:(len(ret)-2)],m)+c)
    initialguess[0]=0.1*np.var(residual)
    initialguess[1]=0.15
    initialguess[2]=0.05
    initialguess[3]=0.75
    optimizedparameters=np.zeros((6,1))
    optimizedparameters[0]=c
    optimizedparameters[1]=m
    optimizedpara=PSO.chaoticPSOOptimize(loglik,lowerbound,upperbound,maximumiteration,initialgusssize,initialguess,numofswarms,tolerance)
    optimizedparameters[2]=optimizedpara[0]
    optimizedparameters[3]=optimizedpara[1]
    optimizedparameters[4]=optimizedpara[2]
    optimizedparameters[5]=optimizedpara[3]
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