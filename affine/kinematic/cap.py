import numpy as np

from affine.affine3d.basic import matr_rotate_z, matr_scale
from kinemsurf import KinematicSurface

class PomponCap(KinematicSurface):
    
    T1_MIN = 0
    T1_MEAN = 0.5*np.pi
    T1_MAX = np.pi
    T2_MIN = 0
    T2_MAX = 2*np.pi
    
    def __init__(self, r1, r2, r3):
        self.__r1 = r1
        self.__r2 = r2
        self.__r3 = r3
        super(PomponCap, self).__init__(
            generatrix = lambda t1, t2: self.__cap_generatrix(t2),
            directrix = lambda t1, t2: self.__cap_directrix(t1),
            transform_matr = self.__transform_matrix,
            t1_min = PomponCap.T1_MIN,
            t1_max = PomponCap.T1_MAX,
            t2_min = PomponCap.T2_MIN,
            t2_max = PomponCap.T2_MAX
        )
    
    @property
    def parameters(self):
        return (self.__r1, self.__r2, self.__r3)
        
    def __cap_directrix(self, t1):
        if PomponCap.T1_MIN <= t1 < PomponCap.T1_MEAN:
            return np.array([self.__r1*np.cos(t1), self.__r1*np.sin(t1), 0, 1])
        else:
            return np.array([-self.__r2*(1 + np.cos(2*t1)), self.__r1, 0, 1])
        
    def __cap_generatrix(self, t2):
        return np.array([np.cos(t2), 0, np.sin(t2), 1])
    
    def __scale_matr(self, t2):
        s = 1 + 0.25*np.abs(np.sin(4*t2))
        return matr_scale(s, s, s)
    
    def __radius_matr(self, t1):
        r = self.__r3*(1-2*t1/np.pi) if PomponCap.T1_MIN <= t1 < PomponCap.T1_MEAN else -self.__r2*np.sin(2*t1)
        return matr_scale(r, r, r)
        
    def __angle_function(self, t1):
        return t1 if PomponCap.T1_MIN <= t1 < PomponCap.T1_MEAN else 0.5*np.pi
    
    def __transform_matrix(self, t1, t2):
        return np.dot(np.dot(self.__scale_matr(t2), self.__radius_matr(t1)), matr_rotate_z(self.__angle_function(t1)))