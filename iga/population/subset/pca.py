import mdp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot
import pylab
from scipy.cluster.vq import *
from scipy import array

NUM_CLUSTERS = 9

def subset(pop, rand, size):
    newpop = pop[:]

    genomes = array([array(map(float, x.genome)) for x in newpop])
    print genomes.ndim
    pcanode = mdp.nodes.PCANode(output_dim = 2, svd = True)

    pcanode.train(genomes)
    pcanode.stop_training()
    data = pcanode.execute(genomes)

    x_values = data[:, 0]
    y_values = data[:, 1]
    pyplot.scatter(x_values, y_values)
    pylab.savefig('myfig.png')
    pyplot.clf()

    w = whiten(data)
    # do k-means clustering using NUM_CLUSTERS random initial points
    # as the centroids
    # 'matrix' option does not work, gives exception
    # 'random' option does not work, it can generate empty clusters
    res, idx = kmeans2(w, NUM_CLUSTERS, minit = 'points')

    color_tuples = [(0,0,0), (1,0,0), (0,1,0), (0,0,1), (1,1,0), (0,1,1), (1,0,1), (.5,.8,.2), (.9,.2,.5)]
    cs = [color_tuples[i] for i in idx]

    print 'idx', idx
    subset_idx = []
    subset_index = []
    i = 0
    while len(subset_idx) < NUM_CLUSTERS:
        if idx[i] not in subset_idx:
            subset_idx.append(idx[i])
            subset_index.append(i)
        i += 1
        

    print subset_idx, subset_index

    subset = [newpop[i] for i in subset_index]
    newindex = [pop.index(ind) for ind in subset]
        

    pyplot.scatter(x_values, y_values, color=cs)
    pylab.savefig('myfig2.png')

    #newpop.sort(key = lambda a: a.fitness)
    #print 'newpop end ', newpop[-1].fitness, 'newpop begin', newpop[0].fitness
    #subset = newpop[-size:]
    #newindex = []
    #for ind in subset:
    #    newindex.append(pop.index(ind))

    return subset, newindex
