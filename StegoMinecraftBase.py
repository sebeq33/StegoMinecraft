import sys
import os
from MinecraftUtility import getAvailMaps, dumpMapDest
from CoverMediaDest import MapDest, ServerDest
from pymclevel import mclevel
from pymclevel.mclevelbase import saveFileDir

# ===================================================================
# ==== StegoMinecraftBase / The whole content resume and process  ===
# ===================================================================

class StegoMinecraftBase():
    def __init__(self):
        self.coverMediaDest = None
        self.plainTxtSrc = None
        self.limits = None
        self.buff = None
        self.key = None
        self.options = None

    def launchProcess():
        pass ##TODO
        
    def loadDefaultLocalMap(): ## for debug / quick tests
        mapList = getAvailMaps()
        if len(mapList) != 0 :
            mapName = mapList[0]
            self.coverMediaDest = MapDest(os.path.join(saveFileDir, mapName))
            print "coverMedia Dest = " + self.coverMediaDest.path
            dumpMapDest(self.coverMediaDest);

Instance = None
