import maya.cmds as cmds
import random

 
def cityBuilding(_name, _area, _placement, _skyOccur,_roadWidth, _paveSize, _gap, _amount, _flatOccur):
    sizeX = random.uniform(0.5,1)    
    sizeZ = random.uniform(0.5,1)
    _skyOccurB = _skyOccur
    _flatOccurB = _flatOccur
    _top = _name + '.f[1]'
    if _skyOccur > 0.7:
        _skyOccurB = 0.7
        _flatOccurB = 1
    elif _skyOccur < 0:
        _skyOccurB = 0.05
        _flatOccurB = 0.2
    
    cmds.polyCube(name = _name)
    cmds.xform(_name, piv = [0, -0.5, 0])
    cmds.move((_placement[0]*_area[0])+(_placement[0]*_gap)+(((_area[0]+_gap)/2)+_roadWidth+_paveSize),0.7,(_placement[1]*((_area[1] + _gap)))+(((_placement[1]+1.0)/_amount)*_gap)+(_roadWidth+_paveSize+(_area[1]/2)), _name, r = True)
    cmds.scale(_area[0]*sizeX, 1,_area[1]*sizeZ, _name)
    buildType = random.random()
    if buildType < _skyOccurB :
        skyscraper(_name, _top, _skyOccur)
    elif _skyOccurB < buildType < _flatOccurB :
        flat(_name, _top)
        cmds.polyColorPerVertex(r= 0.2, g= 0.1 ,b= 0.3, a= 1,colorDisplayOption=True)  
    else:
        shop(_name, _top, _area, _placement, _gap)
        cmds.polyColorPerVertex(r= 0.7, g= 0.1 ,b= 0.3, a= 1,colorDisplayOption=True) 
          
def suburb(_name, _area, _placement,_roadWidth, _paveSize, _gap, _amount, _zipCode,_rgb):
    _treeChance = 1 - random.random()*_zipCode*3
    _moveX = (_placement[0]*_area)+(_placement[0]*_gap)+(((_area+_gap)/2)+_roadWidth+_paveSize)
    _moveZ = (_placement[1]*(_area + _gap))+(((_placement[1]+1.0)/_amount)*_gap)+(_roadWidth+_paveSize+(_area/2))
    if _treeChance > 0.8:
        woods(_name, _area, _moveX,_moveZ,_rgb)
    else:
        _flatOccurSub = random.random()
        _top = _name + '.f[1]'
        cmds.polyCube(name = _name)
        cmds.xform(_name, piv = [0, -0.5, 0])
        cmds.move(_moveX,0.5,_moveZ, _name, r = True)
        if _flatOccurSub < _zipCode:
            sizeX = random.uniform(0.5,1)    
            sizeZ = random.uniform(0.5,1)
            cmds.scale(_area*sizeX, 1,_area*sizeZ, _name)
            flat(_name, _top)
        else:
            house(_name, _area, _gap)

def skyscraper(_name, _top, _skyOccur):
    skyRand = _skyOccur
    if skyRand < 1:
        skyRand = 1
    _levels = random.randint(5,25)
    bottom = random.uniform((10.0*skyRand),(25.0*skyRand))
    scaleFloors(_top, bottom,0.7,1)
    choiceB = random.choice(['gradTop', 'flatTop'])
    choicePt = random.random()
    if choiceB == 'gradTop':
        gradTop(_levels, _top, 0.7,1.0)
        cmds.polyColorPerVertex(r= 0.1, g= 0.1 ,b= 0.2, a= 1,colorDisplayOption=True) 
        if choicePt > 0.5:
            gradTop((_levels/4), _top, 0.7,1.0)
            cmds.polyColorPerVertex(r= 0.1, g= 0.1 ,b= 0.1, a= 1,colorDisplayOption=True) 
    elif choiceB == 'flatTop':
        flatTop(_top)
        cmds.polyColorPerVertex(r= 0.1, g= 0.1 ,b= 0.3, a= 1,colorDisplayOption=True)    
      
 
def flat(_name, _top):
    height = random.randint(3,10)
    cmds.polyExtrudeFacet(_top, translateY = height)
    choiceA = random.choice(['gradTop', 'flatTop'])
    if choiceA == 'gradTop':
        _levels = random.randint(1,5)
        gradTop(_levels, _top, 0.3,1.0)
    elif choiceA == 'flatTop':
        flatTop(_top)
 
 
def shop(_name, _top, _area, _placement, _gap):
    height = random.uniform(2.0,8.0)
    cmds.scale(_area[0]+_gap, 1,_area[1]-1, _name)
    scaleFloors(_top, height,1,1)    
    flatTop(_top)
 

def house(_name, _area, _gap):
    cmds.scale((_area+_gap-0.5)/1.5, 4/1.8, 6/1.8, _name)
    cmds.polyExtrudeFacet(_name + '.f[1]', translateY = 3/1.8)
    cmds.scale(1,1,0, _name + '.f[1]')
    cmds.polyColorPerVertex(r= 0.6, g=0.1 ,b= 0.2, a= 1,colorDisplayOption=True) 

 
def flatTop(_top):
    edge = random.choice([True, False])       
    edgeHeight = random.uniform(0.1,0.5)
    edgeWidth = random.uniform(0.7,0.95)
    boxSizeX = random.uniform(0.2,0.8)
    boxSizeY = random.uniform(0.2,0.8)    
    boxSizeZ = random.uniform(0.2,0.8)
 
    if edge == True:
        cmds.polyExtrudeFacet(_top, translateY = edgeHeight)
        cmds.polyExtrudeFacet(_top, localScale = (edgeWidth, edgeWidth, edgeWidth))    
        cmds.polyExtrudeFacet(_top, translateY = (-1*edgeHeight))
               
    else:
        cmds.polyExtrudeFacet(_top, localScale = (boxSizeX, boxSizeY, boxSizeZ))
        cmds.move(boxSizeX/4, 0, boxSizeZ/4, _top, r = True)
        cmds.polyExtrudeFacet(_top, translateY = 2*edgeHeight)
 
def gradTop(_levels,_top, _scaleMin, _scaleMax):
    for i in range(_levels):
        upIf = random.choice([True, False])
        if upIf == True:
            up = random.uniform(0,(8.0/(i+1)))
            scaleFloors(_top, up, _scaleMin, _scaleMax)
        elif upIf == False:
            up = 0
            scaleFloors(_top, up, _scaleMin, _scaleMax)
            cmds.polyColorPerVertex(r= 0.2, g= 0.3 ,b= 0.2, a= 1,colorDisplayOption=True) 

def scaleFloors(_top, _up, _scaleMin, _scaleMax):
    symmet = random.choice([True, False])
    if symmet == True:
        scaleT = random.uniform(_scaleMin,_scaleMax)
        cmds.polyExtrudeFacet(_top, translateY = _up, localScale = (scaleT, scaleT, scaleT))
    elif symmet == False:
        scaleX = random.uniform(_scaleMin,_scaleMax)
        scaleY = random.uniform(_scaleMin,_scaleMax)
        scaleZ = random.uniform(_scaleMin,_scaleMax)
        cmds.polyExtrudeFacet(_top, translateY = _up, localScale = (scaleX, scaleY, scaleZ))
 

def trunk(_name, _height, _rgb):
    
    cmds.polyCylinder(name = _name, sx=8, sy=1, sz=2, h=_height) 
    cmds.xform(_name, piv = [0, -(_height/2.0), 0])
    cmds.move(0,_height/2.0,0, _name, r = True)
    cmds.scale(0.3, 1, 0.3, _name)

    cmds.select(all=True)

    cmds.polyColorPerVertex(r= 0.3, g= 0.2 ,b= 0.2, a= 1,colorDisplayOption=True)



def canopy(_name, _height):
    _heightCan = random.uniform(_height,6)
    _levels = random.randint(1,3)
    _heightUp = _height*0.4
    for i in range(_levels):
        _nameCan = _name + 'Can' + str(i)
        cmds.polyCone( n= _nameCan, sx=15, sy=1, sz=1, h = _heightCan)
        cmds.xform(_nameCan, piv = [0, -(_heightCan/2.0), 0])
        cmds.move(0,_heightUp + (_heightCan/2) + (0.75*i),0, _nameCan, r = True)
        cmds.scale((0.85**i), (0.9**i), (0.85**i), _nameCan)
        cmds.parent(_nameCan, _name)
        cmds.polyColorPerVertex(r= 0, g= 1 ,b= 0.3, a= 1,colorDisplayOption=True)
 
 
def tree(_name,_rgb):
    _height = random.uniform(2,5)
    trunk(_name, _height,_rgb)
    canopy(_name, _height)
    cmds.polyColorPerVertex(r= 0, g= 1 ,b= 0, a= 1,colorDisplayOption=True)
 
def woods(_name, _area,_moveX, _moveZ,_rgb):
    _treeList = []
    _amount = random.randint(3,_area)
    for i in range(_amount):
        _placeX = random.randint(int(3 + _moveX-_area),int(_moveX + _area-1))
        _placeZ = random.randint(int(3 + _moveZ-_area),int(_moveZ + _area-1))
        if i == 0:
            tree(_name,_rgb)
            cmds.move(_placeX, 0, _placeZ, _name, r = True)
        else:
            _name1 = _name + 'tree' + str(i)
            tree(_name1,_rgb)
            cmds.move(_placeX, 0, _placeZ, _name1, r = True)
            _treeList.append(_name1)
    cmds.parent(_treeList, _name)
 
def block(_name, _area, _amount, _paveSize, _paveList, _roadWidth, _gap, _suburbs):
 
    cmds.polyPlane(name = _name, sx = 1, sy = 1)
    cmds.polyColorPerVertex(_name,r=0,g=1,b=0)
    cmds.xform(_name, piv = [-.5, 0, -.5])
    cmds.move(0.5,0,0.5, _name, r = True)
    cmds.scale((_amount*(_area[0]+_gap))+(2*(_roadWidth+_paveSize)), 1,(_amount*(_area[0]+_gap))+(2*(_roadWidth+_paveSize)), _name)
    cmds.xform(_name, piv = [((_area[0]+4.5)*_amount)/2, 0, ((_area[1]+4.5)*_amount)/2])
    if _suburbs == False:
        paving(_name, _area, _amount, _paveSize, _roadWidth, _paveList, _gap)


def paving(_blockName, _area, _amount, _paveSize ,_roadWidth, _paveList, _gap):
    for i in range(_amount):
        _paving = _blockName + 'paving' + str(i)
        cmds.polyCube(name = _paving)
        cmds.xform(_paving, piv = [-0.5, -0.5, -0.5])
        cmds.move(_roadWidth+_paveSize,0.5,((_area[1]+ _gap)*(i)+_roadWidth)+ (((i+1.0)/_amount)*_gap), _paving, r = True)
        cmds.scale(((_amount*(_area[0]+_gap))+(2*_paveSize)), 0.2,_area[1]+(_paveSize*2), _paving)
        _paveList.append(_paving)
        cmds.polyColorPerVertex(r= 0.1, g= 0.1 ,b= 0.3, a= 1,colorDisplayOption=True) 

 
def rotateBlock(_blockName, _blockGroup, _paveList):
    angle = random.choice([0, 90])
    cmds.parent( _blockGroup + _paveList, _blockName)
    cmds.rotate(0,angle,0, _blockName, ocp = True)
 
def makeCity(_name, _amount, _gap, _area, _roadWidth, _paveSize, _distSize, _citySpread, _rgb):
    _area1 = (_amount*(_area+_gap))+(2*(_roadWidth+_paveSize))
    _centrePt = _area1*(_distSize/2)
    _maxDistance = ((_centrePt**2)*2)**0.5
    _district = []
    for i in range((_distSize**2)):
        _cityBlock = _name + str(i) + 'build'
        x = i % _distSize
        z = int(i / _distSize)        
        _bbox = [x*_area1, z*_area1]
        _distance = (((_centrePt - _bbox[0]) ** 2) + ((_centrePt - _bbox[1]) ** 2)) ** 0.5
        _cityVal = 1 - (_distance/(_centrePt+0.01))
        _zipCode = 1 - (_distance/_maxDistance)
        makeBlock(_cityBlock, _amount, _gap, _area, _roadWidth, _paveSize, _cityVal, _zipCode, _citySpread, _rgb)
        _cityBlockDone = _cityBlock + 'blockShape'
        cmds.move(x*_area1, 0, z*_area1, _cityBlockDone, r = True)
        _district.append(_cityBlock)
        cmds.refresh(f = True)
       # setColor(_rgb)
 
 
def makeBlock(_name, _amount, _gap, _area1, _roadWidth, _paveSize, _cityVal, _zipCode, _citySpread, _rgb):
    _spreadCity = 1 - _citySpread
    _suburbs = False
    _skyOccur = (_cityVal**2)*2
    _flatOccur = (_cityVal**2)*2 + 0.25
    _area = [_area1, _area1] 
    blockGroup = []
    _paveList = []
    _blockName = _name + 'block'
    for i in range(_amount**2):
        x = i % _amount
        z = int(i / _amount)
        buildingX = _name + str(i)
        if _zipCode > _spreadCity:
            cityBuilding(buildingX, (_area[0],_area[1]), (x,z), _skyOccur, _roadWidth, _paveSize, _gap, _amount, _flatOccur)
        else:
            _suburbs = True           
            suburb(buildingX, _area1, (x,z),_roadWidth, _paveSize, _gap, _amount, _zipCode, _rgb)
        blockGroup.append(buildingX)
    block(_blockName, _area, _amount, _paveSize, _paveList, _roadWidth, _gap, _suburbs)
    rotateBlock(_blockName, blockGroup, _paveList)

def UI():
    cityWindow = cmds.window(title = 'City Generator', wh = (400, 300), s = True) 
    cmds.columnLayout(adjustableColumn = True, rowSpacing = 5, cw=100, cal = 'left')
    cmds.text(label = 'Name of city:')
    cmds.textFieldGrp('cityName', ann = 'Name Of City:', tx = 'city')
    cmds.intSliderGrp('buildPerBlockSlider', field = True, label = "Buildings Per Block", v = 4, min = 1, max = 25)
  
    cmds.intSliderGrp('blockSlider', field = True, label = "Number Of Blocks", v = 2, min = 2, max = 30)
    cmds.floatSliderGrp('citySpreadSlider', field = True, label = "City Spread", v = 0.6, min = 0, max = 1.2, fs = 0.1)
    cmds.colorSliderGrp ('cityColorSlider', label = "Colour", rgb = (0.1, 0.1, 1))
    cmds.rowColumnLayout(numberOfColumns = 2, columnWidth = [(1, 200), (2, 200)])
    _rgb = cmds.colorSliderGrp('cityColorSlider',query=True, rgbValue=True)
    cmds.button(label = "Delete City", width = 150, align = 'center', command = 'deleteCity()')
    cmds.button(label = "Make City", width = 150, align = 'center', command = 'getInput()')
 
    cmds.showWindow(cityWindow)

#---------------------------------------------------------------------------------------
# get user input from UI
#--------------------------------------------------------------------------------------- 
def getInput():
    deleteCity()
    _name = cmds.textFieldGrp('cityName', query = True, text = True)
    _amount = cmds.intSliderGrp('buildPerBlockSlider', query = True, value = True)
    _districtSize = cmds.intSliderGrp('blockSlider', query = True, value = True)
    _citySpread = cmds.floatSliderGrp('citySpreadSlider', query = True, value = True)
    _rgb = cmds.colorSliderGrp('cityColorSlider',query=True, rgbValue=True)
    makeCity('city', _amount, 2, 5, 5, 5, _districtSize, _citySpread, _rgb)
	# set color after creation
    setColor(_rgb)
    print 'Your city has been made. Welcome to', _name
#---------------------------------------------------------------------------------------
# delete previous instance
#--------------------------------------------------------------------------------------- 
def deleteCity():
    cmds.select(all = True)
    cmds.delete()
#---------------------------------------------------------------------------------------
# set colors
#---------------------------------------------------------------------------------------
def setColor(_rgb):
    shape=cmds.select(all=True)
    shape=cmds.polyColorPerVertex( rgb=_rgb,colorDisplayOption=True )

#---------------------------------------------------------------------------------------
# show UI
#---------------------------------------------------------------------------------------
UI()