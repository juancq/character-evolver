import app.app as app
from app.helperfuncs import hamming, lcs
from iga.individual import Individual

from treenode import TreeNode

#-------------------------------------------#
class TreeIndividual(Individual):
    def __init__(self, random, genome_len, genome):

        Individual.__init__(self, random, genome_len, genome)


def compareTrees(tree1, tree2):
    if tree1 is None or tree2 is None:
        return 0
    elif tree1 and tree2:
        c1 = compareTrees(tree1.left, tree2.left)
        c2 = compareTrees(tree1.right, tree2.right)
        return c1+c2+1

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


def getTreeBits(tree, all_bits):

    if tree is None:
        return
    else:
        all_bits.append(tree.getGenome())
        getTreeBits(tree.left, all_bits)
        getTreeBits(tree.right, all_bits)

def initTree(tree, genome_len, rand):

    if tree is None:
        return
    else:
        tree.init(genome_len, rand)
        initTree(tree.left, genome_len, rand)
        initTree(tree.right, genome_len, rand)


def createTree(depth, tree):
    if depth is 0:
        return
    else:
        tree.left = TreeNode()
        createTree(depth-1, tree.left)
        tree.right = TreeNode()
        createTree(depth-1, tree.right)

#-------------------------------------------#
class Tree_character3d(app.Application):
    def __init__(self, params, random):
        app.Application.__init__(self, params, random)

        #self.geomNodes = params['init_context']['geomNodes']
        #self.geneLen *= self.geomNodes
        print '^'*30
        print self.attr
        self.geomNodes = params['init_context']['geomNodes']
        print self.geomNodes, self.geneLen
        #self.geneLen *= self.geomNodes
        #print self.geneLen

#-------------------------------------------#
    def createPop(self, popsize):        
        '''
        Need to create trees here.
        '''
        pop = []
        for i in range(popsize):
            depth = 2
            root = TreeNode()
            root.setRoot()
            createTree(depth, root)
            counter = 0
            #printTree(counter, root)
            initTree(root, self.geneLen, self.random)

            ind = Individual(self.random, length = 0, genome = root)
            self.decode(ind)
            pop.append(ind)

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
        if self.clear:
            self.decode(best)
            self.clear = False

        self.decode(ind)
        f1 = hamming(ind.bit_chrome, best.bit_chrome)
        f1 /= float(len(ind.bit_chrome))


        ind_root = ind.decoded_data
        ind_root.stats()

        best_root = best.decoded_data
        best_root.stats()

        
        f3 = compareTrees(ind_root, best_root)
        f3 /= float(max(ind_root.num_children, best_root.num_children)+1)


        f2 = 0

        #print 'comp: ', f3, f1
        #d = 0
        #printTree(d, ind_root)
        #printTree(d, best_root)


        ind.fitness = (f1*2 + f2 + f3) * 100

#-------------------------------------------#
    def draw(self, subset, context):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        print 'called first'
        return [self.decode(ind) for ind in subset]

#-------------------------------------------#
    def decodeTree(self, tree):
        '''
        Decode bit string.
        '''
        if tree is None:
            return
        else:
            self.decodeNode(tree)
            self.decodeTree(tree.left)
            self.decodeTree(tree.right)

#-------------------------------------------#
    def decodeNode(self, ind):
        '''
        Decode bit string.
        '''
        chrom = ind.genome
        bits = 0
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

        ind.decoded_chrom = data.copy()

#-------------------------------------------#
    def decode(self, ind):
        '''
        Decode bit string.
        '''
        root = ind.genome
        all_bits = []
        getTreeBits(root, all_bits)
        #print len(all_bits),len(all_bits[0])

        bit_chrome = []
        for sub_list in all_bits:
            bit_chrome.extend(sub_list)
        ind.bit_chrome = bit_chrome


        self.decodeTree(root)
        ind.decoded_data = root

        return root

#-------------------------------------------#
    def report(self, pop, subset, gen):
        '''
        '''
        print 'gen', gen

#-------------------------------------------#

