import numpy as np

import affine.affine3d.basic as basic
from affine.affine3d.projection import matr_to2d

class Object3D(object):
    """
    Class of 3d objects. Object itself is represented by the matrix of points' homogeneous coordinates.
    """
    
    __INIT_VALUE_ERROR_MSG = 'Invalid \"vertices\" argument, numpy.ndarray of size 4xN or Nx4 expected'
        
    def __init__(self, vertices, faces, draw_visible_edges_only=False, edges=None):
        if type(vertices) == np.ndarray and len(vertices.shape) == 2 and vertices.dtype <> np.object_:
            rows, columns = vertices.shape
            if rows <> 4 and columns == 4:
                self.__vertices = np.transpose(vertices)
            elif rows == 4:
                self.__vertices = vertices
            else:
                raise ValueError(Object3D.__INIT_VALUE_ERROR_MSG)
            self.__with_faces = not (faces is None)
            self.__faces = faces
            if edges is None:
                self.__find_edges()
            else:
                self.__edges = edges
            if self.with_faces:
                self.__build_body_matrix()
            self.__draw_visible_edges_only = draw_visible_edges_only
            if draw_visible_edges_only:
                self.__find_visible_edges()
            else:
                self.__visibleEdgesIndexes = []          
        else:
            raise ValueError(Object3D.__INIT_VALUE_ERROR_MSG) 
          
    @staticmethod
    def create_by_edges(vertices, edges):
        return Object3D(vertices, faces=None, draw_visible_edges_only=False, edges=edges)
    
    @staticmethod
    def create_by_faces(vertices, faces, draw_visible_edges_only=False):
        return Object3D(vertices, faces, draw_visible_edges_only)
        
    @property               
    def draw_visible_edges_only(self):
        return self.__draw_visible_edges_only
    
    @draw_visible_edges_only.setter
    def draw_visible_edges_only(self, value):
        self.__draw_visible_edges_only = value
    
    def get_vertex(self, index):
        return self.__vertices[:,index]
    
    def get_all_vertices(self):
        return self.__vertices
    
    def get_face(self, index):
        return self.__faces[index]
    
    def get_all_faces(self):
        return self.__faces
    
    def get_edge(self, index):
        return self.__edges[index]
    
    @property
    def with_faces(self):
        return self.__with_faces
    
    def get_all_edges(self):
        if self.draw_visible_edges_only:
            return [self.__edges[i] for i in self.__visibleEdgesIndexes]
        else:
            return self.__edges

    def apply_transform(self, transformMatrix):
        """
        Applies the specified transformation to each point of the object
        """
        self.__vertices = np.dot(transformMatrix, self.__vertices)
        if self.with_faces:
            self.__body_matrix = np.dot(self.__body_matrix, np.linalg.inv(transformMatrix))
        if self.draw_visible_edges_only:
            self.__find_visible_edges()
    
    def get_projection(self):
        return np.dot(matr_to2d(), self.__vertices)
    
    def get_custom_projection(self, projection_matrix):
        return np.dot(matr_to2d(), np.dot(projection_matrix, self.__vertices))
    
    def __build_body_matrix(self):
        self.__body_matrix = None        
        for face in self.__faces:
            x1, y1, z1 = basic.to_cartesian(self.__vertices[:,face[0]])
            x2, y2, z2 = basic.to_cartesian(self.__vertices[:,face[1]])
            x3, y3, z3 = basic.to_cartesian(self.__vertices[:,face[2]])
            A = np.linalg.det(np.array([[y1, z1, 1.0],
                                        [y2, z2, 1.0],
                                        [y3, z3, 1.0]]))
            B = np.linalg.det(np.array([[z1, x1, 1.0],
                                        [z2, x2, 1.0],
                                        [z3, x3, 1.0]]))
            C = np.linalg.det(np.array([[x1, y1, 1.0],
                                        [x2, y2, 1.0],
                                        [x3, y3, 1.0]]))
            D = -np.linalg.det(np.array([[x1, y1, z1],
                                         [x2, y2, z2],
                                         [x3, y3, z3]]))
            test_point = None
            index = 0
            while (test_point is None) and index < self.__vertices.shape[1]:
                if not (index in face):
                    test_point = self.__vertices[:,index]
                index = index + 1            
            x, y, z = basic.to_cartesian(test_point)
            if A*x + B*y + C*z + D < 0.0:
                A, B, C, D = -A, -B, -C, -D
            if self.__body_matrix is None:
                self.__body_matrix = np.array([A, B, C, D])
            else:
                self.__body_matrix = np.vstack((self.__body_matrix, np.array([A, B, C, D])))
            
    def __find_edges(self):
        
        def add_edge(edges, newEdge):
            if edges.count(newEdge) == 0 and edges.count(newEdge[::-1]) == 0:
                edges.append(newEdge)
                
        edges = []
        for face in self.__faces:
            for i in range(len(face) - 1):
                edge = tuple(face[i:i + 2])
                add_edge(edges, edge)
            edge = tuple([face[0], face[-1]])
            add_edge(edges, edge)
        self.__edges = edges
    
    def __find_visible_edges(self):
        dotProdValues = zip(range(len(self.__body_matrix)), np.dot(self.__body_matrix, np.array([0, 0, 1, 0])))
        visibleFacesIndexes = []
        for (index, dotProdValue) in dotProdValues:
            if dotProdValue >= 0.0:
                visibleFacesIndexes.append(index)  
        visibleEdgesIndexes = []       
        for (indStart, indEnd) in self.__edges:
            for i in visibleFacesIndexes:
                face = self.__faces[i]
                if (indStart in face) and (indEnd in face):
                    visibleEdgesIndexes.append(self.__edges.index((indStart, indEnd)))
                    break
        self.__visibleEdgesIndexes = visibleEdgesIndexes
        
    def __str__(self):
        s = '3D Object:\n'
        s += 'vertices:\n' + self.__vertices.__str__() + ',\n'
        s += 'edges: ' + self.__edges.__str__() + '\n'
        return s