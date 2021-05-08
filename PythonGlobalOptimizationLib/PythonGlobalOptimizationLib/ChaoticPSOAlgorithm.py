import random
import math
import numpy as np
from typing import Callable

RealFunc = Callable[[np.ndarray], float]  # type alias for a real -> real function

def ConstrainX(x:np.ndarray,lowerbound:np.ndarray, upperbound:np.ndarray)-> np.ndarray:
    for i in range(len(x)):
        if x[i]<lowerbound[i]:
            x[i]=lowerbound[i]
        if x[i]>upperbound[i]:
            x[i]=upperbound[i]
    return x.copy()

def ConstrainV(tempV:np.ndarray,Vmax:float)->np.ndarray:
    for i in range(len(tempV)):
        if tempV[i]<-Vmax:
            tempV[i]=-Vmax
        if tempV[i]>Vmax:
            tempV[i]=Vmax
    return tempV.copy()

def GenerateR(u0:float,y0:float,length:int)->(float,float,np.ndarray):
    result=np.zeros((length,1))
    for i in range(length):
       y0 = math.cos(2 * math.pi * u0) + y0 * math.exp(-3)
       u0 = (u0 + 400 + 12 * y0) % 1.0
       result[i] = min(max(u0, 0), 1)
    return (u0,y0,result)

def swaplocalbest(function:RealFunc,oldx:np.ndarray, newx:np.ndarray)->np.ndarray:
     olderror=function(oldx)
     newerror=function(newx)
     if newerror<olderror:
         return newx.copy()
     if newerror>=olderror:
         return oldx.copy()

def chaoticPSOOptimize(function: RealFunc,lowerbound:np.ndarray,upperbound:np.ndarray,
     maximumiteration:int,initialgusssize:int,initialguess:np.ndarray,numofswarms:int,
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
   temp=np.zeros((len(lowerbound),1))
   tempV=np.zeros((len(lowerbound),1))
   globalbest=initialguess.copy()
   u0=1.0
   y0=1.0
   for i in range(initialgusssize):
     for j in range(len(lowerbound)):
        y0 = math.cos(2 * math.pi * u0) + y0 * math.exp(-3)
        u0 = (u0 + 400 + 12 * y0) % 1.0
        temp[j]=(upperbound[j] - lowerbound[j]) * min(max(u0, 0), 1) + lowerbound[j]
        y0 = math.cos(2 * math.pi * u0) + y0 * math.exp(-3)
        u0 = (u0 + 400 + 12 * y0) % 1.0
        tempV[j] = 2 * Vmax * min(max(u0, 0), 1) - Vmax
     temp=ConstrainX(temp,lowerbound,upperbound)
     tempV=ConstrainV(tempV,Vmax)
     localswarm[i]=temp.copy()
     localbest[i]=initialguess.copy()
     Velocity[i]=tempV.copy()
     if i == 1:
         minerror = function(temp)
     if i>1:
         error = function(temp)
         if error<minerror:
             minerror=error
             globalbest=temp.copy()
   oldglobalerror=minerror
   u0 = 1.00
   y0 = 1.00
   fabs=math.fabs
   for i in range(maximumiteration):
       tempweight = (inertiaweightmin + (inertiaweightmax-inertiaweightmin) / maximumiteration* i)
       for j in range(numofswarms):
            tempx = localswarm[j].copy()
            tempV = Velocity[j].copy()
            templocalbest = localbest[j].copy()
            item1 = tempV*tempweight
            (u0,y0,R1)=GenerateR(u0,y0,len(lowerbound))
            (u0,y0,R2)=GenerateR(u0,y0,len(lowerbound))
            item2 = np.multiply((templocalbest-tempx),R1*c1)
            item3 = np.multiply((globalbest-tempx), R2*c2)
            item1 = np.add(item1, item2)
            item1 = np.add(item1, item3)
            newV =item1*chi
            newV = ConstrainV(newV, Vmax)
            newX = np.add(tempx, newV)
            newX = ConstrainX(newX,lowerbound,upperbound)
            localswarm[j] = newX.copy()
            Velocity[j] = newV.copy()
            newlocalbest = swaplocalbest(function,tempx, newX)
            localbest[j] = newlocalbest.copy()
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
   
