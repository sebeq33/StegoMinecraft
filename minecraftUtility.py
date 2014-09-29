# -*- coding: iso-8859-1 -*-

import sys
import os
import math
from pymclevel import mclevel
from pymclevel.mclevelbase import saveFileDir, ChunkNotPresent
from pymclevel.biome_types import biome_types

# return lis of all existing Minecraft save on default directory
def getAvailMaps():
    return [e for e in os.listdir(saveFileDir) if os.path.isdir(os.path.join(saveFileDir,e))]

# calculate and return :
# - the blocks frequency for each different blocks in the chunk
# - the total Shanon entropy of the chunk (blocksDif for NbBlocks), blocks replace bytes
# ! mean entropy * nbBlocks = min NbBlocks assuming max theorical compression efficiency
# ! http://code.activestate.com/recipes/577476-shannon-entropy-calculation/
# mean the more entropy is the best for steganography
def calculateChunkEntropy(chunk):
    entropy = 0.0
    nbBlocks = chunk.Blocks.size
    freqDic = {}
    # calculate frequency for each blocks
    for x in chunk.Blocks[:,:,:]:
        for y in x[:,:]:
            for z in y[:]:
                name = chunk.materials.get(z).name
                if not freqDic.has_key(name):
                    freqDic[name] = 1
                else:
                    freqDic[name] += 1
    for value in freqDic.values():
        freq = (float(value) / nbBlocks)
        entropy = entropy + freq * math.log(freq, 2)
    return (freqDic, (-entropy))

def getBiomesList(chunk):
    biomeList = []
    for x in chunk.Biomes[:,:]:
        for z in x[:]:
            if not biome_types[z] in biomeList:
                biomeList.append(biome_types[z])
    return (biomeList)

def calculateCapacity(currentDimension, startX = 0, startZ = 0):
    endLeft = False; endRight = False; endTop = False; endBottom = False
    sizeX = 0; sizeZ = 0
    while not endLeft or not endRight or not endTop or not endBottom:
        ## Check one side at a time for emptyChunk, determine starts and max chunk size
        if not endRight:        ## Right
            if chunksEmpty(currentDimension, startX + sizeX, startZ, 1, sizeZ):
                endRight = True
            else:
                sizeX += 1
        if not endBottom:       ## Bottom
            if chunksEmpty(currentDimension, startX, startZ + sizeZ, sizeX, 1):
                endBottom = True
            else:
                sizeZ += 1
        if not endLeft:         ## Left
            if chunksEmpty(currentDimension, startX - 1, startZ, 1, sizeZ):
                endLeft = True
            else:
                startX -= 1
                sizeX += 1
        if not endTop:          ## Top
            if chunksEmpty(currentDimension, startX, startZ - 1, sizeX, 1):
                endTop = True
            else:
                startZ -= 1
                sizeZ += 1
    ##END LOOP
    return (startX, startZ, sizeX, sizeZ);

##
## Check if one of the asked chunks in range is empty
##
def chunksEmpty(dimension, startX, startZ, sizeX, sizeZ):
    for x in range(startX, startX + sizeX):
        for z in range(startZ, startZ + sizeZ):
            if not dimension.containsChunk(x, z):
                return True
    return False


def dumpMapDest(mapDest):
    print "============================"
    print "       MapDest Dump         "
    print "============================"
    print "PATH                       : ", str(mapDest.path.encode('iso-8859-1'))
    print "CURRENT DIMENSION          : ", str(mapDest.selectedDimName)
    print "SEED                       : ", str(mapDest.seed)
    print "NB CHUNKS                  : ", str(mapDest.nbChunks)
    print "CAPACITY startX            : ", str(mapDest.capacity[0])
    print "         startZ            : ", str(mapDest.capacity[1])
    print "         sizeX             : ", str(mapDest.capacity[2])
    print "         sizeZ             : ", str(mapDest.capacity[3])
    print
    print "NB BLOCK IN CHUNK 0, 0     : ", str(mapDest.sampleNbBlock)
    print "NB DIF BLOCK IN CHUNK 0, 0 : ", str(mapDest.sampleDif)
    print "ENTROPY IN CHUNK 0, 0      : ", str(mapDest.sampleEntropy)
    print "BIOMES IN CHUNK 0, 0       : ", str(mapDest.sampleBiomes)

    for key in mapDest.blocksDict.keys():
        print "# ", key, ": ", mapDest.blocksDict[key]
    print
