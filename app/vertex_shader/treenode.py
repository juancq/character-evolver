COUNTER = 0
import random


b_count = 0

class TreeNode:
    def __init__(self, left = None, right = None, depth = 0):

        global COUNTER
        self.id = COUNTER
        COUNTER += 1

        self.left = left
        self.right = right
        self.depth = depth

        self.genome = None
        self.bit_chrome = []

        self.isroot = False
        self.num_children = 0

#-------------------------------------------------#
    def mutation(self, prob, random):
        genome = self.genome
        for i in range(len(genome)):
            if random.random() < prob:
                genome[i] = genome[i] ^ 1

#-------------------------------------------------#
    def mut(self, prob, random):
        '''
        Mutate attributes of nodes.
        '''
        self.mutation(prob, random)
        self.mutNodes(self.left, prob, random)
        self.mutNodes(self.right, prob, random)


#-------------------------------------------------#
    def mutNodes(self, tree, prob, random):
        '''
        Mutate attributes of nodes.
        '''
        if tree is None:
            return
        else:
            tree.mutation(prob, random)
            self.mutNodes(tree.left, prob, random)
            self.mutNodes(tree.right, prob, random)


#-------------------------------------------------#
    def countChildren(self):
        '''
        Counts number of nodes in tree.
        '''
        self.num_children = 0
        self.iterTree(self.left)
        self.iterTree(self.right)

        return self.num_children


#-------------------------------------------------#
    def getBranch(self, node_index):
        self.branch_count = 0
        branch = self.getRecBranch(self.left, node_index)
        if not branch: 
            branch = self.getRecBranch(self.right, node_index)
        return branch

#-------------------------------------------------#
    def getRecBranch(self, tree, node_index):
        if tree is None:
            return None
        else:
            self.branch_count += 1
            if self.branch_count == node_index:
                return tree
            else:
                branch = self.getRecBranch(tree.left, node_index)
                if not branch: 
                    branch = self.getRecBranch(tree.right, node_index)
                return branch

#-------------------------------------------------#
    def insertBranch(self, node_index, branch):
        global b_count
        b_count = 0
        done = insertRecBranch(self.left, node_index, branch)
        print 'b_count', b_count
        if not done: 
            insertRecBranch(self.right, node_index, branch)

#-------------------------------------------------#
    def __insertRecBranch(self, tree, node_index, branch):
        if tree is None:
            return False
        else:
            self.branch_count += 1
            if self.branch_count == node_index:
                tree = branch
                tree = 'akfjda;kljfda;klfdjad'
                return True
            else:
                done = self.insertRecBranch(tree.left, node_index, branch)
                if not done: 
                    self.insertRecBranch(tree.right, node_index, branch)
                return True


#-------------------------------------------------#
    def iterTree(self, tree):
        if tree is None:
            return
        else:
            self.num_children += 1
            self.iterTree(tree.left)
            self.iterTree(tree.right)


#-------------------------------------------------#
    def getNumChildren(self):
        return self.num_children

#-------------------------------------------------#
    def isRoot(self):
        return self.isroot

#-------------------------------------------------#
    def setRoot(self):
        self.isroot = True

#-------------------------------------------------#
    def getGenome(self):
        return self.genome

#-------------------------------------------------#
    def init(self, genome_len, rand):
        self.genome = [rand.randint(0,1) for i in range(int(genome_len))]

#-------------------------------------------------#
    def isLeaf(self):
        return self.left is None and self.right is None

#-------------------------------------------------#
    def stats(self):
        self.num_children = 0
        self.depth = 0

        d = 0
        d1, c1 = self.recStats(self.left, d)
        d2, c2 = self.recStats(self.right, d)
        self.depth = max(d1, d2)
        self.num_children = c1+c2
        #print 'stats', self.depth, self.num_children

#-------------------------------------------------#
    def recStats(self, tree, depth):
        if tree is None:
            return 0, 0
        elif tree.left is None and tree.right is None:
            return depth+1, 1
        else:
            d1, c1 = self.recStats(tree.left, depth+1)
            d2, c2 = self.recStats(tree.right, depth+1)
            return max(d1,d2), c1+c2+1

#-------------------------------------------------#
    def printTree(self):
        print '-'*10
        print self.id
        if self.left:
            print 'Left:'
            self.left.printTree()
        if self.right:
            print 'Right:'
            self.right.printTree()
        

#-------------------------------------------------#

def iterate(tree, c, d):

    if tree is None:
        return
    else:
        
        if tree.left:
            c = iterate(tree, c+1)



#-------------------------------------------------#
def insertRecBranch(tree, node_index, branch):
    if tree is None:
        return False
    else:
        global b_count
        b_count += 1
        if b_count == node_index:
            #tree = branch
            tree.genome = branch.genome
            tree.left = branch.left
            tree.right = branch.right
            #print 'inserting at', tree.id, 'from: ', branch.id
            return True
        else:
            done = insertRecBranch(tree.left, node_index, branch)
            if not done: 
                return insertRecBranch(tree.right, node_index, branch)

