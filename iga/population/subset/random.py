def subset(pop, rand, size):
    subset = rand.sample(pop, size)
    newindex = [pop.index(ind) for ind in subset]
    return subset, newindex
