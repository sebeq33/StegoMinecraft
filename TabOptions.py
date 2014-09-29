# -*- coding: iso-8859-1 -*-

import sys
import os
import StegoMinecraftBase
from PyQt4 import QtGui
from PyQt4 import QtCore

class TabOptions(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.resize(800, 565)

        self._initDimension()
        self._initSeparator()
        self._initLimits()
        # self._initUsedBlocks()
        # self._initProtectedBlocks()

        self.updateInfo()

        # self.infoLbl = QtGui.QTextEdit(self)
        # self.infoLbl.setText("# TODO HERE, reselect dimension, Modification limits X/Y/Z, block used (Pos / negative), protected blocks (Pos / negative)")
        # self.infoLbl.move(5, 5)
        # self.infoLbl.adjustSize()

    def _initDimension(self):
        self.dimLbl = QtGui.QLabel(self)
        self.dimLbl.move(5, 30)
        self.dimLbl.setText("Selected Dimension :")

        self.dimSelect = QtGui.QComboBox(self)
        self.dimSelect.move(150, 30)
        self.dimSelect.addItem(QtCore.QString("Overworld (0)"))
        self.dimSelect.addItem(QtCore.QString("Nether      (1)"))
        self.dimSelect.addItem(QtCore.QString("End           (2)"))
        self.dimSelect.currentIndexChanged.connect(self._handleNewDimension)
        self.dimSelect.setEnabled(False)
        
        self.capLbl = QtGui.QLabel(self)
        self.capLbl.move(5, 70)
        self.capLbl.resize(250, 20)
        self.capLbl.setText("Capacity details (edge modification limits) :")
        self.capValueLbl = QtGui.QLabel(self)
        self.capValueLbl.move(300, 70)

        self.focusInEvent = self._handleFocusIn

    def _handleFocusIn(self, event): ##TO UPDATE DIMENSION
        if StegoMinecraftBase.Instance.coverMediaDest != None:
            ## REDISPLAY INFO IF DIMENSION CHANGED
            cover = StegoMinecraftBase.Instance.coverMediaDest
            if (cover.selectedDim != self.dimSelect.currentIndex()):
                self.dimSelect.setCurrentIndex(cover.selectedDim)
                self.dimSelect.setEnabled(True)
                
                ## CAPACITY
                limNegX = cover.capacity[0] * 16
                limPosX = (cover.capacity[0] + cover.capacity[2]) * 16
                limNegZ = cover.capacity[1] * 16
                limPosZ = (cover.capacity[1] + cover.capacity[3]) * 16
                
                self.capValueLbl.setText(
                    "X(" + str(limNegX) + ", " + str(limPosX) + ") \t" 
                    + "Y(0, 256) \t" 
                    + "Z(" + str(limNegZ) + ", " + str(limPosZ) + ")") 
                self.capValueLbl.adjustSize()

    def _handleNewDimension(self, index):
        if StegoMinecraftBase.Instance.coverMediaDest != None:
            cover = StegoMinecraftBase.Instance.coverMediaDest
            cover.selectDimension(index)
            cover.prepareChunkInfo(0, 0)
            self.updateInfo()

    def updateInfo(self): ##FOR NEW MAP
        if StegoMinecraftBase.Instance.coverMediaDest != None:
            cover = StegoMinecraftBase.Instance.coverMediaDest
            self.dimSelect.setCurrentIndex(cover.selectedDim)
            self.dimSelect.setEnabled(True)

            ## CAPACITY
            limNegX = (cover.capacity[0]) * 16
            limPosX = (cover.capacity[0] + cover.capacity[2]) * 16 - 1
            limNegZ = (cover.capacity[1]) * 16
            limPosZ = (cover.capacity[1] + cover.capacity[3]) * 16 - 1

            self.capValueLbl.setText(
                "X(" + str(limNegX) + ", " + str(limPosX) + ") \t" 
                + "Y(0, 255) \t" 
                + "Z(" + str(limNegZ) + ", " + str(limPosZ) + ")") 
            self.capValueLbl.adjustSize()
            
            ## SELECTION LIMIT RANGE
            self.limitNegXSB.setRange(limNegX, limPosX)
            self.limitNegXSB.setValue(limNegX)
            self.limitPosXSB.setRange(limNegX, limPosX)
            self.limitPosXSB.setValue(limPosX)

            self.limitNegYSB.setRange(0, 255)
            self.limitNegYSB.setValue(0)
            self.limitPosYSB.setRange(0, 255)
            self.limitPosYSB.setValue(255)

            self.limitNegZSB.setRange(limNegZ, limPosZ)
            self.limitNegZSB.setValue(limNegZ)
            self.limitPosZSB.setRange(limNegZ, limPosZ)
            self.limitPosZSB.setValue(limPosZ)
            
            ##ENABLE SpinBox
            self.limitPosXSB.setEnabled(True)
            self.limitNegXSB.setEnabled(True)
            self.limitPosYSB.setEnabled(True)
            self.limitNegYSB.setEnabled(True)            
            self.limitPosZSB.setEnabled(True)
            self.limitNegZSB.setEnabled(True)
            self._handleNewLimits()

    def _initSeparator(self):
        self.hLine = QtGui.QFrame(self)
        self.hLine.setGeometry(5, 100, 150, 5)
        self.hLine.setFrameShadow(QtGui.QFrame.Raised)
        self.hLine.setFrameStyle(QtGui.QFrame.HLine)

    def _createLimitLineEdit(self, x, y, val = 0):
        lim = QtGui.QSpinBox(self)
        lim.move(x, y)
        lim.resize(60, 20)
        lim.setValue(val)
        lim.setEnabled(False)
        lim.focusOutEvent = self._handleNewLimits
        return lim

    def _initLimits(self, x = 0, y = 130):
        self.limitTopLbl = QtGui.QLabel(self)
        self.limitTopLbl.move(x + 5, y)
        self.limitTopLbl.setText("Selected Modification limits (blocks) :")
        self.limitTopLbl.adjustSize()

        self.limitXLbl = QtGui.QLabel(self)
        self.limitXLbl.move(x + 50, y + 30)
        self.limitXLbl.setText("X :")
        self.limitNegXSB = self._createLimitLineEdit(x + 80, y + 30)
        self.limitPosXSB = self._createLimitLineEdit(x + 150, y + 30)

        self.limitYLbl = QtGui.QLabel(self)
        self.limitYLbl.move(x + 240, y + 30)
        self.limitYLbl.setText("Y :")
        self.limitNegYSB = self._createLimitLineEdit(x + 270, y + 30)
        self.limitPosYSB = self._createLimitLineEdit(x + 340, y + 30)

        self.limitZLbl = QtGui.QLabel(self)
        self.limitZLbl.move(x + 430, y + 30)
        self.limitZLbl.setText("Z :")
        self.limitNegZSB = self._createLimitLineEdit(x + 460, y + 30)
        self.limitPosZSB = self._createLimitLineEdit(x + 530, y + 30)

    def _handleNewLimits(self, event = None):
        negX = self.limitNegXSB.value()
        posX = self.limitPosXSB.value()
        negY = self.limitNegYSB.value()
        posY = self.limitPosYSB.value()
        posZ = self.limitPosZSB.value()
        negZ = self.limitNegZSB.value()

        error = None
        if negX > posX:
            error = "Error, negX > posX"
            self.limitPosXSB.setValue(negX)
        if negY > posY:
            error = "Error, negY > posY"
            self.limitPosYSB.setValue(negY)
        if negZ > posZ:
            error = "Error, negZ > posZ"
            self.limitPosZSB.setValue(negZ)

        if error == None:
            StegoMinecraftBase.Instance.limits = ((negX, posX),(negY, posY),(negZ, posZ))



