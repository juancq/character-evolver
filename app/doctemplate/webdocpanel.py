import wx
RECT = 1
RRECT = 2
ELLIPSE = 3
EMPTY = 4

class DocPanel:
    def __init__(self, params, individual = None, quad_tree=[], color_scheme = [],
                name = ''):

        self.shape_list = quad_tree
        self.color_scheme = color_scheme

        self.max_val = params['max_scale']
        self.min_val = params['min_scale']
        self.rr_radius = params['rr_radius']
        self.width = params['plotSizeX']
        self.height = params['plotSizeY']
        
        self.updateShapeList()
        self.drawHiddenBmp(name)

#-------------------------------------------#
    def updateShapeList(self):

        color = self.color_scheme
        len_color = len(color)
        i = 0
        for obj in self.shape_list:
            c = color[i % len_color]
            obj.reset(c)
            i += 1

#-------------------------------------------#
    def drawHiddenBmp(self, name):
        '''
        Draw all shapes to a hidden bitmap, where we assign a unique color to each
        shape. When user clicks on a shape, we use the unique color to determine
        which shape was selected.
        '''
        oldPix  = wx.EmptyBitmap(self.width, self.height)
        dc = wx.MemoryDC()
        dc.SelectObject(oldPix)
        dc.SetBackground(wx.WHITE_BRUSH)  # allocates the space
        dc.Clear()                       # The images have to be cleared

        shape_list = self.shape_list
        shape_i = 0

        dc.SetPen(wx.Pen("black",1))

        for obj in self.shape_list:

            shape = obj.shape_type
            c1, c2, c3, c4 = obj.getPos()
            c = obj.color
            dc.SetBrush(wx.Brush(c))
            if shape == RECT:
                dc.DrawRectangle(c1, c2, c3, c4)
            elif shape == RRECT:
                dc.DrawRoundedRectangle(c1, c2, c3, c4, self.rr_radius)
            elif shape == ELLIPSE:
                dc.DrawEllipse(c1, c2, c3, c4)
            elif shape == EMPTY:
                dc.DrawRectangle(c1, c2, c3, c4)

        dc.SetPen(wx.Pen("black",5))
        dc.DrawLineList([(0, 0, self.width, 0), 
                (self.width, 0, self.width, self.height),
                (self.width, self.height, 0, self.height),
                (0, self.height, 0, 0)]
                )
        dc.SelectObject(wx.NullBitmap)
        oldPix.SaveFile(name, wx.BITMAP_TYPE_JPEG)

#-------------------------------------------#
