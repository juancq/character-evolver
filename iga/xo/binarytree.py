import copy
                
def crossover(p1, p2, prob, params, random):

    if random.random() < prob:
        
        c1_tree = copy.deepcopy(p1.genome)
        c2_tree = copy.deepcopy(p2.genome)

        c1_count = c1_tree.countChildren()
        c2_count = c2_tree.countChildren()
        # get xo node points in trees
        c1_xo_node = random.randint(2, c1_count)
        c2_xo_node = random.randint(2, c2_count)
        
        branch1 = c1_tree.getBranch(c1_xo_node)
        branch2 = c2_tree.getBranch(c2_xo_node)

        c1_tree.insertBranch(c1_xo_node, branch2)
        c2_tree.insertBranch(c2_xo_node, branch1)

        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        c1.genome = c1_tree
        c2.genome = c2_tree

    else:
        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)

    return (c1, c2)
