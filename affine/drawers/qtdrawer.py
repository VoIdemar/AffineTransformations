import numpy as np
from PyQt4 import QtGui, QtCore
import affine.affine2d.basic as basic 

class Object3DQtDrawer(object):
    
    def __init__(self):        
        self.drawer = QtGui.QPainter()
        self.pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        
    def draw(self, obj3d, paintDevice, color):
        self.drawer.begin(paintDevice)
        self.pen.setColor(color)
        self.drawer.setPen(self.pen)
        self.drawer.setRenderHint(self.drawer.Antialiasing)
        self.__draw_projection(obj3d)
        self.drawer.end()
        
    def __draw_projection(self, obj3d):
        if not (obj3d is None):
            projection = obj3d.get_projection()            
            points = np.apply_along_axis(basic.to_cartesian, axis=0, arr=projection)
            for (idx_start, idx_end) in obj3d.get_all_edges():
                (x1, y1), (x2, y2) = points[:,idx_start], points[:,idx_end]
                self.drawer.drawLine(x1, y1, x2, y2)