def cmpInd(ind1, ind2):
    #if ind1.decoded_plan == ind2.decoded_plan:
    #if ind1.roomlist == ind2.roomlist:
    total = 0
    if ind1.decoded_plan == ind2.decoded_plan:
        total += 1
    if ind1.numRoom == ind2.numRoom:
        total += 1
    if ind1.roomarea == ind2.roomarea:
        total += 1
    if ind1.roomlist == ind2.roomlist:
        total += 1
    if ind1.roomDesc == ind2.roomDesc:
        total += 1
    if ind1.roomSizes == ind2.roomSizes:
        total += 1

    if total == 6:
        return True

    return False

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
    done = False
    new_size = min(size, len(newpop))
    print 'enter ', '-'*10
    while len(subset) < new_size:
        if front_index[i] < len(fronts[i]):
            # determine how many to insert from front
            #toinsert = min(3, len(fronts[i]))
            #toinsert = min(toinsert, size - len(subset))

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
                print 'here here'

            front_index[i] += toinsert

        else:
            # needed for very small populations, otherwise you get stuck in an 
            # infinite loop
            skip_thresh += 1
            if skip_thresh > 10:
                break


        i = (i+1) % front_len

    print 'subset ', len(subset)
    newindex = [pop.index(ind) for ind in subset]

    for ind in subset:
        todel = newpop.index(ind)
        del newpop[todel]


    to_del = set()
    new_len = len(newpop)
    for i in xrange(new_len-1):
        for j in xrange(i+1, new_len):
            if newpop[i].isequal(newpop[j]):
                to_del.add(j)

    to_del = list(to_del)
    for i in xrange(len(to_del)):
        del newpop[to_del[i]-i]

    print 'new len ', len(newpop)
    return subset[:size]+newpop, newindex
