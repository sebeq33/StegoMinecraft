from minecraftUtility import getAvailMaps
from PyQt4 import QtGui
from PyQt4 import QtCore

def addList(qwidget, x = 0, y = 0):
    listLbl = QtGui.QLabel(qwidget)
    listLbl.move(x + 5, y + 30)
    listLbl.setText("Save list : ")
    listLbl.setFont(QtGui.QFont("Time New Roman", 10))
    
    listMap = QtGui.QListWidget(self)
    listMap.move(x + 5, y + 55)
    listMap.resize(200, 540)
    
    for m in getAvailMaps():
        self.listMap.addItem(m)
    self.listMap.setCurrentRow(0)
    
    return listMap

def selectItemByPath(listMap, path)
    mapName = os.path.basename(path)        
    items = listMap.findItems(mapName, QtCore.Qt.MatchExactly)
    if len(items) > 0:
        listMap.setCurrentItem(items[0])
