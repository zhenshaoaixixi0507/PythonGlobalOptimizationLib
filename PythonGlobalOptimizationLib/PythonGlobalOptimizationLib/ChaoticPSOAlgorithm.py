import random
import math
class ChaoticPSOOptimization:
 def __init__ (self,lowerbound,upperbound,tolerance,numofswarms,initialgusssize,maximumiteration,objectivefunclass):
        self._lowerbound=lowerbound
        self._upperbound=upperbound
        self._tolerance=tolerance
        self._numofswarms=numofswarms
        self._initialgusssize=initialgusssize
        self._objectfun=objectivefunclass
        self._maximumiteration=maximumiteration
 
 def ConstrainX(x,lowerbound, upperbound):
    result=[0]*len(lowerbound)
    for i in range(len(x)):
        result[i]=x[i]
        if x[i]<lowerbound[i]:
            result[i]=lowerbound[i]
        if x[i]>upperbound[i]:
            result[i]=upperbound[i]
    return result
 def ConstrainV(tempV,Vmax):
    result=[0]*len(tempV)
    for i in range(len(tempV)):
        result[i]=tempV[i]
        if tempV[i]<-Vmax:
            result[i]=-Vmax
        if tempV[i]>Vmax:
            result[i]=Vmax
    return result
 def GenerateR(seed,length):
     random.seed(seed)
     result=[0]*length
     for i in range(len(result)):
         result[i]=random.random()
     return result

 def swaplocalbest(self,oldx, newx):
     result=[0]*len(oldx)
     olderror=self._objectfun.function1(oldx)
     newerror=self._objectfun.function1(newx)
     if newerror<olderror:
         for i in range(len(newx)):
             result[i]=newx[i]
     if newerror>=olderror:
         for i in range(len(oldx)):
             result[i]=oldx[i]
     return result
 def ArrayMinus(x,y):
     result=[0]*len(x)
     for i in range(len(x)):
         result[i]=x[i]-y[i]
     return result
 def ArrayPlus(x,y):
     result=[0]*len(x)
     for i in range(len(x)):
         result[i]=x[i]+y[i]
     return result
 def ArrayMultiplyConstant(x,c):
     result=[0]*len(x)
     for i in range(len(x)):
         result[i]=x[i]*c
     return result
 def ArrayMultiplyArray(x,y):
     result=[0]*len(x)
     for i in range(len(x)):
         result[i]=x[i]*y[i]
     return result
 def optimize(self):
   inertiaweightmax=1.2
   inertiaweightmin=0.1
   chi=1
   c1=2.0
   c2=2.0
   Vmax=4.0
   detalweight = (inertiaweightmax - inertiaweightmin) / self._maximumiteration
   minerror =9999999999999.999
   localswarm ={}
   localbest ={}
   Velocity = {}
   # Initialize 
   temp=[0]*len(self._lowerbound)
   tempV=[0]*len(self._lowerbound)
   globalbest=[0]*len(self._lowerbound)
   C10=0.21
   C20=0.63
   for i in range(self._initialgusssize):
     for j in range(len(self._lowerbound)):
        C10 = 4 * C10 * (1 - C10)
        C20 = 4 * C20 * (1 - C20)
        temp[j]=(self._upperbound[j] - self._lowerbound[j]) * C10 + self._lowerbound[j]
        tempV[j] = 2 * Vmax * C20 - Vmax
     localswarm[i]=temp.copy()
     localbest[i]=temp.copy()
     Velocity[i]=tempV.copy()
     if i == 1:
         minerror = self._objectfun.function1(temp)
     if i>1:
         error = self._objectfun.function1(temp)
         if error<minerror:
             minerror=error
             globalbest=temp
   oldglobalerror=minerror
   C10 = 0.37
   C20 = 0.73
   C30=0.12
   for i in range(self._maximumiteration):
       tempweight = (inertiaweightmin + (inertiaweightmax-inertiaweightmin) / self._maximumiteration* i)*C30
       C30=4*C30*(1-C30)
       for j in range(self._numofswarms):
            C10 = 4 * C10 * (1 - C10)
            C20 = 4 * C20 * (1 - C20)
            tempx = localswarm[j].copy()
            tempV = Velocity[j].copy()
            templocalbest = localbest[j].copy()
            item1 = ChaoticPSOOptimization.ArrayMultiplyConstant(tempV, tempweight)
            item2 = ChaoticPSOOptimization.ArrayMultiplyConstant(ChaoticPSOOptimization.ArrayMinus(templocalbest, tempx),C10*c1)
            item3 = ChaoticPSOOptimization.ArrayMultiplyConstant(ChaoticPSOOptimization.ArrayMinus(globalbest, tempx), C20 * c2)
            item1 = ChaoticPSOOptimization.ArrayPlus(item1, item2)
            item1 = ChaoticPSOOptimization.ArrayPlus(item1, item3)
            newV = ChaoticPSOOptimization.ArrayMultiplyConstant(item1, 1);
            newV = ChaoticPSOOptimization.ConstrainV(newV, Vmax);
            newX = ChaoticPSOOptimization.ArrayPlus(tempx, newV);
            newX = ChaoticPSOOptimization.ConstrainX(newX,self._lowerbound,self._upperbound);
            localswarm[j] = newX
            Velocity[j] = newV
            newlocalbest = ChaoticPSOOptimization.swaplocalbest(self,tempx, newX)
            localbest[j] = newlocalbest
            localerror = self._objectfun.function1(localbest[j])
            if localerror < minerror:
               globalbest = localbest[j]
               minerror = localerror
      
       if math.fabs(oldglobalerror - minerror) < self._tolerance and i > math.floor(self._maximumiteration / 3 * 2):
          break
       else:
         oldglobalerror = minerror
         print("Objective function value: = %f" %minerror)                  
   return globalbest
   
