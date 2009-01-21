def simple_mut(random, prob, chrom):
    for i in xrange(len(chrom)):
        if random.random() < prob:
            chrom[i] ^= 1

def mutation(ind, prob, params, random):
    tree = ind.genome['tree']

    # tree operators
    for branch in tree.branch:
        for shape in branch:
            shape.mut(prob)


    #transf = ind.genome['transf']

    ## mutate x
    #scale = tree[i][j][2]
    #simple_mut(random, prob, scale)

    ## mutate y
    #scale = tree[i][j][3]
    #simple_mut(random, prob, scale)

    ## mutate shape
    #if random.random() < prob:
    #    tree[i][j][4] = tree[i][j][4] + random.randrange(1, 4) % 3 + 1

    if random.random() < prob:
        # operator 5 - add random shape
        tree.addNode()

    if random.random() < prob:
        # operator 4 - delete random shape
        tree.deleteNode()


    if random.random() < prob:
        # operator 3 - clone an existing shape and add to another branch
        tree.cloneNode()


    # mutate color
    color = ind.genome['color']
    simple_mut(random, prob, color)
