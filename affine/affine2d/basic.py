import numpy as np

X_AXIS = 0
Y_AXIS = 1
XY_AXIS = 2

def is_infinite(hg_point):
    return len(hg_point) == 3 and hg_point[2] == 0

def to_homogeneous(point):
    return (point[0], point[1], 1) if len(point) == 2 else point
    
def to_cartesian(hg_point):
    '''
    Returns corresponding cartesian point or the same point if it is infinite.
    '''
    if len(hg_point) == 3 and hg_point[2] <> 0:
        return (hg_point[0] / hg_point[2], hg_point[1] / hg_point[2])
    else:
        return hg_point

def apply_transform(point, transform):
    '''
    Applies given transformation to the point (cartesian or homogeneous). 
    Returns point with the same type of coordinates.
    '''
    return tuple(np.dot(transform if len(point) == 3 else transform[0:2, 0:2], point))
        
def rotate(point, phi):
    T = np.array([[np.cos(phi), -np.sin(phi), 0],
                  [np.sin(phi),  np.cos(phi), 0],
                  [          0,            0, 1]])
    return apply_transform(point, T)

def rotate_norm(point, A, B):
    T = np.array([[A, -B,           0],
                  [B,  A,           0],
                  [0,  0, A**2 + B**2]])
    return apply_transform(point, T)
    
def scale(point, kx=1, ky=1):
    if kx > 0 and ky > 0:
        T = np.array([[kx,  0, 0],
                      [ 0, ky, 0],
                      [ 0,  0, 1]]) 
        return apply_transform(point, T)
    else:
        return point

def reflect(point, axis):
    '''
    Reflects the point across the given axis: Ox, Oy or both axis = X_AXIS, Y_AXIS or XY_AXIS
    '''
    if axis in [X_AXIS, Y_AXIS, XY_AXIS]:
        alpha = -1 if axis in [X_AXIS, XY_AXIS]  else 1
        beta = -1 if axis in [Y_AXIS, XY_AXIS] else 1
        return scale(point, kx=alpha, ky=beta)
    else:
        return point

def identity(point):
    return translate(point)

def translate(point, tx=0, ty=0):
    T = np.array([[1, 0, tx],
                  [0, 1, ty],
                  [0, 0,  1]])
    return apply_transform(to_homogeneous(point), T)