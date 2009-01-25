COUNTER = 0
import random

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
                branch = self.getRecBranch(self.left, node_index)
                if not branch: 
                    branch = self.getRecBranch(self.right, node_index)
                return branch

#-------------------------------------------------#
    def insertBranch(self, node_index, branch):
        self.branch_count = 0
        done = self.insertRecBranch(self.left, node_index, branch)
        if not done: 
            self.insertRecBranch(self.right, node_index, branch)

#-------------------------------------------------#
    def insertRecBranch(self, tree, node_index, branch):
        if tree is None:
            return False
        else:
            self.branch_count += 1
            if self.branch_count == node_index:
                tree = branch
                return True
            else:
                done = self.insertRecBranch(self.left, node_index, branch)
                if not done: 
                    self.insertRecBranch(self.right, node_index, branch)
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
