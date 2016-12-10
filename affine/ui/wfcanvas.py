from PyQt4 import QtGui, QtCore

import affine.affine3d.basic as basic
import affine.affine3d.std as std
from affine.wireframe.wfmodel import WireFrameModel
from affine.surfaces.mobius import MobiusStrip
from affine.surfaces.sphere import Sphere
from affine.surfaces.conical import Conical
from affine.surfaces.torus import Torus
from affine.kinematic.cap import PomponCap
from affine.kinematic.std import kinematic_torus, kinematic_sphere
from affine.drawers.wfdrawer import WFModelQtDrawer

class MainForm(QtGui.QWidget):
    
    SPHERE_RB = 1
    CONICAL_RB = 2
    MOBIUS_RB = 3
    TORUS_RB = 4
    KINEMATIC_SPHERE_RB = 5
    KINEMATIC_TORUS_RB = 6
    POMPON_CAP_RB = 7
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.wfmodel = None
        self.drawer = WFModelQtDrawer((500, 300))
        self.surfaceLabel = QtGui.QLabel(u'Surfaces: ', self)
        
        self.wfmodelRadioGroup = QtGui.QButtonGroup()
        self.sphereRB = QtGui.QRadioButton(u'Sphere', self)
        self.sphereRB.setChecked(True)
        self.conicalRB = QtGui.QRadioButton(u'Conical surface', self)
        self.mobiusRB = QtGui.QRadioButton(u'Mobius strip', self)
        self.torusRB = QtGui.QRadioButton(u'Torus', self)
        self.kinematicTorusRB = QtGui.QRadioButton(u'Kinematic torus', self)
        self.kinematicSphereRB = QtGui.QRadioButton(u'Kinematic sphere', self)
        self.pomponCapRB = QtGui.QRadioButton(u'Pompon cap', self)
        self.wfmodelRadioGroup.addButton(self.sphereRB, MainForm.SPHERE_RB)
        self.wfmodelRadioGroup.addButton(self.conicalRB, MainForm.CONICAL_RB)
        self.wfmodelRadioGroup.addButton(self.mobiusRB, MainForm.MOBIUS_RB)
        self.wfmodelRadioGroup.addButton(self.torusRB, MainForm.TORUS_RB)
        self.wfmodelRadioGroup.addButton(self.kinematicSphereRB, MainForm.KINEMATIC_SPHERE_RB)
        self.wfmodelRadioGroup.addButton(self.kinematicTorusRB, MainForm.KINEMATIC_TORUS_RB)
        self.wfmodelRadioGroup.addButton(self.pomponCapRB, MainForm.POMPON_CAP_RB)
        
        self.drawOnlyVisibleCB = QtGui.QCheckBox(u'Draw visible edges only', self)
        self.drawOnlyVisibleCB.setChecked(False)
        
        self.setGeometry(100, 100, 1000, 600)
        self.set_position()
        self.setFocus()
        
        self.wfmodelRadioGroup.buttonClicked.connect(self.on_wfmodel_clicked)
        self.drawOnlyVisibleCB.stateChanged.connect(self.on_draw_visible_change_state)
        
    def set_wfmodel(self, wfmodel):
        self.wfmodel = wfmodel
        
    def paintEvent(self, event):
        self.set_position()
        if not (self.wfmodel is None):
            self.drawer.draw(self.wfmodel, self, QtCore.Qt.black)        
        
    def on_wfmodel_clicked(self):
        wfmodel = None
        checkedId = self.wfmodelRadioGroup.checkedId()
        if checkedId == MainForm.SPHERE_RB:
            wfmodel = WireFrameModel.create_model_for_surface(Sphere(0, 0, 0, 100), 20, 20)
        elif checkedId == MainForm.CONICAL_RB:
            wfmodel = WireFrameModel.create_model_for_surface(Conical(90, -200, 200), 20, 20)
        elif checkedId == MainForm.MOBIUS_RB:
            wfmodel = WireFrameModel.create_model_for_surface(MobiusStrip(100, 100), 20, 20)
        elif checkedId == MainForm.TORUS_RB:
            wfmodel = WireFrameModel.create_model_for_surface(Torus(100, 200), 20, 20)
        elif checkedId == MainForm.KINEMATIC_SPHERE_RB:
            wfmodel = WireFrameModel.create_model_for_kinematic_surface(kinematic_sphere(), 20, 20)
        elif checkedId == MainForm.KINEMATIC_TORUS_RB:
            wfmodel = WireFrameModel.create_model_for_kinematic_surface(kinematic_torus(1, 1, 5), 20, 20)
        elif checkedId == MainForm.POMPON_CAP_RB:
            wfmodel = WireFrameModel.create_model_for_kinematic_surface(PomponCap(1, 0.1, 0.4), 20, 20)
        else:
            pass
        if not (wfmodel is None):
            self.wfmodel = wfmodel
            self.repaint()
        
    def set_position(self):
        w, h = self.geometry().width(), self.geometry().height()
        upper_margin = h - 180
        self.drawOnlyVisibleCB.setGeometry(w - 140, upper_margin - 20, 150, 15)
        self.surfaceLabel.setGeometry(w - 140, upper_margin, 100, 15)
        self.sphereRB.setGeometry(w - 120, upper_margin + 20, 100, 15)
        self.conicalRB.setGeometry(w - 120, upper_margin + 40, 100, 15)
        self.mobiusRB.setGeometry(w - 120, upper_margin + 60, 100, 15)
        self.torusRB.setGeometry(w - 120, upper_margin + 80, 100, 15)
        self.kinematicSphereRB.setGeometry(w - 120, upper_margin + 100, 100, 15)
        self.kinematicTorusRB.setGeometry(w - 120, upper_margin + 120, 100, 15)
        self.pomponCapRB.setGeometry(w - 120, upper_margin + 140, 100, 15)
        self.drawer.origin = (w/2, h/2)
    
    def on_draw_visible_change_state(self):
        self.drawer.draw_all = not self.drawOnlyVisibleCB.isChecked()
        self.repaint()
        
    def hide_figure(self):
        self.drawer.draw(self.wfmodel, self, QtCore.Qt.white)
    
    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_W, QtCore.Qt.Key_S, QtCore.Qt.Key_A, QtCore.Qt.Key_D,
                           QtCore.Qt.Key_Q, QtCore.Qt.Key_E, QtCore.Qt.Key_O, QtCore.Qt.Key_P,
                           QtCore.Qt.Key_K, QtCore.Qt.Key_L, QtCore.Qt.Key_N, QtCore.Qt.Key_M,
                           QtCore.Qt.Key_V, QtCore.Qt.Key_B, QtCore.Qt.Key_T, QtCore.Qt.Key_Y]:
            print 'Key event: ' + event.key().__str__()
            key = event.key()
            self.wfmodel.apply_transform(
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
                basic.matr_identity
            )
            self.repaint()
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = MainForm()
    form.setWindowTitle(u'Drawing figures')
    form.set_wfmodel(
      WireFrameModel.create_model_for_surface(Sphere(0, 0, 0, 100), 20, 20)    
    )
    form.show()
    sys.exit(app.exec_())