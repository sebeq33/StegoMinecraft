# -*- coding: iso-8859-1 -*-

import sys
import os
import subprocess
import StegoMinecraftBase
from pymclevel.mclevelbase import saveFileDir
from MinecraftUtility import dumpMapDest
from CoverMediaDest import MapDest
from PyQt4 import QtGui
from PyQt4 import QtCore

class TabPreview(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.resize(990, 750)
        self._initLoadButton()
        self._initInfoLabels()
        self._initSeparator()
        self._initDimensions()
        self._initBRepartition()
        self.updateInfo()
        
    def updateInfo(self):
        if (StegoMinecraftBase.Instance != None and StegoMinecraftBase.Instance.coverMediaDest != None):
            cover = StegoMinecraftBase.Instance.coverMediaDest
            self.pathValueLbl.setText(cover.path)
            self.seedValueLbl.setText(str(cover.seed))
            self.nbChunkValueLbl.setText(str(cover.nbChunks))
            self.capValueLbl.setText(str(cover.capacity[2]) 
                                    + " X / " + str(cover.capacity[3])
                                    + " Z (" + str(cover.capacity[2] * cover.capacity[3])
                                    + " Chunks)")

            self.pathValueLbl.adjustSize()
            self.seedValueLbl.adjustSize()
            self.nbChunkValueLbl.adjustSize()
            self.capValueLbl.adjustSize()
            self._updateTable()

    def _initLoadButton(self):
        self.loadBtn = QtGui.QPushButton(self)
        self.loadBtn.move(860, 5)
        self.loadBtn.setText("Load Map")
        self.loadBtn.resize(120, 30)
        self.loadBtn.clicked.connect(self._handleNewLevel)

        self.loadBtn = QtGui.QPushButton(self)
        self.loadBtn.move(860, 50)
        self.loadBtn.setText("Load Server")
        self.loadBtn.resize(120, 30)
        self.loadBtn.setEnabled(False)
        #self.loadBtn.clicked.connect(self._handleNewServer) ##TODO AFTER THE PROJECT (BONUSà

    def _handleNewLevel(self):
        window = self.nativeParentWidget()
        if window != None:
            window.openMapDest()

    def _initInfoLabels(self):
        self.pathLbl = QtGui.QLabel(self)
        self.pathLbl.move(5, 10) ## X -> , Y !
        self.pathLbl.setText("Path :")
        self.pathValueLbl = QtGui.QLabel(self)
        self.pathValueLbl.move(150, 10)

        self.seedLbl = QtGui.QLabel(self)
        self.seedLbl.move(5, 40)
        self.seedLbl.setText("Map Seed :")
        self.seedValueLbl = QtGui.QLabel(self)
        self.seedValueLbl.move(150, 40)
                
        self.nbChunkLbl = QtGui.QLabel(self)
        self.nbChunkLbl.move(5, 70)
        self.nbChunkLbl.setText("Nb Chunk :")
        self.nbChunkValueLbl = QtGui.QLabel(self)
        self.nbChunkValueLbl.move(150, 70)
        
        self.capLbl = QtGui.QLabel(self)
        self.capLbl.move(5, 100)
        self.capLbl.setText("Capacity :")
        self.capValueLbl = QtGui.QLabel(self)
        self.capValueLbl.move(150, 100)
        
    def _initSeparator(self):
        self.hLine = QtGui.QFrame(self)
        self.hLine.setGeometry(5, 150, 150, 5)
        self.hLine.setFrameShadow(QtGui.QFrame.Raised)
        self.hLine.setFrameStyle(QtGui.QFrame.HLine)
        
    def _initDimensions(self):
        self.dimLbl = QtGui.QLabel(self)
        self.dimLbl.move(10, 200)
        self.dimLbl.setText("Selected Dimension :")

        self.dimSelect = QtGui.QComboBox(self)
        self.dimSelect.move(170, 200)
        self.dimSelect.addItem(QtCore.QString("Overworld (0)"))
        self.dimSelect.addItem(QtCore.QString("Nether      (1)"))
        self.dimSelect.addItem(QtCore.QString("End           (2)"))
        self.dimSelect.currentIndexChanged.connect(self._handleNewDimension)
        self.dimSelect.setEnabled(False)
    
        self.focusInEvent = self._handleFocusIn

    def _handleFocusIn(self, event):
        if StegoMinecraftBase.Instance.coverMediaDest != None:
            cover = StegoMinecraftBase.Instance.coverMediaDest
            if (cover.selectedDim != self.dimSelect.currentIndex()):
                self.dimSelect.setCurrentIndex(cover.selectedDim)
                self._handleNewDimension(cover.selectedDim)

    def _handleNewDimension(self, index):
        if StegoMinecraftBase.Instance.coverMediaDest != None:
            cover = StegoMinecraftBase.Instance.coverMediaDest
            self.chunkPosXTxt.setText("0")
            self.chunkPosZTxt.setText("0")
            cover.selectDimension(index)
            cover.prepareChunkInfo(0, 0)
            self.updateInfo()

    def _initBRepartition(self, x = 0, y = 250):
        self.dictLbl = QtGui.QLabel(self)
        self.dictLbl.move(x + 10, y)
        self.dictLbl.setText("Selected preview in Chunk(X, Z) :")

        self.chunkPosXTxt = QtGui.QLineEdit(self)
        self.chunkPosXTxt.move(x + 250, y)
        self.chunkPosXTxt.resize(50, 20)
        self.chunkPosXTxt.setText("0")
        self.chunkPosXTxt.setEnabled(False)

        self.chunkPosZTxt = QtGui.QLineEdit(self)
        self.chunkPosZTxt.move(x + 320, y)
        self.chunkPosZTxt.resize(50, 20)
        self.chunkPosZTxt.setText("0")
        self.chunkPosZTxt.setEnabled(False)
        
        self.chunkBtn = QtGui.QPushButton(self)
        self.chunkBtn.move(x + 390, y)
        self.chunkBtn.setText(">")
        self.chunkBtn.resize(40, 20)
        self.chunkBtn.clicked.connect(self._handleNewChunk)
        self.chunkBtn.setEnabled(False)
        
        self.nbBlockLbl = QtGui.QLabel(self)
        self.nbBlockLbl.move(x + 10, y + 50)
        self.nbBlockLbl.setText("Nb Blocks in Chunk :")
        self.nbBlockValueLbl = QtGui.QLabel(self)
        self.nbBlockValueLbl.move(x + 200, y + 50)
        
        self.nbDifLbl = QtGui.QLabel(self)
        self.nbDifLbl.move(x + 300, y + 50)
        self.nbDifLbl.setText("Nb unique Blocks in Chunk :")
        self.nbDifValueLbl = QtGui.QLabel(self)
        self.nbDifValueLbl.move(x + 500, y + 50)

        self.entLbl = QtGui.QLabel(self)
        self.entLbl.move(x + 10, y + 100)
        self.entLbl.setText("Entropy calculated in Chunk :")
        self.entValueLbl = QtGui.QLabel(self)
        self.entValueLbl.move(x + 200, y + 100)
        
        self.repLbl = QtGui.QLabel(self)
        self.repLbl.move(x + 10, y + 150)
        self.repLbl.setText("Preview blocks repartition :")

        self.repTab = QtGui.QTableWidget(self)
        self.repTab.move(x + 20, y + 200)
        self.repTab.resize(400, 240)
        self.repTab.setColumnCount(2)
        self.repTab.setHorizontalHeaderLabels(['Block','Quantity'])
        self.repTab.horizontalHeader().resizeSection(0, 200);
        self.repTab.setSelectionMode(QtGui.QTableWidget.NoSelection)
        self.repTab.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        
        self.repLbl = QtGui.QLabel(self)
        self.repLbl.move(x + 460, y + 150)
        self.repLbl.setText("Preview biomes repartition :")

        self.biomeTab = QtGui.QTableWidget(self)
        self.biomeTab.move(x + 470, y + 200)
        self.biomeTab.resize(300, 240)
        self.biomeTab.setColumnCount(1)
        self.biomeTab.horizontalHeader().resizeSection(0, 200);
        self.biomeTab.setHorizontalHeaderLabels(['Biome found'])
        self.biomeTab.setSelectionMode(QtGui.QTableWidget.NoSelection)
        self.biomeTab.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)

    def _handleNewChunk(self):
        if StegoMinecraftBase.Instance.coverMediaDest != None:
            posX = self.chunkPosXTxt.text().toInt()
            posZ = self.chunkPosZTxt.text().toInt()
            if (posX[1] == True and posZ[1] == True):
                cover = StegoMinecraftBase.Instance.coverMediaDest 
                cover.prepareChunkInfo(posX[0], posZ[0])
                self._updateTable()

    def _updateTable(self):
        if StegoMinecraftBase.Instance.coverMediaDest != None:
            cover = StegoMinecraftBase.Instance.coverMediaDest
            self.nbBlockValueLbl.setText(str(cover.sampleNbBlock))
            self.nbBlockValueLbl.adjustSize()
            
            self.nbDifValueLbl.setText(str(cover.sampleDif))
            self.nbDifValueLbl.adjustSize()

            self.entValueLbl.setText(str(cover.sampleEntropy))
            self.entValueLbl.adjustSize()

            self.repTab.setRowCount(len(cover.blocksDict))
            for i, key in enumerate(cover.blocksDict.keys()):
                block = QtGui.QTableWidgetItem(key)
                self.repTab.setItem(i, 0, block)
                qtt = QtGui.QTableWidgetItem(str(cover.blocksDict[key]))
                self.repTab.setItem(i, 1, qtt)
        
            self.biomeTab.setRowCount(len(cover.sampleBiomes))
            for i, name in enumerate(cover.sampleBiomes):
                biome = QtGui.QTableWidgetItem(name)
                self.biomeTab.setItem(i, 0, biome)
        
            self.dimSelect.setCurrentIndex(cover.selectedDim)
            self.dimSelect.setEnabled(True)
            self.chunkPosXTxt.setEnabled(True)
            self.chunkPosZTxt.setEnabled(True)
            self.chunkBtn.setEnabled(True)

