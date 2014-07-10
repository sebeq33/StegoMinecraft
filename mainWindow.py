# -*- coding: iso-8859-1 -*-

import sys
import os
import subprocess
import StegoMinecraftBase
from minecraftUtility import getAvailMaps
from coverMediaDest import MapDest, ServerDest
from pymclevel.mclevelbase import saveFileDir
from PyQt4 import QtGui
from PyQt4 import QtCore

class MainWindow(QtGui.QWidget):
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        QtGui.QMainWindow.__init__(self)
        
        self.minecraftBase = StegoMinecraftBase.StegoMinecraftBase()
        self.initWindow()
        self.initList()
        self.initMenuBar()

        self.show()
        sys.exit(self.app.exec_())
        
    def initWindow(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('StegoMinecraft')
        
        #center window on screen
        sc = QtGui.QDesktopWidget().screenGeometry()
        me = self.geometry()
        self.move((sc.width() - me.width()) / 2,
                  (sc.height() - me.height()) / 2)
        
    def initList(self):
        self.listLbl = QtGui.QLabel(self)
        self.listLbl.move(5, 30)
        self.listLbl.setText("Save list : ")
        self.listLbl.setFont(QtGui.QFont("Time New Roman", 10))

        self.listMap = QtGui.QListWidget(self)
        self.listMap.move(5, 55)
        self.listMap.resize(200, 540)
        
        for m in getAvailMaps():
            self.listMap.addItem(m)
            
        self.listMap.setCurrentRow(0)

    def initMenuBar(self):
        self.menuBar = QtGui.QMenuBar(self)
        self.menuBar.resize(800, 25)
        newAct = QtGui.QAction("Open Minecraft Directory", self)
        newAct.triggered.connect(self.openMenu);
        fileMenu = self.menuBar.addMenu("File")
        fileMenu.addAction(newAct)

    def openMenu(self):
        dialog = QtGui.QFileDialog(self, 'Browse', saveFileDir)
        result = dialog.getExistingDirectory().toLocal8Bit().data().decode('iso-8859-1')

        try:
            cover = MapDest(result)
            self.minecraftBase.coverDestMedia = cover 
            print "PATH                       : ", self.minecraftBase.coverDestMedia.path
            print "CURRENT DIMENSION          : ", str(self.minecraftBase.coverDestMedia.selectedDimName)
            print "SEED                       : ", str(self.minecraftBase.coverDestMedia.seed)
            print "NB CHUNKS                  : ", str(self.minecraftBase.coverDestMedia.nbChunks)
            print "NB BLOCK IN CHUNK 0, 0     : ", str(self.minecraftBase.coverDestMedia.sampleNbBlock)
            print "NB DIF BLOCK IN CHUNK 0, 0 : ", str(self.minecraftBase.coverDestMedia.sampleDif)
            print "ENTROPY IN CHUNK 0, 0      : ", str(self.minecraftBase.coverDestMedia.sampleEntropy)
            print "BIOMES IN CHUNK 0, 0       : ", str(self.minecraftBase.coverDestMedia.sampleBiomes)

            for key in self.minecraftBase.coverDestMedia.blocksDict.keys():
                print "# ", key, ": ", self.minecraftBase.coverDestMedia.blocksDict[key] 
            print
        except ValueError, e:
            print str(e) 

        mapName = os.path.basename(result)        
        items = self.listMap.findItems(mapName, QtCore.Qt.MatchExactly)
        if len(items) > 0:
            self.listMap.setCurrentItem(items[0])
