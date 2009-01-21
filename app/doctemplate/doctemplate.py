from docplanind import DocplanIndividual
import parseTree, decodePlan
import webdocpanel as docpanel
import igap.app.app as app

import roomClassifier, sharedWalls
from copy import deepcopy
from shape import ShapeObject
from tree import Tree
import pickle
from wx import App as wxApp


#-------------------------------------------#
class Doctemplate(app.Application):
    def __init__(self, params, random):
        app.Application.__init__(self, params, random)

        import time
        ltime = time.localtime()
        self.hour, self.min = ltime[3], ltime[4]
        #self.fout = open('data/%s_pop_%d-%d' % (params['name'], hour, min), 'w')
        #self.fout.write('gen\tobj\tsubj\t\ttop obj\ttop subj\tc1\tc2\tc3\tc4\tc5\n')


        # parse file with color schemes
        f = open('igap/app/doctemplate/color_schemes')
        data = f.readlines()
        f.close()

        color_key = {}
        colors = []
        # each scheme has 4 colors
        # each color is stored in columns, hence awkard reading from file
        for i in xrange(0, len(data), 4):
            name = data[i].strip()
            new_color = [[], [], [], []]
            for j in xrange(3):
                nums = map(int, data[i+j+1].split()[1:])
                for k in xrange(4):
                    new_color[k].append(nums[k])
            colors.append(new_color)
            color_key[name] = new_color

        self.colors = colors
        self.color_key = color_key
        self.global_color = None

        self.best_saved = None
        self.total_area = self.params['plotSizeX'] * self.params['plotSizeY']
        self.area_threshold = self.total_area * self.params['hide_threshold']

#-------------------------------------------#
    def createPop(self, popsize):        
        
        params = self.params
        random = self.random
        import createInd, math

        pop = []
        color_len = int(math.ceil(math.log(len(self.colors), 2)))
        self.scale_len = int(math.ceil(math.log(params['num_scale'], 2)))

        for i in xrange(popsize):
            tree_genome = createInd.createIndividual(random, params['maxDepth'], params['maxRoom'], params['minRoom'])
            color_genome = [random.randint(0, 1) for i in xrange(color_len)]
            new_ind = DocplanIndividual(random, None, genome={'tree': tree_genome, 'color': color_genome})
            self.initDecode(new_ind)
                
            # evaluate this new individual based on obj criteria only
            #self.fitness(new_ind, None)
            #new_ind.rank = new_ind.fitness

            new_ind.rank = new_ind.fitness = self.obj_fitness(new_ind, None)

            pop.append(new_ind)
        
        # sort population by obj score, and set rank proportional to fitness
        #pop.sort(lambda a, b: cmp(a.fitness, b.fitness))
        #for i in xrange(len(pop)): pop[i].rank = i

        return pop
    
#-------------------------------------------#
    def initDecode(self, ind):
        '''
        '''
        # decode tree chromosome
        room_list = parseTree.parseTree(ind.genome['tree'], self.params['plotSizeX'], self.params['plotSizeY'])

        tree, shape_list = self.getQuadTree(room_list['sizes'], room_list['desc'])
        ind.genome['tree'] = tree
        ind.shape_list = self.purgeShapeList(shape_list)

        plan = self.initNewDecode(tree)

        ind.decoded_plan = plan
        ind.numRoom = plan[0]
        ind.roomarea = plan[1]
        ind.roomlist = plan[2]
        ind.roomDesc = plan[3]
        ind.roomSizes = plan[4]

        # 2nd chromosome
        # decode color chromosome
        chrom = ind.genome['color']
        temp = 0
        len_chrom = len(chrom)
        for i in xrange(len_chrom):
            if chrom[i]:
                temp += 2**(len_chrom-i-1)
        ind.color = self.colors[temp]
    
#-------------------------------------------#
    def decodePlan(self, ind):
        '''
        '''
        # tree decoding
        tree = ind.genome['tree']
        self.newDecode(tree)

        shape_list = ind.shape_list
        shape_list = self.updateShapeList(tree)

        # prune shape list of really small shapes
        # but leave genome tree unchanged
        # draw shapes which are bigger than a threshold
        ind.shape_list = self.purgeShapeList(shape_list)

        # 2nd chromosome
        # decode color chromosome
        if self.global_color:
            ind.color = self.global_color
        else:
            chrom = ind.genome['color']
            temp = 0
            len_chrom = len(chrom)
            for i in xrange(len_chrom):
                if chrom[i]:
                    temp += 2**(len_chrom-i-1)
            ind.color = self.colors[temp]

#-------------------------------------------#
    def purgeShapeList(self, shape_list):
        a_thresh = self.area_threshold
        return filter(lambda s: s.getArea() >= a_thresh, shape_list)

#-------------------------------------------#
    def newDecode(self, tree):
        max_s = self.params['max_scale']
        min_s = self.params['min_scale']

        [i.computePos(max_s, min_s) for b in tree.branch for i in b]

        #for branch in tree.branch:
        #    for ind in branch:
        #        ind.computePos(max_val, min_val)

#-------------------------------------------#
    def initNewDecode(self, tree):
        room_class = []
        room_area = []
        room_sizes = []
        max_val = self.params['max_scale']
        min_val = self.params['min_scale']

        for branch in tree.branch:
            for ind in branch:
                ind.computePos(max_val, min_val)
                room_area.append(ind.getArea())
                room_class.extend([ind.w, ind.l])
                room_sizes.append(list(ind.getPos()))

        room_desc = ['R'] * len(room_area)
        revisedArea = room_area[:]
        revisedArea.sort()

        # call the room-classification routine
        room_desc, num_room = roomClassifier.f1(room_desc, room_sizes,
                                                revisedArea, room_class)

        # call the adjoining-room calculation routine 
        shared_walls = sharedWalls.f1(num_room, room_desc, room_sizes)

        return [num_room, room_area, shared_walls, room_desc, room_sizes]


#-------------------------------------------#
    def callAppSlot(self, slot, args = None):
        if slot == 0:
            self.global_color = args

#-------------------------------------------#
    def updateShapeList(self, tree):
        shape_list = []
        for branch in tree.branch:
            for ind in branch:
                shape_list.append(ind)

        return shape_list

#-------------------------------------------#
    def getQuadTree(self, dimensions, desc):

        max_val = self.params['max_scale']
        min_val = self.params['min_scale']

        coordinates, roomsizes = self.getRoomDesc(dimensions)
        shape_list = self.computeShapeLoc(coordinates, roomsizes, desc, max_val, min_val)

        w, l = self.params['plotSizeX'], self.params['plotSizeY']
        tree = Tree(self.random, w, l, self.scale_len)
        for obj in shape_list:
            cx, cy = obj.getCenter()
            if cx < w/2 and cy < l/2:
                tree.branch[0].append(obj)
            elif cx >= w/2 and cy < l/2:
                tree.branch[1].append(obj)
            elif cx < w/2 and cy >= l/2:
                tree.branch[2].append(obj)
            elif cx >= w/2 and cy >= l/2:
                tree.branch[3].append(obj)


        return tree, shape_list

#-------------------------------------------#
    def getRoomDesc(self, dimensions):
        coordinates = []
        roomsizes = []
        xoffset = 0.0
        yoffset = 0.0

        for i in xrange(0, len(dimensions)):
            coordinates.append(float(dimensions[i][0])+xoffset)
            coordinates.append(float(dimensions[i][1])+yoffset)
            roomsizes.append(float(dimensions[i][2])-float(dimensions[i][0]))
            roomsizes.append(float(dimensions[i][3])-float(dimensions[i][1]))

        return coordinates, roomsizes


#-------------------------------------------#
    def computeShapeLoc(self, coordinates, shape_sizes, desc, max_val, min_val):
        '''
        Compute the coordinates and sizes of all shapes.
        '''
        random = self.random
        num_shapes = self.params['num_shapes']
        shape_list = []
        i = 0
        for j in xrange(len(desc)):

            # if not a blank space
            if desc[j] != 'S':

                shape = random.randrange(1, num_shapes+1)
                shape_obj = ShapeObject(random, shape, coordinates[i], coordinates[i+1], 
                        shape_sizes[i], shape_sizes[i+1], self.scale_len)
                shape_obj.computePos(max_val, min_val)
                shape_list.append(shape_obj)

            i += 2

        return shape_list

#-------------------------------------------#
    def roomDims(self, desc, size):

        dim = []
        for rooms in xrange(len(desc)):
            if desc[rooms] != 'S':
                length = size[rooms][2] - size[rooms][0]
                breadth = size[rooms][3] - size[rooms][1]
                dim.extend([desc[rooms], length, breadth])

        return dim

        

#-------------------------------------------#
    def obj_fitness(self, ind, user_feedback):
        '''
        Compute fitness.
        '''
        shape = shape_list = ind.shape_list
        # if empty list (because it's full of really small useless shapes),
        # then just give it the worst obj fitness (since it's min)
        if not shape:
            return 1.0

        size_x, size_y = self.params['plotSizeX'], self.params['plotSizeY']

        # evaluating white space
        areas = [s.getArea() for s in shape_list]
        # if greater than 1, then lots of shapes with overlap
        # if close to 0, then empty panel
        obj1 = reduce(lambda x, y: x + y, areas, 0.) / self.total_area
        if obj1 > 1.:
            obj1 = 1. - obj1
            if obj1 < 0.: obj1 = 0.

        ## evaluating overlap
        #print 'computing overlap', '-'*20

        len_shape = len(shape_list)
        obj2 = 0.
        for i in xrange(len_shape-1):
            for j in xrange(i+1, len_shape):
                #print 'shape info i', shape[i].Info()
                #print 'shape info j', shape[j].Info()
                if shape[i].right < shape[j].left or shape[i].left > shape[j].right:
                    # no overlap
                    pass
                elif shape[i].bot < shape[j].top or shape[i].top > shape[j].bot:
                    # no overlap
                    pass
                else:
                    l = max(shape[i].left, shape[j].left)
                    r = min(shape[i].right, shape[j].right)
                    t = max(shape[i].top, shape[j].top)
                    b = min(shape[i].bot, shape[j].bot)
                    overlap = (r-l) * (b-t)
                        
                    # overlap is the max percentage of any image area covered
                    # by another image over all of the images
                    temp_obj2 = overlap / min(areas[i], areas[j])
                    obj2 = max(obj2, temp_obj2)

        obj2 = (1. - obj2) * 0.8
        #print 'max overlap is ', obj2

        ## evaluating spatial balance
        l_area = 0.
        r_area = 0.
        t_area = 0.
        b_area = 0.
        mv, mh = size_x/2., size_y/2.
        for i in xrange(len_shape):
            # if shape entirely in left half
            if shape[i].right < mv:
                l_area += areas[i]
            # if shape entirely in right half
            elif shape[i].left > mv:
                r_area += areas[i]

            else:
                # split shape through the plot middle

                # add portion of shape in left to left area
                l = shape[i].left
                r = mv
                length = shape[i].l
                l_area += (r-l) * length

                # add portion of shape in right to right area
                l = mv
                r = shape[i].right
                length = shape[i].l
                r_area += (r-l) * length


            if shape[i].bot < mh:
                t_area += areas[i]
            # if shape entirely in right half
            elif shape[i].top > mh:
                b_area += areas[i]

            else:
                # split shape through the plot middle

                # add portion of shape in top to top area
                t = shape[i].top
                b = mh
                width = shape[i].w
                t_area += width * (b-t)

                # add portion of shape in bottom to bottom area
                t = mh
                b = shape[i].bot
                width = shape[i].w
                b_area += width * (b-t)


        vertical = min(l_area, r_area)/max(l_area, r_area)
        horizontal = min(t_area, b_area)/max(t_area, b_area)
        obj3 = 0.5 * (vertical + horizontal)

        #print 'objs: ', obj1, obj2, obj3
        

        return 1. - ((obj1 + obj2 + obj3) / 3.)

#-------------------------------------------#
    def fitness(self, ind, user_feedback):
        '''
        Compute fitness.
        '''
        best = user_feedback[0]
        if not self.global_color:
            self.global_color = best.color

        self.decodePlan(ind)
        obj_score = self.obj_fitness(ind, user_feedback)

        #ind.fitness = [obj_score, 1.]
        #self.subj_fitness(ind, best)

        ind.fitness = obj_score * 100.
        ind.rank = ind.fitness


#-------------------------------------------#
    def draw(self, subset, context):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        temp_app = wxApp()
        folder = context.get('path', '')
        panels = []
        i = 0
        for ind in subset:
            if ind.shape_list:
                filename = '%s_ind_%d.jpeg' % (folder, i)
                # draw shapes which are bigger than a threshold
                shape_list = deepcopy(ind.shape_list)
                # sort so that smaller shapes are drawn on top of bigger shapes
                shape_list.sort(lambda a, b: -cmp(a.getArea(), b.getArea()))

                doc = docpanel.DocPanel(self.params, individual = ind, 
                        quad_tree = shape_list, color_scheme = ind.color, 
                        name = filename)

                panels.append(filename)
                i += 1

        del temp_app
        return panels


#-------------------------------------------#
    def paramSpace(self, pop, user_selected):
        # Using 5 dimensions, 2 obj and 3 subj
        #best = user_selected[0]
        #objmax = [max(best.numRoom-2, 8-best.numRoom)+1., 5., 1.0, 1.0, 1.0]
        #objmin = [0., 0., 0.0, 0.0, 0.0]

        #self.limits = {'max': objmax, 'min': objmin}

        #return objmax, objmin

#        # Using 2 dimensions, obj and subj
#        best = user_selected[0]
#        tmp_objmax = [max(best.numRoom-2, 8-best.numRoom)+1., 5., 1.0, 1.0, 1.0]
#        #objmax = [tmp_objmax[2]+tmp_objmax[3], tmp_objmax[0]+tmp_objmax[1]+tmp_objmax[4]]
#
#        objmax = [tmp_objmax[2]+tmp_objmax[3], 1.]
#        objmin = [0., 0.]

        objmax = [1., 1.]
        objmin = [0., 0.]

        self.limits = {'max': objmax, 'min': objmin}

        return objmax, objmin


#-------------------------------------------#
    def report(self, pop, subset, gen):
        '''
        Write to console or file
        population statistics.
        '''
        return


        #user = gaParams.getVar('user')
        #app_name = self.params['name']
        #dump_file = 'data/%s_%s_%d_pop_%d_%d.pickle' % (user, app_name, gen, self.hour, self.min)
        #fout = open(dump_file, 'w')
        #pickle.dump(pop, fout)
        #fout.close()

        #return

#-------------------------------------------#
    def close(self):
        return
        #self.fout.close() 

#--------------------------------------------#
    def subj_fitness(self, ind, best):

        # criteria 1 - [0, 1]
        # shape match based on area
        
        # begin of shape match
        best.shape_list.sort(lambda a,b: -cmp(a.getArea(), b.getArea()))
        ind.shape_list.sort(lambda a,b: -cmp(a.getArea(), b.getArea()))

        my_shapes = ind.shape_list
        best_shapes = best.shape_list

        best_len = len(best_shapes)
        my_len = len(my_shapes)

        min_len = min(best_len, my_len)
        max_len = max(best_len, my_len)

        match = 0
        for i in xrange(min_len):
            if best_shapes[i].shape_type == my_shapes[i].shape_type:
                match += 1

        subj = match / float(max_len)
        subj1 = 1. - subj
        # end of shape match


        ## criteria 2 - [0, 1]
        ## area shapes comparison
        match = 0.
        for i in xrange(min_len):
            b_area, my_area = best_shapes[i].getArea(), my_shapes[i].getArea()
            match += abs(b_area - my_area) / (b_area + my_area)

        match += (max_len - min_len)
        subj2 = match / max_len
        ## end of criteria 2

        ind.fitness[-1] = subj1 * 0.5 +  subj2 * 0.5

#-------------------------------------------#
