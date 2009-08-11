#try:
#    import psyco
#    psyco.full()
#except:
#    print 'no psyco'


import sys
import random
import ctypes

sys.path.insert(0,'..')
import PythonOgreConfig

import ogre.renderer.OGRE as ogre
import ogre.gui.CEGUI as CEGUI
import ogre.io.OIS as OIS
import SampleFramework as sf

import evolve

SPACE = 250
VSPACE = 300
MOVE = 500


NEXTID = 1
NEXTNUM = 1
GEN_COUNTER = 0

#-------------------------------------------#
def tempName():
    global NEXTID
    id = NEXTID
    NEXTID += 1
    return 't%d'%id

def nextNum():
    global NEXTNUM
    NEXTNUM += 13
    return NEXTNUM


def get_width_height(cur_node):
    aab = cur_node.getAttachedObject(0).getBoundingBox();
    min = aab.getMinimum() * cur_node.getScale();
    max = aab.getMaximum() * cur_node.getScale();
    center = aab.getCenter() * cur_node.getScale();
    size = ogre.Vector3(abs(max.x - min.x), abs(max.y - min.y), abs(max.z - min.z))
    rad = size.z / 2. if size.x > size.z else size.x / 2.0
    width = size.z if size.x > size.z else size.x
    height = size.y
    return width, height


class GAListener(sf.FrameListener, OIS.MouseListener, OIS.KeyListener):

    OBJ_MASK = 1 << 1

    def __init__(self, renderWindow, camera, sceneManager, cegui):#, ind_nodes):
        sf.FrameListener.__init__(self, renderWindow, camera, True, True)
        OIS.MouseListener.__init__(self)
        OIS.KeyListener.__init__(self)

        # initialized with garbage intentional
        self.peer_genomes = [0]
        self.toggle = 0
        self.mouse_down = False

        self.cam_node = camera.parentSceneNode.parentSceneNode
        self.sceneManager = sceneManager
        self.cegui = cegui

        # Register as MouseListener (Basic tutorial 5)
        self.Mouse.setEventCallback(self)
        self.Keyboard.setEventCallback(self)

        collab = False
        import sys
        if len(sys.argv) > 1:
            collab = True

        #curstudy = 'delta_tree_character3d.yml'
        curstudy = 'vertex_shader.yml'
        l = 7
        ga = evolve.init_iga({'app_name': curstudy, 'geomNodes': l, 'collaborate': collab})
        self.genomes = ga.draw()
        self.ga = ga

        j, vj, vi, offset = 0, 0, 0, SPACE * 4

        # begin animation stuff
        ogre.Animation.setDefaultInterpolationMode(ogre.Animation.IM_SPLINE)
        self.animationStates = []
        self.animationSpeeds = []

        # end animation stuff

        mesh = 'ninja.mesh'
        #mesh = 'robot.mesh'
        # create nodes to hold subset models and peers
        peer_nodes = []
        ind_nodes = []
        for i in range(len(self.genomes)):

            name = 'Node_%d_%d' % (i, (nextNum()))
            ent = sceneManager.createEntity(name, mesh)
            ent.setQueryFlags(self.OBJ_MASK)

            self.animationStates.append(ent.getAnimationState('Walk'))
            self.animationStates[-1].Enabled = True
            #self.animationSpeeds.append(ogre.Math.RangeRandom(0.5, 1.5))
            self.animationSpeeds.append(1.0)

            node = sceneManager.getRootSceneNode().createChildSceneNode('Individual%d' % i)
            node.attachObject(ent)
            #node.position = (vi*SPACE, vj*VSPACE, vi*SPACE)
            node.position = (vi*SPACE, vj*VSPACE, 0)
            # incremental diagonal placement
            #node.position = (vi*SPACE, vj*VSPACE, 0)
            node.yaw(-135)
            #node.yaw(-90)

            #sep_node = sceneManager.getRootSceneNode().createChildSceneNode('Separator%d' % i)
            #sep_node.position = (0,0,0)
            #sep_node.setScale(0.25, 0.25, 0.25)

            #ent = sceneManager.createEntity('Separator%d' %i, 'knot.mesh')
            #ent.setMaterialName('Examples/OgreLogo')
            #sep_node.attachObject(ent)
            #sep_node.setVisible(True)
            #sep_node.position = (vi*SPACE, vj*VSPACE + offset, vi*SPACE + offset)


            name = 'Peer_%d_%d' % (i, (nextNum()))
            ent = sceneManager.createEntity(name, mesh)
            ent.setQueryFlags(self.OBJ_MASK)

            self.animationStates.append(ent.getAnimationState('Walk'))
            self.animationStates[-1].Enabled = True
            self.animationSpeeds.append(ogre.Math.RangeRandom(0.5, 1.5))

            p_node = sceneManager.getRootSceneNode().createChildSceneNode('Peer%d' % i)
            p_node.attachObject(ent)
            #p_node.position = (vi*SPACE + offset, vj*VSPACE, vi*SPACE + offset)
            p_node.position = (vi*SPACE+offset, vj*VSPACE, 0)
            p_node.yaw(-135)
            #p_node.yaw(-180)
            p_node.setVisible(True)

            vi += 1
            j += 1
            if j % 3 == 0:
                vj -= 1
                vi = 0

            ind_nodes.append(node)
            peer_nodes.append(p_node)

        self.ind_nodes = ind_nodes
        self.peer_nodes = peer_nodes

        # add screen splitter
        split = sceneManager.getRootSceneNode().createChildSceneNode('ScreenSplit')
        ent = sceneManager.createEntity('SplitMesh', 'column.mesh')
        split.attachObject(ent)
        split.position = (3*SPACE, -SPACE*2, 0)
        split.setScale(0.25, 5.0, 0.25)


        self.pic_count = 0

        self.mesh_rotate = 0.

        self.rotate = 0.20
        self.move = MOVE

        self.currentObject = None

        self.best_selected = {'index': None, 'individual': None}
        self.peer_selected = {}

        self.raySceneQuery = None
        self.raySceneQuery = self.sceneManager.createRayQuery(ogre.Ray())


        self.num_keys = ['%d' % i for i in range(10)]

        self.all_online = False
        self.collaborate = False

        #self.prev_cam = 

#---------------------------------#
    def mouseMoved(self, evt):
        CEGUI.System.getSingleton().injectMouseMove(evt.get_state().X.rel, evt.get_state().Y.rel)
        #x = evt.get_state().X.rel
        #y = evt.get_state().Y.rel
        #self.cam_node.yaw(ogre.Degree(-self.rotate * x).valueRadians())
        #self.cam_node.getChild(0).pitch(ogre.Degree(-self.rotate * y).valueRadians())
        return True

#---------------------------------#
    def mousePressed(self, evt, id):
        if id == OIS.MB_Left:
            self.onLeftPressed(evt)
        if id == OIS.MB_Right:
            self.onRightPressed(evt)
        return True
 
#---------------------------------#
    def mouseReleased(self, evt, id):
        return True

#---------------------------------#
    def keyPressed(self, evt):

        if evt.key is OIS.KC_N:
            self.newPop()

        elif evt.key is OIS.KC_RETURN:
            print 'the best selected are ', self.best_selected
            print 'from peers', self.peer_selected
            if self.best_selected['index'] is not None:
                b_index = self.best_selected['index']
                inject = self.peer_selected.keys()

                c = {'feedback': [b_index], 'inject_genomes': inject}
                c['user'] = self.ga.getVar('user')
                self.genomes = self.ga.web_step(c)

                if self.collaborate:
                    self.peer_genomes = self.ga.get_peer_genomes()

                self.best_selected['individual'].showBoundingBox(False)
                self.best_selected['index'] = None
                self.best_selected['individual'] = None

                for ind in self.peer_selected.values(): ind.showBoundingBox(False)
                self.peer_selected = {}

                self.newPop()

        elif evt.key is OIS.KC_R:
            self.collaborate = True
            self.all_online = self.ga.pingPeers()
            print 'result', self.all_online

        elif evt.key is OIS.KC_J:
        # save best
            if self.best_selected['index'] is not None:


                global GEN_COUNTER
                if GEN_COUNTER > 0:
                    b_index = self.best_selected['index']
                    f = open('save_best', 'a')
                    t = GEN_COUNTER
                    t -= self.ga.getVar('stepSize')
                    prefix = self.ga.getVar('user')
                    m = '%s_gen_%d_ind_%d\n' % (prefix, t,b_index)
                    f.write(m)
                    f.close()

        elif evt.key is not OIS.KC_ESCAPE:
            pass
            #best_selected = self.Keyboard.getAsString(evt.key)
            #if self.ga and best_selected in self.num_keys:
            #    print 'pressed', self.Keyboard.getAsString(evt.key)
            #    best_selected = int(best_selected)
            #    best_selected -= 1
            #    if best_selected >= 0 and best_selected < 9:
            #        self.genomes = self.ga.web_step({'feedback': [best_selected]})
            #        self.newPop()

        else:
            self.ga.exit()

        return True

#---------------------------------#
    def keyReleased(self, evt):
        return True

#---------------------------------#
    def frameStarted(self, frameEvent):
        if self.renderWindow.isClosed():
            return False

        for index in range(len(self.animationStates)):
            self.animationStates[index].addTime(frameEvent.timeSinceLastFrame * self.animationSpeeds[index])

        #self.mesh_rotate += 0.1
        #self.mesh_rotate %= 360
        #for i, node in enumerate(self.ind_nodes):
        #    node.yaw(self.mesh_rotate)


        #self.renderWindow.writeContentsToFile('pic_%d.png' % self.pic_count)
        #self.pic_count += 1

        #self.renderWindow.debugText = "Hello world"

        self.Keyboard.capture()
        self.Mouse.capture()

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

        if self.Keyboard.isKeyDown(OIS.KC_UP):
            transVector.y += self.move
        if self.Keyboard.isKeyDown(OIS.KC_DOWN):
            transVector.y -= self.move

        if self.Keyboard.isKeyDown(OIS.KC_LEFT):
            transVector.x -= self.move
        if self.Keyboard.isKeyDown(OIS.KC_RIGHT):
            transVector.x += self.move

        
        if self.Keyboard.isKeyDown(OIS.KC_W):
            transVector.z -= self.move
        if self.Keyboard.isKeyDown(OIS.KC_S):
            transVector.z += self.move

        if self.Keyboard.isKeyDown(OIS.KC_A):
            transVector.x -= self.move
        if self.Keyboard.isKeyDown(OIS.KC_D):
            transVector.x += self.move

        if self.Keyboard.isKeyDown(OIS.KC_PGUP):
            transVector.z -= self.move
        if self.Keyboard.isKeyDown(OIS.KC_PGDOWN):
            transVector.z += self.move

        if self.Keyboard.isKeyDown(OIS.KC_Z):
            transVector.y -= self.move
        if self.Keyboard.isKeyDown(OIS.KC_C):
            transVector.y += self.move


        ms = self.Mouse.getMouseState()
        if ms.buttonDown( OIS.MB_Right ):
            rotationX = ogre.Degree(- ms.X.rel )
            rotationY = ogre.Degree(- ms.Y.rel )
            self.camera.yaw(rotationX)
            self.camera.pitch(rotationY)

        #self.cam_node.translate(self.cam_node.orientation * transVector * frameEvent.timeSinceLastFrame)
        self.camera.moveRelative(transVector * frameEvent.timeSinceLastFrame)

        #if curr_mouse.buttonDown(OIS.MB_Right):
        #    self.cam_node.yaw(ogre.Degree(-self.rotate * curr_mouse.X.rel).valueRadians())
        #    self.cam_node.getChild(0).pitch(ogre.Degree(-self.rotate * curr_mouse.Y.rel).valueRadians())

        if not sf.FrameListener.frameStarted(self, frameEvent):
            return False

        return not self.Keyboard.isKeyDown(OIS.KC_ESCAPE)
    
#---------------------------------#
    def onRightPressed(self, evt):
 
        # Setup the ray scene query, use CEGUI's mouse position
        mousePos = CEGUI.MouseCursor.getSingleton().getPosition()
        mouseRay = self.camera.getCameraToViewportRay(mousePos.d_x / float(evt.get_state().width),
                                                      mousePos.d_y / float(evt.get_state().height))
        self.raySceneQuery.setRay(mouseRay)
        self.raySceneQuery.setSortByDistance(True)
        self.raySceneQuery.setQueryMask(self.OBJ_MASK)
 
        # Execute query
        result = self.raySceneQuery.execute()
        if len(result) > 0:
            for item in result:
                if item.movable:
                    name = item.movable.getName()
                    # if model
                    if name.startswith('Node') or name.startswith('Peer'):
                        cur_object = item.movable.getParentSceneNode()
                        print item.movable.getParentSceneNode().getName()
                        print item.movable.getName()

                        ind_index = int(name.split('_')[1])
                        # my own model
                        if name.startswith('Node'):
                            # unselect individual
                            if self.best_selected['individual']:
                                self.best_selected['individual'].showBoundingBox(False)
                                # if selecting same individual, clear selection
                                if ind_index == self.best_selected['index']:
                                    self.best_selected['individual'] =  None
                                    self.best_selected['index'] =  -1
                                else:
                                    cur_object.showBoundingBox(True)
                                    self.best_selected['individual'] = cur_object
                                    self.best_selected['index'] = ind_index
                            else:
                                cur_object.showBoundingBox(True)
                                self.best_selected['individual'] = cur_object
                                self.best_selected['index'] = ind_index

                        # model belonging to peers
                        else:
                            found = self.peer_selected.get(ind_index, None)
                            if found:
                                cur_object.showBoundingBox(False)
                                self.peer_selected.pop(ind_index)
                            else:
                                cur_object.showBoundingBox(True)
                                self.peer_selected[ind_index] = cur_object

                        break # We found an existing object
 

#---------------------------------#
    def onLeftPressed(self, evt):
 
        # Setup the ray scene query, use CEGUI's mouse position
        mousePos = CEGUI.MouseCursor.getSingleton().getPosition()
        mouseRay = self.camera.getCameraToViewportRay(mousePos.d_x / float(evt.get_state().width),
                                                      mousePos.d_y / float(evt.get_state().height))
        self.raySceneQuery.setRay(mouseRay)
        self.raySceneQuery.setSortByDistance(True)
        self.raySceneQuery.setQueryMask(self.OBJ_MASK)
 
        # Execute query
        result = self.raySceneQuery.execute()
        if len(result) > 0:
            for item in result:
                if item.movable:
                    name = item.movable.getName()
                    # if model
                    if name.startswith('Node') or name.startswith('Peer'):
                        cur_object = item.movable.getParentSceneNode()
                        print item.movable.getParentSceneNode().getName()
                        print item.movable.getName()

                        ind_index = int(name.split('_')[1])
                        # my own model
                        if name.startswith('Node'):
                            # unselect individual
                            if self.best_selected['individual']:
                                self.best_selected['individual'].showBoundingBox(False)
                                # if selecting same individual, clear selection
                                if ind_index == self.best_selected['index']:
                                    self.best_selected['individual'] =  None
                                    self.best_selected['index'] =  -1
                                else:
                                    cur_object.showBoundingBox(True)
                                    self.best_selected['individual'] = cur_object
                                    self.best_selected['index'] = ind_index
                            else:
                                cur_object.showBoundingBox(True)
                                self.best_selected['individual'] = cur_object
                                self.best_selected['index'] = ind_index

                        # model belonging to peers
                        else:
                            found = self.peer_selected.get(ind_index, None)
                            if found:
                                cur_object.showBoundingBox(False)
                                self.peer_selected.pop(ind_index)
                            else:
                                cur_object.showBoundingBox(True)
                                self.peer_selected[ind_index] = cur_object

                        break # We found an existing object
 

#----------------------------------------#
    def newPop(self):
        '''
        Create and display a new pop.
        '''
        global GEN_COUNTER
        # ----------------------------------------- #
        user = self.ga.getVar('user')
        ind_gen = '%s_gen' % user
        peer_gen = '%s_peer_gen' % user

        prefix = [ind_gen]
        if self.collaborate and self.peer_genomes:
            prefix = [ind_gen, peer_gen] if GEN_COUNTER else [ind_gen]

        for sf in ['cg', 'program', 'material']:
                
                #prefix = ['gen', 'peer_gen'] if GEN_COUNTER else ['gen']
                for d in prefix:
                    # dynamic loading of material
                    f= file("%s_%d.%s" % (d, GEN_COUNTER, sf), 'r')
                    MatString = f.read()
                    f.close()
                    RawMemBuffer = ctypes.create_string_buffer( MatString  ) ## Note it allocates one extra byte
                    ## Now we create the MemoryDataStream using the void pointer to the ctypes buffer
                    dataptr = ogre.MemoryDataStream ( pMem = ogre.CastVoidPtr(ctypes.addressof ( RawMemBuffer )), 
                            size = len (MatString) + 1 )

                    ogre.MaterialManager.getSingleton().parseScript(dataptr, ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME)

        # ----------------------------------------- #


        sceneManager = self.sceneManager

        print self.genomes

        for i, node in enumerate(self.ind_nodes):
            ent = node.getAttachedObject(0)
            m = '%s_%d_ind_%d' % (ind_gen, GEN_COUNTER,i)
            ent.setMaterialName(m)


        if self.collaborate and GEN_COUNTER > 0:

            for i, node in enumerate(self.peer_nodes):
                ent = node.getAttachedObject(0)
                m = '%s_%d_ind_%d' % (peer_gen, GEN_COUNTER,i)
                ent.setMaterialName(m)



        GEN_COUNTER += self.ga.getVar('stepSize')


#----------------------------------------#

class TutorialApp(sf.Application):

    def _createScene(self):

        self.ceguiRenderer = CEGUI.OgreCEGUIRenderer(self.renderWindow, ogre.RENDER_QUEUE_OVERLAY, False, 3000, self.sceneManager)

        self.ceguiSystem = CEGUI.System(self.ceguiRenderer)
        sceneManager = self.sceneManager
        sceneManager.ambientLight = 0.75, 0.75, 0.75


        light = sceneManager.createLight('Light1')
        light.type = ogre.Light.LT_POINT
        light.position = (0, 1000, -500)
        light.diffuseColour = (1, 1, 1)
        light.specularColour = (1, 1, 1)

        j, vj, vi = 1, 1, 1
        #node = sceneManager.getRootSceneNode().createChildSceneNode('CamNode1', (-800, -400, 600))
        node = sceneManager.getRootSceneNode().createChildSceneNode('CamNode1', (SPACE, -200, 1000))
        #node.yaw(ogre.Degree(-45))

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
        self.camera.setDirection(ogre.Vector3(0, 0, -1))
        #self.camera.lookAt(ogre.Vector3(0, 0, 0))

#---------------------------------#
    def _createFrameListener(self):
        self.frameListener = GAListener(self.renderWindow, self.camera, self.sceneManager,
                                        self.ceguiRenderer)#, self.ind_nodes)
        self.root.addFrameListener(self.frameListener)
        self.frameListener.showDebugOverlay(True)

#---------------------------------#


if __name__ == '__main__':
    try:
        ta = TutorialApp()
        ta.go()
    except ogre.OgreException, e:
        print e
