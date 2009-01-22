import wx
import app.app as app
from app.helperfuncs import hamming, lcs
from iga.individual import Individual

import TreeNode

#-------------------------------------------#
class TreeIndividual(Individual):
    def __init__(self, random, genome_len, genome):

        Individual.__init__(self, random, genome_len, genome)


def printTree(depth, tree):

    if tree is None:
        return
    else:
        s = ''
        for i in range(depth):
            s += '\t'

        s += '%d' % tree.id
        print s
        printTree(depth+1, tree.left)
        printTree(depth+1, tree.right)

def createTree(depth, tree):
    if depth is 0:
        return
    else
        tree.left = TreeNode()
        createTree(depth-1, tree.left)
        tree.right = TreeNode()
        createTree(depth-1, tree.right)

#-------------------------------------------#
class Tree_character3d(app.Application):
    def __init__(self, params, random):
        app.Application.__init__(self, params, random)

        self.geomNodes = params['init_context']['geomNodes']
        self.geneLen *= self.geomNodes

#-------------------------------------------#
    def createPop(self, popsize):        
        '''
        Need to create trees here.
        '''
        depth = 4
        root = TreeNode()
        createTree(depth, root)
        counter = 0
        printTree(counter, root)

        pop = [Individual(self.random, self.geneLen) for i in xrange(popsize)]
        return pop

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
        return [self.decode(ind) for ind in subset]

#-------------------------------------------#
    def decode(self, ind):
        '''
        Decode bit string.
        '''
        chrom = ind.genome
        bits = 0
        data_list = []
        for g_i in range(self.geomNodes):
            data = {}
            for name in self.attr_genome:
                value = self.attr[name]
                temp = 0
                top = int(bits+value['bits'])
                for i in xrange(int(bits), top):
                    if chrom[i]:
                        temp += 2**(top-i-1)

                temp = temp / (2.**value['bits'] - 1)
                temp =  temp * (value['max']-value['min']) + value['min']
                data[name] = temp
                bits += value['bits']

            data_list.append(data)

        ind.decoded_chrom = data_list

        return data_list

#-------------------------------------------#
    def report(self, pop, subset, gen):
        '''
        '''
        print 'gen', gen

#-------------------------------------------#

