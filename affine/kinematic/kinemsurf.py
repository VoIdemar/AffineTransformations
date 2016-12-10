import numpy as np

class KinematicSurface(object):
    
    def __init__(self, generatrix, directrix, transform_matr, t1_min, t1_max, t2_min, t2_max):
        self.__generatrix = generatrix
        self.__directrix = directrix
        self.__transform_matr = transform_matr
        self.__t1_min = t1_min
        self.__t1_max = t1_max
        self.__t2_min = t2_min
        self.__t2_max = t2_max
        
    @property
    def generatrix(self):
        return self.__generatrix
    
    @property
    def directrix(self):
        return self.__directrix
    
    @property
    def transform_matrix(self):
        return self.__transform_matr
    
    @property
    def t1_range(self):
        return (self.__t1_min, self.__t1_max)
    
    @property
    def t2_range(self):
        return (self.__t2_min, self.__t2_max)
    
    def __call__(self, *args):
        t1, t2 = args
        return np.dot(self.__transform_matr(t1, t2), self.__generatrix(t1, t2)) + self.__directrix(t1, t2)