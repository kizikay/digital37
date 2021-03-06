# replace the ";" with ":" for OSX
# or better yet determine your system and
# automatically do it. I'll leave that up to you.
# (hint: try os.name)

import sys
import pymel.core as pm

def getEnvironment():
    scriptPaths = pm.mel.getenv("MAYA_SCRIPT_PATH")
    plugInPaths = pm.mel.getenv("MAYA_PLUG_IN_PATH")
    pythonPaths = pm.mel.getenv("PYTHONPATH")
    iconPaths = pm.mel.getenv("XBMLANGPATH")
    pathPaths = pm.mel.getenv("PATH")
    sysPaths = sys.path

    allScriptPaths = scriptPaths.split(";")
    print "\nMAYA_SCRIPT_PATHs are:"
    for scriptPath in allScriptPaths:
        print scriptPath

    allPlugInPaths = plugInPaths.split(";")
    print "\nMAYA_PLUG_IN_PATHs are:"
    for plugInPath in allPlugInPaths:
        print plugInPath

    allPythonPaths = pythonPaths.split(";")
    print "\nPYTHONPATHs are:"
    for pythonPath in allPythonPaths:
        print pythonPath

    allIconPaths = iconPaths.split(";")
    print "\nXBMLANGPATHs are:"
    for iconPath in allIconPaths:
        print iconPath

    allPathPaths = pathPaths.split(";")
    print "\nPATHs are:"
    for pathPath in allPathPaths:
        print pathPath

    print "\nsys.paths are:"
    for sysPath in sysPaths:
        print sysPath