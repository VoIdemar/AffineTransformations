from PyQt4 import QtGui, QtCore

class Object3DQtDrawer(object):
    
    def __init__(self, paintDevice, obj3d):
        self.obj3d = obj3d
        self.drawer = QtGui.QPainter()
        self.pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        