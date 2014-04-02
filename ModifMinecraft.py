import sys
import os
from mainWindow import MainWindow
from pymclevel import mclevel
from pymclevel.mclevelbase import saveFileDir

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

    print "* MODIF *"
    chunk.Blocks[:,:,0:64] = world.materials.Bedrock.ID
    world.setPlayerPosition((20, 67, 0))

    world.generateLights();
    print "* SAVING *"
    world.saveInPlace()

def main(argv):
    print "SAVE FILE DIR = \"" + saveFileDir +"\""

    print "SAVE(S) AVAILABLE = "
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

             #testModifyMap(world)
             world.close()
         except IOError, e:
             print "ERROR = {0} {1}".format(type(e), e.strerror)

    window = MainWindow()
    
            
if __name__ == '__main__':
    print "---------------------------------------"
    print "---------------------------------------"
    sys.exit(main(sys.argv))
