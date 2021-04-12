import random
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
    for i in range(len(x)):
        x[i]=max(lowerbound[i],min(upperbound[i],x[i]))

 def ConstrainV(tempV,Vmax):
    for i in range(len(tempV)):
        tempV[i]=max(-Vmax,min(Vmax,tempV[i]))

 def GenerateR(seed,length):
     random.seed(seed)
     result=[0]*length
     for i in length(result)
        result[i]=random.random()
    return result

 def optimize(self):
   inertiaweightmax=1.2
   inertiaweightmin=0.1
   chi=0.73
   c1=2.0
   c2=2.0
   Vmax=4
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
     localswarm[i]=temp
     localbest[i]=temp
     Velocity[i]=tempV
     if i == 1:
         minerror = self._objectfun.function1(temp)
     if i>1:
         error = self._objectfun.function1(temp)
         if error<minerror:
             minerror=error
             globalbest=temp
   print("Minerror = %f" %minerror)
   print("--------Best Solution----------")
   print(globalbest)
   
   

	
