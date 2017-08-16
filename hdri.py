import pymel.core as pm
'''
dynamically create  redshift hdri dome, apply image, animate rotation
'''
_path = "" #  image path
_frame = "" #  rotation speed
pm.mel.eval('redshiftCreateDomeLight;')
pm.mel.eval('MASHnewNodeCallback( "rsDomeLightShape1");')
pm.mel.eval('setAttr -type "string" rsDomeLightShape1.tex0 "{0}";'.format(_path))


# set 0 keyframe rotation
pm.mel.eval('currentTime 1;')
pm.mel.eval('setAttr "rsDomeLight1.rotateY 0";')
pm.mel.eval('setKeyframe { "rsDomeLight1.r" };')

#set user keyframe rotation
pm.mel.eval('currentTime 1;')
pm.mel.eval('setAttr "rsDomeLight1.rotateY {0}";'.format(_frame))
pm.mel.eval('setKeyframe { "rsDomeLight1.r" };')
