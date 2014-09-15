# -*- coding: iso-8859-1 -*-

import sys
import os
import subprocess
import StegoMinecraftBase
from PyQt4 import QtGui
from PyQt4 import QtCore

class TabsPreview(QtGui.QWidget):
    def __init__(self, stegoBase = None):
        QtGui.QWidget.__init__(self)

        self._stegoBase = stegoBase
        self.resize(800, 565)
        self._initInfoLabels()
        self._initSeparator()
        self._initDimensions()
        self._initBRepartition()
        self.updateInfo()
        
    def updateInfo(self, stegoBase = None):
        if (stegoBase != None):
            self._stegoBase = stegoBase
        if (self._stegoBase != None and self._stegoBase.coverMediaDest != None):
            cover = self._stegoBase.coverMediaDest
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

    def _initInfoLabels(self):
        self.pathLbl = QtGui.QLabel(self)
        self.pathLbl.move(5, 30) ## X -> , Y !
        self.pathLbl.setText("Path :")
        self.pathValueLbl = QtGui.QLabel(self)
        self.pathValueLbl.move(150, 30)

        self.seedLbl = QtGui.QLabel(self)
        self.seedLbl.move(5, 60)
        self.seedLbl.setText("Map Seed :")
        self.seedValueLbl = QtGui.QLabel(self)
        self.seedValueLbl.move(150, 60)
                
        self.nbChunkLbl = QtGui.QLabel(self)
        self.nbChunkLbl.move(5, 90)
        self.nbChunkLbl.setText("Nb Chunk :")
        self.nbChunkValueLbl = QtGui.QLabel(self)
        self.nbChunkValueLbl.move(150, 90)
        
        self.capLbl = QtGui.QLabel(self)
        self.capLbl.move(5, 120)
        self.capLbl.setText("Capacity :")
        self.capValueLbl = QtGui.QLabel(self)
        self.capValueLbl.move(150, 120)
        
    def _initSeparator(self):
        self.hLine = QtGui.QFrame(self)
        self.hLine.setGeometry(5, 150, 150, 5)
        self.hLine.setFrameShadow(QtGui.QFrame.Raised)
        self.hLine.setFrameStyle(QtGui.QFrame.HLine)
        
    def _initDimensions(self):
        self.dimLbl = QtGui.QLabel(self)
        self.dimLbl.move(5, 170)
        self.dimLbl.setText("Selected Dimension :")

        self.dimSelect = QtGui.QComboBox(self)
        self.dimSelect.move(150, 170)
        self.dimSelect.addItem(QtCore.QString("Overworld (0)"))
        self.dimSelect.addItem(QtCore.QString("Nether      (1)"))
        self.dimSelect.addItem(QtCore.QString("End           (2)"))
        self.dimSelect.currentIndexChanged.connect(self._handleNewDimension)
        self.dimSelect.setEnabled(False)

    def _handleNewDimension(self, index):
        if self._stegoBase != None and self._stegoBase.coverMediaDest != None:
            self.chunkPosXTxt.setText("0")
            self.chunkPosZTxt.setText("0")
            self._stegoBase.coverMediaDest.selectDimension(index)
            self._stegoBase.coverMediaDest.prepareChunkInfo(0, 0)
            self._updateTable()

    def _initBRepartition(self):
        self.dictLbl = QtGui.QLabel(self)
        self.dictLbl.move(5, 210)
        self.dictLbl.setText("Selected preview in Chunk(X, Z) :")

        self.chunkPosXTxt = QtGui.QLineEdit(self)
        self.chunkPosXTxt.move(205, 210)
        self.chunkPosXTxt.resize(40, 20)
        self.chunkPosXTxt.setText("0")
        self.chunkPosXTxt.setEnabled(False)

        self.chunkPosZTxt = QtGui.QLineEdit(self)
        self.chunkPosZTxt.move(255, 210)
        self.chunkPosZTxt.resize(40, 20)
        self.chunkPosZTxt.setText("0")
        self.chunkPosZTxt.setEnabled(False)
        
        self.chunkBtn = QtGui.QPushButton(self)
        self.chunkBtn.move(305, 210)
        self.chunkBtn.setText(">")
        self.chunkBtn.resize(30, 20)
        self.chunkBtn.clicked.connect(self._handleNewChunk)
        self.chunkBtn.setEnabled(False)
        
        self.nbBlockLbl = QtGui.QLabel(self)
        self.nbBlockLbl.move(350, 210)
        self.nbBlockLbl.setText("Nb Blocks in Chunk :")
        self.nbBlockValueLbl = QtGui.QLabel(self)
        self.nbBlockValueLbl.move(480, 210)
        
        self.nbDifLbl = QtGui.QLabel(self)
        self.nbDifLbl.move(540, 210)
        self.nbDifLbl.setText("Nb unique Blocks in Chunk :")
        self.nbDifValueLbl = QtGui.QLabel(self)
        self.nbDifValueLbl.move(710, 210)

        self.entLbl = QtGui.QLabel(self)
        self.entLbl.move(350, 250)
        self.entLbl.setText("Entropy calculated in Chunk :")
        self.entValueLbl = QtGui.QLabel(self)
        self.entValueLbl.move(520, 250)

    def _handleNewChunk(self):
        if self._stegoBase != None and self._stegoBase.coverMediaDest != None:
            posX = self.chunkPosXTxt.text().toInt()
            posZ = self.chunkPosZTxt.text().toInt()
            if (posX[1] == True and posZ[1] == True):
                self._stegoBase.coverMediaDest.prepareChunkInfo(posX[0], posZ[0])
                self._updateTable()

    def _updateTable(self):
        if self._stegoBase != None and self._stegoBase.coverMediaDest != None:
            self.nbBlockValueLbl.setText(str(self._stegoBase.coverMediaDest.sampleNbBlock))
            self.nbBlockValueLbl.adjustSize()
            
            self.nbDifValueLbl.setText(str(self._stegoBase.coverMediaDest.sampleDif))
            self.nbDifValueLbl.adjustSize()

            self.entValueLbl.setText(str(self._stegoBase.coverMediaDest.sampleEntropy))
            self.entValueLbl.adjustSize()

            self.dimSelect.setCurrentIndex(self._stegoBase.coverMediaDest.selectedDim)
            self.dimSelect.setEnabled(True)
            self.chunkPosXTxt.setEnabled(True)
            self.chunkPosZTxt.setEnabled(True)
            self.chunkBtn.setEnabled(True)

