import numpy as np
class GARCHParameters:
    def __init__(self, omega:float, alpha:float,beta:float,distribution:str):
        self.omega = omega
        self.alpha = alpha
        self.beta=beta
        self.distribution=distribution
def GARCHLoglik(ret:np.ndarray,parameters:GARCHParameters)->float:
    residual=ret-np.mean(ret)