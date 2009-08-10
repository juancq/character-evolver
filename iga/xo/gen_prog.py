import copy

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

                
def crossover(p1, p2, prob, params, random):

    if random.random() < prob:
        
        child1, child2 = p1.tree + p2.tree

        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        c1.tree = child1
        c2.tree = child2

        c1.from_p1 = 0.5
        c2.from_p1 = 0.5

        c1.from_p2 = 1. - c1.from_p1
        c2.from_p2 = 1. - c2.from_p1

    else:
        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)

    return (c1, c2)
