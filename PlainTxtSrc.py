# -*- coding: iso-8859-1 -*-

import sys
import os
from pymclevel import mclevel
from pymclevel.mclevelbase import saveFileDir, ChunkNotPresent
from MinecraftUtility import *

class PlainTxtSrc():
    def __init__():
        pass

    def popTxt(self):
        raise NotImplementedError("Empty PlainTxtSrc interface, use srcTxt or srcFile")


class srcTxt(PlainTxtSrc):
    def __init__(txt = ""):
        self.txt = txt
        pass

    def popTxt(self):
        slide = self.txt[0:16]
        self.txt = self.txt[16:]
        return slide

    def getTxt(self):
        return self.txt

    def setTxt(self, txt):
        self.txt = txt

class srcFile(PlainTxtSrc):
    def __init__(path = None):
        self.path = path
        self.f = None

    def popTxt(self):
        if self.f == None:
            self.f = open(path, 'r')
        return self.f.read(16);

    def setFile(self, path):
        self.path = path
        if (self.f not None):
            self.f.close()
            self.f = None

    def __del__(self):
        if (self.f not None):
            self.f.close()
