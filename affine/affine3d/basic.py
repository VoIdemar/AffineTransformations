import numpy as np

XZ_PLANE = 0
YZ_PLANE = 1
XY_PLANE = 2
XYZ_REFLECT = 3

def is_infinite(hg_point):
    return len(hg_point) == 4 and hg_point[3] == 0

def to_homogeneous(point):
    return (point[0], point[1], point[2], 1) if len(point) == 3 else point
    
def to_cartesian(hg_point):
    """
    Returns corresponding cartesian point or the same point if it is infinite
    """
    if len(hg_point) == 4 and hg_point[3] <> 0:
        return (hg_point[0] / hg_point[3], hg_point[1] / hg_point[3], hg_point[2] / hg_point[3])
    else:
        return hg_point

def apply_transform(point, transform):
    """
    Applies given transformation to the point (cartesian or homogeneous)
    Returns point with the same type of coordinates.
    """
    return np.dot(transform if len(point) == 4 else transform[0:3, 0:3], point)

def matr_rotate_x(phi):
    T = np.array([[1,           0,            0, 0],
                  [0, np.cos(phi), -np.sin(phi), 0],
                  [0, np.sin(phi),  np.cos(phi), 0],
                  [0,           0,            0, 1]])
    return T

def matr_rotate_y(phi):
    T = np.array([[ np.cos(phi),   0, np.sin(phi), 0],
                  [           0,   1,           0, 0],
                  [-np.sin(phi),   0, np.cos(phi), 0],
                  [0,              0,           0, 1]])
    return T

def matr_rotate_z(phi):
    T = np.array([[np.cos(phi), -np.sin(phi), 0, 0],
                  [np.sin(phi),  np.cos(phi), 0, 0],
                  [          0,            0, 1, 0],
                  [          0,            0, 0, 1]])
    return T

def matr_scale(kx, ky, kz):
    T = np.array([[kx,  0,  0, 0],
                  [ 0, ky,  0, 0],
                  [ 0,  0, kz, 0],
                  [ 0,  0,  0, 1]])
    return T

def matr_rotate_x_norm(A, B):
    T = np.array([[1, 0,  0,           0],
                  [0, A, -B,           0],
                  [0, B,  A,           0],
                  [0, 0,  0, A**2 + B**2]])
    return T

def matr_rotate_y_norm(A, B):
    T = np.array([[ A, 0, B,            0],
                  [ 0, 1, 0,            0],
                  [-B, 0, A,            0],
                  [ 0, 0, 0, A**2 + B**2]])
    return T

def matr_rotate_z_norm(A, B):
    T = np.array([[A, -B, 0,           0],
                  [B,  A, 0,           0],
                  [0,  0, 1,           0],
                  [0,  0, 0, A**2 + B**2]])
    return T

def matr_general_scale(s):
    T = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, s]])
    return T

def matr_translate(tx, ty, tz):
    T = np.array([[1, 0, 0, tx],
                  [0, 1, 0, ty],
                  [0, 0, 1, tz],
                  [0, 0, 0,  1]])
    return T

def matr_identity():
    T = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]])
    return T

def matr_reflect(plane):
    if plane in [XY_PLANE, XZ_PLANE, YZ_PLANE, XYZ_REFLECT]:
        alpha = -1 if plane in [XZ_PLANE, XYZ_REFLECT] else 1
        beta = -1 if plane in [YZ_PLANE, XYZ_REFLECT] else 1
        gamma = -1 if plane in [XY_PLANE, XYZ_REFLECT] else 1
        return matr_scale(kx=alpha, ky=beta, kz=gamma)
    else:
        return matr_identity()
    
def rotate_x(point, phi):
    return apply_transform(point, matr_rotate_x(phi))

def rotate_y(point, phi):
    return apply_transform(point, matr_rotate_y(phi))

def rotate_z(point, phi):
    return apply_transform(point, matr_rotate_z(phi))
    
def rotate_x_norm(point, A, B):
    return apply_transform(point, matr_rotate_x_norm(A, B))

def rotate_y_norm(point, A, B):
    return apply_transform(point, matr_rotate_y_norm(A, B))

def rotate_z_norm(point, A, B):
    return apply_transform(point, matr_rotate_z_norm(A, B))

def scale(point, kx=1, ky=1, kz=1):
    if kx > 0 and ky > 0 and kz > 0:
        return apply_transform(point, matr_scale(kx, ky, kz))
    else:
        return point

def general_scale(point, s):
    if s > 0:
        return apply_transform(point, matr_general_scale(s))
    else:
        return point

def reflect(point, plane):
    """
    Reflects the point across the given plane: xOy, zOx, yOz or against the origin
    """
    return apply_transform(point, matr_reflect(plane))
    
def translate(point, tx=0, ty=0, tz=0):
    """
    (x, y, z) -> (x + tx, y + ty, z + tz, 1)
    """
    return apply_transform(to_homogeneous(point), matr_translate(tx, ty, tz))

def identity(point):
    return point