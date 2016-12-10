import numpy as np

from affine.affine3d.projection import to2d
from affine.affine3d.basic import apply_transform, to_cartesian
from discreteerror import WrongDiscretizationError

class WireFrameModel(object):
        
    def __init__(self, x, y, z, t1_min, t1_max, t2_min, t2_max, N=10, M=10):
        self.__x = x
        self.__y = y
        self.__z = z
        self.__t1_min = t1_min
        self.__t1_max = t1_max
        self.__t2_min = t2_min
        self.__t2_max = t2_max
        self.reset_number_of_discrete_levels(N, M) 
        self.__find_faces()       
        self.__build_edges()
        self.__build_body_matrix()        
    
    @staticmethod
    def create_model_for_surface(surface, N=10, M=10):
        return WireFrameModel(
          x = surface.x,
          y = surface.y,
          z = surface.z,
          t1_min = surface.t1_min,
          t1_max = surface.t1_max,
          t2_min = surface.t2_min,
          t2_max = surface.t2_max,
          N = N, 
          M = M
        )
    
    @staticmethod
    def create_model_for_kinematic_surface(kinematic, N=10, M=10):
        return WireFrameModel(
          x = lambda t1, t2: to_cartesian(kinematic(t1, t2))[0],
          y = lambda t1, t2: to_cartesian(kinematic(t1, t2))[1],
          z = lambda t1, t2: to_cartesian(kinematic(t1, t2))[2],
          t1_min = kinematic.t1_range[0],
          t1_max = kinematic.t1_range[1],
          t2_min = kinematic.t2_range[0],
          t2_max = kinematic.t2_range[1],
          N = N,
          M = M
        )
    
    @property
    def grid(self):
        return self.__grid
    
    @property
    def faces(self):
        return self.__faces
    
    @property
    def edges(self):
        return self.__edges
    
    def reset_number_of_discrete_levels(self, N, M):
        if N < 1 or M < 1:
            raise WrongDiscretizationError(u'Incorrect number of discretization levels: N and M should not be lower than 1')
        self.__N = N
        self.__M = M
        self.__t1_grid = np.linspace(self.__t1_min, self.__t1_max, N + 1)
        self.__t2_grid = np.linspace(self.__t2_min, self.__t2_max, M + 1)
        self.__calculate_grid()    
    
    def apply_transform(self, transform_matr):
        for i in range(0, self.__grid.shape[0]):
            for j in range(0, self.__grid.shape[1]):        
                self.__grid[i][j] = apply_transform(self.__grid[i][j], transform_matr)
        self.__body_matr = np.dot(self.__body_matr, np.linalg.inv(transform_matr))
        
    def get_grid_projection(self):
        projection = np.empty(self.__grid.shape, np.ndarray)
        for i in range(0, projection.shape[0]):
            for j in range(0, projection.shape[1]):
                projection[i][j] = to2d(self.__grid[i][j])
        return projection
    
    def get_visible_edges(self):
        dotProdValues = zip(range(len(self.__body_matr)), np.dot(self.__body_matr, np.array([0, 0, 1, 0])))
        visibleFacesIndexes = []
        for (index, dotProdValue) in dotProdValues:
            if dotProdValue >= 0:
                visibleFacesIndexes.append(index)    
        visibleEdges = []
        for index in visibleFacesIndexes:
            face = self.__faces[index]
            for edge in [(face[0], face[1]), (face[1], face[2]), (face[3], face[2]), (face[0], face[3])]:
                if not (edge in visibleEdges):
                    visibleEdges.append(edge)
        return visibleEdges
    
    def __calculate_grid(self):
        x, y, z = self.__x, self.__y, self.__z
        N, M = self.__N, self.__M
        t1_grid, t2_grid = self.__t1_grid, self.__t2_grid
        self.__grid = np.empty((N + 1, M + 1), np.ndarray)
        for i in range(0, t1_grid.shape[0]):
            for j in range(0, t2_grid.shape[0]):
                t1, t2 = t1_grid[i], t2_grid[j]
                self.__grid[i][j] = np.array([x(t1, t2), y(t1, t2), z(t1, t2), 1])
    
    def __build_edges(self):
        edges = []
        maxI = self.__grid.shape[0] - 1
        maxJ = self.__grid.shape[1] - 1
        for i in range(0, maxI):
            for j in range(0, maxJ):
                edges.append( ((i, j), (i+1, j)) )
                edges.append( ((i, j), (i, j+1)) )
            edges.append( ((i, maxJ), (i+1, maxJ)) )
        for j in range(0, maxJ):
            edges.append( ((maxI, j), (maxI, j+1)) )
        self.__edges = edges
    
    def __get_three_unique_points(self, points):
        unique = []
        indexes = []
        for (i, j) in points:
            point = tuple(self.__grid[i][j])
            if not (point in unique) and len(unique) < 3:
                indexes.append((i, j))
                unique.append(point)        
        return (indexes, unique)
            
    def __build_body_matrix(self):
        body_matr = None
        for face in self.__faces:
            indexes, points = self.__get_three_unique_points(face)
            (i1, j1), (i2, j2), (i3, j3) = indexes
            x1, y1, z1 = to_cartesian(self.__grid[i1][j1])
            x2, y2, z2 = to_cartesian(self.__grid[i2][j2])
            x3, y3, z3 = to_cartesian(self.__grid[i3][j3])            
            A = np.linalg.det(np.array([[y1, z1, 1],
                                        [y2, z2, 1],
                                        [y3, z3, 1]]))
            B = np.linalg.det(np.array([[z1, x1, 1],
                                        [z2, x2, 1],
                                        [z3, x3, 1]]))
            C = np.linalg.det(np.array([[x1, y1, 1],
                                        [x2, y2, 1],
                                        [x3, y3, 1]]))
            D = -np.linalg.det(np.array([[x1, y1, z1],
                                         [x2, y2, z2],
                                         [x3, y3, z3]]))
            i1, i2 = -1, -1
            for i in range(0, self.__grid.shape[0]):
                for j in range(0, self.__grid.shape[1]):
                    if (i, j) in face or tuple(self.__grid[i][j]) in points:
                        continue
                    i1, i2 = i, j
                    break            
            x, y, z = to_cartesian(self.__grid[i1][i2])
            if A*x + B*y + C*z + D < 0:
                A, B, C, D = -A, -B, -C, -D
            if body_matr is None:
                body_matr = np.array([A, B, C, D])
            else:
                body_matr = np.vstack( (body_matr, np.array([A, B, C, D])) )           
        self.__body_matr = body_matr
    
    def __find_faces(self):
        self.__faces = [((i, j), (i+1, j), (i+1, j+1), (i, j+1)) 
                        for i in range(0, self.__grid.shape[0] - 1)
                        for j in range(0, self.__grid.shape[1] - 1)]