import copy

def crossover(p1, p2, prob, params, random, extra_params):

    if random.random() < prob:
        
        ops = extra_params['operators']
        c1Genome = copy.deepcopy(p1.genome['tree'])
        c2Genome = copy.deepcopy(p2.genome['tree'])

        ops_applied = [0] * 5

        i = 0
        if random.random() < ops[i]:
            # operator 5 - add random shape
            c1Genome.addNode()
            c2Genome.addNode()
            ops_applied[i] = 1

        i += 1
        if random.random() < ops[i]:
            # operator 4 - delete random shape
            c1Genome.deleteNode()
            c2Genome.deleteNode()
            ops_applied[i] = 1


        i += 1
        if random.random() < ops[i]:
            # operator 3 - clone an existing shape and add to another branch
            c1Genome.cloneNode()
            c2Genome.cloneNode()
            ops_applied[i] = 1


        i += 1
        if random.random() < ops[0]:
            # quad tree, so pick between 0 and 4
            b1, b2 = random.sample(range(0, 4), 2)
            
            branch1 = c1Genome.branch[b1][:]
            branch2 = c2Genome.branch[b2][:]
            c1Genome.branch[b1] = branch2
            c2Genome.branch[b2] = branch1
            # operator 2
            c1Genome.rearrange()
            c2Genome.rearrange()
            ops_applied[0] = 1

        else:
            b1, b2 = random.sample(range(0, 4), 2)
            
            branch1 = c1Genome.branch[b1][:]
            branch2 = c2Genome.branch[b2][:]
            # operator 1
            b1_centers = [j.getCenter() for j in branch1]
            b2_centers = [j.getCenter() for j in branch2]
            c1Genome.quadrantSwap(b1, b1_centers)
            c2Genome.quadrantSwap(b2, b2_centers)
            #print 'centers', b1_centers, b2_centers
            ops_applied[1] = 1



        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        c1.genome['tree'] = c1Genome
        c2.genome['tree'] = c2Genome
        c1.operators = ops_applied[:]
        c2.operators = ops_applied[:]

    else:
        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)

    return (c1, c2)

#        c1Genome = copy.deepcopy(p1.genome['tree'])
#        c2Genome = copy.deepcopy(p2.genome['tree'])
#
#        ops = gaParams.getVar('operators')
#
#        ops_applied = [0] * 5
#
#        i = 0
#        if random.random() < ops[i]:
#            # operator 5 - add random shape
#            c1Genome.addNode()
#            c2Genome.addNode()
#            ops_applied[i] = 1
#
#        i += 1
#        if random.random() < ops[i]:
#            # operator 4 - delete random shape
#            c1Genome.deleteNode()
#            c2Genome.deleteNode()
#            ops_applied[i] = 1
#
#
#        i += 1
#        if random.random() < ops[i]:
#            # operator 3 - clone an existing shape and add to another branch
#            c1Genome.cloneNode()
#            c2Genome.cloneNode()
#            ops_applied[i] = 1
#
#
#        i += 1
#        if random.random() < ops[i]:
#            # quad tree, so pick between 0 and 4
#            b1, b2 = random.sample(range(0, 4), 2)
#            
#            branch1 = c1Genome.branch[b1][:]
#            branch2 = c2Genome.branch[b2][:]
#            c1Genome.branch[b1] = branch2
#            c2Genome.branch[b2] = branch1
#            # operator 2
#            c1Genome.rearrange()
#            c2Genome.rearrange()
#            ops_applied[i] = 1
#
#        i += 1
#        if random.random() < ops[i]:
#            b1, b2 = random.sample(range(0, 4), 2)
#            
#            branch1 = c1Genome.branch[b1][:]
#            branch2 = c2Genome.branch[b2][:]
#            # operator 1
#            b1_centers = [j.getCenter() for j in branch1]
#            b2_centers = [j.getCenter() for j in branch2]
#            c1Genome.quadrantSwap(b1, b1_centers)
#            c2Genome.quadrantSwap(b2, b2_centers)
#            #print 'centers', b1_centers, b2_centers
#            ops_applied[i] = 1
#
#
#
#        c1 = copy.deepcopy(p1)
#        c2 = copy.deepcopy(p2)
#        c1.genome['tree'] = c1Genome
#        c2.genome['tree'] = c2Genome
#        c1.operators = ops_applied[:]
#        c2.operators = ops_applied[:]
#
#    else:
#        c1 = copy.deepcopy(p1)
#        c2 = copy.deepcopy(p2)
#
