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


    def getGenome(self):
        return self.genome

    def init(self, genome_len, rand):
        self.genome = [rand.randint(0,1) for i in range(int(genome_len))]

    def isLeaf(self):
        return self.left is None and self.right is None
