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

        self.infoLbl = QtGui.QTextEdit(self)
        self.infoLbl.setText("# TODO HERE, reselect dimension, Modification limits X/Y/Z, block used (Pos / negative), protected blocks (Pos / negative)")
        self.infoLbl.move(5, 5)
        self.infoLbl.adjustSize()
