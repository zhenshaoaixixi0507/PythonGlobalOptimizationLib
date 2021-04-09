from TestFun import Testfunction
#class PSOAlogrithm:
	#def __init__(self,lowerbound,upperbound,tolerance):
		#self.lowerbound=lowerbound
		#self.upperbound=upperbound
		#self.tolerance=tolerance
        #numofswarms=200
		#maximumiteration=5000;
		#inertiaweightmax = 1.2
		#inertiaweightmin = 0.1
		#chi = 0.73
		#c1=2
		#c2=2
		#Vmax = 4
parameters=[2,3,4,5,5]
testfun= Testfunction(parameters)
print(testfun.funvalue)
	
