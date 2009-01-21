import sys
sys.path.insert(0,'..')
import PythonOgreConfig

import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import SampleFramework as sf


class TutorialFrameListener(sf.FrameListener):

    def __init__(self, renderWindow, camera, sceneManager):
        sf.FrameListener.__init__(self, renderWindow, camera)

        self.toggle = 0
        self.mouse_down = False

        self.cam_node = camera.parentSceneNode.parentSceneNode
        self.scene_manager = sceneManager

        self.rotate = 0.13
        self.move = 250


    def frameStarted(self, frameEvent):
        if self.renderWindow.isClosed():
            return False

        self.Keyboard.capture()
        self.Mouse.capture()

        curr_mouse = self.Mouse.getMouseState()

        if curr_mouse.buttonDown(OIS.MB_Left) and not self.mouse_down:
            light = self.scene_manager.getLight('Light1')
            light.visible = not light.visible

        self.mouse_down = curr_mouse.buttonDown(OIS.MB_Left)

        if self.toggle >= 0:
            self.toggle -= frameEvent.timeSinceLastFrame


        if self.toggle < 0 and self.Keyboard.isKeyDown(OIS.KC_1):
            self.toggle = 0.1
            self.camera.parentSceneNode.detachObject(self.camera)
            self.cam_node = self.scene_manager.getSceneNode('CamNode1')
            self.scene_manager.getSceneNode('PitchNode1').attachObject(self.camera)

        elif self.toggle < 0 and self.Keyboard.isKeyDown(OIS.KC_2):
            self.toggle = 0.1
            self.camera.parentSceneNode.detachObject(self.camera)
            self.cam_node = self.scene_manager.getSceneNode('CamNode2')
            self.scene_manager.getSceneNode('PitchNode2').attachObject(self.camera)


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

        if curr_mouse.buttonDown(OIS.MB_Right):
            self.cam_node.yaw(ogre.Degree(-self.rotate * curr_mouse.X.rel).valueRadians())
            self.cam_node.getChild(0).pitch(ogre.Degree(-self.rotate * curr_mouse.Y.rel).valueRadians())

        return not self.Keyboard.isKeyDown(OIS.KC_ESCAPE)



class TutorialApp(sf.Application):

    def _createScene(self):
        sceneManager = self.sceneManager
        sceneManager.ambientLight = 0.25, 0.25, 0.25

        cube = sceneManager.createEntity('Cube', 'cube.mesh')
        cube_node = sceneManager.getRootSceneNode().createChildSceneNode('CubeNode')
        cube_node.attachObject(cube)
        cube_node.position = (80,0,0)
        cube_node.setScale(0.01, 1, 1)
        cube_node.yaw(ogre.Degree(45))

        sphere = sceneManager.createEntity('Sphere', 'sphere.mesh')
        sphere_node = sceneManager.getRootSceneNode().createChildSceneNode('SphereNode')
        sphere_node.attachObject(sphere)
        sphere_node.position = (-80,0,0)

        entity = sceneManager.createEntity('Ninja', 'ninja.mesh')
        node = sceneManager.getRootSceneNode().createChildSceneNode('NinjaNode')
        node.attachObject(entity)

        mesh_mg = ogre.MeshManager.getSingleton()
        ninja = mesh_mg.getByName('ninja.mesh')
        print '^' * 30, ninja.getNumSubMeshes()

        light = sceneManager.createLight('Light1')
        light.type = ogre.Light.LT_POINT
        light.position = (250, 150, 250)
        light.diffuseColour = (1, 1, 1)
        light.specularColour = (1, 1, 1)

        node = sceneManager.getRootSceneNode().createChildSceneNode('CamNode1', (-400, 200, 400))
        node.yaw(ogre.Degree(-45))

        node = node.createChildSceneNode('PitchNode1')
        node.attachObject(self.camera)

        node = sceneManager.getRootSceneNode().createChildSceneNode('CamNode2', (0, 200, 400))
        node.createChildSceneNode('PitchNode2')


    def _createCamera(self):
        self.camera = self.sceneManager.createCamera('PlayerCam')
        self.camera.nearClipDistance = 5

    def _createFrameListener(self):
        self.frameListener = TutorialFrameListener(self.renderWindow, self.camera, self.sceneManager)
        self.root.addFrameListener(self.frameListener)
        self.frameListener.showDebugOverlay(True)



if __name__ == '__main__':
    try:
        ta = TutorialApp()
        ta.go()
    except ogre.OgreException, e:
        print e
