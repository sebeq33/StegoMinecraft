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

def calculateCapacity(currentDimension):
    endLeft = False; endRight = False; endTop = False; endBottom = False
    startX = 0; startY = 0; sizeX = 0; sizeY = 0
    checkDirection = 0
    while not endLeft or not endRight or not endTop or not endBottom:
        ## Check one side at a time for emptyChunk, determine starts and max chunk size
        if checkDirection == 0 and not endLeft:             ## Left
            if chunksEmpty(currentDimension, startX, startY, sizeX, 1):
                endLeft = True
            else:
                startX -= 1
                sizeX += 1
        elif checkDirection == 1 and not endRight:       ## Right
            if chunksEmpty(currentDimension, startX + sizeX, startY, sizeX, 1):
                endRight = True
            else:
                sizeX += 1
        elif checkDirection == 2 and not endBottom:      ## Bottom
            if chunksEmpty(currentDimension, startX, startY, 1, sizeY):
                endBottom = True
            else:
                startY -= 1
                sizeY += 1
        elif not endTop:                                ## Top
            if chunksEmpty(currentDimension, startY + sizeY, startY, 1, sizeY):
                endTop = True
            else:
                sizeY += 1
        checkDirection += 1
        if checkDirection > 3:
            checkDirection = 0
    ##END LOOP
    return (startX, startY, sizeX, sizeY);

##
## Check if one of the asked chunks in range is empty
##
def chunksEmpty(dimension, startX, startY, sizeX, sizeY):
    for x in range(startX, startX + sizeX):
        for y in range(startY, startY + sizeY):
            if not dimension.containsChunk(x, y):
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
    print "         startY            : ", str(mapDest.capacity[1])
    print "         sizeX             : ", str(mapDest.capacity[2])
    print "         sizeY             : ", str(mapDest.capacity[3])
    print
    print "NB BLOCK IN CHUNK 0, 0     : ", str(mapDest.sampleNbBlock)
    print "NB DIF BLOCK IN CHUNK 0, 0 : ", str(mapDest.sampleDif)
    print "ENTROPY IN CHUNK 0, 0      : ", str(mapDest.sampleEntropy)
    print "BIOMES IN CHUNK 0, 0       : ", str(mapDest.sampleBiomes)

    for key in mapDest.blocksDict.keys():
        print "# ", key, ": ", mapDest.blocksDict[key]
    print
