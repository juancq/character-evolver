from wx.glcanvas import GLCanvas
import wx
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
init = 0

class IGAGLCanvas(GLCanvas):
    def __init__(self, parent, data, tick = 100, size = (250, 250)):
	GLCanvas.__init__(self, parent, size = size, 
                style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
	wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_CHAR(self, self.OnKey)

        self.Bind(wx.EVT_SIZE, self.processSizeEvent, self)
        self.data = data

        self.zOffset = 0.
        self.InitGL()
        self.rtri = 0.0
        self.rquad = 0.0

        TIMER_ID = wx.NewId()
        self.timer = wx.Timer(self, TIMER_ID)  # message will be sent to the panel
        # milliseconds
        self.timer.Start(tick)
        wx.EVT_TIMER(self, TIMER_ID, self.tick)  # call the on_timer function

#------------------------------------------#
    def Destroy(self):
        self.timer.Stop()
        GLCanvas.Destroy(self)

#------------------------------------------#
    def tick(self, event):
        self.Refresh()

#------------------------------------------#
    def OnKey(self, event):
        keycode = chr(event.GetKeyCode())
        if keycode == 'j':
            pass
        elif keycode == 'k':
            pass
        elif keycode == 'z':
            self.zOffset += 1.0

        self.Refresh()
        event.Skip()

#------------------------------------------#
    def OnPaint(self,event):
	#dc = wx.PaintDC(self)
	self.SetCurrent()
	self.OnDraw()


#------------------------------------------#
    def OnReshape(self, width, height):
        """
        Reshape the OpenGL viewport based on the dimensions of the window.
        """
        if height==0:
            height=1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0*width/height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    
#------------------------------------------#
    def GetGLExtents(self):
        """Get the extents of the OpenGL canvas."""
        return self.GetClientSize()

#------------------------------------------#
    def processSizeEvent(self, event):
        """Process the resize event.""" 
        if self.GetContext():
            # Make sure the frame is shown before calling SetCurrent.
            self.Show()
            self.SetCurrent()
            
            size = self.GetGLExtents()
            self.OnReshape(size.width, size.height)
            self.Refresh(False)
        event.Skip()


#------------------------------------------#
    def OnDraw(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	
        glEnable(GL_DEPTH_TEST)
        glLoadIdentity();					
        glTranslatef(-1.5,0.0,-6.0)
        #glRotatef(self.rtri, 0.0, 1.0, 0.0)

        glTranslatef(self.data['xorigin'], 0.0, self.data['xorigin'])
        glRotatef(self.data['xrot'], 1.0, 0.0, 0.0)
        glRotatef(self.data['yrot'], 0.0, 1.0, 0.0)
        glRotatef(self.data['zrot'], 0.0, 0.0, 1.0)

        glBegin(GL_TRIANGLES)				

        glColor3f(1.0,0.0,0.0)
        glVertex3f( 0.0, 1.0, 0.0)		
        glColor3f(0.0,1.0,0.0)
        glVertex3f(-1.0,-1.0, 1.0)
        glColor3f(0.0,0.0,1.0)	
        glVertex3f( 1.0,-1.0, 1.0)
        
        glColor3f(1.0,0.0,0.0)	
        glVertex3f( 0.0, 1.0, 0.0)
        glColor3f(0.0,0.0,1.0)	
        glVertex3f( 1.0,-1.0, 1.0)
        glColor3f(0.0,1.0,0.0)	
        glVertex3f( 1.0,-1.0, -1.0)

        glColor3f(1.0,0.0,0.0)	
        glVertex3f( 0.0, 1.0, 0.0)
        glColor3f(0.0,1.0,0.0)	
        glVertex3f( 1.0,-1.0, -1.0)
        glColor3f(0.0,0.0,1.0)	
        glVertex3f(-1.0,-1.0, -1.0)
                    
                    
        glColor3f(1.0,0.0,0.0)	
        glVertex3f( 0.0, 1.0, 0.0)
        glColor3f(0.0,0.0,1.0)	
        glVertex3f(-1.0,-1.0,-1.0)
        glColor3f(0.0,1.0,0.0)	
        glVertex3f(-1.0,-1.0, 1.0)
        glEnd()


        #glLoadIdentity()
        #glTranslatef(1.5,0.0,-7.0)
        #glRotatef(self.rquad,1.0,1.0,1.0)
        #glBegin(GL_QUADS)	


        #glColor3f(0.0,1.0,0.0)
        #glVertex3f( 1.0, 1.0,-1.0)
        #glVertex3f(-1.0, 1.0,-1.0)		
        #glVertex3f(-1.0, 1.0, 1.0)		
        #glVertex3f( 1.0, 1.0, 1.0)		

        #glColor3f(1.0,0.5,0.0)	
        #glVertex3f( 1.0,-1.0, 1.0)
        #glVertex3f(-1.0,-1.0, 1.0)		
        #glVertex3f(-1.0,-1.0,-1.0)		
        #glVertex3f( 1.0,-1.0,-1.0)		

        #glColor3f(1.0,0.0,0.0)		
        #glVertex3f( 1.0, 1.0, 1.0)
        #glVertex3f(-1.0, 1.0, 1.0)		
        #glVertex3f(-1.0,-1.0, 1.0)		
        #glVertex3f( 1.0,-1.0, 1.0)		

        #glColor3f(1.0,1.0,0.0)	
        #glVertex3f( 1.0,-1.0,-1.0)
        #glVertex3f(-1.0,-1.0,-1.0)
        #glVertex3f(-1.0, 1.0,-1.0)		
        #glVertex3f( 1.0, 1.0,-1.0)		

        #glColor3f(0.0,0.0,1.0)	
        #glVertex3f(-1.0, 1.0, 1.0)
        #glVertex3f(-1.0, 1.0,-1.0)		
        #glVertex3f(-1.0,-1.0,-1.0)		
        #glVertex3f(-1.0,-1.0, 1.0)		

        #glColor3f(1.0,0.0,1.0)	
        #glVertex3f( 1.0, 1.0,-1.0)
        #glVertex3f( 1.0, 1.0, 1.0)
        #glVertex3f( 1.0,-1.0, 1.0)		
        #glVertex3f( 1.0,-1.0,-1.0)		
        #glEnd()	

        glFinish()
        self.SwapBuffers()

        self.data['xrot'] = (self.data['xrot'] + self.data['update']) % 360 
        self.data['yrot'] = (self.data['yrot'] + self.data['update']) % 360
        self.data['zrot'] = (self.data['zrot'] + self.data['update']) % 360

        #self.rtri += 0.5
        #self.rquad -= 0.55

	
#------------------------------------------#
    def InitGL(self):
        global init
	if not init:
	    init = 1

            glutInit('')
            glShadeModel(GL_SMOOTH)
            glClearColor(0.0, 0.0, 0.0, 0.0)
            glClearDepth(1.0)
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LEQUAL)
            glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

#------------------------------------------#
