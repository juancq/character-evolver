import wx
from wx.lib.ogl import *

wx.OGLInitialize()


class MyEvtHandler(wx.ShapeEvtHandler):
    """
    Overwrite the default event handler to implement some custom features. 
    """
    def __init__(self):
        wx.ShapeEvtHandler.__init__(self)

    def OnLeftClick(self, x, y, keys = 0, attachment = 0):
        """
        The dragging is done here. 
        You should probably comment out the EVT_MOTION below, to see it work. 
        """
        shape = self.GetShape()
        print shape.__class__, shape.GetClassName(), shape.a
        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)

        if shape.Selected():
            shape.Select(False, dc)
            canvas.Redraw(dc)
        else:
            redraw = False
            shapeList = canvas.GetDiagram().GetShapeList()
            toUnselect = []
            for s in shapeList:
                if s.Selected():
                    toUnselect.append(s)

            shape.Select(True, dc)

            if toUnselect:
                for s in toUnselect:
                    s.Select(False, dc)
                canvas.Redraw(dc)



class OGLCanvas(wx.ShapeCanvas):
    def __init__(self, parent, frame):
        wx.ShapeCanvas.__init__(self, parent)

        self.SetBackgroundColour("LIGHT BLUE")
        self.diagram = wx.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)

        self.circle = wx.CircleShape(100)
        self.circle.SetCanvas(self)
        self.circle.a="Circle identified"
        self.diagram.AddShape(self.circle)
        self.circle.Show(True)

        self.evthandler = MyEvtHandler()
        self.evthandler.SetShape(self.circle)
        self.evthandler.SetPreviousHandler(self.circle.GetEventHandler())
        self.circle.SetEventHandler(self.evthandler)

        EVT_MOTION(self, self.OnMotion)

    def OnMotion(self, event):
        shape = self.evthandler.GetShape()

        bx = shape.GetX()
        by = shape.GetY()
        bw, bh = shape.GetBoundingBoxMax()
        oldrect = wx.Rect(int(bx-bw/2)-1, int(by-bh/2)-1, int(bw)+2, int(bh)+2)

        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)

        shape.Move(dc, event.GetPosition()[0], event.GetPosition()[1])
        canvas.Refresh(False, oldrect)
        event.Skip()


class OGLFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)

        self.SetTitle("OGL TEST")
        self.SetBackgroundColour(wx.Colour(8, 197, 248))
        self.canvas = OGLCanvas(self, self)

class Main(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame = OGLFrame(None, -1, "")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

if __name__ == "__main__":
    app = Main()
    app.MainLoop()
