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

    def count(self):
        raise NotImplementedError("Empty PlainTxtSrc interface, use srcTxt or srcFile")



class SrcTxt(PlainTxtSrc):
    def __init__(self, txt = ""):
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

    def count(self):
        return len(self.txt)

class SrcFile(PlainTxtSrc):
    def __init__(self, path = None):
        self.path = path
        self.f = None

    def isReady():
        return (self.path != None and self.path != "")
        
    def popTxt(self):
        if self.path == None:
            return ""
        if self.f == None:
            self.f = open(self.path, 'r')
        return self.f.read(16);

    def setPath(self, path):
        print "SET PATH"
        self.path = path
        if (self.f != None):
            self.f.close()
            self.f = None

    def count(self):
        if (self.path != None):
            try:
                return os.path.getsize(self.path)
            except:
                return 0
        return 0
        
    def close(self):
        if (self.f != None):
            self.f.close()
        
    def __del__(self):
        if (self.f != None):
            self.f.close()
