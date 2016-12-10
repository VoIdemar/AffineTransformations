import numpy as np

from affine.opengl.routines import draw_3d_object
from affine.opengl.interactivecontext import GLUTInteractiveContext
from affine.datastruct.object3d import Object3D
from affine.datastruct.auxobj import GridObject, AxisObject
from affine.datainput.input import read_geometry_from_obj_file
import affine.affine3d.basic as basic
import affine.affine3d.custom as custom
import affine.affine3d.std as std
import affine.misc as misc
import affine.opengl.glutconstants as consts
from affine.affine3d.projection import perspective_projection

class GLCanvas3DForm(object):
    
    GRID_SIZE = 600.0
    GRID_COUNT = 20
    ORT_LENGTH = 300.0
    ANGLE = 1.8
    DISTANCE_CHANGE_STEP = 30
    INITIAL_OX = np.array([1.0, 0.0, 0.0, 1.0])
    INITIAL_OY = np.array([0.0, 1.0/np.sqrt(2), -1.0/np.sqrt(2), 1.0])
    
    def __init__(self, obj3d, window_name, width, height):
        grid_size = GLCanvas3DForm.GRID_SIZE
        grid_count = GLCanvas3DForm.GRID_COUNT
        self.obj3d = obj3d        
        self.context = GLUTInteractiveContext(window_name, width, height, self.display_func)
        self.context.set_keyboard_func(self.key_press_event)
        self.context.set_mouse_move_func(self.mouse_move_func)
        self.context.set_mouse_wheel_func(self.mouse_wheel_func)
        self.D = 1000.0
        self.axis = AxisObject(GLCanvas3DForm.ORT_LENGTH)
        self.grid = GridObject((-grid_size, grid_size), (-grid_size, grid_size), grid_count, grid_count)
        self.last_x = 0
        self.last_y = 0
        self.OX = GLCanvas3DForm.INITIAL_OX
        self.OY = GLCanvas3DForm.INITIAL_OY
    
    def display_func(self):
        x1, y1, z1 = basic.to_cartesian(self.OX)
        x2, y2, z2 = basic.to_cartesian(self.OY)
        proj_matr = perspective_projection(x1, y1, z1, x2, y2, z2, self.D)
        draw_3d_object(self.obj3d, r=1, g=0, b=0, projection_matr=proj_matr)
        draw_3d_object(self.grid, r=0.5, g=0.5, b=0.5, projection_matr=proj_matr)
        draw_3d_object(self.axis, r=0, g=0, b=1, projection_matr=proj_matr, line_width=2)        
    
    def mouse_move_func(self, x, y):
        angle = GLCanvas3DForm.ANGLE
        x_modification = abs(x - self.last_x)
        y_modification = abs(y - self.last_y)
        if x_modification > y_modification:
            self.OX = basic.apply_transform(
                self.OX, 
                std.matr_rotate_y_angle(-angle) if x - self.last_x > 0 else std.matr_rotate_y_angle(angle)
            )
            self.OY = basic.apply_transform(
                self.OY, 
                std.matr_rotate_y_angle(-angle) if x - self.last_x > 0 else std.matr_rotate_y_angle(angle)
            )
        else:
            self.OX = basic.apply_transform(
                self.OX, 
                std.matr_rotate_x_angle(-angle) if y - self.last_y > 0 else std.matr_rotate_x_angle(angle)
            )
            self.OY = basic.apply_transform(
                self.OY, 
                std.matr_rotate_x_angle(-angle) if y - self.last_y > 0 else std.matr_rotate_x_angle(angle)
            )
        self.last_x = x
        self.last_y = y
    
    def mouse_wheel_func(self, button, direction, x, y):
        step = GLCanvas3DForm.DISTANCE_CHANGE_STEP
        self.D -= direction*step
    
    def key_press_event(self, key, x, y):
        xStart, yStart, zStart, _ = self.obj3d.get_vertex(6)         
        xEnd, yEnd, zEnd, _ = self.obj3d.get_vertex(7)
        self.obj3d.apply_transform(
            std.matr_translate_y_minus if key == consts.KEY_S else
            std.matr_translate_y_plus if key == consts.KEY_W else
            std.matr_translate_x_minus if key == consts.KEY_A else
            std.matr_translate_x_plus if key == consts.KEY_D else
            std.matr_translate_z_minus if key == consts.KEY_Q else
            std.matr_translate_z_plus if key == consts.KEY_E else
            std.matr_rotate_x_minus if key == consts.KEY_O else
            std.matr_rotate_x_plus if key == consts.KEY_P else
            std.matr_rotate_y_minus if key == consts.KEY_K else
            std.matr_rotate_y_plus if key == consts.KEY_L else 
            std.matr_rotate_z_minus if key == consts.KEY_N else
            std.matr_rotate_z_plus if key == consts.KEY_M else  
            std.matr_scale_x2 if key == consts.KEY_B else
            std.matr_scale_half if key == consts.KEY_V else    
            std.matr_rotate_custom_axis_plus if key == consts.KEY_T else
            std.matr_rotate_custom_axis_minus if key == consts.KEY_Y else
            custom.matr_rotate_around_custom_axis2(
               self.obj3d.get_vertex(6),
               xEnd-xStart, yEnd-yStart, zEnd-zStart, misc.to_rad(1)
            ) if key == consts.KEY_H else
            custom.matr_rotate_around_custom_axis2(
               self.obj3d.get_vertex(6), 
               xEnd-xStart, yEnd-yStart, zEnd-zStart, misc.to_rad(-1)
            ) if key == consts.KEY_G else
            basic.matr_identity()
        )
        if key == consts.KEY_C:
            self.OX = GLCanvas3DForm.INITIAL_OX
            self.OY = GLCanvas3DForm.INITIAL_OY
    
    def run_context(self):
        self.context.draw()
        
if __name__ == '__main__':
    vertices, faces = read_geometry_from_obj_file('C:\\Users\\Voldemar\\Desktop\\untitled.obj')    
    obj3d = Object3D(vertices, faces)    
    form = GLCanvas3DForm(obj3d, "Affine transformations with GLUT", 1000, 600)
    form.run_context()