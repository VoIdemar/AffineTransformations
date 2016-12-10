import numpy as np

from affine.affine3d import basic
from kinemsurf import KinematicSurface

def kinematic_sphere():
    return KinematicSurface(
        generatrix = lambda t1, t2: np.array([np.sin(t2), np.cos(t2), 0, 1]),
        transform_matr = lambda t1, t2: basic.matr_rotate_y(t1),
        directrix = lambda t1, t2: np.array([0, 0, 0, 1]),
        t1_min = 0,
        t1_max = 2*np.pi,
        t2_min = 0,
        t2_max = np.pi
    )

def kinematic_torus(a, b, r):
    return KinematicSurface(
       generatrix = lambda t1, t2: np.array([np.sin(t2), np.cos(t2), 0, 1]),
       directrix = lambda t1, t2: np.array([r*np.cos(t1), 0, -r*np.sin(t1), 1]),
       transform_matr = lambda t1, t2: np.dot(basic.matr_scale(a, b, 0), basic.matr_rotate_y(t1)),
       t1_min = 0,
       t1_max = 1.5*np.pi,
       t2_min = 0,
       t2_max = np.pi
    )