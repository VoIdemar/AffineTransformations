from math import cosh, sinh, cos, sin, pi

from surface import Surface

class Hyperboloid(Surface):
    
    def __init__(self, a, b, c, v_min, v_max):
        Surface.__init__(self,
            x = lambda v, theta: a*cosh(v)*cos(theta),
            y = lambda v, theta: b*cosh(v)*sin(theta),
            z = lambda v, theta: c*sinh(v),
            t1_min = v_min,
            t1_max = v_max,
            t2_min = 0,
            t2_max = 2*pi
        )
        self.__a = a
        self.__b = b
        self.__c = c
    
    @property
    def hyperboloid_params(self):
        return (self.__a, self.__b, self.__c)