from math import cos, sin, pi
from surface import Surface

class Sphere(Surface):
    
    def __init__(self, x0, y0, z0, r):
        Surface.__init__(
             self, 
             x = lambda theta, phi: x0 + r*cos(theta)*sin(phi), 
             y = lambda theta, phi: y0 + r*sin(theta)*sin(phi), 
             z = lambda theta, phi: z0 + r*cos(phi), 
             t1_min = 0,
             t1_max = 2*pi,
             t2_min = 0,
             t2_max = pi
        )
        self.__x0 = x0
        self.__y0 = y0
        self.__z0 = z0
        self.__r = r
    
    @property
    def center(self):
        return (self.__x0, self.__y0, self.__z0)
    
    @property
    def radius(self):
        return self.__r