# -*- coding: iso-8859-1 -*-

import sys
import os
import subprocess
import StegoMinecraftBase
from PyQt4 import QtGui
from PyQt4 import QtCore

class tabsPreview(QtGui.QWidget):
    def __init__(self, stegoBase):
        self.stegoBase = stegoBase

        self._initInfoLabels()
        self._initDimensions()
        self._initBRepartition()
        self.updateInfo()
        ##self.show();
        
    def updateInfo():
        self.pathValueLbl.setText(self.stegoBase.coverMediaDest.path)
        pass
    
    def _initInfoLabels(self):
        self.pathLbl = QtGui.QLabel(self)
        self.pathLbl.move(5, 5)
        self.pathLbl.setText("Path :")
        self.pathValueLbl = QtGui.QLabel(self)
        self.pathValueLbl.move(30, 5)

    def _initDimensions(self):
        pass

    def _initBRepartions(self):
        pass


