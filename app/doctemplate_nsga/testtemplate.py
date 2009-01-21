import wx, pickle
from tooldlg import InsertDialog
from wx.lib import wordwrap
from shape import ShapeObject
from iga.gacommon import gaParams

RECT = 1
RRECT = 2
ELLIPSE = 3
EMPTY = 4


class TestTemplate(wx.Frame):

    def __init__(self, parent, shape_list, color_scheme, 
            rr_radius, panel_size):

        self.parent = parent
        self.scale_factor = scale_factor = 3
        self.width = panel_size[0] * scale_factor
        self.height = panel_size[1] * scale_factor
        wx.Frame.__init__(self, None, wx.NewId())#, size=(self.width, self.height))
        self.SetTitle('Test Template')

        #self.shape_sizes = shape_sizes
        self.color_scheme = color_scheme
        self.rr_radius = rr_radius * scale_factor
        self.bgcolor = wx.WHITE

        self.shape_list = shape_list
        self.updateShapeList()
        self.drawHiddenBmp()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.canvas = wx.Panel(self, size =(self.width, self.height), style=wx.SUNKEN_BORDER)
        self.canvas.Bind(wx.EVT_PAINT, self.draw)
        self.canvas.Bind(wx.EVT_LEFT_DOWN, self.onClickBar)
        

        MARGIN = (30,30)
        vsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer.AddSpacer(MARGIN)
        vsizer.Add(self.canvas)
        vsizer.AddSpacer(MARGIN)

        self.sizer.AddSpacer(MARGIN)
        self.sizer.Add(vsizer)
        self.sizer.AddSpacer(MARGIN)

        self.SetSizer(self.sizer)

        self.Layout()
        self.Fit()

        self.moving = None

        self.action_stack = []

        print 'shapes: ', shape_list

#-------------------------------------------#
    def onResizeShape(self, shape, pos):
        self.moving = [pos, shape]

        self.canvas.Bind(wx.EVT_MOTION, self.onResizeMotion)
        self.canvas.Bind(wx.EVT_LEFT_UP, self.onResizeClickUp)
        self.canvas.Unbind(wx.EVT_LEFT_DOWN)

#-------------------------------------------#
    def onResizeMotion(self, event):
        pos = event.GetPosition()
        old_pos, shape = self.moving
        shape.setOffset(pos[0]-old_pos[0], pos[1]-old_pos[1], 'resize')
        self.moving[0] = pos
        self.Refresh()

#-------------------------------------------#
    def onResizeClickUp(self, event):

        if self.moving:
            pos = event.GetPosition()

            self.canvas.Unbind(wx.EVT_MOTION)
            self.canvas.Unbind(wx.EVT_LEFT_UP)
            self.canvas.Bind(wx.EVT_LEFT_DOWN, self.onClickBar)

            old_pos, shape = self.moving
            shape.setOffset(pos[0]-old_pos[0], pos[1]-old_pos[1], 'resize')
            self.moving = None
            self.drawHiddenBmp()
            self.Refresh()

#-------------------------------------------#
    def onMoveShape(self, shape, pos):

        self.moving = [pos, shape]

        self.canvas.Bind(wx.EVT_MOTION, self.onMotion)
        self.Bind(wx.EVT_MOTION, self.onMotion)

        self.canvas.Bind(wx.EVT_LEFT_UP, self.onClickUp)
        self.Bind(wx.EVT_LEFT_UP, self.onClickUp)
        self.canvas.Unbind(wx.EVT_LEFT_DOWN)

#-------------------------------------------#
    def onClickUp(self, event):

        if self.moving:
            pos = event.GetPosition()
            if event.GetEventObject() == self:
                pos = pos[0]-30, pos[1]-30

            self.Unbind(wx.EVT_MOTION)
            self.Unbind(wx.EVT_LEFT_UP)
            self.canvas.Unbind(wx.EVT_MOTION)
            self.canvas.Unbind(wx.EVT_LEFT_UP)
            self.canvas.Bind(wx.EVT_LEFT_DOWN, self.onClickBar)


            old_pos, shape = self.moving
            shape.setOffset(pos[0]-old_pos[0], pos[1]-old_pos[1])
            self.moving = None
            self.drawHiddenBmp()
            self.Refresh()

#-------------------------------------------#
    def onMotion(self, event):
        pos = event.GetPosition()
        if event.GetEventObject() == self:
            pos = pos[0]-30, pos[1]-30
        old_pos, shape = self.moving
        shape.setOffset(pos[0]-old_pos[0], pos[1]-old_pos[1])
        self.moving[0] = pos
        self.Refresh()

#-------------------------------------------#
    def onClickBar(self, event):
        '''
        Determine shape clicked, then ask the user to 
        choose an image to replace current shape.
        '''
        dc = self.hidden_canvas
        pos = event.GetPosition()
        i = dc.GetRed(pos[0], pos[1])

        undo = False
        shape_list_copy = self.copyShapes()
        if i < 255:

            # Ask the user to load an image to replace selected shape
            dirname = ''
            shape = self.shape_list[i]
            shape_pos = shape.getPos()
            text_data = shape.getText()

            disabled = []
            if not self.action_stack: disabled = ['undo']

            dlg = InsertDialog(self, shape_pos, text_data, disabled=disabled)

            if dlg.ShowModal() == wx.ID_OK:
                if dlg.action == 'image':
                    path = dlg.image
                    shape.img = self.createWxImage(path, shape)

                elif dlg.action == 'text':
                    text_data = dlg.text_data
                    shape.setText(text_data)
                    self.drawHiddenBmp()

                elif dlg.action == 'color':
                    shape.color = dlg.color
                    shape.fillColor(dlg.color)

                elif dlg.action == 'color_scheme':
                    self.recolor(dlg.color_scheme)

                elif dlg.action == 'save':
                    self.save(dlg.save)

                elif dlg.action == 'delete':
                    del(self.shape_list[i])
                    self.drawHiddenBmp()

                elif dlg.action == 'move':
                    self.onMoveShape(shape, pos)

                elif dlg.action == 'resize':
                    self.onResizeShape(shape, pos)

                elif dlg.action == 'bring_forward':
                    s = self.shape_list.pop(i)
                    self.shape_list.append(s)
                    self.drawHiddenBmp()

                elif dlg.action == 'undo':
                    self.onUndo()
                    undo = True

                #if not undo:
                #    self.action_stack.append(shape_list_copy)

        else:
            # Ask the user to load an image to replace selected shape
            dirname = ''
            new_size = pos[0], pos[1], 200, 100
            disabled = ['delete', 'move', 'resize', 'bring_forward']
            if not self.action_stack: disabled.append('undo')
            dlg = InsertDialog(self, new_size, disabled = disabled)
                
            if dlg.ShowModal() == wx.ID_OK:
                # create a new shape to hold image or text
                if dlg.action == 'image' or dlg.action == 'text':
                    shape = ShapeObject(gaParams.getRandom(), 1, 0, 0, 1, 1, 10)
                    shape.clear(new_size)

                    if dlg.action == 'image':
                        path = dlg.image
                        shape.img = self.createWxImage(path, shape, original_size = True)

                    elif dlg.action == 'text':
                        text_data = dlg.text_data
                        text_data['border'] = False
                        shape.setText(text_data)

                    self.shape_list.append(shape)
                    self.drawHiddenBmp()

                # if picking new color, then user wants to change bg color
                elif dlg.action == 'color':
                    self.bgcolor = dlg.color

                elif dlg.action == 'color_scheme':
                    self.recolor(dlg.color_scheme)

                elif dlg.action == 'save':
                    self.save(dlg.save)

                elif dlg.action == 'undo':
                    self.onUndo()
                    undo = True

                #if not undo:
                #    self.action_stack.append(shape_list_copy)

            dlg.Destroy()
        self.Refresh()

#-------------------------------------------#
    def createWxImage(self, name, shape_info, original_size = False):
        shape = shape_info.shape_type
        c1, c2, c3, c4 = shape_info.getPos()

        oldPix  = wx.Bitmap(name)
        tmp_img = oldPix.ConvertToImage()

        if original_size:
            new_w, new_h = tmp_img.GetSize()
            shape_info.setSize(new_w, new_h)
        else:
            tmp_img.Rescale(c3, c4)

        oldPix = tmp_img.ConvertToBitmap()
        newPix  = wx.EmptyBitmap(c3, c4)
        mem = wx.MemoryDC()
        mem.SelectObject(newPix)          # because wxEmptyBitmap only
        mem.SetBackground(wx.BLACK_BRUSH)  # allocates the space
        mem.Clear()

        mem.SetPen(wx.RED_PEN)
        mem.SetBrush(wx.Brush('RED'))
        if shape == RECT:
            mem.DrawRectangle(0, 0, c3, c4)
        elif shape == RRECT:
            mem.DrawRoundedRectangle(0, 0, c3, c4, self.rr_radius)
        elif shape == ELLIPSE:
            mem.DrawEllipse(0, 0, c3, c4)
        
        mem.SelectObject(oldPix)
        newPix.SetMask(wx.Mask(newPix, wx.RED))
        mem.DrawBitmap(newPix, 0, 0, True)
        oldPix.SetMask(wx.Mask(newPix, wx.BLACK))

        return oldPix

#-------------------------------------------#
    def updateShapeList(self):
        shape_list = self.shape_list
        scale_factor = self.scale_factor

        for ind in shape_list:
            ind.scale(scale_factor)

#-------------------------------------------#
    def recolor(self, new_color):
        self.color_scheme = new_color
        len_color = len(new_color)
        i = 0
        for obj in self.shape_list:
            obj.reset(new_color[i % len_color], clear_all = False)
            i += 1
        self.Refresh()


#-------------------------------------------#
    def drawHiddenBmp(self):
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
            c = (shape_i, 0, 0)
            shape_i += 1
            dc.SetBrush(wx.Brush(c))
            if shape == RECT:
                dc.DrawRectangle(c1, c2, c3, c4)
            elif shape == RRECT:
                dc.DrawRoundedRectangle(c1, c2, c3, c4, self.rr_radius)
            elif shape == ELLIPSE:
                dc.DrawEllipse(c1, c2, c3, c4)
            elif shape == EMPTY:
                dc.DrawRectangle(c1, c2, c3, c4)

        self.hidden_canvas = oldPix.ConvertToImage()


#-------------------------------------------#
    def draw(self, event):
        '''
        Draw the document with various shapes, but no overlap (ignore x and y
        deformation values).
        '''
        dc = wx.PaintDC(self.canvas)
        self.drawToDevice(dc)

        #dc.SetPen(wx.Pen("black",4))
        #dc.DrawLineList([(0, 0, self.width, 0), 
        #        (self.width, 0, self.width, self.height),
        #        (self.width, self.height, 0, self.height),
        #        (0, self.height, 0, 0)]
        #        )

#-------------------------------------------#
    def save(self, name):
        '''
        Draw the document with various shapes, but no overlap (ignore x and y
        deformation values).
        '''
        oldPix  = wx.EmptyBitmap(self.width, self.height)
        dc = wx.MemoryDC()
        dc.SelectObject(oldPix)

        self.drawToDevice(dc)

        template = oldPix.ConvertToImage()
        # so currently save as png, but maybe provide more options later
        template.SaveFile(name, wx.BITMAP_TYPE_PNG)


#-------------------------------------------#
    def onUndo(self):
        if self.action_stack:
            try:
                shape_list_str = self.action_stack.pop()
                self.shape_list = pickle.loads(shape_list_str)
                self.drawHiddenBmp()
            except:
                print 'cannot undo because of swig object'

#-------------------------------------------#
    def copyShapes(self):
        return None
        mylist = pickle.dumps(self.shape_list)
        return mylist

#-------------------------------------------#
    def drawToDevice(self, dc):
        '''
        Draw the document with various shapes, but no overlap (ignore x and y
        deformation values).
        '''
        dc.SetBackground(wx.Brush(self.bgcolor))
        dc.Clear()

        shape_list = self.shape_list
        def_font = self.GetFont()
        dc.SetPen(wx.Pen("black",1))

        for obj in self.shape_list:

            shape = obj.shape_type
            c1, c2, c3, c4 = obj.getPos()
            c = obj.color

            if obj.img:
                dc.DrawBitmap(obj.img, c1, c2, True)
            else:
                dc.SetBrush(wx.Brush(c))
                if shape == RECT:
                    dc.DrawRectangle(c1, c2, c3, c4)
                elif shape == RRECT:
                    dc.DrawRoundedRectangle(c1, c2, c3, c4, self.rr_radius)
                elif shape == ELLIPSE:
                    dc.DrawEllipse(c1, c2, c3, c4)

            if obj.text:
                if obj.font:
                    dc.SetFont(obj.font)

                if obj.font_color:
                    dc.SetTextForeground(obj.font_color)

                temp = wordwrap.wordwrap(obj.text, c3-10, dc)

                dc.DrawLabel(temp, (c1, c2, c3, c4), obj.font_align)
                dc.SetFont(def_font)
                dc.SetTextForeground(wx.BLACK)

#-------------------------------------------#
