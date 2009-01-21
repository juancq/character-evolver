import sys
sys.path.insert(0,'..')
import PythonOgreConfig

import ogre.renderer.OGRE as ogre
import ogre.gui.CEGUI as CEGUI
import ogre.io.OIS as OIS
import SampleFramework as sf


class MouseQueryListener(sf.FrameListener, OIS.MouseListener):

    def __init__(self, win, cam, sc, renderer):

        sf.FrameListener.__init__(self, win, cam, True, True)
        OIS.MouseListener.__init__(self)

        self.sceneManager = sc
        self.renderer = renderer
        self.camera = cam

        # register as mouse listener
        self.Mouse.setEventCallback(self)

        self.raySceneQuery = None
        self.leftMouseDown = False
        self.rightMouseDown = False
        self.robotCount = 0
        self.currentObject = None
        self.moveSpeed = 50
        self.rotateSpeed = 1/500.

        self.raySceneQuery = self.sceneManager.createRayQuery(ogre.Ray())

        self.robotMode = True
        self.debugText = 'Robot Mode Enabled - Press Space to Toggle'


#--------------------------------------------#
    def frameStarted(self, evt):
        if not sf.FrameListener.frameStarted(self, evt):
            return False

        #if self.Keyboard.isKeyDown(OIS.KC_SPACE) and self.timeUntilNextToggle <= 0:
        if self.Keyboard.isKeyDown(OIS.KC_SPACE):
            self.robotMode = not self.robotMode
            ent_type = 'Robot' if self.robotMode else 'Ninja'
            self.debugText = '%s Mode Enabled - Press Space to Toggle' % ent_type



        camPos = self.camera.getPosition()
        # origin, direction
        updateRay = ogre.Ray((camPos.x, 5000., camPos.y), ogre.Vector3().NEGATIVE_UNIT_Y)
        self.raySceneQuery.setRay(updateRay)

        result = self.raySceneQuery.execute()
        if len(result) > 0:
            item = result[0]
            if item.worldFragment is not None:
                terrainHeight = item.worldFragment.singleIntersection.y
                if (terrainHeight + 10.0) > camPos.y:
                    self.camera.setPosition(camPos.x, terrainHeight + 10., camPos.z)

        return True


#--------------------------------------------#
    def mouseMoved(self, evt):
        CEGUI.System.getSingleton().injectMouseMove(evt.get_state().X.rel, evt.get_state().Y.rel)

        if self.leftMouseDown:
            
            mousePos = CEGUI.MouseCursor.getSingleton().getPosition()
            # evt.get_state().width and height gives the current screen's width and height resolution
            mouseRay = self.camera.getCameraToViewportRay(mousePos.d_x / float(evt.get_state().width),
                                                           mousePos.d_y / float(evt.get_state().height))

            self.raySceneQuery.setRay(mouseRay)

            result = self.raySceneQuery.execute()
            if len(result) > 0:
                item = result[0]
                if item.worldFragment:
                    self.currentObject.setPosition(item.worldFragment.singleIntersection)

        elif self.rightMouseDown:
            self.camera.yaw(ogre.Degree(-evt.get_state().X.rel * self.rotateSpeed))
            self.camera.pitch(ogre.Degree(-evt.get_state().Y.rel * self.rotateSpeed))

        return True

#--------------------------------------------#
    def mousePressed(self, evt, id):
        if id == OIS.MB_Left:
            self.onLeftPressed(evt)
            self.leftMouseDown = True

        elif id == OIS.MB_Right:
            CEGUI.MouseCursor.getSingleton().hide()
            self.rightMouseDown = True
        return True

#--------------------------------------------#
    def mouseReleased(self, evt, id):
        if id == OIS.MB_Left:
            self.leftMouseDown = False
        elif id == OIS.MB_Right:
            CEGUI.MouseCursor.getSingleton().show()
            self.rightMouseDown = False
        return True

#--------------------------------------------#
    def _processUnbufferedMouseInput(self, frameEvent):
        pass


#--------------------------------------------#
    def onLeftPressed(self, evt):
        if self.currentObject:
            self.currentObject.showBoundingBox(False)

        mousePos = CEGUI.MouseCursor.getSingleton().getPosition()
        mouseRay = self.camera.getCameraToViewportRay(mousePos.d_x / float(evt.get_state().width),
                                                      mousePos.d_y / float(evt.get_state().height))
        self.raySceneQuery.setRay(mouseRay)

        result = self.raySceneQuery.execute()
        if len(result) > 0:
            item = result[0]
            if item.worldFragment:
                ent_type = 'robot' if self.robotMode else 'ninja'
                name = '%s%d' % (ent_type, self.robotCount)
                ent = self.sceneManager.createEntity(name, '%s.mesh' % ent_type)

                self.robotCount += 1
                self.currentObject = self.sceneManager.getRootSceneNode().createChildSceneNode('%sNode' % name, item.worldFragment.singleIntersection)
                self.currentObject.attachObject(ent)
                self.currentObject.setScale(0.1, 0.1, 0.1)

        if self.currentObject:
            self.currentObject.showBoundingBox(True)


#--------------------------------------------#
    def onRightPressed(self, evt):
        pass



#----------------------------------------------------------------#
class MyApplication(sf.Application):

    def _chooseSceneManager(self):
        self.sceneManager = self.root.createSceneManager(ogre.ST_EXTERIOR_CLOSE, 'TerrainSM')


#--------------------------------------------#
    def _createScene(self):
        self.ceguiRenderer = CEGUI.OgreCEGUIRenderer(self.renderWindow, ogre.RENDER_QUEUE_OVERLAY, False, 3000, self.sceneManager)
        self.ceguiSystem = CEGUI.System(self.ceguiRenderer)

        self.sceneManager.setAmbientLight((0.5, 0.5, 0.5))
        self.sceneManager.setSkyDome(True, 'Examples/CloudySky', 5, 8)

        self.sceneManager.setWorldGeometry('terrain.cfg')

        self.camera.setPosition(40, 100, 580)
        self.camera.pitch(ogre.Degree(-30))
        self.camera.yaw(ogre.Degree(-45))

        CEGUI.SchemeManager.getSingleton().loadScheme('TaharezLookSkin.scheme')
        CEGUI.MouseCursor.getSingleton().setImage('TaharezLook', 'MouseArrow')


#--------------------------------------------#
    def _createFrameListener(self):
        self.frameListener = MouseQueryListener(self.renderWindow, self.camera, self.sceneManager, self.ceguiRenderer)
        self.root.addFrameListener(self.frameListener)
        self.frameListener.showDebugOverlay(True)


#----------------------------------------------------------------#

if __name__ == '__main__':
    ta = MyApplication()
    ta.go()
