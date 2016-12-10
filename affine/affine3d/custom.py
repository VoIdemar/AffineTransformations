import numpy as np
import basic

def matr_reflect_over_plane(A, B, C):
    T = np.array([[B**2 + C**2 - A**2,             -2*A*B,             -2*A*C,                  0],
                  [            -2*A*B, C**2 + A**2 - B**2,             -2*B*C,                  0],
                  [            -2*A*C,             -2*B*C, A**2 + B**2 - C**2,                  0],
                  [                 0,                  0,                  0, A**2 + B**2 + C**2]])
    return T

def matr_reflect_over_plane2(A, B, C, D):
    T = np.array([[B**2 + C**2 - A**2,             -2*A*B,             -2*A*C,             -2*A*D],
                  [            -2*A*B, C**2 + A**2 - B**2,             -2*B*C,             -2*B*D],
                  [            -2*A*C,             -2*B*C, A**2 + B**2 - C**2,             -2*C*D],
                  [                 0,                  0,                  0, A**2 + B**2 + C**2]])
    return T

def matr_rotate_around_axis(A, B, C, theta):
    if B <> 0 or C <> 0:
        cosPsi, sinPsi = B / np.sqrt(B**2 + C**2), C / np.sqrt(B**2 + C**2)
        cosPhi, sinPhi = A / np.sqrt(A**2 + B**2 + C**2), np.sqrt(B**2 + C**2) / np.sqrt(A**2 + B**2 + C**2)
        T = np.dot(basic.matr_rotate_z_norm(cosPhi, -sinPhi), basic.matr_rotate_x_norm(cosPsi, -sinPsi))
        T = np.dot(basic.matr_rotate_x(theta), T)
        T = np.dot(basic.matr_rotate_z_norm(cosPhi, sinPhi), T)
        T = np.dot(basic.matr_rotate_x_norm(cosPsi, sinPsi), T)
        return T
    else:
        return basic.matr_identity()

def matr_rotate_around_custom_axis(M, A, B, C, theta):
    if B <> 0 or C <> 0:
        mx, my, mz, _ = M
        T = np.dot(matr_rotate_around_axis(A, B, C, theta), basic.matr_translate(tx=(-mx), ty=(-my), tz=(-mz)))
        return np.dot(basic.matr_translate(tx=mx, ty=my, tz=mz), T)
    else:
        return basic.matr_identity()

def matr_rotate_around_axis2(A, B, C, theta):
    if A <> 0 or B <> 0:
        cosPsi, sinPsi = B / np.sqrt(B**2 + A**2), A / np.sqrt(B**2 + A**2)
        cosPhi, sinPhi = np.sqrt(B**2 + A**2) / np.sqrt(A**2 + B**2 + C**2), C / np.sqrt(A**2 + B**2 + C**2) 
        T = np.dot(basic.matr_rotate_x_norm(cosPhi, -sinPhi), basic.matr_rotate_z_norm(cosPsi, sinPsi))
        T = np.dot(basic.matr_rotate_y(theta), T)
        T = np.dot(basic.matr_rotate_x_norm(cosPhi, sinPhi), T)
        T = np.dot(basic.matr_rotate_z_norm(cosPsi, -sinPsi), T)
        return T
    else:
        return basic.matr_identity()
    
def matr_rotate_around_custom_axis2(M, A, B, C, theta):
    if A <> 0 or B <> 0:
        mx, my, mz, _ = M 
        T = np.dot(matr_rotate_around_axis2(A, B, C, theta), basic.matr_translate(tx=(-mx), ty=(-my), tz=(-mz)))
        return np.dot(basic.matr_translate(tx=mx, ty=my, tz=mz), T)
    else:
        return basic.matr_identity()

def reflect_over_plane(point, A, B, C):
    if A <> 0 or B <> 0 or C <> 0:
        return basic.apply_transform(point, matr_reflect_over_plane(A, B, C))
    else:
        return point
    
def reflect_over_plane2(point, A, B, C, D):
    if A <> 0 or B <> 0 or C <> 0:
        return basic.apply_transform(point, matr_reflect_over_plane2(A, B, C, D))
    else:
        return point
    
def rotate_around_axis(point, A, B, C, theta):
    return basic.apply_transform(point, matr_rotate_around_axis(A, B, C, theta))

def rotate_around_custom_axis(point, M, A, B, C, theta):
    return basic.apply_transform(point, matr_rotate_around_custom_axis(M, A, B, C, theta))   