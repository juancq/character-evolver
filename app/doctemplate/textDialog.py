import wx

LEFT = wx.NewId()
RIGHT = wx.NewId()
CENTER = wx.NewId()

class TextDialog(wx.Dialog):

    def __init__(self, parent, title, box_size, text_data = None):

        wx.Dialog.__init__(self, parent, wx.NewId(), title, style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.FULL_REPAINT_ON_RESIZE)

        if text_data:
            text = text_data['text']
            font = text_data['font']
            color = text_data['font_color']
            align = text_data['align']
        else:
            text = font = color = None
            align = wx.ALIGN_CENTER
                
                
        w, l = box_size[-2], box_size[-1]
        self.text_box = wx.TextCtrl(self, -1, text or '', size = (w, l), style = wx.TE_MULTILINE)
        self.text_box.SetFocus()
        if font:
            self.text_box.SetFont(font)
        self.font = font
        self.color = color
        self.align = align

        left_bmp = wx.Bitmap('app/doctemplate/justify-left.png')
        right_bmp = wx.Bitmap('app/doctemplate/justify-right.png')
        center_bmp = wx.Bitmap('app/doctemplate/justify-center.png')

        b = {}
        b[wx.ALIGN_LEFT] = align_left = wx.BitmapButton(self, LEFT, bitmap = left_bmp)
        b[wx.ALIGN_RIGHT] = align_right = wx.BitmapButton(self, RIGHT, bitmap = right_bmp)
        b[wx.ALIGN_CENTER] = align_center = wx.BitmapButton(self, CENTER, bitmap = center_bmp)
        self.align_button = b

        self.align_button[self.align].SetBackgroundColour('GREEN')

        self.Bind(wx.EVT_BUTTON, self.onAlign, align_left)
        self.Bind(wx.EVT_BUTTON, self.onAlign, align_right)
        self.Bind(wx.EVT_BUTTON, self.onAlign, align_center)

        font_button = wx.Button(self, -1, 'Font...')
        font_color_button = wx.Button(self, -1, 'Font Color...')
        self.Bind(wx.EVT_BUTTON, self.onFontChange, font_button)
        self.Bind(wx.EVT_BUTTON, self.onFontColor, font_color_button)

        sizer = wx.StdDialogButtonSizer()
        sizer.AddButton(wx.Button(self, wx.ID_OK, ''))
        sizer.AddButton(wx.Button(self, wx.ID_CANCEL, ''))
        sizer.Realize()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.AddSpacer((10,14))
        self.sizer.Add(self.text_box, 1, wx.EXPAND)
        self.sizer.AddSpacer((10,10))

        align_sizer = wx.BoxSizer(wx.HORIZONTAL)
        align_sizer.Add(align_left)
        align_sizer.AddSpacer((10, 10))
        align_sizer.Add(align_center)
        align_sizer.AddSpacer((10, 10))
        align_sizer.Add(align_right)
        self.sizer.Add(align_sizer)
        self.sizer.AddSpacer((10,10))

        font_sizer = wx.BoxSizer(wx.HORIZONTAL)
        font_sizer.Add(font_button)
        font_sizer.AddSpacer((10, 10))
        font_sizer.Add(font_color_button)

        self.sizer.Add(font_sizer)
        self.sizer.AddSpacer((10,14))
        self.sizer.Add(sizer)

        self.SetSizer(self.sizer)
        self.Fit()

#-------------------------------------------#
    def onFontColor(self, event):
        def_color = wx.ColourData()
        if self.color:
            def_color.SetColour(self.color)
                
        colorDialog = wx.ColourDialog(self, def_color)

        ret_value = wx.ID_CANCEL
        if colorDialog.ShowModal() == wx.ID_OK:
            data = colorDialog.GetColourData()
            # color tuple
            color = data.GetColour().Get()
            self.color = color

        colorDialog.Destroy()

#-------------------------------------------#
    def onFontChange(self, event):

        def_font = self.text_box.GetFont()
        data = wx.FontData()
        data.SetInitialFont(def_font)
        dlg = wx.FontDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            new_data = dlg.GetFontData()
            self.font = new_data.GetChosenFont()
            self.text_box.SetFont(self.font)

        dlg.Destroy()

#-------------------------------------------#
    def onAlign(self, event):
        id = event.GetId()
        self.align_button[self.align].SetBackgroundColour('LIGHT_GRAY')
        if id == LEFT:
            self.align = wx.ALIGN_LEFT
        elif id == RIGHT:
            self.align = wx.ALIGN_RIGHT
        elif id == CENTER:
            self.align = wx.ALIGN_CENTER

        self.align_button[self.align].SetBackgroundColour('GREEN')
        button = event.GetEventObject()
        button.SetBackgroundColour('GREEN')

#-------------------------------------------#
    def GetValue(self):
        ret_value = {}
        ret_value['text'] = self.text_box.GetValue()
        ret_value['font'] = self.font
        ret_value['font_color'] = self.color
        ret_value['size'] = self.text_box.GetSize()
        ret_value['align'] = self.align
        return ret_value

#-------------------------------------------#
