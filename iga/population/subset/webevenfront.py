
# ------------------------------ #
def getDups1(_ind_list):
    dups = []
    # remove duplicates from inds to be inserted to subset
    len_ind_list = len(_ind_list)
    for j in xrange(0, len_ind_list-1):
        for k in xrange(j+1, len_ind_list):
            if _ind_list[j].isequal(_ind_list[k]):
                dups.append(k)
                if len(dups) == len_ind_list-1:
                    return {}.fromkeys(dups).keys()
    return {}.fromkeys(dups).keys()

# ------------------------------ #
def getDups2(_ind_list, _subset):
    dups = []
    len_ind_list = len(_ind_list)
    len_subset = len(_subset)
    # remove duplicates from subset
    for j in xrange(0, len_ind_list):
        for k in xrange(0, len_subset):
            if _ind_list[j].isequal(_subset[k]):
                dups.append(j)
                if len(dups) == len_ind_list:
                    return {}.fromkeys(dups).keys()
    return {}.fromkeys(dups).keys()

# ------------------------------ #
def subset(pop, rand, size):
    newpop = pop[:]
    newpop.sort(lambda a,b: cmp(a.rank, b.rank))
    fronts = []
    ranks = []
    for ind in newpop:
        if ind.rank in ranks:
            fronts[ranks.index(ind.rank)].append(ind)
        else:
            ranks.append(ind.rank)
            fronts.append([ind])

    subset = []
    front_len = len(fronts)
    front_index = [0] * front_len

    skip_thresh = 0
    dups_check = 0
    i = 0
    new_size = min(size, len(newpop))
    while len(subset) < new_size:
        if front_index[i] < len(fronts[i]):
            # determine how many to insert from front
            toinsert = min(len(fronts[i]), size - len(subset))
            ind_list = fronts[i][front_index[i] : front_index[i]+toinsert]

            if dups_check < size:


                if len(ind_list) > 1:
                    # remove duplicates from individuals to be added to subset
                    dups = getDups1(ind_list)
                    for j in xrange(len(dups)):
                        del ind_list[dups[j]-j]


                # compare inds to be inserted with inds already in subset, remove duplicates
                dups = getDups2(ind_list, subset)
                if not (len(dups) == len(ind_list)):
                    for j in xrange(len(dups)):
                        del ind_list[dups[j]-j]

                    subset.extend(ind_list)

                else:
                    # if we go (subset size) number of times without inserting
                    # a unique individual, then just insert even if they're not unique
                    dups_check += 1

            else:
                subset.extend(ind_list)

            front_index[i] += toinsert

        # if we are not able to pull anymore unique individuals (because of pop size)
        # just get a random sample to fill the rest of subset
        else:
            skip_thresh += 1
            if skip_thresh > 20:
                break

        i = (i+1) % front_len


    if len(subset) < size:
        subset.extend(rand.sample(newpop, size-len(subset)))

    print 'size is ', size, subset
    newindex = [pop.index(ind) for ind in subset]

    return subset, newindex
