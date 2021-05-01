import numpy as np
import math
def LogReturnCalculation(p:np.ndarray)->np.ndarray:
    log=math.log
    return [log(p[i+1]/p[i])*100 for i in range(len(p)-1)]