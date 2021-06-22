import random
from math import exp,fabs,cos,pi
from numpy import zeros,multiply,add,ndarray
from typing import Callable

RealFunc = Callable[[ndarray], float]  # type alias for a real -> real function

def ConstrainX(x:ndarray,lowerbound:ndarray, upperbound:ndarray)-> ndarray:
    for i in range(len(x)):
        x[i]=min(max(x[i],lowerbound[i]),upperbound[i])
    
    return x.copy()


def ConstrainV(tempV:ndarray,Vmax:float)->ndarray:
    for i in range(len(tempV)):
        tempV[i]=min(max(tempV[i],-Vmax),Vmax)

    return tempV.copy()


def GenerateR(u0:float,y0:float,length:int)->(float,float,ndarray):
    result=zeros((length,1))
    for i in range(length):
       y0 = cos(2 * pi * u0) + y0 * exp(-3)
       u0 = (u0 + 400 + 12 * y0) % 1.0
       result[i] = min(max(u0, 0), 1)
    return (u0,y0,result)


def swaplocalbest(function:RealFunc,oldx:ndarray, newx:ndarray)->ndarray:
     olderror=function(oldx)
     newerror=function(newx)
     if newerror<olderror:
         return newx.copy()
     if newerror>=olderror:
         return oldx.copy()


def chaoticPSOOptimize(function: RealFunc,lowerbound:ndarray,upperbound:ndarray,
     maximumiteration:int,initialgusssize:int,initialguess:ndarray,numofswarms:int,
     tolerance:float
) -> float:
   inertiaweightmax=1.2
   inertiaweightmin=0.1
   chi=0.73
   c1=2.0
   c2=2.0
   Vmax=4.0
   detalweight = (inertiaweightmax - inertiaweightmin) / maximumiteration
   minerror =9999999999999.999
   localswarm ={}
   localbest ={}
   Velocity = {}
   # Initialize 
   temp=zeros((len(lowerbound),1))
   tempV=zeros((len(lowerbound),1))
   globalbest=initialguess.copy()
   minerror = function(globalbest)
   u0=1.0
   y0=1.0
   for i in range(initialgusssize):
     for j in range(len(lowerbound)):
        y0 = cos(2 * pi * u0) + y0 * exp(-3)
        u0 = (u0 + 400 + 12 * y0) % 1.0
        temp[j]=(upperbound[j] - lowerbound[j]) * min(max(u0, 0), 1) + lowerbound[j]
        y0 = cos(2 * pi * u0) + y0 * exp(-3)
        u0 = (u0 + 400 + 12 * y0) % 1.0
        tempV[j] = 2 * Vmax * min(max(u0, 0), 1) - Vmax
     localswarm[i]=ConstrainX(temp,lowerbound,upperbound)
     localbest[i]=initialguess.copy()
     Velocity[i]=ConstrainV(tempV,Vmax)
     error = function(temp)
     if error<minerror:
        minerror=error
        globalbest=temp.copy()
   oldglobalerror=minerror
   u0 = 1.00
   y0 = 1.00
   for i in range(maximumiteration):
       tempweight = (inertiaweightmin+(inertiaweightmax-inertiaweightmin) / maximumiteration* i)
       for j in range(numofswarms):
            (u0,y0,R1)=GenerateR(u0,y0,len(lowerbound))
            (u0,y0,R2)=GenerateR(u0,y0,len(lowerbound))
            item2 = multiply((localbest[j].copy()-localswarm[j].copy()),R1*c1)
            item3 = multiply((globalbest-localswarm[j].copy()), R2*c2)
            item1 = add( Velocity[j].copy()*tempweight, item2)
            item1 = add(item1, item3)
            localswarm[j] = ConstrainX(add(localswarm[j].copy(), ConstrainV(item1*chi, Vmax)),lowerbound,upperbound)
            Velocity[j] = ConstrainV(item1*chi, Vmax)
            newlocalbest = swaplocalbest(function,localswarm[j].copy(), localswarm[j])
            localbest[j] = newlocalbest
            localerror = function(localbest[j])
            if localerror < minerror:
               globalbest = localbest[j].copy()
               minerror = localerror
      
       if fabs(oldglobalerror - minerror) < tolerance and i>5:
          print("Objective function value: = %f" %minerror)
          break
       else:
         oldglobalerror = minerror
         print("Objective function value: = %f" %minerror)                  
   return globalbest
   
