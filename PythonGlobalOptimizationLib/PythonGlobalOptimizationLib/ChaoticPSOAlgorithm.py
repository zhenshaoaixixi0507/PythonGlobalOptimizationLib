import random
import math
from typing import Callable

RealFunc = Callable[[float], float]  # type alias for a real -> real function

def ConstrainX(x:[float],lowerbound:[float], upperbound:[float])-> [float]:
    result=[0]*len(lowerbound)
    for i in range(len(x)):
        result[i]=x[i]
        if x[i]<lowerbound[i]:
            result[i]=lowerbound[i]
        if x[i]>upperbound[i]:
            result[i]=upperbound[i]
    return result
def ConstrainV(tempV:[float],Vmax:[float])->[float]:
    result=[0]*len(tempV)
    for i in range(len(tempV)):
        result[i]=tempV[i]
        if tempV[i]<-Vmax:
            result[i]=-Vmax
        if tempV[i]>Vmax:
            result[i]=Vmax
    return result
def GenerateR(u0:float,y0:float,length:int)->(float,float,[float]):
    result=[0]*length
    for i in range(length):
       y0 = math.cos(2 * math.pi * u0) + y0 * math.exp(-3)
       u0 = (u0 + 400 + 12 * y0) % 1.0
       result[i] = min(max(u0, 0), 1)
    return (u0,y0,result)

def swaplocalbest(function:RealFunc,oldx:[float], newx:[float])->[float]:
     result=[0]*len(oldx)
     olderror=function(oldx)
     newerror=function(newx)
     if newerror<olderror:
         result=newx.copy()
     if newerror>=olderror:
         result=oldx.copy()
     return result
def ArrayMinus(x:[float],y:[float])->[float]:
     result=[x[i]-y[i] for i in range(len(x))]
     return result
def ArrayPlus(x:[float],y:[float])->[float]:
     result=[x[i]+y[i] for i in range(len(x))]
     return result
def ArrayMultiplyConstant(x:[float],c:float)->[float]:
     result=[x[i]*c for i in range(len(x))]
     return result
def ArrayMultiplyArray(x:[float],y:[float])->[float]:
    result=[x[i]*y[i] for i in range(len(x))]
    return result
def chaoticPSOOptimize(function: RealFunc,lowerbound:[float],upperbound:[float],
     maximumiteration:int,initialgusssize:int,numofswarms:int,
     tolerance:float
) -> float:
   inertiaweightmax=1.2
   inertiaweightmin=0.1
   chi=1
   c1=2.0
   c2=2.0
   Vmax=4.0
   detalweight = (inertiaweightmax - inertiaweightmin) / maximumiteration
   minerror =9999999999999.999
   localswarm ={}
   localbest ={}
   Velocity = {}
   # Initialize 
   temp=[0]*len(lowerbound)
   tempV=[0]*len(lowerbound)
   globalbest=[0]*len(lowerbound)
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
     localswarm[i]=temp.copy()
     localbest[i]=temp.copy()
     Velocity[i]=tempV.copy()
     if i == 1:
         minerror = function(temp)
     if i>1:
         error = function(temp)
         if error<minerror:
             minerror=error
             globalbest=temp
   oldglobalerror=minerror
   u0 = 1.00
   y0 = 1.00
   for i in range(maximumiteration):
       tempweight = (inertiaweightmin + (inertiaweightmax-inertiaweightmin) / maximumiteration* i)
       for j in range(numofswarms):
           
            tempx = localswarm[j].copy()
            tempV = Velocity[j].copy()
            templocalbest = localbest[j].copy()
            item1 = ArrayMultiplyConstant(tempV, tempweight)
            (u0,y0,R1)=GenerateR(u0,y0,len(lowerbound))
            (u0,y0,R2)=GenerateR(u0,y0,len(lowerbound))
            item2 = ArrayMultiplyArray(ArrayMinus(templocalbest, tempx),ArrayMultiplyConstant(R1,c1))
            item3 = ArrayMultiplyArray(ArrayMinus(globalbest, tempx), ArrayMultiplyConstant(R2,c2))
            item1 = ArrayPlus(item1, item2)
            item1 = ArrayPlus(item1, item3)
            newV =ArrayMultiplyConstant(item1, 1);
            newV = ConstrainV(newV, Vmax);
            newX = ArrayPlus(tempx, newV);
            newX = ConstrainX(newX,lowerbound,upperbound);
            localswarm[j] = newX
            Velocity[j] = newV
            newlocalbest = swaplocalbest(function,tempx, newX)
            localbest[j] = newlocalbest
            localerror = function(localbest[j])
            if localerror < minerror:
               globalbest = localbest[j]
               minerror = localerror
      
       if math.fabs(oldglobalerror - minerror) < tolerance and i > 50:
          break
       else:
         oldglobalerror = minerror
         print("Objective function value: = %f" %minerror)                  
   return globalbest
   
