COUNTER = 0

class TreeNode:
    def __init__(self, genome, left = None, right = None, depth = 0):

        global COUNTER
        self.id = COUNTER
        COUNTER += 1

        self.left = left
        self.right = right
        self.depth = depth

        #self.genome = [random.randint(0,1) for i in xrange(0, int(length))]


    def isLeaf(self):
        return self.left is None and self.right is None
