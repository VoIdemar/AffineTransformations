import numpy as np

from affine.opengl.routines import draw_planar_figure
from affine.opengl.interactivecontext import GLUTInteractiveContext
from affine.datastruct.figure import PlanarFigure
import affine.affine2d.basic as basic
import affine.affine2d.custom as custom
import affine.affine2d.std as std
import affine.misc as misc
import affine.opengl.glutconstants as consts

class GLPlanarForm(object):
    
    def __init__(self, obj3d, window_name, width, height):
        self.figure = obj3d        
        self.context = GLUTInteractiveContext(window_name, width, height, self.display_func)
        self.context.set_keyboard_func(self.key_press_event)
    
    def display_func(self):
        draw_planar_figure(self.figure, r=1, g=0, b=0)
    
    def key_press_event(self, key, x, y):
        self.figure.apply_transform(
            std.move_down if key == consts.KEY_S else
            std.move_up if key == consts.KEY_W else
            std.move_left if key == consts.KEY_A else
            std.move_right if key == consts.KEY_D else
            std.turn_left if key == consts.KEY_Q else
            std.turn_right if key == consts.KEY_E else
            (lambda point: custom.rotate_around(point, self.figure[0], misc.to_rad(1))) if key == consts.KEY_Z else
            (lambda point: custom.rotate_around(point, self.figure[0], misc.to_rad(-1))) if key == consts.KEY_C else
            (lambda point: custom.relative_scale(point, self.figure[0], 2, 2)) if key == consts.KEY_T else
            (lambda point: custom.relative_scale(point, self.figure[0], 0.5, 0.5)) if key == consts.KEY_Y else
            (lambda point: basic.to_cartesian(custom.reflect_over_line(point, 1, -1, 0))) if key == consts.KEY_G else
            basic.identity
        )    
    
    def run_context(self):
        self.context.draw()
        
if __name__ == '__main__':
    figure = PlanarFigure(np.array([[100, 100, 1],
                                    [160, 160, 1],
                                    [220, 100, 1]]))
    form = GLPlanarForm(figure, "Affine transformations with GLUT", 1000, 600)
    form.run_context()