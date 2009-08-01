import app.app as app
from app.helperfuncs import hamming, lcs
from iga.individual import Individual

from treenode import TreeNode

GEN_COUNTER = 0

#-------------------------------------------#
class TreeIndividual(Individual):
    def __init__(self, random, genome_len, genome):

        Individual.__init__(self, random, genome_len, genome)


#-------------------------------------------#
class Vertex_shader(app.Application):
    def __init__(self, params, random):
        app.Application.__init__(self, params, random)

        #self.geomNodes = params['init_context']['geomNodes']
        #self.geneLen *= self.geomNodes
        print '^'*30
        print self.attr
        self.geomNodes = params['init_context']['geomNodes']
        print self.geomNodes, self.geneLen
        #self.geneLen *= self.geomNodes
        #print self.geneLen

#-------------------------------------------#
    def createPop(self, popsize):        
        '''
        Need to create trees here.
        '''
        from prog_node import MyProg
        pop = []
        for i in range(popsize):
            tree = MyProg()
            genome = tree.dump_operands()
            ind = Individual(self.random, 0, genome)
            ind.decoded = tree.dump()
            ind.tree = tree
            pop.append(ind)

        return pop

        #pop = []
        #for i in range(popsize):
        #    depth = 2
        #    root = TreeNode()
        #    root.setRoot()
        #    createTree(depth, root)
        #    counter = 0
        #    #printTree(counter, root)
        #    initTree(root, self.geneLen, self.random)

        #    ind = Individual(self.random, length = 0, genome = root)
        #    self.decode(ind)
        #    pop.append(ind)

        #return pop

#-------------------------------------------#
    def fitness(self, ind, user_feedback):
        '''
        Compute fitness.
        user_feedback is a list of the user's input,
        the list contents are ordered the same as the 
        feedback variable in the config yaml file.
        [best]
        '''
        best = user_feedback[0]
        if self.clear:
            self.decode(best)
            self.clear = False

        self.decode(ind)
        min_len = min(len(ind.genome), len(best.genome))

        ind_genome = ind.genome
        best_genome = best.genome

        #print ind_genome, ind_genome[0]

        fit = 0.
        done = {}
        for i in range(min_len):
            if ind_genome[i] in best_genome[i]:
                if not done.get(ind_genome[i], False):
                    ind_c = ind_genome.count(ind_genome[i])
                    best_c = best_genome.count(best_genome[i])
                    if ind_c == best_c:
                        fit += ind_c
                    else:
                        fit += abs(ind_c - best_c)
                    done[ind_genome[i]] = True

                
        ind.fitness = fit
        print 'fitness ', fit

        if len(ind_genome) > 10:
            ind.fitness *= 0.5

#-------------------------------------------#
    def draw(self, subset, context):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        global GEN_COUNTER
        gen = GEN_COUNTER

        material = open('gen_%d.material' % gen, 'w')
        program = open('gen_%d.program' % gen, 'w')
        cg = open('gen_%d.cg' % gen, 'w')

        mbody_open = '{\n\ttechnique\n{\n\tpass\n{\n\t'
        mbody_close = '''
        {
                param_named_auto        time            costime_0_2pi 2
                param_named             factor          float 10
        }
        }\n}\n}
'''

        pbody_close = '''profiles vs_1_1 arbvp1
    default_params
    {
        param_named_auto worldViewProj WORLDVIEWPROJ_MATRIX
    }
}\n\n'''


        cg_open = '''in float4  position        : POSITION,
                in float3 normal        : NORMAL,
                out float4 oPosition    : POSITION,
                out float4 oColor       : COLOR,
                uniform float4x4 worldViewProj,
                uniform float time,
                uniform float factor
                )
{
    float4 p = position;
'''
        cg_close = '''
    oPosition = mul(worldViewProj, p);
    oColor.rgb = 0.5*normal+0.5;
    oColor.a = 1.0;
}\n
'''

        #for i,ind in enumerate(subset):
        for i,ind in enumerate(subset):
            mname = 'gen_%d_ind_%d' % (gen, i)
            material.write('material %s\n' % mname)
            material.write(mbody_open)
            material.write('vertex_program_ref %s' % mname)
            material.write(mbody_close + '\n')

            program.write('vertex_program %s cg\n' %  mname)
            program.write('{\n\tsource gen_%d.cg\n' % gen)
            program.write('entry_point ind_%d_vp\n' % i)
            program.write(pbody_close)


            cg.write('void ind_%d_vp(' % i)
            cg.write(cg_open)
            print '%s += %s + cos(time);' % (ind.tree.eq_picked, ind.decoded)

            cg.write('%s += %s + cos(time);' % (ind.tree.eq_picked, ind.decoded))
            #cg.write('p.xyz += %s + cos(time);' % ind.decoded)
            #cg.write('p.x += 8*sin(%d*9+time+factor*p.y);' % i)
            #cg.write('p.y -= 2*cos(%d*9+time+factor);' % i)
            #cg.write('p.z += 2*tan(%d*9+time+factor);' % i)
            cg.write(cg_close)


        material.close()
        program.close()
        cg.close()


        GEN_COUNTER += 1

        return [i for i in range(len(subset))]
        #return [self.decode(ind) for ind in subset]


#-------------------------------------------#
    def decode(self, ind):
        '''
        Decode bit string.
        '''
        ind.decoded = ind.tree.dump()
        ind.genome = ind.tree.dump_operands()

        return

#-------------------------------------------#
    def report(self, pop, subset, gen):
        '''
        '''
        print 'gen', gen

#-------------------------------------------#

