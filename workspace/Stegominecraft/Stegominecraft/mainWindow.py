import sys
import os
from PyQt4 import QtGui
from pymclevel.mclevelbase import saveFileDir

class MainWindow(QtGui.QWidget):
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        QtGui.QMainWindow.__init__(self)
        
        self.initWindow()
        self.initList()
        self.initMenuBar()

        self.show()
        sys.exit(self.app.exec_())
        
    def initWindow(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('StegoMinecraft')
        
        #center window on screen
        sc = QtGui.QDesktopWidget().screenGeometry()
        me = self.geometry()
        self.move((sc.width() - me.width()) / 2,
                  (sc.height() - me.height()) / 2)
        
    def initList(self):
        self.listLbl = QtGui.QLabel(self)
        self.listLbl.move(5, 30)
        self.listLbl.setText("Save list : ")
        self.listLbl.setFont(QtGui.QFont("Time New Roman", 10))

        self.listMap = QtGui.QListWidget(self)
        self.listMap.move(5, 55)
        self.listMap.resize(200, 540)
        
        for m in self.getAvailSave():
            self.listMap.addItem(m)
            
        self.listMap.setCurrentRow(0)

    def initMenuBar(self):
        self.menuBar = QtGui.QMenuBar(self)
        self.menuBar.resize(800, 25)
        fileMenu = self.menuBar.addMenu("File");
        # fileMenu->addAction(newAct);

    def getAvailSave(self):
        #return all existing Minecraft save
        return [e for e in os.listdir(saveFileDir) if os.path.isdir(os.path.join(saveFileDir,e))]

