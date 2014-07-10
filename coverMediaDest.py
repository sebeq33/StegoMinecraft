import sys
import os
from pymclevel import mclevel
from pymclevel.mclevelbase import saveFileDir, ChunkNotPresent
from minecraftUtility import calculateChunkEntropy, getBiomesList

# Destination interface
class CoverMediaDest():
    def __init__():
        pass

    def put(self, pos, block):
        raise NotImplementedError("Empty CoverMediaDest interface, use MapDest or ServerDest")

class MapDest(CoverMediaDest):
    def __init__(self, path = None):
        self.path = path
        try:
            self.world = mclevel.fromFile(path, True, True)
        except (IOError, ValueError), e:
            self.world = None
            raise ValueError("Not a Minecraft Map: " + str(e))
        self.seed = self.world.RandomSeed
        self.selectDimension(0)
        self.nbChunks = self.currentDimension.chunkCount
        self.getChunkInfo(0, 0)

    def getChunkInfo(self, x, z):
        try:
            sampleChunk = self.currentDimension.getChunk(x, z)
            self.sampleNbBlock = sampleChunk.Blocks.size 
            self.blocksDict, self.sampleEntropy = calculateChunkEntropy(sampleChunk) 
            self.sampleDif = len(self.blocksDict)
            self.sampleBiomes = getBiomesList(sampleChunk)
        except ChunkNotPresent:
            self.sampleNbBlock = 0
            self.blocksDict = {}
            self.sampleEntropy = 0 
            self.sampleDif = 0
            self.sampleBiomes = []
            
    def selectDimension(self, nbDim):
        self.selectedDim = nbDim
        if nbDim == 0:
            self.currentDimension = self.world
            self.selectedDimName = "{0} (Overworld)".format(self.world.LevelName)
        else:
            self.currentDimension = self.world.getDimension(nbDim)
            self.selectedDimName = self.currentDimension.displayName
        
    def __del__(self):
        self.close()

    def close(self):
        if self.world != None:
            self.world.close()
            self.world = None

    def put(self, pos, block):
        pass # TODO

class ServerDest(CoverMediaDest):
    def __init__(self, serverIp = None, severPort = None):
        self.serverIp = serverIp
        self.serverPort = serverPort

    def put(self, pos, block):
        pass # TODO
