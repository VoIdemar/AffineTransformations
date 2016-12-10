import numpy as np

from affine.datastruct.object3d import Object3D

class AxisObject(Object3D):
    
    def __init__(self, ort_length):
        self.__ort_length = ort_length
        center = [0.0, 0.0, 0.0, 1.0]
        OX = [ort_length, 0.0, 0.0, 1.0]
        OY = [0.0, ort_length, 0.0, 1.0]
        OZ = [0.0, 0.0, ort_length, 1.0]
        vertices = np.transpose(np.array([center, OX, OY, OZ]))
        edges = [(0, 1), (0, 2), (0, 3)]
        super(AxisObject, self).__init__(
             vertices, 
             faces=None, 
             draw_visible_edges_only=False,
             edges = edges
        )
    
    @property
    def ort_length(self):
        return self.__ort_length
    
class GridObject(Object3D):
    
    def __init__(self, x_range, z_range, N, M):
        self.__N = N
        self.__M = M
        self.__x_range = x_range
        self.__z_range = z_range
        vertices = self._fill_vertices()
        edges = self._fill_edges()
        super(GridObject, self).__init__(
             vertices, 
             faces=None, 
             draw_visible_edges_only=False,
             edges = edges
        )
        
    @property
    def N(self):
        return self.__N
    
    @property
    def M(self):
        return self.__M
    
    @property
    def x_range(self):
        return self.__x_range
    
    @property
    def z_range(self):
        return self.__z_range
    
    def _fill_vertices(self):
        xmin, xmax = self.x_range
        zmin, zmax = self.z_range
        x = np.linspace(xmin, xmax, self.N + 1)
        z = np.linspace(zmin, zmax, self.M + 1)
        
        # Fill horizontal
        z_horiz0 = np.empty(self.N + 1)
        z_horiz0.fill(z[0])
        z_horizN = np.empty(self.N + 1)
        z_horizN.fill(z[self.N])
        y_horiz = np.empty(self.N + 1)
        y_horiz.fill(0.0)
        w_horiz = np.empty(self.N + 1)
        w_horiz.fill(1.0)
        vertices = zip(x, y_horiz, z_horiz0, w_horiz) + zip(x, y_horiz, z_horizN, w_horiz)
        
        # Fill vertical
        x_vert0 = np.empty(self.M - 1)
        x_vert0.fill(x[0])
        x_vertM = np.empty(self.M - 1)
        x_vertM.fill(x[self.M])
        y_vert = np.empty(self.M - 1)
        y_vert.fill(0.0)
        w_vert = np.empty(self.M - 1)
        w_vert.fill(1.0)
        vertices = vertices + zip(x_vert0, y_vert, z[1:-1], w_vert) + zip(x_vertM, y_vert, z[1:-1], w_vert)
        
        return np.array(vertices)
    
    def _fill_edges(self):
        edges = []
        for i in range(self.N + 1):
            edges.append((i, i + 1 + self.N))
        i0 = 2*self.N + 2
        for i in range(self.M - 1):
            edges.append((i0 + i, i0 + i + self.M - 1))
        return edges