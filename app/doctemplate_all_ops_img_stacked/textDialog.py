import wx

class TextDialog(wx.Dialog):

    def __init__(self, parent, title, box_size, text = None, font = None, color = None):

        wx.Dialog.__init__(self, parent, wx.NewId(), title, style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

        w, l = box_size[-2], box_size[-1]
        self.text_box = wx.TextCtrl(self, -1, text or '', size = (w, l), style = wx.TE_MULTILINE)
        if font:
            self.text_box.SetFont(font)
        self.font = font
        self.color = color

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
    def GetValue(self):
        ret_value = {}
        ret_value['text'] = self.text_box.GetValue()
        ret_value['font'] = self.font
        ret_value['font_color'] = self.color
        ret_value['size'] = self.text_box.GetSize()
        return ret_value

#-------------------------------------------#
