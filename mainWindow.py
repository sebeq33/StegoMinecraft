# -*- coding: iso-8859-1 -*-

import sys
import os
import subprocess
import StegoMinecraftBase
from TabPreview import TabPreview
from TabSrc import TabSrc
from TabSecurity import TabSecurity
from TabOptions import TabOptions
from TabOptionsAdv import TabOptionsAdv
from TabProcess import TabProcess
from MinecraftUtility import getAvailMaps, dumpMapDest
from CoverMediaDest import MapDest, ServerDest
from pymclevel.mclevelbase import saveFileDir
from PyQt4 import QtGui
from PyQt4 import QtCore

class MainWindow(QtGui.QWidget):
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        QtGui.QMainWindow.__init__(self)
        
        StegoMinecraftBase.Instance = StegoMinecraftBase.StegoMinecraftBase()

        self._initWindow()
        self._initMenuBar()
        self._initMenuTabs()
        self.closeEvent = self._handleClose

        self.show()
        sys.exit(self.app.exec_())
        
    def _handleClose(self, event):
        StegoMinecraftBase.Instance.close()

    def _initWindow(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('StegoMinecraft')
        
        #center window on screen
        sc = QtGui.QDesktopWidget().screenGeometry()
        me = self.geometry()
        self.move((sc.width() - me.width()) / 2,
                  (sc.height() - me.height()) / 2)
            
    def _initMenuBar(self):
        self.menuBar = QtGui.QMenuBar(self)
        self.menuBar.resize(800, 25)
        openDirAct = QtGui.QAction("Open Minecraft Directory", self)
        openDirAct.triggered.connect(self.openMapDest);
        debugAct = QtGui.QAction("Debug", self)
        debugAct.triggered.connect(self.debug);
        fileMenu = self.menuBar.addMenu("File")
        fileMenu.addAction(openDirAct)
        fileMenu.addAction(debugAct)
        
    def _initMenuTabs(self):
        self.menuTabs = QtGui.QTabWidget(self)
        self.menuTabs.resize(800, 565)
        self.menuTabs.move(0, 30)
        self.menuTabs.setTabPosition(QtGui.QTabWidget.North)
        
        self.previewTab = TabPreview()
        self.srcTab = TabSrc()
        self.optionsTab = TabOptions()
        self.optionsAdvTab = TabOptionsAdv()
        self.securityTab = TabSecurity()
        self.processTab = TabProcess()
        self.menuTabs.addTab(self.previewTab, QtCore.QString("Dest, Preview Info"))
        self.menuTabs.addTab(self.srcTab, QtCore.QString("Src Input"))
        self.menuTabs.addTab(self.optionsTab, QtCore.QString("Options"))
        self.menuTabs.addTab(self.optionsAdvTab, QtCore.QString("Options (Adv)"))
        self.menuTabs.addTab(self.securityTab, QtCore.QString("Security"))
        self.menuTabs.addTab(self.processTab, QtCore.QString("Process"))
        self.menuTabs.currentChanged.connect(self._handleNewTab)

    def _handleNewTab(self):
        self.menuTabs.currentWidget().setFocus() ## mandatory to make focusIn event works

    def openMapDest(self):
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

    def updateInfo(self):
        self.previewTab.updateInfo()
        self.optionsTab.updateInfo()

    def debug(self):
        msg = str(StegoMinecraftBase.Instance) + "\n"
        msg += str(StegoMinecraftBase.Instance.coverMediaDest) + "\n"
        msg += str(StegoMinecraftBase.Instance.plainTxtSrc) + "\n"
        msg += str(StegoMinecraftBase.Instance.limits) + "\n"
        msg += str(StegoMinecraftBase.Instance.options)
        QtGui.QMessageBox.information(self, 'Info Message', msg, QtGui.QMessageBox.Ok)
