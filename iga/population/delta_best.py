import nsga_ii
from iga.gacommon import gaParams
import copy

class Population(nsga_ii.Population):
    def __init__(self, paramClass, paramDict):
        nsga_ii.Population.__init__(self, paramClass, paramDict)

        ops = gaParams.getVar('operators')
        len_ops = len(ops)
        op_prob = 1. / len_ops
        for i in xrange(len_ops):
            ops[i] = op_prob
        self.op_len = len(ops)
        print 'ops ', ops

#---------------------------------------#
    def fitnessBias(self, pop):
        pass

#---------------------------------------#
    def userInput(self, user_selection = []):
        '''
        Takes a list of the indices of the individuals selected 
        by the user during evaluation, and we save the actual
        users on a list, to be used during fitness evaluation.
        It is the programmer's responsibility to decide on
        the meaning of the user feedback.
        '''
        # if feedback provided, otherwise the user selection was made
        # on the injected individuals
        if user_selection:
            user_selected = []

            ops = gaParams.getVar('operators')

            inc_prob = .05
            dec_prob = .05 / len(ops)-1
            for i in user_selection:
                ind = self.subset[i]
                user_selected.append(ind)

                ind_ops = ind.operators
                ind_ops.count(1)
                if ind_ops:
                    for j in xrange(self.op_len):
                        if ind_ops[j]:
                            ops[j] = min(ops[j] + 0.05, 0.9)
                        else:
                            ops[j] = max(ops[j] - 0.05, 0.1)


            print 'ops ', ops

            self.user_selected = user_selected

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
            self.params.mutate(newPop[-1], 0.30)

        # evaluate children
        self.eval(newPop)

        self.pop = newPop
        best.rank = 0.

#---------------------------------------#
