import sys
sys.path.insert(0,'..')
import PythonOgreConfig

import ogre.renderer.OGRE as ogre
import ogre.gui.CEGUI as CEGUI
import ogre.io.OIS as OIS
import SampleFramework as sf

import evolve

SPACE = 1000
MOVE = 1000

def node_helper(cur_node, _genes):
    cur_node.yaw(ogre.Degree(_genes['yaw']))
    cur_node.pitch(ogre.Degree(_genes['pitch']))
    cur_node.roll(ogre.Degree(_genes['roll']))
    cur_node.setScale(_genes['sx'], _genes['sy'], _genes['sz'])
    #cur_node.showBoundingBox(True)
    print cur_node.getName()

    return 0
    #return dist


def ent_helper(cur_node, _ent, n = 0):
    #_ent.setMaterialName('Examples/TextureEffect%d' % (node_id % 3 + 1))
    _ent.setMaterialName('Examples/Rockwall')
    cur_node.attachObject(_ent)


class GAListener(sf.FrameListener, OIS.MouseListener, OIS.KeyListener):

    def __init__(self, renderWindow, camera, sceneManager, cegui, ind_nodes):
        sf.FrameListener.__init__(self, renderWindow, camera, True, True)
        OIS.MouseListener.__init__(self)
        OIS.KeyListener.__init__(self)

        self.toggle = 0
        self.mouse_down = False

        self.cam_node = camera.parentSceneNode.parentSceneNode
        self.sceneManager = sceneManager
        self.cegui = cegui

        self.ga = None
        self.genomes = []
        self.ind_nodes = ind_nodes

        # Register as MouseListener (Basic tutorial 5)
        self.Mouse.setEventCallback(self)
        self.Keyboard.setEventCallback(self)

        self.rotate = 0.20
        self.move = MOVE

        self.currentObject = None
        self.raySceneQuery = None
        self.raySceneQuery = self.sceneManager.createRayQuery(ogre.Ray())


        self.num_keys = ['%d' % i for i in range(10)]

#---------------------------------#
    def mouseMoved(self, evt):
        CEGUI.System.getSingleton().injectMouseMove(evt.get_state().X.rel, evt.get_state().Y.rel)
        return True

#---------------------------------#
    def mousePressed(self, evt, id):
        if id == OIS.MB_Left:
            self.onLeftPressed(evt)
        return True
 
#---------------------------------#
    def mouseReleased(self, evt, id):
        return True

#---------------------------------#
    def keyPressed(self, evt):
        print 'pressed', self.Keyboard.getAsString(evt.key)

        if evt.key is OIS.KC_N:
            curstudy = 'character3d.yml'
            l = 6
            ga = evolve.init_iga({'app_name': curstudy, 'geomNodes': l})
            self.genomes = ga.draw()
            self.ga = ga

            self.newPop()

        elif evt.key is not OIS.KC_ESCAPE:
            best_selected = self.Keyboard.getAsString(evt.key)
            if self.ga and best_selected in self.num_keys:
                best_selected = int(best_selected)
                self.genomes = self.ga.web_step({'feedback': [best_selected]})
                self.newPop()
        return True

#---------------------------------#
    def keyReleased(self, evt):
        return True

#---------------------------------#
    def frameStarted(self, frameEvent):
        if self.renderWindow.isClosed():
            return False

        self.Keyboard.capture()
        #self.Mouse.capture()

        #curr_mouse = self.Mouse.getMouseState()

        #if curr_mouse.buttonDown(OIS.MB_Left) and not self.mouse_down:
        #    light = self.sceneManager.getLight('Light1')
        #    light.visible = not light.visible

        #self.mouse_down = curr_mouse.buttonDown(OIS.MB_Left)

        if self.toggle >= 0:
            self.toggle -= frameEvent.timeSinceLastFrame

        #if self.toggle < 0 and self.Keyboard.isKeyDown(OIS.KC_1):
        #    self.toggle = 0.1
        #    self.camera.parentSceneNode.detachObject(self.camera)
        #    self.cam_node = self.sceneManager.getSceneNode('CamNode1')
        #    self.sceneManager.getSceneNode('PitchNode1').attachObject(self.camera)

        #elif self.toggle < 0 and self.Keyboard.isKeyDown(OIS.KC_2):
        #    self.toggle = 0.1
        #    self.camera.parentSceneNode.detachObject(self.camera)
        #    self.cam_node = self.sceneManager.getSceneNode('CamNode2')
        #    self.sceneManager.getSceneNode('PitchNode2').attachObject(self.camera)


        transVector = ogre.Vector3(0, 0, 0)
        
        if self.Keyboard.isKeyDown(OIS.KC_UP) or self.Keyboard.isKeyDown(OIS.KC_W):
            transVector.z -= self.move
        if self.Keyboard.isKeyDown(OIS.KC_DOWN) or self.Keyboard.isKeyDown(OIS.KC_S):
            transVector.z += self.move

        if self.Keyboard.isKeyDown(OIS.KC_LEFT) or self.Keyboard.isKeyDown(OIS.KC_A):
            transVector.x -= self.move
        if self.Keyboard.isKeyDown(OIS.KC_RIGHT) or self.Keyboard.isKeyDown(OIS.KC_D):
            transVector.x += self.move

        if self.Keyboard.isKeyDown(OIS.KC_PGUP) or self.Keyboard.isKeyDown(OIS.KC_Q):
            transVector.y -= self.move
        if self.Keyboard.isKeyDown(OIS.KC_PGDOWN) or self.Keyboard.isKeyDown(OIS.KC_E):
            transVector.y += self.move


        self.cam_node.translate(self.cam_node.orientation * transVector * frameEvent.timeSinceLastFrame)

        #if curr_mouse.buttonDown(OIS.MB_Right):
        #    self.cam_node.yaw(ogre.Degree(-self.rotate * curr_mouse.X.rel).valueRadians())
        #    self.cam_node.getChild(0).pitch(ogre.Degree(-self.rotate * curr_mouse.Y.rel).valueRadians())

        if not sf.FrameListener.frameStarted(self, frameEvent):
            return False

        return not self.Keyboard.isKeyDown(OIS.KC_ESCAPE)

#---------------------------------#
    def onLeftPressed(self, evt):
        #if self.currentObject:
        #    self.currentObject.showBoundingBox(False)
 
        # Setup the ray scene query, use CEGUI's mouse position
        mousePos = CEGUI.MouseCursor.getSingleton().getPosition()
        mouseRay = self.camera.getCameraToViewportRay(mousePos.d_x / float(evt.get_state().width),
                                                      mousePos.d_y / float(evt.get_state().height))
        self.raySceneQuery.setRay(mouseRay)
        self.raySceneQuery.setSortByDistance(True)
        #self.raySceneQuery.setQueryMask(self.sceneManager.ENTITY_TYPE_MASK)
 
        # Execute query
        result = self.raySceneQuery.execute()
        if len(result) > 0:
            for item in result:
                if item.movable:
                    print 'movable'
                    self.currentObject = item.movable.getParentSceneNode()
                    item.movable.getParentSceneNode().showBoundingBox(True)
                    print item.movable.getParentSceneNode().getName()
                    break # We found an existing object
 
        if self.currentObject:
            self.currentObject.showBoundingBox(True)

#----------------------------------------#
    def newPop(self):
        '''
        Create and display a new pop.
        '''
        sceneManager = self.sceneManager
        sceneManager.destroyAllEntities()
        root_node = sceneManager.getRootSceneNode()

        #[root_node.getChild('Individual%d' % i).removeAllChildren() for i in range(9)]

        for i, node in enumerate(self.ind_nodes):
            node.removeAndDestroyAllChildren()
            node_genes = self.genomes[i]
            node.position = (0, 0, 0)
            self.makeCharacter(i, node, node_genes)
            node.position = (i*SPACE, 0, 0)

            sep_node = sceneManager.getSceneNode('Separator%d' % i)
            sep_node.removeAllChildren()
            ent = sceneManager.createEntity('Separator%d' %i, 'knot.mesh')
            sep_node.attachObject(ent)

#---------------------------------#
    def makeCharacter(self, node_id, parent_node, genome = []):
        '''
        Create a 3d character with 6 parts: head, torso, 2 arms, 2 legs.
        '''
        sceneManager = self.sceneManager
        pt_sphere, pt_cube = sceneManager.PT_SPHERE, sceneManager.PT_CUBE
        c = 0
        genes = genome[c]
        i = node_id

        # head
        ent_type = pt_sphere if genes['shape'] else pt_cube
        node = head_node = parent_node.createChildSceneNode('Head%d' % i)
        ent = sceneManager.createEntity('Head%d' %i, ent_type)
        ent_helper(node, ent, c % 3 + 1)
        dist = node_helper(node, genes)
        dist = node.getParentSceneNode().getAttachedObject(0).getBoundingRadius() + node.getAttachedObject(0).getBoundingRadius()

        c += 1
        genes = genome[c]
        # torso
        node = torso_node = head_node.createChildSceneNode('Torso%d' % i)
        ent = sceneManager.createEntity('Torso%d' %i, sceneManager.PT_CUBE)
        ent_helper(node, ent, c % 3 + 1)
        dist = node_helper(node, genes)
        node.position = (0, -dist, 0)

        c += 1
        genes = genome[c]
        # left arm
        node = leftarm_node = torso_node.createChildSceneNode('LeftArm%d' % i)
        ent = sceneManager.createEntity('LeftArm%d' %i, sceneManager.PT_SPHERE)
        ent_helper(node, ent, c % 3 + 1)
        dist = node_helper(node, genes)
        node.position = (-dist, 0, 0)

        c += 1
        genes = genome[c]
        # right arm
        node = rightarm_node = torso_node.createChildSceneNode('RightArm%d' % i)
        ent = sceneManager.createEntity('RightArm%d' %i, sceneManager.PT_SPHERE)
        ent_helper(node, ent, c % 3 + 1)
        dist = node_helper(node, genes)
        node.position = (dist, 0, 0)

        c += 1
        genes = genome[c]
        # left leg
        node = leftleg_node = torso_node.createChildSceneNode('LeftLeg%d' % i)
        ent = sceneManager.createEntity('LeftLeg%d' %i, sceneManager.PT_CUBE)
        ent_helper(node, ent, c % 3 + 1)
        dist = node_helper(node, genes)
        node.position = (-dist, -dist, 0)

        c += 1
        genes = genome[c]
        # right leg
        node = rightleg_node = torso_node.createChildSceneNode('RightLeg%d' % i)
        ent = sceneManager.createEntity('RightLeg%d' %i, sceneManager.PT_CUBE)
        ent_helper(node, ent, c % 3 + 1)
        dist = node_helper(node, genes)
        node.position = (dist, -dist, 0)

#----------------------------------------#



class TutorialApp(sf.Application):

    def _createScene(self):

        self.ceguiRenderer = CEGUI.OgreCEGUIRenderer(self.renderWindow, ogre.RENDER_QUEUE_OVERLAY, False, 3000, self.sceneManager)

        self.ceguiSystem = CEGUI.System(self.ceguiRenderer)
        sceneManager = self.sceneManager
        sceneManager.ambientLight = 0.75, 0.75, 0.75


        #ind_nodes = []
        #for i in range(9):
        #    node_genes = self.genomes[i]
        #    ind_node = sceneManager.getRootSceneNode().createChildSceneNode('Individual%d' % i)
        #    ind_node.position = (0, 0, 0)
        #    self.makeCharacter(i, ind_node, node_genes)
        #    ind_node.position = (i*SPACE, 0, 0)

        #    sep_node = sceneManager.getRootSceneNode().createChildSceneNode('Separator%d' % i)
        #    sep_node.position = (i*SPACE, 200, 0)
        #    sep_node.setScale(0.5, 0.5, 0.5)
        #    ent = sceneManager.createEntity('Separator%d' %i, 'knot.mesh')
        #    sep_node.attachObject(ent)

        #    ind_nodes.append(ind_node)

        #self.ind_nodes = ind_nodes

        ind_nodes = []
        for i in range(9):
            ind_node = sceneManager.getRootSceneNode().createChildSceneNode('Individual%d' % i)
            ind_node.position = (0, 0, 0)

            sep_node = sceneManager.getRootSceneNode().createChildSceneNode('Separator%d' % i)
            sep_node.position = (i*SPACE, 200, 0)
            sep_node.setScale(0.5, 0.5, 0.5)

            ind_nodes.append(ind_node)

        self.ind_nodes = ind_nodes

        light = sceneManager.createLight('Light1')
        light.type = ogre.Light.LT_POINT
        light.position = (0, 1000, -500)
        light.diffuseColour = (1, 1, 1)
        light.specularColour = (1, 1, 1)

        node = sceneManager.getRootSceneNode().createChildSceneNode('CamNode1', (-400, 200, 400))
        node.yaw(ogre.Degree(-45))

        node = node.createChildSceneNode('PitchNode1')
        node.attachObject(self.camera)

        node = sceneManager.getRootSceneNode().createChildSceneNode('CamNode2', (0, 200, 400))
        node.createChildSceneNode('PitchNode2')

        # Show the mouse cursor
        CEGUI.SchemeManager.getSingleton().loadScheme("TaharezLookSkin.scheme")
        CEGUI.MouseCursor.getSingleton().setImage("TaharezLook", "MouseArrow")

#---------------------------------#
    def _createCamera(self):
        self.camera = self.sceneManager.createCamera('PlayerCam')
        self.camera.nearClipDistance = 5

#---------------------------------#
    def _createFrameListener(self):
        self.frameListener = GAListener(self.renderWindow, self.camera, self.sceneManager,
                                        self.ceguiRenderer, self.ind_nodes)
        self.root.addFrameListener(self.frameListener)
        self.frameListener.showDebugOverlay(True)

#---------------------------------#


if __name__ == '__main__':
    try:
        ta = TutorialApp()
        ta.go()
    except ogre.OgreException, e:
        print e
