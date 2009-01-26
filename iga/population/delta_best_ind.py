import igastandard
from iga.gacommon import gaParams
import copy

class Population(igastandard.Population):
    def __init__(self, paramClass, paramDict):
        igastandard.Population.__init__(self, paramClass, paramDict)

#---------------------------------------#
    def nextgen(self):
        '''
        Create next generation from current population.
        '''
        random = self.params.random

        best = copy.deepcopy(self.user_selected[0])
        newPop = [best]
        for i in xrange(self.popsize-1):
            newPop.append(copy.deepcopy(self.user_selected[0]))
            self.params.mutate(newPop[-1], 0.10)

        # evaluate children
        self.eval(newPop)

        self.pop = newPop
        best.rank = 0.

#---------------------------------------#
