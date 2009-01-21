import wx

INSERT_IMG = wx.NewId()
INSERT_TEXT = wx.NewId()
INSERT_COLOR = wx.NewId()
CHANGE_SCHEME = wx.NewId()
MOVE = wx.NewId()
RESIZE = wx.NewId()
BRING_FORWARD = wx.NewId()
SAVE = wx.NewId()
DELETE = wx.NewId()
UNDO = wx.NewId()

class InsertDialog(wx.Dialog):

    def __init__(self, parent, shape_size, text_data = None, disabled = []):
        wx.Dialog.__init__(self, parent, wx.NewId(), 'Insert...')

        self.parent = parent
        self.shape_size = shape_size
        # Setting up Toolbar
        toolbar1 = wx.ToolBar(self, id=-1, style=wx.TB_HORIZONTAL | wx.NO_BORDER |
                                        wx.TB_FLAT | wx.TB_TEXT)

        toolbar1.AddSimpleTool(INSERT_IMG,
              wx.Image('app/doctemplate/insert_img.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
              'Insert Image', '')
        toolbar1.AddSimpleTool(INSERT_TEXT,
              wx.Image('app/doctemplate/insert_text.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
              'Insert Text', '')
        toolbar1.AddSimpleTool(INSERT_COLOR,
              wx.Image('app/doctemplate/insert_color.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
              'Insert Color', '')

        toolbar1.AddSimpleTool(CHANGE_SCHEME,
              wx.Image('app/doctemplate/insert_scheme.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
              'Change Color Scheme', '')

        toolbar1.AddSeparator()
        toolbar1.AddSimpleTool(MOVE,
              wx.Image('app/doctemplate/move.png',
                  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Move Shape', '')
        toolbar1.AddSimpleTool(RESIZE,
              wx.Image('app/doctemplate/resize.png',
                  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Resize Shape', '')
        toolbar1.AddSimpleTool(BRING_FORWARD,
              wx.Image('app/doctemplate/bring_forward.png',
                  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Bring Shape Forward', '')

        toolbar1.AddSeparator()
        toolbar1.AddSimpleTool(UNDO,
              wx.Image('app/doctemplate/undo.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
              'Undo Action', '')
        toolbar1.AddSimpleTool(DELETE,
              wx.Image('gui/delete.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
              'Delete Shape', '')

        toolbar1.AddSeparator()
        toolbar1.AddSimpleTool(SAVE,
              wx.Image('app/doctemplate/save.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
              'Save Template', '')

        toolbar1.Realize()
        toolbar1.Bind(wx.EVT_TOOL, self.OnInsertImg, id=INSERT_IMG)
        toolbar1.Bind(wx.EVT_TOOL, self.OnInsertText, id=INSERT_TEXT)
        toolbar1.Bind(wx.EVT_TOOL, self.OnInsertColor, id=INSERT_COLOR)
        toolbar1.Bind(wx.EVT_TOOL, self.OnChangeScheme, id=CHANGE_SCHEME)
        toolbar1.Bind(wx.EVT_TOOL, self.OnGenericAction, id=MOVE)
        toolbar1.Bind(wx.EVT_TOOL, self.OnGenericAction, id=RESIZE)
        toolbar1.Bind(wx.EVT_TOOL, self.OnGenericAction, id=BRING_FORWARD)
        toolbar1.Bind(wx.EVT_TOOL, self.OnGenericAction, id=UNDO)
        toolbar1.Bind(wx.EVT_TOOL, self.OnSave, id=SAVE)
        toolbar1.Bind(wx.EVT_TOOL, self.OnGenericAction, id=DELETE)

        # disable buttons if necessary
        if 'delete' in disabled:
            toolbar1.EnableTool(DELETE, False)
        if 'move' in disabled:
            toolbar1.EnableTool(MOVE, False)
        if 'resize' in disabled:
            toolbar1.EnableTool(RESIZE, False)
        if 'undo' in disabled:
            toolbar1.EnableTool(UNDO, False)
        if 'bring_forward' in disabled:
            toolbar1.EnableTool(BRING_FORWARD, False)

        self.toolbar1 = toolbar1

        self.Fit()

        self.image = None
        self.color_scheme = None
        self.text_data = text_data

        # parse file with color schemes
        f = open('app/doctemplate/color_schemes')
        data = f.readlines()
        f.close()

        colors = {}
        # each scheme has 4 colors
        # each color is stored in columns, hence awkard reading from file
        for i in xrange(0, len(data), 4):
            name = data[i].strip()
            new_color = [[], [], [], []]
            for j in xrange(3):
                nums = map(int, data[i+j+1].split()[1:])
                for k in xrange(4):
                    new_color[k].append(nums[k])
            colors[name] = new_color

        self.colors = colors
        self.action = None

#-------------------------------------------#
    def OnInsertImg(self, event):
        '''
        Insert image into current shape.
        '''
        # Ask the user to load an image
        dirname = '../images/'
        dlg = wx.FileDialog(self, "Insert Image", dirname, "", 'All files (*)|*|PNG (*png)|*png|BMP (*bmp)|*bmp|JPEG (*jpg)|*jpg', wx.OPEN)

        ret_value = wx.ID_CANCEL
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.image = path
            ret_value = wx.ID_OK
            self.action = 'image'
        dlg.Destroy()
        self.EndModal(ret_value)


#-------------------------------------------#
    def OnInsertText(self, event):
        '''
        Add text to current shape.
        '''
        from textDialog import TextDialog
        dlg = TextDialog(self, 'Insert Text', self.shape_size, self.text_data)

        ret_value = wx.ID_CANCEL
        if dlg.ShowModal() == wx.ID_OK:
            self.text_data = dlg.GetValue()
            self.action = 'text'
            ret_value = wx.ID_OK
        dlg.Destroy()
        self.EndModal(ret_value)

#-------------------------------------------#
    def OnChangeScheme(self, event):
        '''
        Change color scheme dialog.
        '''
        ret_value = wx.ID_CANCEL
        from colorschemedlg import ColorSchemeDialog
        dialog = ColorSchemeDialog(self, self.colors)
        if dialog.ShowModal() == wx.ID_OK:
            color = dialog.getColorSelection()
            self.color_scheme = self.colors[color]
            ret_value = wx.ID_OK
            self.action = 'color_scheme'
                    
        dialog.Destroy()
        self.EndModal(ret_value)


#-------------------------------------------#
    def colorPick(self, color):
        self.color_scheme = self.colors[color]
        self.parent.recolor(self.color_scheme)

#-------------------------------------------#
    def OnInsertColor(self, event):
        '''
        Bucket fill current shape or background color.
        '''
        colorDialog = wx.ColourDialog(self)

        ret_value = wx.ID_CANCEL
        if colorDialog.ShowModal() == wx.ID_OK:
            data = colorDialog.GetColourData()
            # color tuple
            colorScheme = data.GetColour().Get()
            ret_value = wx.ID_OK
            self.color = colorScheme
            self.action = 'color'

        colorDialog.Destroy()
        self.EndModal(ret_value)


#-------------------------------------------#
    def OnGenericAction(self, event):
        id = event.GetId()

        # Delete shape.
        if id == DELETE:
            self.action = 'delete'
        elif id == MOVE:
            self.action = 'move'
        elif id == RESIZE:
            self.action = 'resize'
        elif id == UNDO:
            self.action = 'undo'
        elif id == BRING_FORWARD:
            self.action = 'bring_forward'

        self.EndModal(wx.ID_OK)

#-------------------------------------------#
    def OnSave(self, event):
        '''
        Save template.
        '''
        dirname = ''
        dlg = wx.FileDialog(self, "Save Template", dirname, "", 
                style = wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)

        ret_value = wx.ID_CANCEL
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.save = path
            ret_value = wx.ID_OK
            self.action = 'save'
        dlg.Destroy()
        self.EndModal(ret_value)

#-------------------------------------------#
