from parameters import Parameters

class GA:
    def __init__(self, params_dict):
        self.params = Parameters(params_dict)
        self.gen = 0
        self.database = params_dict

#---------------------------------------#
    def run(self):
        '''
        '''
        self.params.pop.eval()
        self.params.app.report(self.params.pop.pop, self.gen)
        gen = self.gen
        limit = self.params.params['numgen']
        while gen < limit:
            self.params.pop.nextgen()
            gen += 1
            self.params.app.report(self.params.pop.pop, gen)


#---------------------------------------#
    def callAppSlot(self, slot, args):
        self.params.app.callAppSlot(slot, args)

#---------------------------------------#
    def updateMask(self, mask):
        self.params.app.updateMask(self.params.pop.pop, mask)

#---------------------------------------#
    def getPop(self):
        return self.params.pop.pop

#---------------------------------------#
