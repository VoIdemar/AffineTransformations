from math import cos, sin, pi

from surface import Surface

class Torus(Surface):
    
    def __init__(self, tube_radius, torus_radius):
        Surface.__init__(self,
            x = lambda theta, phi: (torus_radius + tube_radius*cos(phi))*cos(theta),
            y = lambda theta, phi: (torus_radius + tube_radius*cos(phi))*sin(theta),
            z = lambda theta, phi: tube_radius*sin(phi),
            t1_min = 0,
            t1_max = 2*pi,
            t2_min = 0,
            t2_max = 2*pi
        )
        self.__tube_radius = tube_radius
        self.__torus_radius = torus_radius
    
    @property
    def tube_radius(self):
        return self.__tube_radius
    
    @property
    def torus_radius(self):
        return self.__torus_radius