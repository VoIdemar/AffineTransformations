import basic as bt
import affine.misc as misc

move_up = lambda point: bt.translate(point, tx=0, ty=1)
move_down = lambda point: bt.translate(point, tx=0, ty=(-1))
move_left = lambda point: bt.translate(point, tx=(-1), ty=0)
move_right = lambda point: bt.translate(point, tx=1, ty=0)
turn_left = lambda point: bt.rotate(point, misc.to_rad(1))
turn_right = lambda point: bt.rotate(point, misc.to_rad(-1))

gl_move_up = lambda point: bt.translate(point, tx=0, ty=0.01)
gl_move_down = lambda point: bt.translate(point, tx=0, ty=(-0.01))
gl_move_left = lambda point: bt.translate(point, tx=(-0.01), ty=0)
gl_move_right = lambda point: bt.translate(point, tx=0.01, ty=0)