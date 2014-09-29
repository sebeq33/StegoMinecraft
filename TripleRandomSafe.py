import sys
import os
import random

class TripleRandomSafe(object):
    def __init__(self, seed = 0):
        self._gen = random.Random() ##its own instance not the default global one
        self._gen.seed(seed)
        self._usedPos = set() ##for speed and memory

    def get3DPos(self, limitX, limitY, limitZ):
        found = False
        while found == False:
            x = self._gen.randint(limitX[0], limitX[1])
            y = self._gen.randint(limitY[0], limitY[1])
            z = self._gen.randint(limitZ[0], limitZ[1])
            if (x, y, z) not in self._usedPos:
                self._usedPos.add((x, y, z))
                found = True
        return (x, y, z)

    def reset(self, newSeed):
        self._gen = random.Random()
        self._gen.seed(newSeed)
        self._usedPos = set() ##for speed and memory
