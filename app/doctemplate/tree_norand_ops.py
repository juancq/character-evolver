from copy import deepcopy
from shape import ShapeObject

#-------------------------------------------#
class Tree:
    def __init__(self, random, size_x, size_y, scale_len):

        self.random = random
        self.branch = [[], [], [], []]
        self.size_x = size_x
        self.size_y = size_y
        self.scale_len = scale_len

        self.cx = size_x / 2.
        self.cy = size_y / 2.

#-------------------------------------------#
    def randCenter(self, b1, branch1, min_len, len_b1):
        '''
        Assign random centers to shapes that fall on new quadrant.
        '''
        random = self.random
        xoffset, yoffset = 0., 0.
        if b1 == 1:
            xoffset = self.cx
        elif b1 == 2:
            yoffset = self.cy
        elif b1 == 3:
            xoffset = self.cx
            yoffset = self.cy

        for i in xrange(min_len, len_b1):
            cx_rand = random.random()
            cx_rand *= self.cx
            cy_rand = random.random()
            cy_rand *= self.cy
            branch1[i].setCenter(cx_rand + xoffset, cy_rand + yoffset)


#-------------------------------------------#
    def randNodeCenter(self, b1, node):
        random = self.random
        xoffset, yoffset = 0., 0.
        if b1 == 1:
            xoffset = self.cx
        elif b1 == 2:
            yoffset = self.cy
        elif b1 == 3:
            xoffset = self.cx
            yoffset = self.cy

        cx_rand = random.random()
        cx_rand *= self.cx
        cy_rand = random.random()
        cy_rand *= self.cy
        node.setCenter(cx_rand + xoffset, cy_rand + yoffset)


#-------------------------------------------#
    def getAnyNode(self):

        for branch in self.branch:
            if branch:
                return branch[0]

#-------------------------------------------#
    def addNode(self):

        random = self.random

        b1 = -1
        for branch in self.branch:
            if not branch:
                b1 = self.branch.index(branch)

        if b1 == -1:
            b1 = self.random.randrange(0, len(self.branch))
        branch = self.branch[b1]

        xoffset, yoffset = 0., 0.
        if b1 == 1:
            xoffset = self.cx
        elif b1 == 2:
            yoffset = self.cy
        elif b1 == 3:
            xoffset = self.cx
            yoffset = self.cy

        cx_rand = random.random()
        cx_rand *= self.cx
        cy_rand = random.random()
        cy_rand *= self.cy

        shape_type = random.randrange(1, 4)
        node = ShapeObject(self.random, shape_type, cx_rand + xoffset, cy_rand + yoffset,
                                self.cx * random.uniform(0.10, 0.50), 
                                self.cy * random.uniform(0.10, 0.50), 
                                self.scale_len)
                                        
        branch.append(node)


#-------------------------------------------#
    def deleteNode(self):
        random = self.random
        len_b = 0
        i, save = 0, 0
        for b in self.branch:
            if len(b) > len_b:
                len_b = len(b)
                save = i
            i += 1
                
        branch = self.branch[save]
        if branch:
            i = random.randrange(0, len(branch))
            del branch[i]

#-------------------------------------------#
    def cloneNode(self):
        # move from most dense branch to leanest branch
        random = self.random
        min_b = max_b = len(self.branch[0])
        max_i = min_i = 0

        for b in self.branch:
            if len(b) > max_b:
                max_b = len(b)
                max_i = self.branch.index(b)
            elif len(b) < min_b:
                min_b = len(b)
                min_i = self.branch.index(b)
                
        b1, b2 = max_i, min_i
        # if the biggest branch is empty, then add a random node,
        # instead of cloning
        if not max_b:
            self.addNode()
        elif b1 == b2:
            # if cloning a node and adding to the same branch,
            # then pick two random branches, one to pick a clone
            # and one to insert the clone
            b1, b2 = random.sample(range(0, len(self.branch)), 2)
        else:
            # either b1 or b2 are full
            branch1, branch2 = self.branch[b1], self.branch[b2]
            i = random.randrange(0, len(branch1))
            clone = deepcopy(branch1[i])
            branch2.append(clone)
            self.randNodeCenter(b2, clone)



#-------------------------------------------#
    def quadrantSwap(self, b1, other_branch):

        branch1 = self.branch[b1]

        len_b1 = len(branch1)
        len_b2 = len(other_branch)
        min_len = min(len_b1, len_b2)

        for i in xrange(min_len):
            cx_1, cy_1 = branch1[i].getCenter()
            cx_2, cy_2 = other_branch[i]
            branch1[i].setCenter(cx_2, cy_2)

        if branch1:
            self.randCenter(b1, branch1, min_len, len_b1)

#-------------------------------------------#
    def rearrange(self):

        new_tree = [[], [], [], []]
        for branch in self.branch:
            for shape in branch:
                cx, cy = shape.getCenter()
                if cx < self.cx and cy < self.cy:
                    new_tree[0].append(shape)
                elif cx >= self.cx and cy < self.cy:
                    new_tree[1].append(shape)
                elif cx < self.cx and cy >= self.cy:
                    new_tree[2].append(shape)
                elif cx >= self.cx and cy >= self.cy:
                    new_tree[3].append(shape)

        self.branch = new_tree

    #def __repr__(self):
    #    ret_value = '-' * 30
    #    for branch in self.branch:
    #        ret_value += '\nbranch:kk'
    #        for shape in branch:
    #            print 'shape', shape.printMe()
#-------------------------------------------#
