import math
import copy
import gastandard

class Population(gastandard.Population):
    def __init__(self, paramClass, paramDict):
        gastandard.Population.__init__(self, paramClass, paramDict)

        # reevaluate the need to keep a ref to the subset dictionary
        subset = paramDict['subset']
        execstr = 'from subset.%s import subset as subsetfunc' % (subset['type'])
        exec(execstr)
        self.subsetfunc = subsetfunc

        inject = paramDict['inject']
        execstr = 'from inject.%s import %s as injectfunc' % (inject['type'], inject['type'])
        exec(execstr)
        self.injectfunc = injectfunc

        self.subset = []
        self.user_selected = []


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
            for i in user_selection:
                user_selected.append(self.subset[i])
            self.user_selected = user_selected

#---------------------------------------#
    def getNRandom(self, num):
        if num < self.popsize:
            return self.params.random.sample(self.pop, num)
        else:
            return self.params.random.sample(self.pop, min(self.popsize, num))

#---------------------------------------#
    def fitnessBias(self, pop):
        for ind in pop:
            bias = ind.bloodline
            ind.fitness += ind.fitness * bias * 2

#---------------------------------------#
    def eval(self, pop=None):
        if not pop:
            pop = self.pop

        self.params.app.preFitnessEval(None, None)
        fitness_func = self.params.app.fitness
        user_selected = self.user_selected
        for ind in pop:
            fitness_func(ind, user_selected)

        # fitness bias of population
        self.fitnessBias(pop)
        # scale fitness of population
        self.params.app.scaleFitness(pop)


#---------------------------------------#
    def setBloodLine(self, p1, p2, c1, c2):
        '''
        p1, p2: parent1, parent2
        c1, c2: child1, child2
        Set the bloodline of the children based on the bloodline of the parents.
        '''
        p1_blood, p2_blood = p1.bloodline, p2.bloodline
        c1.bloodline = c1.from_p1 * p1_blood + c1.from_p2 * p2_blood
        c2.bloodline = c2.from_p1 * p1_blood + c2.from_p2 * p2_blood

#---------------------------------------#
    def crossover(self, parent1, parent2):
        child1, child2 = self.params.crossover(parent1, parent2)
        self.setBloodLine(parent1, parent2, child1, child2)
        return child1, child2

#---------------------------------------#
    def injectGenomes(self, injection_feedback):
        '''
        Take a list of individuals from peers and inject them
        into the population replacing a % of the current pop.
        If user selected the best from a peer, then store
        it as the global best of the current pop.
        '''
        genomes = injection_feedback.get('genomes', None)
        best = injection_feedback.get('best', None)
        if genomes:
            for ind in genomes:
                ind.bloodline = 1.

            to_replace = int(self.popsize * self.paramDict['inject']['percent'])
            self.injectfunc(self.pop, genomes, self.params.random, to_replace)

            if best:
                self.user_selected = [best]

#---------------------------------------#
    def selectSubset(self):
        '''
        Select a small subset from the large population of the
        IGA to be displayed for user evaluation.
        '''
        self.subset, self.subset_index = self.subsetfunc(self.pop, self.params.random, self.paramDict['subset']['size'])
        return self.subset

#---------------------------------------#
    def getSubset(self, all=False):
        if all:
            return self.subset[:]
        else:
            sub = self.user_selected[:]
            sub_size = self.paramDict['subset']['size']
            if sub:
                sub_size -= 1
            to_return = sub + self.subset[:sub_size]
            return to_return


##---------------------------------------#
#    def linear_scaling(self):
#
#        s_factor = 1.2
#
#        _max = pop[0].fitness
#        avg = 0.
#        for ind in pop:
#            _max = ind.fitness if ind.fitness > _max
#            avg += ind.fitness
#
#        average = avg/len(pop)
#        _min = pop[0].fitness
#        for ind in pop:
#            _min = ind.fitness if ind.fitness < _min
#
#
#
#        if _min > (s_factor*average - _max)/(s_factor - 1.0):
#            delta = _max - average
#            a = (s_factor - 1.0)*average/delta
#            b = average * (_max - s_factor*average)/delta
#        else:
#            delta = average - _min
#            a = average/delta
#            b = -1.0*_min*average/delta
#        param = [a, b]
#
#
##---------------------------------------#
#    def fitness_scaling(self):
#
#        s = 1.005
#        for i in range(0, self.popsize):
#            self.popsize[i].fitness = math.pow(self.popsize[i], s_power)
#        return scale_fit
#

#---------------------------------------#
    def nextgen(self):
        '''
        Create next generation from current population.
        '''
        newPop = []
        for i in range(0, self.popsize, 2):
            p1 = self.selectParent()
            p2 = self.selectParent()
            c1, c2 = self.crossover(p1, p2)
            self.params.mutate(c1)
            self.params.mutate(c2)
            newPop.extend([c1, c2])

        self.eval(newPop)
        self.combinepop(newPop)
        try:
            randPos = self.params.random.randrange(0, self.popsize)
            self.pop[randPos] = copy.deepcopy(self.user_selected[0])
            self.pop[randPos].fitness = 100
        except:
            print 'could not copy'
            pass

#---------------------------------------#
    def setPop(self, newPop):
        self.pop = newPop

#---------------------------------------#
    def setSubset(self, subset):
        self.subset = subset

#---------------------------------------#
    def get_best(self, context):

        return [self.user_selected[0]] + self.subset[1:3]

#---------------------------------------#
    def getPop(self):
        return self.pop[:]

#---------------------------------------#
