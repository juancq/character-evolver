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
        #print '^'*30
        #print self.attr
        self.geomNodes = params['init_context']['geomNodes']
        #print self.geomNodes, self.geneLen
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
        self.decode(best)

        #if self.clear:
        #    self.decode(best)
        #    self.clear = False

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

        if ind.genome == best.genome:
            ind.fitness *= 2
            print '^%^'*10
        #elif len(ind_genome) > 10:
        #    ind.fitness *= 0.5

#-------------------------------------------#
    def draw(self, subset, context):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        prefix = '%s_' % context['user']
        global GEN_COUNTER
        if context.has_key('peer_genomes'):
            prefix += 'peer_gen'
            GEN_COUNTER -= 1
        else:
            prefix += 'gen'

        gen = GEN_COUNTER

        material = open('%s_%d.material' % (prefix, gen), 'w')
        program = open('%s_%d.program' % (prefix, gen), 'w')
        cg = open('%s_%d.cg' % (prefix, gen), 'w')

        mbody_open = '{\n\ttechnique\n{\n\tpass\n{\n\t'
        mbody_close = '''
        {
                param_named_auto        time            costime_0_2pi 2
                param_named             factor          float 10
                param_named_auto lightPos[0] light_position 0
                param_named_auto lightPos[1] light_position 1
                param_named_auto lightDiffuseColour[0] light_diffuse_colour 0
                param_named_auto lightDiffuseColour[1] light_diffuse_colour 1
                param_named_auto ambient ambient_light_colour
        }

        texture_unit
        {
            texture nskingr.jpg
            //texture r2skin.jpg
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
                in float2 uv       : TEXCOORD0,
                out float4 oPosition    : POSITION,
                out float4 oColor       : COLOR,
                out float2 oUv       : TEXCOORD0,
                uniform float4x4 worldViewProj,
                uniform float time,
                uniform float factor,
                uniform float4   lightPos[2],
                uniform float4   lightDiffuseColour[2],
                uniform float4   ambient
                )
{
    float4 p = position;
'''
        cg_close = '''


    oPosition = mul(worldViewProj, p);

    //oColor.rgb = 0.5*normal+0.5;
    //oColor.a = 1.0;

    // transform normal
    //float3 norm = mul(worldViewProj, normal);
    float3 norm = normal;
    // Lighting - support point and directional
    float3 lightDir0 = 	normalize(
            lightPos[0].xyz -  (p.xyz * lightPos[0].w));
    float3 lightDir1 = 	normalize(
            lightPos[1].xyz -  (p.xyz * lightPos[1].w));

    oUv = uv;
    oColor = ambient + 
            (saturate(dot(lightDir0, norm)) * lightDiffuseColour[0]) + 
            (saturate(dot(lightDir1, norm)) * lightDiffuseColour[1]);
    
}\n
'''

        #for i,ind in enumerate(subset):
        for i,ind in enumerate(subset):
            mname = '%s_%d_ind_%d' % (prefix, gen, i)
            material.write('material %s\n' % mname)
            material.write(mbody_open)
            material.write('vertex_program_ref %s' % mname)
            material.write(mbody_close + '\n')

            program.write('vertex_program %s cg\n' %  mname)
            program.write('{\n\tsource %s_%d.cg\n' % (prefix, gen))
            program.write('entry_point ind_%d_vp\n' % i)
            program.write(pbody_close)


            cg.write('void ind_%d_vp(' % i)
            cg.write(cg_open)
            #print '%s += %s + cos(time);' % (ind.tree.eq_picked, ind.decoded)

            for eq in ind.tree.eq_picked:
                cg.write('%s += %s;' % (eq, ind.decoded))

            #cg.write('%s += %s;' % (ind.tree.eq_picked, ind.decoded))

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

