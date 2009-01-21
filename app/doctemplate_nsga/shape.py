from wx import ALIGN_CENTER
RECT = 1
RRECT = 2
ELLIPSE = 3
EMPTY = 4

#-------------------------------------------#
class ShapeObject:
    def __init__(self, random, shape_type = RECT, x = 0, y = 0, w = 0, l = 0, num_scale = 10):

        self.random = random
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.w = w
        self.l = l

        self.sx = 0
        self.sy = 0
        self.pos = 0

        self.img = None
        self.color = None
        self.text = None
        self.font = None
        self.font_color = None
        self.font_align = ALIGN_CENTER
        self.xscale_chrom = [random.randint(0, 1) for i in xrange(num_scale)]
        self.yscale_chrom = [random.randint(0, 1) for i in xrange(num_scale)]


        #self.sx = sx
        #self.sy = sy

#-------------------------------------------#
    def computePos(self, max_val = None, min_val = None):
        if max_val and min_val:
            self.max_val = max_val
            self.min_val = min_val
        else:
            max_val = self.max_val
            min_val = self.min_val

        # create transformation chromosomes on shapes
        xscale_chrom = self.xscale_chrom
        yscale_chrom = self.yscale_chrom
        len_scale = len(xscale_chrom)
        temp_x, temp_y = 0., 0.
        for j in xrange(len_scale):
            if xscale_chrom[j]:
                temp_x += 2**(len_scale-j-1)
            if yscale_chrom[j]:
                temp_y += 2**(len_scale-j-1)

        sx = temp_x/(2**len_scale)
        sy = temp_y/(2**len_scale)
        xdiff =  sx * (max_val-min_val) + min_val
        ydiff =  sy * (max_val-min_val) + min_val

        #w = self.w - self.x
        #l = self.l - self.y
        #w = float(w) * xdiff * 0.5
        #l = float(l) * ydiff * 0.5

        w = self.w
        l = self.l
        w = float(w) * xdiff * 0.5
        l = float(l) * ydiff * 0.5

        self.w += w
        self.l += l
        self.x += w
        self.y += l


        self.xdiff = 0.
        self.ydiff = 0.

        self.top = self.y
        self.bot = self.y+self.l

        self.left = self.x
        self.right = self.x+self.w

#-------------------------------------------#
    def Info(self):
        return self.left, self.right, self.top, self.bot

#-------------------------------------------#
    def getArea(self):
        if self.w*self.l < 0:
            print 'error'
        return (self.w * self.l)

#-------------------------------------------#
    def getPos(self):
        pos = self.x, self.y, self.w, self.l
        #pos = self.x + self.xdiff, self.y + self.ydiff, self.w + self.xdiff, self.l + self.ydiff
        return pos

#-------------------------------------------#
    def clear(self, new_size):
        self.shape_type = RECT
        x, y, w, l = new_size
        self.reset((255,255,255))
        self.x = x
        self.y = y
        self.w = w
        self.l = l

        #self.setCenter(x, y)

        self.xdiff = 0.
        self.ydiff = 0.

#-------------------------------------------#
    def fillColor(self, color):
        self.color = color
        if self.shape_type == EMPTY:
            self.shape_type = RECT

#-------------------------------------------#
    def reset(self, color, clear_all = True):
        self.color = color
        if clear_all:
            self.img = None
            self.text = None
            self.font = None

#-------------------------------------------#
    def randCenter(self, cx, cy):
        self.setCenter(cx, cy)
        self.randShape()
        self.w += self.w * 0.01
        self.l += self.l * 0.01

#-------------------------------------------#
    def setCenter(self, cx, cy):
        self.x = cx - self.w/2.
        self.y = cy - self.l/2.

#-------------------------------------------#
    def getCenter(self):
        cx = (self.x + (self.x + self.w))/2.
        cy = (self.y + (self.y + self.l))/2.
        return cx, cy

#-------------------------------------------#
    def getText(self):
        text_data = {}
        text_data['text'] = self.text
        text_data['font'] = self.font
        text_data['font_color'] = self.font_color
        text_data['size'] = self.w, self.l
        text_data['align'] = self.font_align

        return text_data

#-------------------------------------------#
    def setText(self, text_data):
        if text_data.has_key('text'):
            self.text = text_data['text']
        if text_data.has_key('font'):
            self.font = text_data['font']
        if text_data.has_key('font_color'):
            self.font_color = text_data['font_color']
        if text_data.has_key('size'):
            w, l = text_data['size']
            self.setSize(w, l)
        if text_data.has_key('border'):
            if not text_data['border']:
                self.shape_type = EMPTY
        if text_data.has_key('align'):
            self.font_align = text_data['align']

#-------------------------------------------#
    def mut(self, prob):

        random = self.random
        chrom = self.xscale_chrom
        for i in xrange(len(chrom)):
            if random.random() < prob:
                chrom[i] ^= 1

        chrom = self.yscale_chrom
        for i in xrange(len(chrom)):
            if random.random() < prob:
                chrom[i] ^= 1

        if random.random() < prob:
            self.x += self.x * random.random()
        if random.random() < prob:
            self.y += self.y * random.random()
        if random.random() < prob:
            self.w += self.w * random.random()
        if random.random() < prob:
            self.l += self.l * random.random()

        if random.random() < prob:
            self.shape_type = (self.shape_type + random.randrange(1, 4)) % 3 + 1

#-------------------------------------------#
    def xo(self, operator, other):

        c1Genome = copy.deepcopy(p1.genome['tree'])
        c2Genome = copy.deepcopy(p2.genome['tree'])

        # quad tree, so pick between 0 and 4
        b1, b2 = random.sample(range(0, 4), 2)
        
        branch1 = c1Genome[b1][:]
        branch2 = c2Genome[b2][:]
        c1Genome[b1] = branch2
        c2Genome[b2] = branch1

        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        c1.genome['tree'] = c1Genome
        c2.genome['tree'] = c2Genome

#-------------------------------------------#
    def randShape(self):
        self.shape_type = self.random.randrange(1, 4)

#-------------------------------------------#
    def setPos(self, x, y):
        self.x = x
        self.y = y

#-------------------------------------------#
    def setOffset(self, dx, dy, offset_type = 'move'):
        if offset_type == 'move':
            self.x += dx
            self.y += dy
        elif offset_type == 'resize':
            self.w += dx
            self.l += dy

#-------------------------------------------#
    def setSize(self, w, l):
        self.w = w
        self.l = l
        self.xdiff = 0.
        self.ydiff = 0.

#-------------------------------------------#
    def scale(self, factor):
        self.x *= factor
        self.y *= factor
        self.w *= factor
        self.l *= factor

#-------------------------------------------#
    def printMe(self):
        print '-' * 30
        print 'obj: ', self.x, self.y, self.w, self.l

#-------------------------------------------#
    def __repr__(self):
        return 'obj: %f %f %f %f' % (self.x, self.y, self.w, self.l)
#-------------------------------------------#
