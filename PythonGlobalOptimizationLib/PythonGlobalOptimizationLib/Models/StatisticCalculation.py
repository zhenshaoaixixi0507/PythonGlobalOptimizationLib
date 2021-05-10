import numpy as np
import math
def LogReturnCalculation(p:np.ndarray)->np.ndarray:
    log=math.log
    return [log(p[i+1]/p[i])*100 for i in range(len(p)-1)]
def UnconditionalVolCalculation(ret:np.ndarray)->np.ndarray:
    result=np.zeros((len(ret),1))
    vol=np.sqrt(np.var(ret))
    for i in range(len(result)):
        result[i]=vol
    return result