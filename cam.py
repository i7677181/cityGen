## @package ultraMaya_turntable
# @brief turntable script
#

import maya.cmds as cmds
import pymel.core as pm
# import inspect
import math as m
from PySide import QtGui, QtCore
import os


# cam = pm.ls(type='camera')[0]
# repr(cam)

##--------------------------------------------------------------------------------------------------##
# positions camera, constrain bbox to locator for rotation
##--------------------------------------------------------------------------------------------------##
def setupCamera(fov, punch, view,frames):
    # set hdri image
    pm.mel.eval('redshiftCreateDomeLight;')
    pm.mel.eval('MASHnewNodeCallback( "rsDomeLightShape1");')
    pm.mel.eval('setAttr -type "string" rsDomeLightShape1.tex0 "Q:/Lighting/hdriBrowser/outdoor/sunny/park/BourenmouthCentralParkSunny_7k_22EV_HDR.exr";')
    pm.mel.eval('currentTime 1;')
    pm.mel.eval('setAttr "rsDomeLight1.rotateY" 0;')
    pm.mel.eval('setKeyframe { "rsDomeLight1.r" };')
    pm.mel.eval('currentTime {0};'.format(frames))
    pm.mel.eval('setAttr "rsDomeLight1.rotateY" 360;')
    pm.mel.eval('setKeyframe { "rsDomeLight1.r" };')

    # ui input
    isTopView = view
    # get bbox
    geo = pm.ls(type='dagContainer')
    geo = geo[0]
    centerPivot(geo)
    print "imported  ", geo
#    assignShaderToObj(geo)
    # get bbox
    bbox = geo.boundingBox()
    # Create a camera and get the shape name.
    cameraName = pm.camera()
    cameraShape = cameraName[1]
    print "camera{0} looking at{1}\n".format(cameraShape, geo)
    # create locator and parent to geo
    locator = pm.spaceLocator()
    # set rotation
    locator.rotateY.setKey(t=0, v=0)
    locator.rotateY.setKey(t=frames, v=360)

    # set usr fov , get vertical fov
    cameraShape.setHorizontalFieldOfView(fov)
    vfov = cameraShape.getVerticalFieldOfView()
    print "vfov:", vfov

    cameraShape.displayCameraFrustum.set(1)
    # bbox width,height horizontal
    # y = abs(bbox[0][2])
    # x = abs(bbox[0][0])

    y_v = abs(bbox[1][1])  # vertical height
    x_v = abs(bbox[0][0])  # vertical width
    z_v = abs(bbox[1][2])   # vertical depth
    print "vertical size:", y_v, x_v, z_v
    #  math stuff
    # calc horizontal radius
 #   h_r = calcDiag(y, x)
    # calc dist
#    h_dist = calcDist(h_r, fov)

    v_r = calcDiag(y_v, x_v)
    v_dist = calcDist(v_r, vfov)

    print "vDiag:{0},vDist:{1}".format(v_r,v_dist)

    #  if top view enabled, rotate cam then dolly in viewing dir
    if isTopView:
        print "top", isTopView
        rot_mat = cameraName[0].getRotation()
        rot_mat[0] = -90
        cameraName[0].setRotation(rot_mat)

    ##  translate camera
    #  @note temporarily using dolly cuz its faster
    cameraShape.dolly(v_dist)

    #  check if camera is inside bbox
    camPos = cameraName[0].getTranslation()
    print "campos:",camPos, z_v

    # if camera is inside bbox even after dolly, reposition
    if z_v >= camPos[2]:
        print "cam inside bbox"
        # calculate new distance based on bbox Z
        newDiag = calcDiag(z_v, x_v)
        newDist2 = calcDist(newDiag, vfov)
        print "new", newDist2
        cameraShape.dolly(v_dist*newDist2)

    """"
    after done calculating camera distance from obj bbox,
    parent obj to locator for rotation
    parenting duplicates the object in the outliner,creating 
    empty referenced group 
    """
    geo = pm.parent(geo, locator)
    print "parented", geo, "to", locator

    #  set render cam
    if cameraShape.getAttr('renderable')==False:
        cameraShape.setAttr('renderable', True)
        print "setting {0} as renderable".format(cameraShape)
    pm.renderSettings(cam=cameraShape)

    # create proxy
    pm.select(clear=True)
    proxy = pm.mel.eval("redshiftCreateProxy")
    proxyNode = pm.ls(proxy)[0]
    proxyNode.setAttr('fileName', str(geo))


    # scale props
    prop = pm.ls("props_GRP")
    grd = pm.ls("groundPlane_GEO")
    grd[0].setTranslation([0, -51, 0])
    offsetZ = v_r
    offsetY = v_r * 0.50
    offsetX = v_r * 0.70
    s = float(v_r)
    su = float(s / 100) # to unit scale
    prop[0].setScale([su, su, su])
    prop[0].setTranslation([offsetX, offsetY, offsetZ])

    pm.group(cameraShape, locator, proxy, 'redshiftProxyPlaceholder1', n="deleteMe")


##--------------------------------------------------------------------------------------------------##
# calculate diagonal of model's bbox
##--------------------------------------------------------------------------------------------------##
def calcDiag(_y, _x):
    x = _x
    y = _y
    r = m.sqrt(x * x + y * y)
    return r


##--------------------------------------------------------------------------------------------------##
# calculate new position for camera based on bbox radius/diagonal and cam fov
##--------------------------------------------------------------------------------------------------##
def calcDist(_r, _fov):
    r = _r
    fov = m.sin(m.radians(_fov / 2))
    dist = r / fov
    return dist


##--------------------------------------------------------------------------------------------------##
# delete previously created camera and locator
##--------------------------------------------------------------------------------------------------##
def clear():
    # delete previous
    allObj = pm.ls(type=['camera','locator','dagContainer'])
    if allObj:
        try:
            for obj in allObj:
                print "deleting ", obj
                pm.delete(obj)
            pm.delete(allObj)
        except: "ERROR:failed clearing previous scene"
    else: print "nothing to delete"

    try:
        prevGrp = pm.select("deleteMe")
        pm.delete("deleteMe")
    except:
        print "nothing to delete?"
##--------------------------------------------------------------------------------------------------##
# ui class to get specifications for turntable
##--------------------------------------------------------------------------------------------------##
class TurntableUI(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("turntable settings")
        mainLay = QtGui.QVBoxLayout()
        subLay = QtGui.QHBoxLayout()

        # init default values
        self.fov = 45
        self.frames = 30
        self.punch = 1

        self.top_chk = QtGui.QCheckBox("top view")
        ok_btn = QtGui.QPushButton("ok")
        ok_btn.clicked.connect(self.getStuff)

        self.cb_frame = QtGui.QComboBox()
        self.cb_frame.addItem("290")
        self.cb_frame.setEditable(True)

        self.cb_fov = QtGui.QComboBox()
        self.cb_fov.addItem("45")
        self.cb_fov.setEditable(True)

        #  punch slider
        self.sld_punch = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.sld_punch.setMaximum(10)
        self.sld_punch.setMinimum(1)
        self.sld_punch.setValue(1)
        self.sld_punch.setSingleStep(1)
        self.sld_punch.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sld_punch.setTickInterval(5)
        self.sld_punch.valueChanged.connect(self.getMoreStuff)

        # the validator will only accept integers between 1 and 290
        validator = QtGui.QIntValidator(1, 290, self)
        validator_f = QtGui.QIntValidator(1, 500, self)
        self.cb_fov.setValidator(validator)
        self.cb_frame.setValidator(validator_f)

        lbl_fr = QtGui.QLabel("Frames:")
        lbl_fov = QtGui.QLabel("FOV:")
        lbl_0 = QtGui.QLabel("0")
        lbl_10 = QtGui.QLabel("10")

        subLay.addWidget(lbl_fr)
        subLay.addWidget(self.cb_frame)
        subLay.addWidget(lbl_fov)
        subLay.addWidget(self.cb_fov)
        subLay.addWidget(lbl_0)
        subLay.addWidget(self.sld_punch)
        subLay.addWidget(lbl_10)
        subLay.addWidget(self.top_chk)
        subLay.addWidget(ok_btn)

        mainLay.addLayout(subLay)
        self.setLayout(mainLay)

        self.exec_()

    ##--------------------------------------------------------------------------------------------------##
    # get user frames, fov, possibly comment
    ##--------------------------------------------------------------------------------------------------##
    def getStuff(self):
        self.frames = self.cb_frame.currentText()
        self.fov = self.cb_fov.currentText()

        print self.frames, self.fov, self.punch
        self.hide()
        topView = self.top_chk.isChecked()
        setupCamera(int(self.frames), int(self.fov), int(self.punch),topView)

    ##--------------------------------------------------------------------------------------------------##
    # get extra attributes, additional distance
    ##--------------------------------------------------------------------------------------------------##
    def getMoreStuff(self):
        self.punch = int(self.sld_punch.value())
        return self.punch


##--------------------------------------------------------------------------------------------------##
# get cwd path,save scene and show ui
##--------------------------------------------------------------------------------------------------##
def showUI():
    # path = pm.mel.eval("pwd") #  path to script
    path = pm.workspace(q=True, rootDirectory=True)

    ui = TurntableUI()
    ui.show()

def setRenderSettings(_in,_cam):
    cam = _cam
    pm.renderSettings(cam=cam)

def assignShaderToObj(_obj):
    # assign shader
    mtl = pm.shadingNode("RedshiftArchitectural", asShader=True, name="rsMtl")
    mtlShader = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name="tmp")
    mtl.outColor >> mtlShader.surfaceShader
    pm.sets(mtlShader, edit=True, forceElement=_obj)
    pm.hyperShade("tml", _obj, assign=True)
    return _obj
    print "applied shader? D:\n"
def centerPivot(obj):
    obj.centerPivots()
    pm.manipPivot(p=(0,0,0),snapPos=True)
    obj.setTranslation((0,0,0))
    pm.select(obj)
    pm.mel.eval('move -rpr -y 0')
    pm.mel.eval('manipPivot -p 0 0 0')
    pm.delete(obj, constructionHistory=True)
    pm.makeIdentity(obj,apply=True,t=1,r=1,s=1,n=0)
    print "centered pivot of {0}\n".format(obj)
