def mutation(ind, prob, params, random):

    tree = ind.tree
    ind.tree = tree.mutate()

    return
