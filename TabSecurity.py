# -*- coding: iso-8859-1 -*-

import sys
import os
import StegoMinecraftBase
import hashlib
from PyQt4 import QtGui
from PyQt4 import QtCore

class TabSecurity(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.resize(800, 565)
        self._initPass()
        self._initEncryption()
        self._initCompression()

    def _initPass(self):
        self.passLbl = QtGui.QLabel(self)
        self.passLbl.move(5, 10)
        self.passLbl.setText("Set a password (to create hash): ")
        self.passLbl.resize(200, 30)

        self.countLbl = QtGui.QLabel(self)
        self.countLbl.move(220, 15)
        self.countLbl.setText("(0) bytes")
        self.countLbl.resize(200, 20)

        self.passTxt = QtGui.QLineEdit(self)
        self.passTxt.move(10, 50)
        self.passTxt.resize(400, 30)
        self.passTxt.setMaxLength(999)
        self.passTxt.setEchoMode(QtGui.QLineEdit.Password)
        self.passTxt.focusOutEvent = self._handlePassFocusLost
        self.passTxt.textChanged.connect(self._handleCountChanged)

    def _handlePassFocusLost(self, event):
        passw = self.passTxt.text().toLocal8Bit().data()
        if passw != "":
            StegoMinecraftBase.Instance.key = hashlib.sha256(passw).hexdigest() ## No salt, bc no data are saved

    def _handleCountChanged(self):
        self.countLbl.setText("("+ str(self.passTxt.text().count()) +") bytes")

    def _initEncryption(self):
        self.encryptCb = QtGui.QCheckBox(self)
        self.encryptCb.move(5, 200)
        self.encryptCb.setText("Enable encryption (using same password)")
        self.encryptCb.stateChanged.connect(self._handleEncryption)
        self.encryptCb.setEnabled(False)

    def _handleEncryption(self):
        StegoMinecraftBase.Instance.options.encryption = self.encryptCb.isChecked()

    def _initCompression(self):
        self.comprCb = QtGui.QCheckBox(self)
        self.comprCb.move(5, 230)
        self.comprCb.setText("Enable compression")
        self.comprCb.stateChanged.connect(self._handleCompression)
        self.comprCb.setEnabled(False)

    def _handleCompression(self):
        StegoMinecraftBase.Instance.options.compression = self.comprCb.isChecked()
