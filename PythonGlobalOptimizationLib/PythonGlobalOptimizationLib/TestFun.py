class Testfunction:
    def __init__(self,parameters):
        self.parameters=parameters
    returval=0
    def funvalue(self):
        for x in self.parameters:
            returnval=returval+x*x