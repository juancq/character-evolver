import math
def subset(pop, rand, size):
    newpop = pop[:]
    newpop.sort()
    print 'newpop end ', newpop[-1].fitness, 'newpop begin', newpop[0].fitness
    best_size = int(math.floor(size/2.))
    subset = newpop[-best_size:]
    newindex = []
    for ind in subset:
        newindex.append(pop.index(ind))

    rand_size = int(math.ceil(size/2.))

    for i in range(rand_size):
        r_index = rand.randrange(size-best_size)
        subset.append(newpop[r_index])
        newindex.append(pop.index(subset[-1]))


    return subset, newindex
