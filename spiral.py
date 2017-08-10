import maya.cmds as cmds
import pymel.core as pm
import random
from math import *
_obj = ""
_amount = 2
files = ""
isImport=False
origin = 0 
rad = 5
t = 45
obj= pm.ls(sl=True)
obj=obj[0]
make(1,obj,1)
def make(_amount,_obj,_rgb):
    a = 1
    theta = 0.0
    r = a
    prev_x = int(r*cos(theta))
    prev_y = int(r*sin(theta))
    while theta < 2 * loops * pi:
        theta += step
        r = a + b*theta
        # Draw pixels, but remember to convert to Cartesian:
        x = int(r*cos(theta))
        y = int(r*sin(theta))
        obj.setTranslation((prev_x, 0,prev_y))
        prev_x = x
        prev_y = y

    cmds.select(all=True)
    fileList = cmds.ls(sl=True)
    print fileList
    for obj in fileList:
        print obj
        pm.mel.eval('duplicate {0}; move 3 0 0; duplicate -st; duplicate -st;'.format(obj))   




def scatter(_obj):
    # random position obj here
    print "scatter"
def UI():
    cityWindow = cmds.window(title = 'importer', wh = (400, 200), s = True) 
    cmds.columnLayout(adjustableColumn = True, rowSpacing = 5, cw=100, cal = 'left')
    cmds.text(label = 'Name of :')
    cmds.textFieldGrp('Name', ann = 'Name Of :', tx = 'smth')
    cmds.button(label="import geo",width = 150, align = 'center' , command = 'loadModel()')
    cmds.colorSliderGrp ('ColorSlider', label = "Colour", rgb = (0.1, 0.1, 1))
    cmds.rowColumnLayout(numberOfColumns = 2, columnWidth = [(1, 200), (2, 200)])
    _rgb = cmds.colorSliderGrp('ColorSlider',query=True, rgbValue=True)
    cmds.button(label = "Delete ", width = 150, align = 'center', command = 'deleteCity()')
    cmds.button(label = "Make", width = 150, align = 'center', command = 'getInputSettings()')
    
    cmds.showWindow(cityWindow)

def loadModel():

    _pathToFile = "path"
    fileType = "obj"
    
    files = cmds.getFileList(folder=_pathToFile, filespec='*.%s' % fileType)
    if len(files) == 0:
        cmds.warning("No files found")
        isImport=False
        return 0
    else:
        isImport = True
        for f in files:
            cmds.file(_pathToFile + f, i=True)
            print f
        return files
        
        
#---------------------------------------------------------------------------------------
# get user input from UI
#--------------------------------------------------------------------------------------- 
def getInputSettings():
    #deleteAll()
    _name = cmds.textFieldGrp('Name', query = True, text = True)
    _rgb = cmds.colorSliderGrp('ColorSlider',query=True, rgbValue=True)
    make(_amount,_obj, _rgb)
	# set color after creation
    setColor(_rgb)
    print 'Done with', _name
#---------------------------------------------------------------------------------------
# delete previous instance
#--------------------------------------------------------------------------------------- 
def deleteAll():
    cmds.select(all = True)
    cmds.delete()
#---------------------------------------------------------------------------------------
# set colors
#---------------------------------------------------------------------------------------
def setColor(_rgb):
    shape=cmds.select(all=True)
    if shape:
        shape=cmds.polyColorPerVertex( rgb=_rgb, colorDisplayOption=True )

#---------------------------------------------------------------------------------------
# show UI
#---------------------------------------------------------------------------------------
UI()