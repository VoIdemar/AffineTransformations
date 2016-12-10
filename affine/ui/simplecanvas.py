import numpy as np
from PyQt4 import QtGui, QtCore

import affine.affine2d.basic as basic
import affine.affine2d.std as std
import affine.affine2d.custom as custom
from affine.datastruct.figure import PlanarFigure
import affine.datainput.input as arrinput
import affine.misc as misc

class MainForm(QtGui.QWidget):
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.qp = QtGui.QPainter()
        self.figure = None
                
        self.button = QtGui.QPushButton(u'Load', self)
        self.inputFileLabel = QtGui.QLabel(u'Input file: ', self)
        self.inputFileEdit = QtGui.QLineEdit(u'', self)
        
        self.setGeometry(100, 100, 640, 480)
        self.origin = (0.5*self.width(), 0.5*self.height())
        self.set_position()
        self.setFocus()
        
        QtCore.QObject.connect(self.button, QtCore.SIGNAL('clicked()'), self.on_load_clicked)       
        
    def set_figure(self, figure):
        self.figure = figure
        
    def paintEvent(self, event):
        self.qp.begin(self)
        self.qp.setRenderHint(self.qp.Antialiasing)
        self.set_position()
        if not (self.figure is None):
            self.draw_figure(QtCore.Qt.black)
        self.qp.end()
    
    def on_load_clicked(self):
        path = self.inputFileEdit.text()
        points = arrinput.read_numarray_from_file(path)
        f = PlanarFigure(points)
        self.hide_figure()
        self.set_figure(f)
        self.repaint()
    
    def set_position(self):
        w, h = self.geometry().width(), self.geometry().height()
        self.button.setGeometry(w - 80, h - 20, 80, 20)
        self.inputFileLabel.setGeometry(w - 200, h - 40, 50, 20)
        self.inputFileEdit.setGeometry(w - 120, h - 40, 120, 20)
        
    def draw_figure(self, color):
        pen = QtGui.QPen(color, 2, QtCore.Qt.SolidLine)
        self.qp.setPen(pen)
        points = np.apply_along_axis(basic.to_cartesian, axis=1, arr=self.figure.get_all_vertices())
        tx, ty = self.origin
        for i in range(1, len(points)):
            (x1, y1), (x2, y2) = points[i - 1:i + 1]
            self.qp.drawLine(x1+tx, y1+ty, x2+tx, y2+ty)
        xl, yl = points[-1]
        x0, y0 = points[0]
        self.qp.drawLine(xl+tx, yl+ty, x0+tx, y0+ty)
    
    def hide_figure(self):
        self.draw_figure(QtCore.Qt.white)
    
    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_W, QtCore.Qt.Key_S, QtCore.Qt.Key_A, QtCore.Qt.Key_D,
                           QtCore.Qt.Key_Q, QtCore.Qt.Key_E, QtCore.Qt.Key_Z, QtCore.Qt.Key_C,
                           QtCore.Qt.Key_T, QtCore.Qt.Key_Y, QtCore.Qt.Key_G]:
            key = event.key()
            self.figure.apply_transform(
                std.move_down if key == QtCore.Qt.Key_W else
                std.move_up if key == QtCore.Qt.Key_S else
                std.move_left if key == QtCore.Qt.Key_A else
                std.move_right if key == QtCore.Qt.Key_D else
                std.turn_left if key == QtCore.Qt.Key_Q else
                std.turn_right if key == QtCore.Qt.Key_E else
                (lambda point: custom.rotate_around(point, self.figure[0], misc.to_rad(1))) if key == QtCore.Qt.Key_Z else
                (lambda point: custom.rotate_around(point, self.figure[0], misc.to_rad(-1))) if key == QtCore.Qt.Key_C else
                (lambda point: custom.relative_scale(point, self.figure[0], 2, 2)) if key == QtCore.Qt.Key_T else
                (lambda point: custom.relative_scale(point, self.figure[0], 0.5, 0.5)) if key == QtCore.Qt.Key_Y else
                (lambda point: basic.to_cartesian(custom.reflect_over_line(point, 1, -1, 0))) if key == QtCore.Qt.Key_G else
                basic.identity
            )
            self.repaint()
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = MainForm()
    form.setWindowTitle(u'Drawing figures')
    form.set_figure(PlanarFigure(np.array([[100, 100, 1],
                                           [160, 160, 1],
                                           [220, 100, 1]])))
    form.show()
    sys.exit(app.exec_()) 
        
        