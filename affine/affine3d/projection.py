import numpy as np
import basic

def matr_project_onto_custom_plane(A, B, C, D):
    if A <> 0 or B <> 0 or C <> 0:
        T = (1.0 / (A**2 + B**2 + C**2))*np.array([[B**2 + C**2,        -A*B,        -A*C, -A*D],
                                                   [       -A*B, C**2 + A**2,        -B*C, -B*D],
                                                   [       -A*C,        -B*C, A**2 + B**2, -C*D],
                                                   [          0,           0,           0,    1]])
        return T
    else:
        return basic.matr_identity()

def matr_to2d():
    T = np.array([[1.0, 0.0, 0.0, 0.0],
                  [0.0, 1.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0, 1.0]])
    return T

def project(point, plane):
    if plane in [basic.XY_PLANE, basic.XZ_PLANE, basic.YZ_PLANE]:
        alpha = 0 if plane == basic.YZ_PLANE else 1
        beta = 0 if plane == basic.XZ_PLANE else 1
        gamma = 0 if plane == basic.XY_PLANE else 1
        return basic.scale(point, kx=alpha, ky=beta, kz=gamma)
    else:
        return point

def perspective_projection(ax, bx, cx, ay, by, cy, d):
    tx = (cx*by - bx*cy)/float(d)
    ty = (ax*cy - cx*ay)/float(d)
    tz = (bx*ay - ax*by)/float(d)
    T = np.array([[ ax,   bx,  cx, 0.0],
                  [ ay,   by,  cy, 0.0],
                  [0.0,  0.0, 0.0, 0.0],
                  [ tx,   ty,  tz, 1.0]])
    return T

def project_onto_custom_plane(point, A, B, C, D=0):
    return basic.apply_transform(point, matr_project_onto_custom_plane(A, B, C, D))

def to2d(point):
    if len(point) == 4:
        return basic.apply_transform(point, matr_to2d())
    else:
        return point