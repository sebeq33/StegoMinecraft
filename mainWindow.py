# -*- coding: iso-8859-1 -*-

import sys
import os
import subprocess
import StegoMinecraftBase
from TabsPreview import TabsPreview
from MinecraftUtility import getAvailMaps, dumpMapDest
from CoverMediaDest import MapDest, ServerDest
from pymclevel.mclevelbase import saveFileDir
from PyQt4 import QtGui
from PyQt4 import QtCore

class MainWindow(QtGui.QWidget):
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        QtGui.QMainWindow.__init__(self)
        
        self.minecraftBase = StegoMinecraftBase.StegoMinecraftBase()
        self._initWindow()
        self._initMenuBar()
        self._initMenuTabs()

        self.show()
        sys.exit(self.app.exec_())
        
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
        newAct = QtGui.QAction("Open Minecraft Directory", self)
        newAct.triggered.connect(self.openMenu);
        fileMenu = self.menuBar.addMenu("File")
        fileMenu.addAction(newAct)
        
    def _initMenuTabs(self):
        self.tabs = TabsPreview(self.minecraftBase)
        self.menuTabs = QtGui.QTabWidget(self)
        self.menuTabs.resize(800, 565)
        self.menuTabs.move(0, 30)
        self.menuTabs.setTabPosition(QtGui.QTabWidget.North)
        self.menuTabs.addTab(self.tabs, QtCore.QString("Preview"))
        self.menuTabs.addTab(None, QtCore.QString("TEST2"))
        #self.menuTabs.setTabEnabled(0, True)

    def openMenu(self):
        dialog = QtGui.QFileDialog(self, 'Browse', saveFileDir)
        result = dialog.getExistingDirectory().toLocal8Bit().data().decode('iso-8859-1')

        try:
            cover = MapDest(result)
            self.minecraftBase.coverMediaDest = cover
            self.tabs.updateInfo(self.minecraftBase)
            dumpMapDest(cover)

        except ValueError, e:
            print str(e) 

    
