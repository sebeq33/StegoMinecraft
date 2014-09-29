# -*- coding: iso-8859-1 -*-

import sys
import os
import StegoMinecraftBase
from PyQt4 import QtGui
from PyQt4 import QtCore
from PlainTxtSrc import SrcTxt, SrcFile

class TabSrc(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.resize(800, 565)
        self._initTxt()
        self._initFile()
        StegoMinecraftBase.Instance.plainTxtSrc = SrcTxt()

    def _initTxt(self):
        self.txtRBtn = QtGui.QRadioButton(self)
        self.txtRBtn.move(5, 10)
        self.txtRBtn.setChecked(True)
        self.txtRBtn.setText("Input with text :")
        self.txtRBtn.toggled.connect(self.selectTxt)
 
        self.countLbl = QtGui.QLabel(self)
        self.countLbl.move(5, 35)
        self.countLbl.setText("(0) bytes")

        self.txtTEdit = QtGui.QTextEdit(self)
        self.txtTEdit.move(5, 60)
        self.txtTEdit.resize(780, 200)
        self.txtTEdit.textChanged.connect(self._handleTxtCountChanged)
        self.txtTEdit.focusOutEvent = self._handleTxtValueChanged

    def _handleTxtCountChanged(self):
        self.countLbl.setText("("+ str(self.txtTEdit.document().characterCount() - 1) +") bytes")
        self.countLbl.adjustSize()

    def _handleTxtValueChanged(self, event):
        StegoMinecraftBase.Instance.plainTxtSrc.setTxt(self.txtTEdit.document().toPlainText().toLocal8Bit().data())

    def selectTxt(self):
        if not self.fileRBtn.isChecked():
            self.fileRBtn.setChecked(False)

            self.fileTxt.setEnabled(False)
            self.fileBtn.setEnabled(False)
            self.txtTEdit.setEnabled(True)
            StegoMinecraftBase.Instance.plainTxtSrc = SrcTxt()

        
    def selectFile(self):
        if not self.txtRBtn.isChecked():
            self.txtRBtn.setChecked(False)

            self.fileTxt.setEnabled(True)
            self.fileBtn.setEnabled(True)
            self.txtTEdit.setEnabled(False)
            StegoMinecraftBase.Instance.plainTxtSrc = SrcFile()

    def _initFile(self):
        self.fileRBtn = QtGui.QRadioButton(self)
        self.fileRBtn.move(5, 270)
        self.fileRBtn.setChecked(False)
        self.fileRBtn.setText("Input with selected file :")
        self.fileRBtn.toggled.connect(self.selectFile)

        self.fileTxt = QtGui.QLineEdit(self)
        self.fileTxt.move(20, 320)
        self.fileTxt.resize(670, 25)
        self.fileTxt.setText("")
        self.fileTxt.setEnabled(False)
        self.fileTxt.setReadOnly(True)

        self.fileBtn = QtGui.QPushButton(self)
        self.fileBtn.move(700, 320)
        self.fileBtn.setText("Select File")
        self.fileBtn.resize(80, 25)
        self.fileBtn.clicked.connect(self._handleNewFile)
        self.fileBtn.setEnabled(False)

    def _handleNewFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                "Select input file", '',
                "All Files (*)").toLocal8Bit().data().decode('iso-8859-1')

        if not fileName:
            QtGui.QMessageBox.information(self, 'Info Message', "No File Selected !", QtGui.QMessageBox.Ok)
        else:
            self.fileTxt.setText(fileName)
            StegoMinecraftBase.Instance.plainTxtSrc.setPath(fileName)
