import wx
from iga.gacommon import gaParams

class DocDesign(wx.Panel):
    def __init__(self, parent, size = None, color = "LIGHT BLUE", style = None):
        wx.Panel.__init__(self, parent, -1, size=size, style = wx.DOUBLE_BORDER)

        self.SetBackgroundColour('WHITE')
        self.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL,wx.FONTWEIGHT_BOLD))
        self.parent = parent

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # pick color button
        self.pick_color = wx.Button(self, -1, 'Pick Color...')
        self.pick_color.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.onColorPick, self.pick_color)
        self.sizer.Add(self.pick_color, 0, wx.ALIGN_CENTER) 

        # final sizer and fitting stuff
        self.SetSizer(self.sizer)
        self.Layout()

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

#-------------------------------------------#
    def onRun(self):
        self.pick_color.Enable(True)

#-------------------------------------------#
    def onColorPick(self, event):
        '''
        Population slider event handler.
        '''
        from colorschemedlg import ColorSchemeDialog

        dialog = ColorSchemeDialog(self, self.colors)
        if dialog.ShowModal() == wx.ID_OK:
            # ignore
            pass
            #color = dialog.getColorSelection()
            #gaParams.callAppSlot(0, self.colors[color])
            #self.parent.recolor(self.colors[color])
                    
        dialog.Destroy()

#-------------------------------------------#
    def colorPick(self, color):
        gaParams.callAppSlot(0, self.colors[color])
        self.parent.recolor(self.colors[color])

#-------------------------------------------#
