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

        self.resize(800, 565)
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
        self.loadBtn.move(690, 5)
        self.loadBtn.setText("Load Map")
        self.loadBtn.resize(100, 30)
        self.loadBtn.clicked.connect(self._handleNewLevel)

        self.loadBtn = QtGui.QPushButton(self)
        self.loadBtn.move(690, 45)
        self.loadBtn.setText("Load Server")
        self.loadBtn.resize(100, 30)
        self.loadBtn.setEnabled(False)
        #self.loadBtn.clicked.connect(self._handleNewServer) ##TODO AFTER THE PROJECT (BONUSà

    def _handleNewLevel(self):
        ## copied from MainWindow loadMap
        dialog = QtGui.QFileDialog(self, 'Browse', saveFileDir)
        result = dialog.getExistingDirectory().toLocal8Bit().data().decode('iso-8859-1')
        
        try:
            cover = MapDest(result)
            StegoMinecraftBase.Instance.coverMediaDest = cover
            self.updateInfo()
            dumpMapDest(cover)
            
        except ValueError, e:
            print str(e)
            QtGui.QMessageBox.information(self, 'Info Message', str(e), QtGui.QMessageBox.Ok)

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
        self.hLine.setGeometry(5, 130, 150, 5)
        self.hLine.setFrameShadow(QtGui.QFrame.Raised)
        self.hLine.setFrameStyle(QtGui.QFrame.HLine)
        
    def _initDimensions(self):
        self.dimLbl = QtGui.QLabel(self)
        self.dimLbl.move(5, 145)
        self.dimLbl.setText("Selected Dimension :")

        self.dimSelect = QtGui.QComboBox(self)
        self.dimSelect.move(150, 145)
        self.dimSelect.addItem(QtCore.QString("Overworld (0)"))
        self.dimSelect.addItem(QtCore.QString("Nether      (1)"))
        self.dimSelect.addItem(QtCore.QString("End           (2)"))
        self.dimSelect.currentIndexChanged.connect(self._handleNewDimension)
        self.dimSelect.setEnabled(False)

    def _handleNewDimension(self, index):
        if StegoMinecraftBase.Instance != None and StegoMinecraftBase.Instance.coverMediaDest != None:
            self.chunkPosXTxt.setText("0")
            self.chunkPosZTxt.setText("0")
            self._stegoBase.coverMediaDest.selectDimension(index)
            self._stegoBase.coverMediaDest.prepareChunkInfo(0, 0)
            self._updateTable()

    def _initBRepartition(self):
        self.dictLbl = QtGui.QLabel(self)
        self.dictLbl.move(5, 190)
        self.dictLbl.setText("Selected preview in Chunk(X, Z) :")

        self.chunkPosXTxt = QtGui.QLineEdit(self)
        self.chunkPosXTxt.move(205, 190)
        self.chunkPosXTxt.resize(40, 20)
        self.chunkPosXTxt.setText("0")
        self.chunkPosXTxt.setEnabled(False)

        self.chunkPosZTxt = QtGui.QLineEdit(self)
        self.chunkPosZTxt.move(255, 190)
        self.chunkPosZTxt.resize(40, 20)
        self.chunkPosZTxt.setText("0")
        self.chunkPosZTxt.setEnabled(False)
        
        self.chunkBtn = QtGui.QPushButton(self)
        self.chunkBtn.move(305, 190)
        self.chunkBtn.setText(">")
        self.chunkBtn.resize(30, 20)
        self.chunkBtn.clicked.connect(self._handleNewChunk)
        self.chunkBtn.setEnabled(False)
        
        self.nbBlockLbl = QtGui.QLabel(self)
        self.nbBlockLbl.move(370, 190)
        self.nbBlockLbl.setText("Nb Blocks in Chunk :")
        self.nbBlockValueLbl = QtGui.QLabel(self)
        self.nbBlockValueLbl.move(500, 190)
        
        self.nbDifLbl = QtGui.QLabel(self)
        self.nbDifLbl.move(560, 190)
        self.nbDifLbl.setText("Nb unique Blocks in Chunk :")
        self.nbDifValueLbl = QtGui.QLabel(self)
        self.nbDifValueLbl.move(730, 190)

        self.entLbl = QtGui.QLabel(self)
        self.entLbl.move(370, 220)
        self.entLbl.setText("Entropy calculated in Chunk :")
        self.entValueLbl = QtGui.QLabel(self)
        self.entValueLbl.move(540, 220)
        
        self.repLbl = QtGui.QLabel(self)
        self.repLbl.move(10, 260)
        self.repLbl.setText("Preview blocks repartition :")

        self.repTab = QtGui.QTableWidget(self)
        self.repTab.move(20, 290)
        self.repTab.resize(400, 240)
        self.repTab.setColumnCount(2)
        self.repTab.setHorizontalHeaderLabels(['Block','Quantity'])
        self.repTab.horizontalHeader().resizeSection(0, 200);
        self.repTab.setSelectionMode(QtGui.QTableWidget.NoSelection)
        self.repTab.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        
        self.repLbl = QtGui.QLabel(self)
        self.repLbl.move(460, 260)
        self.repLbl.setText("Preview biomes repartition :")

        self.biomeTab = QtGui.QTableWidget(self)
        self.biomeTab.move(470, 290)
        self.biomeTab.resize(300, 240)
        self.biomeTab.setColumnCount(1)
        self.biomeTab.setHorizontalHeaderLabels(['Biome found'])
        self.biomeTab.setSelectionMode(QtGui.QTableWidget.NoSelection)
        self.biomeTab.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)

    def _handleNewChunk(self):
        if StegoMinecraftBase.Instance != None and StegoMinecraftBase.Instance.coverMediaDest != None:
            posX = self.chunkPosXTxt.text().toInt()
            posZ = self.chunkPosZTxt.text().toInt()
            if (posX[1] == True and posZ[1] == True):
                cover = StegoMinecraftBase.Instance.coverMediaDest 
                cover.prepareChunkInfo(posX[0], posZ[0])
                self._updateTable()

    def _updateTable(self):
        if StegoMinecraftBase.Instance != None and StegoMinecraftBase.Instance.coverMediaDest != None:
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

