from maya.cmds import *
import baseCheckTools as bc

#ui = loadUI(f=r'//server-cgi/RND/tools/DIGITAL37/Maya/Python/digital37/maya/modeling/37checkTools.u')
dialogString=r"""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Frame</class>
 <widget class="QFrame" name="Frame">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>850</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Frame</string>
  </property>
  <property name="frameShape">
   <enum>QFrame::StyledPanel</enum>
  </property>
  <property name="frameShadow">
   <enum>QFrame::Raised</enum>
  </property>
  <widget class="QTextEdit" name="textEdit">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>10</y>
     <width>381</width>
     <height>211</height>
    </rect>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton4">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>350</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>doubleDisplay</string>
   </property>
   <property name="+command" stdset="0">
    <string>&quot;doubleDisplay()&quot;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton1">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>230</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>baseInfo</string>
   </property>
   <property name="+command" stdset="0">
    <string>&quot;baseInfo()&quot;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton6">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>430</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>reRangeUV</string>
   </property>
   <property name="+command" stdset="0">
    <string>&quot;reRangeUV()&quot;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton10">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>590</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>deleteDisplayLayer</string>
   </property>
   <property name="+command" stdset="0">
    <string>&quot;deleteDisplayLayer()&quot;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton3">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>310</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>zeroObject</string>
   </property>
   <property name="+command" stdset="0">
    <string>&quot;zeroObject()&quot;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton9">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>550</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>deleteLight</string>
   </property>
   <property name="+command" stdset="0">
    <string>&quot;deleteLight()&quot;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton2">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>270</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>shapeAndTransformName</string>
   </property>
   <property name="+command" stdset="0">
    <string>&quot;shapeAndTransformName()&quot;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton8">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>510</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>deleteCamera</string>
   </property>
   <property name="+command" stdset="0">
    <string>&quot;deleteCamera()&quot;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton14">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>750</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>unloadPlugins</string>
   </property>
   <property name="+command" stdset="0">
    <string>&quot;unloadPlugins()&quot;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton5">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>390</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>fiveFace</string>
   </property>
   <property name="+command" stdset="0">
    <string>&quot;fiveFace()&quot;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton7">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>470</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>deleteHistory</string>
   </property>
   <property name="+command" stdset="0">
    <string>&quot;deleteHistory()&quot;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton11">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>630</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>deleteRenderLayer</string>
   </property>
   <property name="+command" stdset="0">
    <string>&quot;deleteRenderLayer()&quot;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton15">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>790</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>deleteUnknow</string>
   </property>
   <property name="+command" stdset="0">
    <string>&quot;deleteUnknow()&quot;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton12">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>670</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>deleteEmptyGroup</string>
   </property>
   <property name="+command" stdset="0">
    <string>&quot;deleteEmptyGroup()&quot;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton13">
   <property name="geometry">
    <rect>
     <x>20</x>
     <y>710</y>
     <width>361</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>faceNormal</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
 """

ui = loadUI(uiString=dialogString)
node = bc.baseCheckTools(ui)
showWindow(ui)

def baseInfo():

    node.checkBaseInfo()
    
def shapeAndTransformName():

    node.checkShapeTransName()
    
def zeroObject():

    node.zeroObject()
    
def doubleDisplay():

    node.doubleDisplay()
    
def fiveFace():
    
    node.checkFiveFace()
    
def reRangeUV():

    node.checkUV()
    
def deleteHistory():

    node.deleteHistory()
    
def deleteCamera():

    node.deleteCamera()
    
def deleteLight():
    
    node.deleteLight()
    
def deleteDisplayLayer():

    node.deleteDisplayLayer()
    
def deleteRenderLayer():

    node.deleteRenderLayer()
    
def deleteEmptyGroup():

    node.deleteEmptyGroups()
    
def unloadPlugins():

    node.unloadPlugins()
    
def deleteUnknow():

    node.deleteUnknowNode()
