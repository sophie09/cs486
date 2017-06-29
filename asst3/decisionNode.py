class DecisionNode:
    def __init__(self,word=-1,tb=None,fb=None,tResult=None,fResult=None):
        self.word = word
        self.tb = tb
        self.fb = fb
        self.tResult = tResult
        self.fResult = fResult

    def tAdd(self,value):
        if isinstance(value, int):
            self.tResult = value
        else:
            self.tb = value

    def fAdd(self,value):
        if isinstance(value, int):
            self.fResult = value
        else:
            self.fb = value



