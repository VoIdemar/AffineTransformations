import numpy as np
from PyQt4 import QtGui, QtCore
from affine.affine2d.basic import to_cartesian

class WFModelQtDrawer(object):
       
    def __init__(self, origin, draw_all=True):        
        self.__drawer = QtGui.QPainter()
        self.__pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)        
        self.__origin = origin
        self.__draw_all = draw_all
        
    def draw(self, wfmodel, paintDevice, color):
        self.__drawer.begin(paintDevice)
        self.__pen.setColor(color)
        self.__drawer.setPen(self.__pen)
        self.__drawer.setRenderHint(self.__drawer.Antialiasing)
        self.__draw_projection(wfmodel)
        self.__drawer.end()
        
    @property
    def origin(self):
        return self.__origin
    
    @origin.setter
    def origin(self, value):
        self.__origin = value
    
    @property
    def draw_all(self):
        return self.__draw_all
    
    @draw_all.setter
    def draw_all(self, value):
        self.__draw_all = value
    
    def __draw_projection(self, wfmodel):
        if not (wfmodel is None):
            x, y = self.__origin
            points = WFModelQtDrawer.__to_cartesian(wfmodel.get_grid_projection())
            edges = wfmodel.edges if self.__draw_all else wfmodel.get_visible_edges()           
            for ((i1, j1), (i2, j2)) in edges:
                (x1, y1), (x2, y2) = points[i1][j1], points[i2][j2]
                self.__drawer.drawLine(x+x1, y+y1, x+x2, y+y2)
                 
    @staticmethod
    def __to_cartesian(grid):        
        cartesian_grid = np.empty(grid.shape, np.ndarray)
        for i in range(0, grid.shape[0]):
            for j in range(0, grid.shape[1]):
                cartesian_grid[i][j] = to_cartesian(grid[i][j])
        return cartesian_grid