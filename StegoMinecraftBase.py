import sys
import os
from minecraftUtility import getAvailMaps
from coverMediaDest import MapDest, ServerDest
from pymclevel import mclevel
from pymclevel.mclevelbase import saveFileDir

# ===================================================================
# ======= StegoMinecraftBase / The whole content resume  ============
# ===================================================================

class StegoMinecraftBase():
    def __init__(self):
        self.coverMediaDest = None
        self.plainTxtSrc = None
        self.buffer = None
        self.key = None
        self.options = None
        
        mapList = getAvailMaps()
        if len(mapList) != 0 :
            mapName = mapList[0]
            self.coverMediaDest = MapDest(os.path.join(saveFileDir, mapName))
            print "coverMedia Dest = " + self.coverMediaDest.path
        
