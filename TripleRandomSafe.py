import sys
import os
import random

class TripleRandomSafe(object):
    def __init__(self, seed = 0):
        self.gen = random.Random() ##its own instance not the default global one
        self.gen.seed(seed)
        self._usedPos = set() ##for speed and memory

    def get3DPos(self, limitX, limitY, limitZ):
        found = False
        while found == False:
            x = self.gen.randint(limitX[0], limitX[1])
            y = self.gen.randint(limitY[0], limitY[1])
            z = self.gen.randint(limitZ[0], limitZ[1])
            if (x, y, z) not in self._usedPos:
                self._usedPos.add((x, y, z))
                found = True
            else:
                print "DUPLICATE POSITION, re-loop (", x, ",", y, ",", z,")"
        return (x, y, z)

    def reset(self, newSeed):
        self.gen = random.Random()
        self.gen.seed(newSeed)
        self._usedPos = set() ##for speed and memory
