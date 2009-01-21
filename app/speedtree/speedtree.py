import wx
import app.app as app
from app.helperfuncs import hamming, lcs


class Speedtree(app.Application):
    def __init__(self, params, random):
        app.Application.__init__(self, params, random)

#-------------------------------------------#
    def fitness(self, ind, user_feedback):
        '''
        Compute fitness.
        user_feedback is a list of the user's input,
        the list contents are ordered the same as the 
        feedback variable in the config yaml file.
        [best]
        '''
        best = user_feedback[0]

        ind.fitness = hamming(ind.genome, best.genome)

#-------------------------------------------#
    def draw(self, subset, context):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        [self.decode(ind) for ind in subset]
        # example, creating empty panels to display
        return [ind.decoded_chrom for ind in subset]

#-------------------------------------------#
    def report(self, pop, subset, gen):
        '''
        '''
        print 'gen', gen

#-------------------------------------------#

