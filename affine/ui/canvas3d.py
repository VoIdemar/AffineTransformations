from PyQt4 import QtGui, QtCore

import affine.affine3d.basic as basic
import affine.affine3d.std as std
import affine.affine3d.custom as custom
import affine.misc as misc
from affine.datastruct.object3d import Object3D
import affine.datainput.input as arrinput
from affine.drawers.qtdrawer import Object3DQtDrawer

class MainForm(QtGui.QWidget):
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.obj3d = None
        self.drawer = Object3DQtDrawer()
        self.button = QtGui.QPushButton(u'Load', self)
        self.inputCoordsFileLabel = QtGui.QLabel(u'Input coordinates file: ', self)
        self.inputCoordsFileEdit = QtGui.QLineEdit(u'', self)
        self.inputFaceMapLabel = QtGui.QLabel(u'Input face map file: ', self)
        self.inputFaceMapEdit = QtGui.QLineEdit(u'', self)
        
        self.setGeometry(100, 100, 640, 480)
        self.set_position()
        self.setFocus()
        
        QtCore.QObject.connect(self.button, QtCore.SIGNAL('clicked()'), self.on_load_clicked)       
        
    def set_object3d(self, obj3d):
        self.obj3d = obj3d
        
    def paintEvent(self, event):
        self.set_position()
        if not (self.obj3d is None):
            self.drawer.draw(self.obj3d, self, QtCore.Qt.black)        
    
    def on_load_clicked(self):
        coordsFilePath = self.inputCoordsFileEdit.text()
        faceMapPath = self.inputFaceMapEdit.text()
        points = arrinput.read_numarray_from_file(coordsFilePath)
        faceMap = arrinput.read_numarray_from_file(faceMapPath)
        obj3d = Object3D(points, faceMap)
        self.set_object3d(obj3d)
        self.repaint()
    
    def set_position(self):
        w, h = self.geometry().width(), self.geometry().height()
        self.button.setGeometry(w - 80, h - 20, 80, 20)
        self.inputCoordsFileLabel.setGeometry(w - 230, h - 70, 120, 20)
        self.inputCoordsFileEdit.setGeometry(w - 120, h - 70, 120, 20)
        self.inputFaceMapLabel.setGeometry(w - 218, h - 40, 120, 20)
        self.inputFaceMapEdit.setGeometry(w - 120, h - 40, 120, 20)
        
    def hide_figure(self):
        self.drawer.draw(self.obj3d, self, QtCore.Qt.white)
    
    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_W, QtCore.Qt.Key_S, QtCore.Qt.Key_A, QtCore.Qt.Key_D,
                           QtCore.Qt.Key_Q, QtCore.Qt.Key_E, QtCore.Qt.Key_O, QtCore.Qt.Key_P,
                           QtCore.Qt.Key_K, QtCore.Qt.Key_L, QtCore.Qt.Key_N, QtCore.Qt.Key_M,
                           QtCore.Qt.Key_V, QtCore.Qt.Key_B, QtCore.Qt.Key_T, QtCore.Qt.Key_Y,
                           QtCore.Qt.Key_G, QtCore.Qt.Key_H]:
            key = event.key()
            xStart, yStart, zStart, _ = self.obj3d.get_vertex(6)         
            xEnd, yEnd, zEnd, _ = self.obj3d.get_vertex(7)
            self.obj3d.apply_transform(
                std.matr_translate_y_minus if key == QtCore.Qt.Key_W else
                std.matr_translate_y_plus if key == QtCore.Qt.Key_S else
                std.matr_translate_x_minus if key == QtCore.Qt.Key_A else
                std.matr_translate_x_plus if key == QtCore.Qt.Key_D else
                std.matr_translate_z_minus if key == QtCore.Qt.Key_Q else
                std.matr_translate_z_plus if key == QtCore.Qt.Key_E else
                std.matr_rotate_x_minus if key == QtCore.Qt.Key_O else
                std.matr_rotate_x_plus if key == QtCore.Qt.Key_P else
                std.matr_rotate_y_minus if key == QtCore.Qt.Key_K else
                std.matr_rotate_y_plus if key == QtCore.Qt.Key_L else 
                std.matr_rotate_z_minus if key == QtCore.Qt.Key_N else
                std.matr_rotate_z_plus if key == QtCore.Qt.Key_M else  
                std.matr_scale_x2 if key == QtCore.Qt.Key_B else
                std.matr_scale_half if key == QtCore.Qt.Key_V else    
                std.matr_rotate_custom_axis_plus if key == QtCore.Qt.Key_T else
                std.matr_rotate_custom_axis_minus if key == QtCore.Qt.Key_Y else
                custom.matr_rotate_around_custom_axis2(self.obj3d.get_vertex(6), xEnd-xStart, yEnd-yStart, zEnd-zStart, misc.to_rad(1)) if key == QtCore.Qt.Key_H else
                custom.matr_rotate_around_custom_axis2(self.obj3d.get_vertex(6), xEnd-xStart, yEnd-yStart, zEnd-zStart, misc.to_rad(-1)) if key == QtCore.Qt.Key_G else
                basic.matr_identity()
            )
            self.repaint()
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = MainForm()
    form.setWindowTitle(u'Drawing figures')    
    vertices, faces = arrinput.read_geometry_from_obj_file('C:\\Users\\Voldemar\\Desktop\\untitled2.obj')
    obj3d = Object3D(vertices*100, faces, draw_visible_edges_only=True)
    form.set_object3d(obj3d)
    form.show()
    sys.exit(app.exec_())