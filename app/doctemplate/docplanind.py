from igap.iga.individual import Individual

class DocplanIndividual(Individual):
    def __init__(self, random, genome_len, genome):
        Individual.__init__(self, random, genome_len, genome)

        self.rank = 10
        self.crowded_distance = 0
        self.decoded_plan = None
        self.numRoom = None
        self.roomarea = None
        self.roomlist = None
        self.roomDesc = None
        self.roomSizes = None

        self.shape_list = None

        self.operators = []


#-------------------------------------------#
    def isequal(self, other):
        '''
        Compare two individuals by comparing their respective
        shapes.
        Currently, if the two lists have the exact same shape types, 
        regardless of size, then they're considered equal.
        '''
        my_len = len(self.shape_list)
        other_len = len(other.shape_list)
        if my_len != other_len:
            return False
        else:
            my_s = self.shape_list
            other_s = other.shape_list
                
            for i in xrange(my_len):
                if my_s[i].shape_type != other_s[i].shape_type:
                    return False
                else:
                    my_pos = my_s[i].getPos()
                    other_pos = other_s[i].getPos()
                    dist = 0.
                    for i in xrange(4):
                        dist += (my_pos[i]-other_pos[i])**2
                    dist = dist ** 0.5

                    if dist > 1:
                        return False

            return True
                

#-------------------------------------------#
    def floorplan_isequal(self, other):
        if self.numRoom == other.numRoom and self.roomarea == other.roomarea and self.roomlist == other.roomlist and self.roomDesc == other.roomDesc and self.roomSizes == other.roomSizes:
            return True
        else:
            return False
                
        return cmp(self.rank, other.rank)


#-------------------------------------------#
    def __cmp__(self, other):
        return cmp(self.rank, other.rank)
#-------------------------------------------#
