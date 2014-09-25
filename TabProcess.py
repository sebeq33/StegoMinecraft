# -*- coding: iso-8859-1 -*-

import sys
import os
import StegoMinecraftBase
from PyQt4 import QtGui
from PyQt4 import QtCore
from pymclevel.mclevelbase import ChunkNotPresent

class TabProcess(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.resize(800, 565)
        self._initProcess()
        self._initSeparator()
        self._initRetrieve()

    def _initProcess(self):
        self.okLbl = QtGui.QLabel(self)
        self.okLbl.move(5, 10)
        self.okLbl.setText("Insert the input source in the selected minecraft map")
        self.okLbl.adjustSize()

        self.launchBtn = QtGui.QPushButton(self)
        self.launchBtn.move(700, 200)
        self.launchBtn.setText("Launch")
        self.launchBtn.resize(80, 30)
        self.launchBtn.clicked.connect(self._launchProcess)

    def _initSeparator(self):
        self.hLine = QtGui.QFrame(self)
        self.hLine.setGeometry(5, 250, 780, 5)
        self.hLine.setFrameShadow(QtGui.QFrame.Raised)
        self.hLine.setFrameStyle(QtGui.QFrame.HLine)
        
    def _initRetrieve(self):
        self.outFileTxt = QtGui.QLineEdit(self)
        self.outFileTxt.move(5, 300)
        self.outFileTxt.resize(640, 30)
        self.outFileTxt.setText("Result.txt")

        self.fileBtn = QtGui.QPushButton(self)
        self.fileBtn.move(670, 300)
        self.fileBtn.setText("Select Output File")
        self.fileBtn.resize(110, 30)
        self.fileBtn.clicked.connect(self._handleNewFile)

        self.readLbl = QtGui.QLabel(self)
        self.readLbl.move(5, 350)
        self.readLbl.setText("Nb bytes to read : ")
        self.readLbl.resize(120, 30)
        
        self.readFileTxt = QtGui.QLineEdit(self)
        self.readFileTxt.move(140, 350)
        self.readFileTxt.resize(100, 30)
        self.readFileTxt.setText("0")

        self.retrBtn = QtGui.QPushButton(self)
        self.retrBtn.move(700, 500)
        self.retrBtn.setText("Retrieve")
        self.retrBtn.resize(80, 30)
        self.retrBtn.clicked.connect(self._retrieveProcess)

    def _handleNewFile(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                "Select output file", '',
                "All Files (*)").toLocal8Bit().data().decode('iso-8859-1')

        if fileName != None:
            self.outFileTxt.setText(fileName)
        else:
            QtGui.QMessageBox.warning(self, 'Info Message', "No File Selected !", QtGui.QMessageBox.Ok)

    def _launchProcess(self):
        self.launchBtn.setEnabled(False)
        self.launchBtn.repaint()
        if StegoMinecraftBase.Instance.isProcessReady():
            try:
                nb = StegoMinecraftBase.Instance.launchProcess()
                msg = "Finished !\n" + str(nb) + " Byte(s) inserted"
                QtGui.QMessageBox.information(self, 'Info Message', msg, QtGui.QMessageBox.Ok)
            except Exception, e:
                print str(e)
                QtGui.QMessageBox.warning(self, 'Info Message', str(e), QtGui.QMessageBox.Ok)
        self.launchBtn.setEnabled(True)

    def _retrieveProcess(self):
        self.retrBtn.setEnabled(False)
        self.retrBtn.repaint()
        if StegoMinecraftBase.Instance.isRetrieveReady():
            try:
                nbBytes, valid = self.readFileTxt.text().toInt()
                path = self.outFileTxt.text().toLocal8Bit().data().decode('iso-8859-1')
                if not valid:
                    raise ValueError("Nb Bytes is not a number")

                StegoMinecraftBase.Instance.retrieveProcess(path, nbBytes)
                msg = "Finished !\n" + str(nbBytes) + " Byte(s) retrieved\nOutput file : " + path
                QtGui.QMessageBox.information(self, 'Info Message', msg, QtGui.QMessageBox.Ok)
            except ChunkNotPresent, e:
                msg = "Wrong limits, reached empty chunk"
                print msg
                QtGui.QMessageBox.warning(self, 'Info Message', msg, QtGui.QMessageBox.Ok)
            except Exception, e:
                print str(e)
                QtGui.QMessageBox.warning(self, 'Info Message', str(e), QtGui.QMessageBox.Ok)
        self.retrBtn.setEnabled(True)
