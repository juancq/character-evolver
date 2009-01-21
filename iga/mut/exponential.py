from math import log

def mutation(ind, prob, params, random):
    for i in xrange(0, len(ind.genome)):
        if random.random() < prob:
            v = -log(random.random()) / params['lambda']
            if random.random() < 0.5:
                v = -v
            ind.genome[i] += v
