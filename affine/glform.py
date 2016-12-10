from PyQt4 import QtGui, QtCore
import numpy as np

from opengl.glwidget import QtOpenGLWidget
from datastruct.figure import PlanarFigure
import affine2d.basic as basic
import affine2d.std as std
import affine2d.custom as custom
import misc

class OpenGLForm(QtGui.QMainWindow):
    
    def __init__(self):
        super(OpenGLForm, self).__init__()
        
        self.glwidget = QtOpenGLWidget()
        self.figure = None
        
        # put the window at the screen position (100, 100)
        self.setGeometry(100, 100, self.glwidget.width, self.glwidget.height)
        self.setCentralWidget(self.glwidget)
        
        self.show()
        
    def set_figure(self, figure):   
        self.figure = figure
        self.glwidget.set_rendered_data(self.figure.get_cartesian_coords())
    
    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_W, QtCore.Qt.Key_S, QtCore.Qt.Key_A, QtCore.Qt.Key_D,
                           QtCore.Qt.Key_Q, QtCore.Qt.Key_E, QtCore.Qt.Key_Z, QtCore.Qt.Key_C,
                           QtCore.Qt.Key_T, QtCore.Qt.Key_Y, QtCore.Qt.Key_G]:
            #print 'Key event: ' + event.key().__str__()
            key = event.key()
            self.figure.apply_transform(
                std.gl_move_down if key == QtCore.Qt.Key_W else
                std.gl_move_up if key == QtCore.Qt.Key_S else
                std.gl_move_left if key == QtCore.Qt.Key_A else
                std.gl_move_right if key == QtCore.Qt.Key_D else
                std.turn_left if key == QtCore.Qt.Key_Q else
                std.turn_right if key == QtCore.Qt.Key_E else
                (lambda point: custom.rotate_around(point, self.figure[0], misc.to_rad(1))) if key == QtCore.Qt.Key_Z else
                (lambda point: custom.rotate_around(point, self.figure[0], misc.to_rad(-1))) if key == QtCore.Qt.Key_C else
                (lambda point: custom.relative_scale(point, self.figure[0], 2, 2)) if key == QtCore.Qt.Key_T else
                (lambda point: custom.relative_scale(point, self.figure[0], 0.5, 0.5)) if key == QtCore.Qt.Key_Y else
                (lambda point: basic.to_cartesian(custom.reflect_over_line(point, 1, -1, 0))) if key == QtCore.Qt.Key_G else
                basic.identity
            )
            self.glwidget.updateGL()
            
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    planar_figure = PlanarFigure(np.array([[0, 0, 1],
                                           [0.5, 0.5, 1],
                                           [0.5, 0, 1]]))
    window = OpenGLForm()
    window.set_figure(planar_figure)
    window.show()
    app.exec_()