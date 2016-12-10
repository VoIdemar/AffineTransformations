import numpy as np

def read_numarray_from_file(filename):
    """
    Reads an array from a file with the following structure:
    x[1] y[1] (z[1]) u[1]...
    x[2] y[2] (z[2]) u[2]... 
    ...
    x[n] y[n] (z[n]) u[n]...
    Raises IOError
    """
    geometry_file = open(filename, 'r')
    res = np.array(map(float, geometry_file.readline().split(' ')))
    for line in file:
        res = np.vstack((res, np.array(map(float, line.split(' ')))))
    geometry_file.close()
    return res

def read_geometry_from_obj_file(filename):
    """
    Read geometry from Wavefront geometry definition *.obj file.
    1) Vertex indices are decreased by 1.
    2) Homogeneous coordinate = 1.0 added to each vertex (if not found in the file)
    """
    obj_file = open(filename, 'r')
    vertices = []
    faces = []
    for line in obj_file:
        if line.startswith('v'):
            vertex_coords = map(float, line.split(' ')[1:])
            if len(vertex_coords) < 4:
                vertex_coords.append(1.0)
            vertices.append(np.array(vertex_coords))
        elif line.startswith('f'):
            face = map(int, line.split(' ')[1:])
            faces.append(np.array(face))
    obj_file.close()
    return (np.array(vertices), np.array(faces) - 1)