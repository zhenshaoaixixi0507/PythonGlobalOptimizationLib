import numpy as np
import math
def LogReturnCalculation(p:np.ndarray)->np.ndarray:
    return [math.log(p[i+1]/p[i]) for i in range(len(p)-1)]