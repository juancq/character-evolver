import wx

class ColorSchemeDialog(wx.Dialog):

    def __init__(self, parent, color_schemes):
        wx.Dialog.__init__(self, parent, wx.NewId(), 'Color Scheme Chooser')

        self.parent = parent

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer((10,20))
        
        group = wx.RadioButton(self, -1, '', (1,1), style=wx.RB_GROUP)
        group.Hide()

        for name, color in color_schemes.iteritems():
            vsizer = wx.BoxSizer(wx.HORIZONTAL)
            vsizer.Add(wx.RadioButton(self, 2, name, size = (100,20)))
            for c in color:
                p = wx.Panel(self, -1, size=(20,20), style = wx.DOUBLE_BORDER)
                p.SetBackgroundColour(tuple(c))
                vsizer.Add(p)
                vsizer.AddSpacer((2,10))

            sizer.Add(vsizer)
            sizer.AddSpacer((10,10))


        wx.EVT_RADIOBUTTON(self, 2, self.onClick)

        sizer.AddSpacer((10,10))
        button_sizer = wx.StdDialogButtonSizer()
        button_sizer.AddButton(wx.Button(self, wx.ID_OK, ''))
        button_sizer.AddButton(wx.Button(self, wx.ID_CANCEL, ''))
        button_sizer.Realize()

        sizer.Add(button_sizer)
        self.SetSizer(sizer)
        self.Fit()

        self.color_pick = None

#-------------------------------------------#
    def getColorSelection(self):
        return self.color_pick

#-------------------------------------------#
    def onClick(self, event):
        obj = event.GetEventObject()
        self.color_pick = str(obj.GetLabel())
        self.parent.colorPick(self.color_pick)

#-------------------------------------------#
