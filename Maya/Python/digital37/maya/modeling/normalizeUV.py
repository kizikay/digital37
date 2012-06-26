import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    
    allObj = cmds.ls(type = 'mesh')
    for all in allObj:
        try:
            cmds.polyNormalizeUV(all, nt = 1, pa = False)
            loger.debug("normalize %s uv to 0-1 range successful" %all)
        except:
            if self.boolUI:
                loger.warning("dont normalize %s uv to 0-1 range" %all)