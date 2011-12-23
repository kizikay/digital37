# -*- coding: utf-8 -*-
#Description:
#Author:honglou(hongloull@gmail.com)
#Create:2011.12.06
#Update:
#How to use :
import logging
LOG_LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}
LOG_LEVEL = LOG_LEVELS.get('debug')
logging.basicConfig(level=LOG_LEVEL)

import os.path                                     
import maya.cmds as cmds
import pymel.core as pm
from pymel.all import mel
from pymel.core.general import PyNode

# Load mental ray plugin first, else can not made some global var      
def loadMRPlugin():
    #Check MR plugin load or not
    if not cmds.pluginInfo( 'Mayatomr', query=True, loaded=True ) :
        logging.warning('Maya to MentalRay Plugin has not been loaded.Loading Mayatomr now.')
        cmds.loadPlugin( 'Mayatomr' )
loadMRPlugin()

def setAttr(self,attr,val):
    # Check if attr exists
    logging.debug('attr: ' + str(attr))
    if pm.objExists(attr) :
        logging.debug('attr: ' + str(attr))
        # Unlock if locked
        isLock = 0
        if attr.isLocked() == 1:
            attr.unlock()
            isLock = 1
            
        # Break connections
        attrInputs = attr.connections(p=1,d=1)
        if len(attrInputs) >= 1 :
            attr.disconnect( attrInputs[0] )
            
        # Set attr 
        try :
            attr.set(val)
        except :
            logging.warning('set attr error:' + str(attr) + str(val))
                
        # Re lock again if locked before
        if isLock == 1 :
            attr.lock()
        else :
            logging.warning(str(attr) + ' does not exists')

DEFAULT_RENDER_GLOBALS = PyNode('defaultRenderGlobals')

# Let maya make some mr attr            
def setRendererToMR(): 
    renderer = DEFAULT_RENDER_GLOBALS.currentRenderer.get()
    if renderer != 'mentalRay' :
        DEFAULT_RENDER_GLOBALS.currentRenderer.set('mentalRay')
    DEFAULT_RENDER_GLOBALS.currentRenderer.set(renderer)
setRendererToMR()

# Get some global var
MAYA_LOCATION = mel.getenv('MAYA_LOCATION')
MI_DEFAULT_OPTIONS = PyNode('miDefaultOptions')
MI_DEFAULT_FRAME_BUFFER = PyNode('miDefaultFramebuffer')
                         
LIGHT_TYPES = ['<class \'pymel.core.nodetypes.SpotLight\'>',\
               '<class \'pymel.core.nodetypes.DirectionalLight\'>',\
               '<class \'pymel.core.nodetypes.VolumeLight\'>',\
               '<class \'pymel.core.nodetypes.AreaLight\'>',\
               '<class \'pymel.core.nodetypes.AmbientLight\'>',\
               '<class \'pymel.core.nodetypes.PointLight\'>']
GEOMETRY_TYEPS = ['<class \'pymel.core.nodetypes.Mesh\'>',\
                  '<class \'pymel.core.nodetypes.NurbsSurface\'>',\
                  '<class \'pymel.core.nodetypes.Subdiv\'>']   
SHADING_ENGINE_TYPE = '<class \'pymel.core.nodetypes.ShadingEngine\'>'
            
def getSelection():
    logging.debug('MRRenderLayerPass getSelection')
    selObjShort = pm.ls(sl=1)
    selObj = pm.ls(sl=1,dag=1)
    logging.debug(str(selObjShort))
    if not selObjShort :
        logging.warning('select some objects first.')
        return None
    else :
        return selObj

def getGeometrySelection():
    logging.debug('MRRenderLayerPass getSelection')
    selObjShort = pm.ls(sl=1)
    selObj = pm.ls(sl=1,dag=1,lf=1,type=['mesh','nurbsSurface','subdiv'])
    logging.debug(str(selObjShort))
    if not selObj :
        logging.warning('select some objects first.')
        return None
    else :
        return selObj
    
def getLightSelection():
    logging.debug('MRRenderLayerPass getSelection')
    selObj = pm.ls(sl=1,dag=1,lf=1,type=['spotLight','directionalLight',\
                                         'volumeLight','areaLight','ambientLight','pointLight'])
    if not selObj :
        logging.warning('select some objects first.')
        return None
    else :
        return selObj
    
def createShader(shaderType,shaderName):
    surfaceShader = pm.shadingNode(shaderType,n=shaderName,asShader=True)
    shadingSG = pm.sets(renderable=True,noSurfaceShader=True,empty=True,name=(shaderName+'_SG'))
    surfaceShader.outColor.connect(shadingSG.surfaceShader)
    return ( surfaceShader, shadingSG )

def getDisplacementShader(input):
    displacementShader = None
    connectionAll = input.connections(d=1)
    logging.debug('input: '+str(input))
    logging.debug('connectionAll: '+str(connectionAll))
    for connection in connectionAll :
        if str( type(connection) ) == SHADING_ENGINE_TYPE :
            dispConnections = connection.displacementShader.connections(p=1,d=1)
            if len(dispConnections) >= 1 :
                displacementShader = dispConnections[0]
                logging.debug('displacement shader: '+str(displacementShader))
    return displacementShader
             
def setRenderStatus(renderStatus):
    sels = getGeometrySelection()
    if sels :
        for sel in sels :
            for k,v in renderStatus.items() :
                attr = PyNode(sel.name()+'.'+k)
                setAttr(attr,v[1])

                                                        
class MRRenderLayerPass():
    def __init__(self):
        logging.debug('Init MRRenderLayerPass class')

    def getRenderLayers(self):
        selObj = pm.ls(sl=1,type='renderLayer')
        if not selObj :
            logging.warning('select some objects first.')
            return None
        else :
            selObj.remove(PyNode('defaultRenderLayer'))
            return selObj
            
    def createNewLayer(self,layerName):
        newLayer = pm.createRenderLayer(n=layerName)
        pm.editRenderLayerGlobals(currentRenderLayer=newLayer)
        #editRenderLayerAdjustment "defaultRenderGlobals.currentRenderer"
        pm.editRenderLayerAdjustment(DEFAULT_RENDER_GLOBALS.currentRenderer)
        DEFAULT_RENDER_GLOBALS.currentRenderer.set('mentalRay')    
        return newLayer     
    
    def setRenderLayerAttr(self,attr,val):
        # Check if attr exists
        logging.debug('attr: ' + str(attr))
        if pm.objExists(attr) :
            logging.debug('attr: ' + str(attr))
            # Unlock if locked
            isLock = 0
            if attr.isLocked() == 1:
                attr.unlock()
                isLock = 1
            
            # Break connections
            attrInputs = attr.connections(p=1,d=1)
            if len(attrInputs) >= 1 :
                attr.disconnect( attrInputs[0] )
            
            # Set attr 
            try:   
                pm.editRenderLayerAdjustment(attr)
            except :
                logging.warning('editRenderLayerAdjustment error:' + str(attr) + 'skip set attr')
            try :
                attr.set(val)
            except :
                logging.warning('set attr error:' + str(attr) + str(val))
                
            # Re lock again if locked before
            if isLock == 1 :
                attr.lock()
        else :
            logging.warning(str(attr) + ' does not exists')
            
    def disConnectCamShader(self):
        '''        string $allCams[] = `ls -ca`;
        for ($each in $allCams){
            string $camRenderAttr = `getAttr ($each + ".renderable")`;
            if ($camRenderAttr == 1){
                string $renderCam = $each;
                string $renderCamLensSHD[] = `listConnections -d 1 ($renderCam + ".miLensShader")`;
                if ($renderCamLensSHD[0] != ""){
                    editRenderLayerAdjustment ($renderCam + ".miLensShader");
                    disconnectAttr ($renderCamLensSHD[0] + ".message") ($renderCam + ".miLensShader");
                }
                string $renderCamEnv[] = `getAttr ($each + ".miEnvironmentShader")`;
                if ($renderCamEnv[0] != ""){
                    editRenderLayerAdjustment ($renderCam + ".miEnvironmentShader");
                    disconnectAttr ($renderCamEnv[0] + ".message") ($renderCam + ".miEnvironmentShader");
                }                 
            }
        }'''
        # disconnecet lensShader and envShader
        allCams = pm.ls(type='camera')
        for cam in allCams :
            if cam.renderable.get() == 1 :
                renderCamLensSHD = cam.miLensShader.connections(d=1)
                if renderCamLensSHD :
                    pm.editRenderLayerAdjustment(cam.miLensShader)
                    renderCamLensSHD[0].message.disconnect(cam.miLensShader)
                renderCamEnv = cam.miEnvironmentShader.get()
                if renderCamEnv :
                    pm.editRenderLayerAdjustment(cam.miEnvironmentShader)
                    renderCamEnv[0].message.disconnect(cam.miEnvironmentShader)

#// create my default render passes Color Layer
#
#global proc createMyColorRPasses(string $layer){
#
#    createNode -name ("beauty_" + $layer) renderPass;
#    string $sel[] = `ls -sl`;
#    applyAttrPreset $sel[0] "C:/Program Files/Autodesk/Maya2012/presets/attrPresets/renderPass/beauty.mel" 1;
#    connectAttr -nextAvailable ($layer + ".renderPass") ($sel[0] + ".owner");    
#    
#    createNode -name ("depth_" + $layer) renderPass;
#    string $sel[] = `ls -sl`;
#    applyAttrPreset $sel[0] "C:/Program Files/Autodesk/Maya2012/presets/attrPresets/renderPass/cameraDepth.mel" 1;
#    connectAttr -nextAvailable ($layer + ".renderPass") ($sel[0] + ".owner");    
#    
#    createNode -name ("diffuse_" + $layer) renderPass;
#    string $sel[] = `ls -sl`;
#    applyAttrPreset $sel[0] "C:/Program Files/Autodesk/Maya2012/presets/attrPresets/renderPass/diffuse.mel" 1;
#    connectAttr -nextAvailable ($layer + ".renderPass") ($sel[0] + ".owner");
#    
#    createNode -name ("incandescence_" + $layer) renderPass;
#    string $sel[] = `ls -sl`;
#    applyAttrPreset $sel[0] "C:/Program Files/Autodesk/Maya2012/presets/attrPresets/renderPass/incandescence.mel" 1;
#    connectAttr -nextAvailable ($layer + ".renderPass") ($sel[0] + ".owner");    
#    
#    createNode -name ("indirect_" + $layer) renderPass;
#    string $sel[] = `ls -sl`;
#    applyAttrPreset $sel[0] "C:/Program Files/Autodesk/Maya2012/presets/attrPresets/renderPass/indirect.mel" 1;
#    connectAttr -nextAvailable ($layer + ".renderPass") ($sel[0] + ".owner");
#    
#    createNode -name ("normalWorld_" + $layer) renderPass;
#    string $sel[] = `ls -sl`;
#    applyAttrPreset $sel[0] "C:/Program Files/Autodesk/Maya2012/presets/attrPresets/renderPass/normalWorld.mel" 1;
#    connectAttr -nextAvailable ($layer + ".renderPass") ($sel[0] + ".owner");
#    
#    createNode -name ("reflection_" + $layer) renderPass;
#    string $sel[] = `ls -sl`;
#    applyAttrPreset $sel[0] "C:/Program Files/Autodesk/Maya2012/presets/attrPresets/renderPass/reflection.mel" 1;
#    connectAttr -nextAvailable ($layer + ".renderPass") ($sel[0] + ".owner");
#    
#    createNode -name ("refraction_" + $layer) renderPass;
#    string $sel[] = `ls -sl`;
#    applyAttrPreset $sel[0] "C:/Program Files/Autodesk/Maya2012/presets/attrPresets/renderPass/refraction.mel" 1;
#    connectAttr -nextAvailable ($layer + ".renderPass") ($sel[0] + ".owner");
#    
#    createNode -name ("shadow_" + $layer) renderPass;
#    string $sel[] = `ls -sl`;
#    applyAttrPreset $sel[0] "C:/Program Files/Autodesk/Maya2012/presets/attrPresets/renderPass/shadow.mel" 1;
#    connectAttr -nextAvailable ($layer + ".renderPass") ($sel[0] + ".owner");
#    
#    createNode -name ("specular_" + $layer) renderPass;
#    string $sel[] = `ls -sl`;
#    applyAttrPreset $sel[0] "C:/Program Files/Autodesk/Maya2012/presets/attrPresets/renderPass/specular.mel" 1;
#    connectAttr -nextAvailable ($layer + ".renderPass") ($sel[0] + ".owner");
#
#}
    def createPass(self,prefix,layer):
        renderPass = pm.createNode( 'renderPass', n=(prefix+'_'+layer) )
        #renderPass = pm.ls(sl=1)
        #logging.debug('MAYA_LOCATION: '+MAYA_LOCATION)
        if prefix != 'depth' :
            presetMel = MAYA_LOCATION+'/presets/attrPresets/renderPass/'+prefix+'.mel'
        else :
            presetMel = MAYA_LOCATION+'/presets/attrPresets/renderPass/cameraDepth.mel'
        logging.debug('presetMel: '+presetMel)
        
        mel.applyAttrPreset(renderPass, presetMel, 1)
        layer.renderPass.connect(renderPass.owner,nextAvailable=1)
        
    def createColorPasses(self,layer):
        for p in ['beauty','depth','diffuse','incandescence','indirect','normalWorld',
                  'reflection','refraction','shadow','specular'] :
            self.createPass(p, layer)
            
#//Create color
    def createColorLayer(self):
        selObj = getSelection()
        if selObj :
#        string $Newlayer = `createRenderLayer -n "color"`;
#        editRenderLayerGlobals -currentRenderLayer $Newlayer;
#        createMyColorRPasses $Newlayer;     
            newLayer = self.createNewLayer('color')
            self.createColorPasses(newLayer)  
#        editRenderLayerAdjustment "defaultRenderGlobals.imageFilePrefix";
#        editRenderLayerAdjustment "defaultRenderGlobals.imageFormat";
#        editRenderLayerAdjustment "defaultRenderGlobals.imfPluginKey";
#        setAttr "defaultRenderGlobals.imageFormat" 51;
#        setAttr -type "string" "defaultRenderGlobals.imfPluginKey" "exr";
#        setAttr "defaultRenderGlobals.multiCamNamingMode" 1;
#        setAttr -type "string" "defaultRenderGlobals.bufferName" "<RenderPass>";
#        setAttr -type "string" "defaultRenderGlobals.imageFilePrefix" "images/<Scene>/<RenderLayer>/<RenderLayer>";
#        setAttr "miDefaultFramebuffer.datatype" 5;              
            self.setRenderLayerAttr(MI_DEFAULT_FRAME_BUFFER.datatype, 5)
            self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.imageFormat, 51)
            self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.imfPluginKey, 'exr')
            self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.multiCamNamingMode, 1)
            self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.bufferName, '<RenderPass>')
            self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.imageFilePrefix, 'images/<Scene>/<RenderLayer>/<RenderLayer>')

            pm.select(cl=1)

    def createAmbientOcclusionLayer(self):
        selObj = getSelection()
        
        newLayer = self.createNewLayer('AO')
        
        AOMat = pm.shadingNode('surfaceShader',n='AO_mat',asShader=True)
        AONode = pm.createNode('mib_amb_occlusion')
        AONode.outValue.connect(AOMat.outColor)
        AONode.samples.set(64)
        
        if selObj :
            for each in selObj :
                nodeType = type(each)
                logging.debug(str(nodeType))
                
                # Get dispalcement shader if input is geometry
                if str(nodeType) in GEOMETRY_TYEPS :
                    logging.debug('****'+str(each))
                    eachSn = each.getParent()
                    displacementShader = getDisplacementShader(each)
                    if displacementShader :
                        shader,shaderSG = createShader('lambert',(newLayer+'_'+str(eachSn)+'_MAT'))
                        shader.color.set([0,0,0])
                        shader.transparency.set([0,0,0])
                                
                        displacementShader.connect(shaderSG.displacementShader)
                        AONode = pm.createNode('mib_amb_occlusion')
                        AONode.outValue.connect(shader.incandescence)
                        AONode.samples.set(64)
                                
                        pm.select(eachSn)
                        mel.hyperShade(assign=shader)
                                
                    else :
                        pm.select(eachSn)
                        mel.hyperShade(assign=AOMat)
                else :
                    if str(nodeType) in LIGHT_TYPES :
                        lightSn = each.getParent()
                        pm.editRenderLayerMembers(newLayer,lightSn,remove=1)
                        pm.editRenderLayerMembers(newLayer,each,remove=1)
                
                pm.select(each)
                logging.debug('each: '+str(each))
                eachSn = pm.pickWalk(d='down')
                logging.debug('eachSn: '+str(eachSn[0]))
                if eachSn[0] != each :
                    pm.editRenderLayerMembers(newLayer,eachSn[0],remove=1)

        # Adjust render layer attr
        self.setRenderLayerAttr(MI_DEFAULT_OPTIONS.finalGather, 0)
        self.setRenderLayerAttr(MI_DEFAULT_OPTIONS.caustics, 0)
        self.setRenderLayerAttr(MI_DEFAULT_OPTIONS.globalIllum, 0)
        self.setRenderLayerAttr(MI_DEFAULT_FRAME_BUFFER.datatype, 2)
        self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.imageFormat, 7)
        self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.imfPluginKey, 'iff')
        self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.multiCamNamingMode, 1)
        self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.bufferName, '<RenderPass>')

        # Remove cam lens and env shader            
        self.disConnectCamShader()
        
        pm.select(cl=1)

    def createLightLayer(self,name):
        selObj = getGeometrySelection()
        selLight = getLightSelection()
        if selObj == None :
            logging.warning('select some lights and some objects first.')
            return None
        elif selLight == None :
            logging.warning('select some lights and some objects first.')
            return None
        else :
            
#        string $Newlayer = `createRenderLayer -n $name`;
#        editRenderLayerGlobals -currentRenderLayer $Newlayer;
#        string $LuzMat = `shadingNode -n ($name + "_MAT") -asShader lambert`;
#        setAttr ($LuzMat + ".diffuse") 1;
#        setAttr "miDefaultOptions.rayTracing" 1;
            newLayer = self.createNewLayer('Light')
            
            luzMat = pm.shadingNode('lambert',n=(name+'_MAT'),asShader=True)
            luzMat.diffuse.set(1)
            MI_DEFAULT_OPTIONS.rayTracing.set(1)
        
            for each in selObj :
                nodeType = type(each)
                logging.debug(str(nodeType))
                
                # Get dispalcement shader if input is geometry
                if str(nodeType) in GEOMETRY_TYEPS :
                    logging.debug('****'+str(each))
                    eachSn = each.getParent()
                    displacementShader = getDisplacementShader(each)
                    if displacementShader :
#                        string $LuzObjMat = `shadingNode -n ($name + "_" + $eachSn[0] + "_MAT") -asShader lambert`;
#                            setAttr ($LuzObjMat + ".diffuse") 1;                           
#                            string $LuzObjSG = `sets -renderable true -noSurfaceShader true -empty -name ($LuzObjMat + "_SG")`;
#                            connectAttr -f ($LuzObjMat + ".outColor") ($LuzObjSG + ".surfaceShader");
#                            connectAttr -f $dispCon[0] ($LuzObjSG + ".displacementShader");
#                            select $eachSn[0];                            
#                            hyperShade -assign $LuzObjMat;
                        shader,shaderSG = createShader('lambert',(newLayer+'_'+str(eachSn)+'_MAT'))
                        shader.diffuse.set(1)
                        displacementShader.connect(shaderSG.displacementShader)

                        pm.select(each,r=1)
                        mel.hyperShade(assign=shader)
                                
                    else :
                        pm.select(each,r=1)
                        mel.hyperShade(assign=luzMat)
                else :
                    if str(nodeType) in LIGHT_TYPES :
#                                        editRenderLayerAdjustment ($each + ".color");
#                setAttr ($each + ".color") 0 1 0 ;
#                editRenderLayerAdjustment ($each + ".intensity");
#                setAttr ($each + ".intensity") 5;
#                editRenderLayerAdjustment ($each + ".shadowColor");
#                setAttr ($each + ".lightAngle") 5;
#                setAttr ($each + ".shadowColor") 0 0 1 ;
#                setAttr ($each + ".useRayTraceShadows") 1;
#                setAttr ($each + ".shadowRays") 20;
                        self.setRenderLayerAttr(each.intensity, 5)
                        self.setRenderLayerAttr(each.color, [0,1,0])
                        self.setRenderLayerAttr(each.shadowColor, [0,0,1])
                        if each.hasAttr( 'lightAngle' ):
                            self.setRenderLayerAttr(each.lightAngle, 5)
                        self.setRenderLayerAttr(each.useRayTraceShadows, 1)
                        self.setRenderLayerAttr(each.shadowRays, 20)

                pm.select(each,r=1)
                logging.debug('each: '+str(each))
                eachSn = pm.pickWalk(d='down')
                logging.debug('eachSn: '+str(eachSn[0]))
                if eachSn[0] != each :
                    pm.editRenderLayerMembers(newLayer,eachSn[0],remove=1)

            # Adjust render layer attr
            self.setRenderLayerAttr(MI_DEFAULT_OPTIONS.finalGather, 0)
            self.setRenderLayerAttr(MI_DEFAULT_OPTIONS.caustics, 0)
            self.setRenderLayerAttr(MI_DEFAULT_OPTIONS.globalIllum, 0)
            self.setRenderLayerAttr(MI_DEFAULT_FRAME_BUFFER.datatype, 2)
            self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.imageFormat, 7)
            self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.imfPluginKey, 'iff')
            self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.multiCamNamingMode, 1)
            self.setRenderLayerAttr(DEFAULT_RENDER_GLOBALS.bufferName, '<RenderPass>')

            # Remove cam lens and env shader            
            self.disConnectCamShader()
        
            pm.select(cl=1)
            
            return True


class MRMaterial():
    def __init__(self):
        logging.debug('Init MRMaterial class')
    
    # Create and assign black shader
    # createShader([0,0,0],[1,1,1],'BLACK')
    def createShader(self,outColor,outAlpha,shaderName):
        selObj = getGeometrySelection()
        if selObj :
            for each in selObj :
                # Get dispalcement shader if input is geometry
                eachSn = each.getParent()
                displacementShader = getDisplacementShader(each)
                if displacementShader :
                    shaderNameWithDisp = "MATTE_" + eachSn + "_MAT"
                    if pm.objExists(shaderNameWithDisp) :
                        pm.select(each,r=1)
                        pm.hyperShade(assign=PyNode(shaderNameWithDisp))
                    else :
                        shader,shaderSG = createShader('surfaceShader', shaderNameWithDisp)
                        displacementShader.connect(shaderSG.displacementShader)
                        shader.outColor.set(outColor)
                        shader.outMatteOpacity.set(outAlpha)
                        pm.select(each,r=1)
                        mel.hyperShade(assign=shader)
                else :
                    if not pm.objExists(shaderName) :
                        shader,shaderSG = createShader('surfaceShader', shaderName)
                        shader.outColor.set(outColor)
                        shader.outMatteOpacity.set(outAlpha)
                    pm.select(each,r=1)
                    pm.hyperShade(assign=PyNode(shaderName))

    # Create and assign black shader
    def createShadowShader(self,shaderName='Shadow_Mask_MAT'):
        selObj = getGeometrySelection()
        if selObj :
            for each in selObj :
                # Get dispalcement shader if input is geometry
                eachSn = each.getParent()
                displacementShader = getDisplacementShader(each)
                if displacementShader :
                    shaderNameWithDisp = "SHADOW_" + eachSn + "_MAT"
                    if pm.objExists(shaderNameWithDisp) :
                        pm.select(each,r=1)
                        pm.hyperShade(assign=PyNode(shaderNameWithDisp))
                    else :
                        shader,shaderSG = createShader('useBackground', shaderNameWithDisp)
                        displacementShader.connect(shaderSG.displacementShader)
                        shader.specularColor.set([0,0,0])
                        shader.reflectivity.set(0)
                        shader.reflectionLimit.set(0)
                        pm.select(each,r=1)
                        mel.hyperShade(assign=shader)
                else :
                    if not pm.objExists(shaderName) :
                        shader,shaderSG = createShader('useBackground', shaderName)
                        shader.specularColor.set([0,0,0])
                        shader.reflectivity.set(0)
                        shader.reflectionLimit.set(0)
                    pm.select(each,r=1)
                    pm.hyperShade(assign=PyNode(shaderName))

    #Z-DEPTH
    def createZDepthNetwork(self,shaderName):
        shader,shaderSG = createShader('surfaceShader', shaderName)
                        
        zDepthRange = pm.shadingNode('setRange',n='Z_Depth_setRange',asUtility=1)
        zDepthRange.outValueX.connect(shader.outColorR,f=1)
        zDepthRange.outValueX.connect(shader.outColorG,f=1)
        zDepthRange.outValueX.connect(shader.outColorB,f=1)
        zDepthRange.minX.set(0)
        zDepthRange.maxX.set(1)
                        
        zDepthMultiDiv = pm.shadingNode('multiplyDivide',n='Z_Depth_multiplyDivide',asUtility=1)
        zDepthMultiDiv.input2X.set(-1)
        zDepthMultiDiv.outputX.connect(zDepthRange.valueX,f=1)
        
        zDepthSampInfo = pm.shadingNode('samplerInfo',n='Z_Depth_samplerInfo',asUtility=1)
        
        zDepthSampInfo.addAttr('cameraNearClipPlane1',at='double',dv=0.1)
        zDepthSampInfo.cameraNearClipPlane1.set(k=1)
        
        zDepthSampInfo.addAttr('cameraFarClipPlane1',at='double',dv=100)
        zDepthSampInfo.cameraFarClipPlane1.set(k=1)

        zDepthSampInfo.pointCameraZ.connect(zDepthMultiDiv.input1X)
        zDepthSampInfo.cameraNearClipPlane1.connect(zDepthRange.oldMinX)
        zDepthSampInfo.cameraFarClipPlane1.connect(zDepthRange.oldMaxX)
        
        return (shader,shaderSG)
                        
    def createZDepthShader(self,shaderName='Z_Depth_MAT'):
        selObj = getGeometrySelection()
        if selObj :
            for each in selObj :
                # Get dispalcement shader if input is geometry
                eachSn = each.getParent()
                displacementShader = getDisplacementShader(each)
                if displacementShader :
                    shaderNameWithDisp = "Z_Depth_" + eachSn + "_MAT"
                    if pm.objExists(shaderNameWithDisp) :
                        pm.select(each,r=1)
                        pm.hyperShade(assign=PyNode(shaderNameWithDisp))
                    else :
                        shader,shaderSG = self.createZDepthNetwork(shaderNameWithDisp)
                        displacementShader.connect(shaderSG.displacementShader)
                        
                        pm.select(each,r=1)
                        mel.hyperShade(assign=shader)
                else :
                    if not pm.objExists(shaderName) :
                        shader,shaderSG = self.createZDepthNetwork(shaderName)
                    pm.select(each,r=1)
                    pm.hyperShade(assign=PyNode(shaderName))

class MRRenderSubSet():
    def __init__(self):
        logging.debug('Init MRRenderSubSet class')     
        
    def createRenderSubSet(self,subSetName):
        selObj = getGeometrySelection()
#string $subsetShader=`mrCreateCustomNode -asUtility "" mip_render_subset`;
        subSetShader = pm.createNode('mip_render_subset',asUtility=1)
                                                                    
#MRRenderLayerPass()
#MRRenderLayerPass().createAmbientOcclusionLayer()
#MRMaterial().createShadowShader()
#MRMaterial().createZDepthShader()
#MRRenderLayerPass().createLightLayer('test')
#MRRenderLayerPass().createColorLayer()

