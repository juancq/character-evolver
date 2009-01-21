# ------------------------------ #
def subset(pop, rand, size):
    newpop = pop[:]
    newpop.sort(lambda a,b: cmp(a.rank, b.rank))

    for ind in newpop:
        print ind.rank

    subset = newpop[:size]
    newindex = [pop.index(ind) for ind in subset]

    return subset+newpop[size:], newindex
