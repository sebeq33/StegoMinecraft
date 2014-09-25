import sys
import os
import random
from TripleRandomSafe import TripleRandomSafe
from MinecraftUtility import getAvailMaps, dumpMapDest
from CoverMediaDest import MapDest, ServerDest
from PlainTxtSrc import SrcFile, SrcTxt
from pymclevel import mclevel
from pymclevel.mclevelbase import saveFileDir, ChunkNotPresent

# ===================================================================
# ==== StegoMinecraftBase / The whole content resume and process  ===
# ===================================================================

Instance = None

class StegoMinecraftBase():
    def __init__(self):
        self.coverMediaDest = None
        self.plainTxtSrc = None
        self.limits = None
        self.key = None
        self.options = None

    def isProcessReady(self):
        if self.coverMediaDest == None:
            return False
        if self.plainTxtSrc == None:
            return False
        ##TO COMPLETE / FINISH
        return True

    def isRetrieveReady(self):
        if self.coverMediaDest == None:
            return False
        return True

    def launchProcess(self):
        self.key = 0
        self.limits = ((-160, 160), (2, 5), (-160, 160))

        count = 0
        end = False
        triple = TripleRandomSafe(self.key)
        buff = self.plainTxtSrc.popTxt()
        while buff != None and buff != "":
            for char in buff:
                count += 1
                for j in range(0, 8):
                    bit = (ord(char) >> j) & 1 
                    x, y, z = triple.get3DPos(self.limits[0], self.limits[1], self.limits[2])
                    block = None
                    if bit == 1:
                        block = self.coverMediaDest.currentDimension.materials.Bedrock.ID
                    else:
                        block = self.coverMediaDest.currentDimension.materials.Air.ID
                    self.coverMediaDest.put((x, y, z), block)
            ##END BUFF LOOP
            buff = self.plainTxtSrc.popTxt()
        ## END PROCESS LOOP
        self.coverMediaDest.finishedInput()
        return count

    def retrieveProcess(self, pathDest, qtt):
        self.key = 0
        self.limits = ((-160, 160),(2, 5),(-160, 160))

        fileDest = open(pathDest, 'wb') ## write binary
        triple = TripleRandomSafe(self.key)
        buff = ""
        for i in range(0, qtt):
            result = 0
            for k in range(0, 8): ## 7, 6, ..., 0
                x, y, z = triple.get3DPos(self.limits[0], self.limits[1], self.limits[2])
                block = self.coverMediaDest.get(x, y, z)
                if block == self.coverMediaDest.currentDimension.materials.Bedrock.ID:
                    result = result | (1 << k)
            buff += chr(result)
            if ((i + 1) % 16 == 0):
                fileDest.write(buff)
                buff = ""
        ## END PROCESS LOOP
        fileDest.write(buff)
        fileDest.close()
        return True

    def loadDefaultLocalMap(self): ## for debug / quick tests
        mapList = getAvailMaps()
        if len(mapList) != 0 :
            mapName = mapList[0]
            self.coverMediaDest = MapDest(os.path.join(saveFileDir, mapName))
            print "coverMedia Dest = " + self.coverMediaDest.path
            dumpMapDest(self.coverMediaDest);

    def close(self):
        if self.coverMediaDest != None:
            self.coverMediaDest.close()
        if self.plainTxtSrc != None and type(self.plainTxtSrc) == SrcFile:
            self.plaintxtSrc.close()

