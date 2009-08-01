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
        
        c1_tree = copy.deepcopy(p1.genome)
        c2_tree = copy.deepcopy(p2.genome)


        c1_count = c1_tree.countChildren()
        c2_count = c2_tree.countChildren()
        # get xo node points in trees
        c1_xo_node = random.randint(1, c1_count)
        c2_xo_node = random.randint(1, c2_count)

        #print 'random nums', c1_xo_node, c2_xo_node


        #d = 0
        #printTree(d, c1_tree)
        #printTree(d, c2_tree)

        
        branch1 = c1_tree.getBranch(c1_xo_node)
        branch2 = c2_tree.getBranch(c2_xo_node)

        #print 'branches'
        #printTree(d, branch1)
        #printTree(d, branch2)

        b1 = copy.deepcopy(branch1)
        b2 = copy.deepcopy(branch2)
        c1_tree.insertBranch(c1_xo_node, b2)
        c2_tree.insertBranch(c2_xo_node, b1)

        #printTree(d, c1_tree)
        #printTree(d, c2_tree)

        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        c1.genome = c1_tree
        c2.genome = c2_tree

        #print 'children', c1.genome.countChildren(), c2.genome.countChildren()

    else:
        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)

    return (c1, c2)
