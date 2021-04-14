import random
import math
class PSOOptimization:
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
   chi=0.73
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
   for i in range(self._initialgusssize):
     random.seed(i+1)
     for j in range(len(self._lowerbound)):
        temp[j]=(self._upperbound[j] - self._lowerbound[j]) * random.random() + self._lowerbound[j]
        tempV[j] = 2 * Vmax * random.random() - Vmax
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
   for i in range(self._maximumiteration):
       tempweight = inertiaweightmin + (inertiaweightmax-inertiaweightmin) / self._maximumiteration* i
       for j in range(self._numofswarms):
            tempx = localswarm[j].copy()
            tempV = Velocity[j].copy()
            templocalbest = localbest[j].copy()
            r1 = PSOOptimization.GenerateR(j + i + 1, len(tempx))
            r2 = PSOOptimization.GenerateR(j+i+2,len(tempV))
            item1 = PSOOptimization.ArrayMultiplyConstant(tempV, tempweight)
            item2 = PSOOptimization.ArrayMultiplyConstant(r1, c1)
            item2 = PSOOptimization.ArrayMultiplyArray(item2, PSOOptimization.ArrayMinus(templocalbest, tempx))
            item3 = PSOOptimization.ArrayMultiplyConstant(r2, c2)
            globalbest_tempx=PSOOptimization.ArrayMinus(globalbest, tempx)
            item3 = PSOOptimization.ArrayMultiplyArray(item3,globalbest_tempx )
            item1 = PSOOptimization.ArrayPlus(item1, item2)
            item1 = PSOOptimization.ArrayPlus(item1, item3)
            newV = PSOOptimization.ArrayMultiplyConstant(item1, chi)
            newV = PSOOptimization.ConstrainV(newV, Vmax)
            newX = PSOOptimization.ArrayPlus(tempx, newV)
            newX = PSOOptimization.ConstrainX(newX,self._lowerbound,self._upperbound)
            localswarm[j] = newX
            Velocity[j] = newV
            newlocalbest = PSOOptimization.swaplocalbest(self,tempx, newX)
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
   
