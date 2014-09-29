# -*- coding: iso-8859-1 -*-

import sys
import os
from pymclevel import mclevel
from pymclevel.mclevelbase import saveFileDir, ChunkNotPresent
from MinecraftUtility import *

# Destination interface
class CoverMediaDest():
    def __init__():
        self.seed = self.world.RandomSeed
        self.nbChunks = 0
        self.chunkPos = (0, 0)
        self.capacity = (0, 0, 0, 0)
        self.sampleNbBlock = 0
        self.blocksDict = {}
        self.sampleEntropy = 0
        self.sampleDif = 0
        self.sampleBiomes = []
        self.selectedDim = None
        self.currentDimension = None
        self.selectedDimName = ""

    def selectDimension(self, nbDim):
        raise NotImplementedError("Empty CoverMediaDest interface, use MapDest or ServerDest")

    def prepareChunkInfo(self, x, z):
        raise NotImplementedError("Empty CoverMediaDest interface, use MapDest or ServerDest")
    def put(self, pos, block):
        raise NotImplementedError("Empty CoverMediaDest interface, use MapDest or ServerDest")

    def get(self, x, y, z):
        raise NotImplementedError("Empty CoverMediaDest interface, use MapDest or ServerDest")

    def finishedInput(self):
        raise NotImplementedError("Empty CoverMediaDest interface, use MapDest or ServerDest")

class MapDest(CoverMediaDest):
    def __init__(self, path = None):
        self.path = path
        try:
            self.world = mclevel.fromFile(path, True, False)
        except (IOError, ValueError), e:
            self.world = None
            raise ValueError("Not a Minecraft Map: " + str(e))

        self.seed = self.world.RandomSeed
        self.selectedDim = None
        self.selectDimension(0)
        self.nbChunks = self.currentDimension.chunkCount
        self.chunkPos = None
        self.prepareChunkInfo(0, 0)
        self.modified = False

    def prepareChunkInfo(self, x, z):
        if self.chunkPos != None and self.chunkPos[0] == x and self.chunkPos[1] == z:
            return ## Just Not Realoading everything, avoid useless calculation
        try:
            sampleChunk = self.currentDimension.getChunk(x, z)
            self.sampleNbBlock = sampleChunk.Blocks.size
            self.blocksDict, self.sampleEntropy = calculateChunkEntropy(sampleChunk)
            self.sampleDif = len(self.blocksDict)
            self.sampleBiomes = getBiomesList(sampleChunk)
            self.chunkPos = (x, z)
        except ChunkNotPresent:
            self.sampleNbBlock = 0
            self.blocksDict = {}
            self.sampleEntropy = 0
            self.sampleDif = 0
            self.sampleBiomes = []
            self.chunkPos = None

    def selectDimension(self, nbDim):
        if self.selectedDim != None and nbDim == self.selectedDim:
            return
        self.selectedDim = nbDim
        if nbDim == 0:
            self.currentDimension = self.world
            self.selectedDimName = "{0} (Overworld)".format(self.world.LevelName)
        else:
            self.currentDimension = self.world.getDimension(nbDim)
            self.selectedDimName = self.currentDimension.displayName
        self.sampleNbBlock = 0
        self.blocksDict = {}
        self.sampleEntropy = 0
        self.sampleDif = 0
        self.sampleBiomes = []
        self.chunkPos = None
        spawnX, _, spawnZ = self.currentDimension.playerSpawnPosition()
        self.capacity = calculateCapacity(self.currentDimension, 
                                          spawnX / 16, 
                                          spawnZ / 16);

    def close(self):
        if self.world != None:
            if self.modified == True:
                self.currentDimension.saveInPlace()
                self.modified = False
            self.world.close()
            self.world = None

    def put(self, pos, blockid):
        x, y, z = pos
        self.modified = True
        self.currentDimension.setBlockAt(x, y, z, blockid)
        self.currentDimension.markDirtyChunk(x / 16, z / 16) ##only chunk set dirty are saved, All Y is setted dirty already

    def get(self, x, y, z):
        chunkPosX = x / 16
        chunkPosZ = z / 16
        blockPosX = x % 16
        blockPosZ = z % 16
        try:
            chunk = self.currentDimension.getChunk(chunkPosX, chunkPosZ)
        except ChunkNotPresent, e:
            raise e
        return (chunk.Blocks[blockPosX, blockPosZ, y])

    def finishedInput(self):
        if self.world != None and self.modified == True:
            self.currentDimension.saveInPlace()
            self.modified = False

class ServerDest(CoverMediaDest):
    def __init__(self, serverIp = None, severPort = None):
        self.serverIp = serverIp
        self.serverPort = serverPort

    def prepareChunkInfo(self, x, z):
        pass ##TODO

    def put(self, pos, block):
        pass # TODO
