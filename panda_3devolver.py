import math
import sys

#import direct.directbase.DirectStart
from direct.showbase import ShowBase
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *

from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *

import evolve

ShowBase.ShowBase()


class MeshEvolver(DirectObject):
    def __init__(self):

        base.oobe()
        self.initEntities()

        #self.start_x = base.win.getXSize()

        [self.accept("%d" % i, self.selectBest, ['%d' % i]) for i in range(0,9)]
        self.accept('escape', sys.exit)

        #self.setupPicker()

##-------------------------------------------#
#    def setupPicker(self):
#
#        picker_node = CollisionNode('mouseRay')
#        pickerNP = camera.attachNewNode(picker_node)
#        picker_node.setFromCollideMask(GeomNode.getDefaultCollideMask())
#        pickerRay = CollisionRay()
#        picker_node.addSolid(pickerRay)


#-------------------------------------------#
    def initEntities(self):
        # load default entity, set texture and default configuration of mesh
        # then make copies to render
        ent = loader.loadModel("../mesh/nsplitninja")
        tex = loader.loadTexture('../mesh/textures/spacesky.jpg')
        ent.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        ent.setTexture(tex)
        #ent.showBounds()
        # last coord is height
        ent.setPos(0, 0, 0)
        ent.setHpr(0, -90, 180)
        #ent.setScale(0.5, 0.5, 0.5)
        self.root_ent = ent

        scale_factor = 0.5
        pos_offset = 10
        ent_list = [ent.copyTo(NodePath('Individual')) for i in range(9)]
        self.entity_list = ent_list
        for i, entity in enumerate(ent_list):
            entity.reparentTo(render)
            entity.setPos(i*10, 0, 0)
            entity.setScale(scale_factor, scale_factor, scale_factor)

            #nodes = entity.findAllMatches('**/+GeomNode')
            #l = nodes.asList()
            #for path in nodes.asList():
            #    g_node = path.node()
            #    #ent.setScale(scale_factor, scale_factor, scale_factor)
            #    ent.setHpr(0,-90,180)
            #    mat = ent.getMat()
            #    #newCS = Mat4(   3, 0, 0, 0,
            #    #                0, 3, 0, 0,
            #    #                0, 0, 3, 0,
            #    #                0, 0, 0, 1)
            #    g_node.setTransform(TransformState.makeMat(mat))



        #scale_factor = 0.1
        #for i in range(9):
        #    place_holder = render.attachNewNode('ent-place-holder')
        #    place_holder.setPos(i*5, 0, 0)
        #    place_holder.setScale(i*scale_factor, i*scale_factor, i*scale_factor)
        #    ent.instanceTo(place_holder)
        #    nodes = place_holder.findAllMatches('**/+GeomNode')
        #    l = nodes.asList()
        #    if i == 4:
        #        for path in nodes.asList():
        #            g_node = path.node()
        #            newCS = Mat4(1,-0.3,0,0,
        #                            0,1,2,0,
        #                            0,0,1,0,
        #                            0,0,0,1)
        #            g_node.setTransform(TransformState.makeMat(newCS))
               

        nodes = ent.findAllMatches('**/+GeomNode')
        l = nodes.asList()

        curstudy = 'character3d.yml'
        ga = evolve.init_iga({'app_name': curstudy, 'geomNodes': len(l)})
        self.genomes = ga.draw()
        self.ga = ga
        self.newPop()

#----------------------------------------#
    def newPop(self):
        # for every entity in scene
        for i, entity in enumerate(self.entity_list):
            entity_genes = self.genomes[i]
            # for every geomnode
            nodes = entity.findAllMatches('**/+GeomNode')
            for j, path in enumerate(nodes.asList()):
                node_genes = entity_genes[j]
                sx, sy, sz = node_genes['sx'], node_genes['sy'], node_genes['sz']
                rx, ry, rz = node_genes['rx'], node_genes['ry'], node_genes['rz']
                g_node = path.node()

                self.root_ent.clearMat()
                self.root_ent.clearTransform()
                self.root_ent.setScale(sx, sy, sz)
                self.root_ent.setHpr(rx, ry, rz)
                mat = self.root_ent.getMat()
                g_node.clearTransform()
                g_node.setTransform(TransformState.makeMat(mat))

#----------------------------------------#
    def selectBest(self, num):
        print num, 'selected', type(num)
        best_selected = int(num)
        self.genomes = self.ga.web_step({'feedback': [best_selected]})
        self.newPop()

#----------------------------------------#


if __name__ == '__main__':
    evolv = MeshEvolver()
    run()
