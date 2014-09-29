import sys
import os
from pymclevel import mclevel
from pymclevel.mclevelbase import saveFileDir
from MinecraftUtility import calculateChunkEntropy

#return all existing Minecraft save
def getAvailSave():
    return [e for e in os.listdir(saveFileDir) if os.path.isdir(os.path.join(saveFileDir,e))]

def accessChunk(world, x, z):
    print "* LOAD CHUNK ({0}, {1}) *".format(x, z)
    try:
        world.createChunk(x, z)
    except ValueError, e:
        pass #already created
    return world.getChunk(x, z)

def testModifyMap(world):    
    chunk = accessChunk(world, 0, 0)
    print "CHUNK POSITION = " + str(chunk.chunkPosition)

    print
    freq, entropy = calculateChunkEntropy(chunk)
    for key in freq.keys():
        print "# ", key, ": ", freq[key]
    print
    
    print "* MODIF *"
    chunk.Blocks[:,:,256] = world.materials.Bedrock.ID ## X, Z, Y
    chunk.dirty = True

    print
    freq, entropy = calculateChunkEntropy(chunk)
    for key in freq.keys():
        print "# ", key, ": ", freq[key]
    print

    world.setPlayerPosition((40, 256, 40))
    world.generateLights();
    print "* SAVING *"
    world.saveInPlace()

def testCapacity(world):
    print "* TEST CAPACITY"
    print "SPAWN = ", str(world.playerSpawnPosition())
    # startx = -13; endx = 15; startz = -6; endz = 8
    startx = -23; endx = -18; startz = 12; endz = 18
    for x in range(startx, endx):
        for z in range(startz, endz):
            print "Chunk (", x, ", ", z, ") ", world.containsChunk(x, z)

def main(argv):
    print "* SAVE FILE DIR = \"" + saveFileDir +"\""

    print "* SAVE(S) AVAILABLE = "
    for save in getAvailSave():
        print save
    
    if len(argv) > 1:
         try:
             filename = os.path.join(saveFileDir, argv[1])
             print "FULL FILENAME = \"" + filename +"\""
             world = mclevel.loadWorld(argv[1]);
             print "* MAP SUCCESSFULLY LOADED *"
             print "SEED = " + str(world.RandomSeed)
             print "NUMBER OF LOADED CHUNKS = " + str(len(list(world.allChunks)))

             testModifyMap(world)
             # testCapacity(world)
             world.close()
         except IOError, e:
             print "ERROR = {0} {1}".format(type(e), e.strerror)
            
if __name__ == '__main__':
    print "---------------------------------------"
    print "---------------------------------------"
    sys.exit(main(sys.argv))
