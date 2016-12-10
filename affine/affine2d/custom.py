import numpy as np
import basic as bt

def rotate_around(point, anchor, phi):
    '''Rotation around the specified anchor point (composition of transform matrices)'''
    ax, ay, au = bt.to_homogeneous(anchor)
    if au <> 0:
        return bt.translate(bt.rotate(bt.translate(point, -ax, -ay), phi), ax, ay)
    else:
        return point
    
def rotate_around2(point, anchor, phi):
    '''Rotation around the specified anchor point'''
    ax, ay, au = bt.to_homogeneous(anchor)
    if au <> 0:
        T = np.array([[np.cos(phi), -np.sin(phi), ax*(1 - np.cos(phi)) + ay*np.sin(phi)],
                      [np.sin(phi),  np.cos(phi), ay*(1 - np.cos(phi)) - ax*np.sin(phi)],
                      [          0,            0,                                     1]])
        return bt.apply_transform(bt.to_homogeneous(point), T)
    else:
        return point

def relative_scale(point, anchor, kx, ky):    
    ax, ay, au = bt.to_homogeneous(anchor)
    if au <> 0 and kx > 0 and ky > 0:
        return bt.translate(bt.scale(bt.translate(point, -ax, -ay), kx, ky), ax, ay)
    else:
        return point
    
def reflect_over_line(point, A, B, C):
    if A <> 0 or B <> 0:
        T = (1.0/(A**2 + B**2))*np.array([[B**2-A**2,    -2*A*B,    -2*A*C],
                                          [   -2*A*B, A**2-B**2,    -2*B*C],
                                          [        0,         0, A**2+B**2]])
        return bt.apply_transform(bt.to_homogeneous(point), T)
    else:
        return point