import sys
import os
import math
from pymclevel import mclevel
from pymclevel.mclevelbase import saveFileDir
from pymclevel.biome_types import biome_types

# return lis of all existing Minecraft save on default directory
def getAvailMaps():
    return [e for e in os.listdir(saveFileDir) if os.path.isdir(os.path.join(saveFileDir,e))]

# calculate and return :
# - the blocks frequency for each different blocks in the chunk
# - the total Shanon entropy of the chunk (blocksDif for NbBlocks), blocks replace bytes
# ! mean entropy * nbBlocks = min NbBlocks assuming max theorical compression efficiency
# ! http://code.activestate.com/recipes/577476-shannon-entropy-calculation/
# mean the more is the best for steganography
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
