from math import cos, sin, pi
from surface import Surface

class MobiusStrip(Surface):
    
    def __init__(self, width, radius):
        Surface.__init__(self,
            x = lambda u, v: (radius + 0.5*v*cos(0.5*u))*cos(u),
            y = lambda u, v: (radius + 0.5*v*cos(0.5*u))*sin(u),
            z = lambda u, v: 0.5*v*sin(0.5*u),
            t1_min = 0,
            t1_max = 2*pi,
            t2_min = -width,
            t2_max = width
        )
        self.__radius = radius
        self.__width = width
        
    @property
    def width(self):
        return self.__width
    
    @property
    def radius(self):
        return self.__radius