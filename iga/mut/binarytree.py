def mutation(ind, prob, params, random):

    tree = ind.genome
    tree.mut(prob, random)

    return
