import numpy as np

from affine.affine2d.basic import to_homogeneous, to_cartesian

class PlanarFigure(object):
    '''
    Class representing planar figures. Figure itself is represented by the matrix of points' homogeneous coordinates
    '''
    __INIT_VALUE_ERROR_MSG = 'Invalid argument, numpy.ndarray of size 3xN or Nx3 expected'
        
    def __init__(self, matrix):
        if type(matrix) == np.ndarray and len(matrix.shape) == 2 and matrix.dtype <> np.object_:
            if matrix.shape[1] == 3:
                self.__matr = matrix[:]
            elif matrix.shape[0] == 3:
                self.__matr = np.transpose(matrix)
            else:
                raise ValueError(PlanarFigure.__INIT_VALUE_ERROR_MSG)
        else:
            raise ValueError(PlanarFigure.__INIT_VALUE_ERROR_MSG)
    
    def __getitem__(self, index):
        return tuple(self.__matr[index])
    
    def __setitem__(self, index, point):
        x, y, u = to_homogeneous(point)
        if u <> 0:
            self.__matr[index] = (x, y, u)
    
    def get_all_vertices(self):
        return self.__matr
    
    def get_cartesian_coords(self):
        return np.apply_along_axis(to_cartesian, axis=1, arr=self.__matr)
    
    def apply_transform(self, transform):
        '''
        Applies the specified transformation to each point of the figure
        '''
        self.__matr = np.apply_along_axis(transform, axis=1, arr=self.__matr)
        
    def __str__(self):
        return self.__matr.__str__()