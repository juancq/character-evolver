from copy import deepcopy
import ga

class IGA(ga.GA):
    def __init__(self, params):
        ga.GA.__init__(self, params)
        self.history = []

#---------------------------------------#
    def close(self):
        self.params.app.close()

#---------------------------------------#
    def back(self):
        oldgen, pop, subset = self.history.pop()
        self.params.pop.setPop(pop)
        self.params.pop.setSubset(subset)

        panels_to_display = self.params.app.draw(subset)
        self.gen = oldgen
        return panels_to_display, oldgen

#---------------------------------------#
    def getSubset(self):
        return self.params.pop.getSubset()

#---------------------------------------#
    def getNRandom(self, num):
        return self.params.pop.getNRandom(num)

#---------------------------------------#
    def draw(self, context):
        '''
        It might be more useful to have a
        reference to the application file 
        on gacommon.
        '''
        print 'here'
        subset_genomes = context['peer_genomes']
        return self.params.app.draw(subset_genomes, context)

#---------------------------------------#
    def run(self):
        panels_to_display = self.igaStep({})
        return panels_to_display

#---------------------------------------#
    def igaStep(self, context):
        '''
        Select subset of individuals to display
        and create panels for them.
        Return the panels to the GUI.
        '''
        to_display = self.params.pop.selectSubset()
        panels_to_display = self.params.app.draw(self.params.pop.subset, context)
        return panels_to_display


#---------------------------------------#
    def pushHistory(self):
        pop = self.params.pop.getPop()
        subset = self.params.pop.getSubset(all=True)
        self.history.append([self.gen, deepcopy(pop), deepcopy(subset)])

#---------------------------------------#
    def step(self, user_selection, inject_genomes, context):
        '''
        Need to look into further detail into the processing
        order of the GA functions.
        Need to rename this param thing.
        '''
        self.pushHistory()
        self.params.pop.injectGenomes(inject_genomes)
        self.params.pop.userInput(user_selection)
        #self.params.app.preFitnessEval(self.params.pop.pop, self.gen)
        self.params.pop.eval()
        #self.params.app.scaleFitness(self.params.pop.pop)
        #self.params.app.postFitnessEval(self.params.pop.pop, self.gen)
        #self.params.app.report(self.params.pop.pop, self.gen)

        gen = self.gen
        limit = min(gen + self.params.params['stepSize'], self.params.params['numgen'])
        panels_to_display = []
        while gen < limit:
            self.params.pop.nextgen()
            gen += 1
            panels_to_display = self.igaStep(context)
            self.params.app.report(self.params.pop.pop, self.params.pop.subset, gen)
        self.gen = gen

        return panels_to_display


#---------------------------------------#
    def get_best(self, context):

        return self.params.pop.get_best(context)

#---------------------------------------#
