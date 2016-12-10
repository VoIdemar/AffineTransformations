from math import cos, sin, pi

from surface import Surface

class Conical(Surface):
    
    def __init__(self, aperture, v_min, v_max):
        Surface.__init__(self,
            x = lambda u, v: u*cos(aperture/2.0)*cos(v),
            y = lambda u, v: u*cos(aperture/2.0)*sin(v),
            z = lambda u, v: u*sin(aperture/2.0),
            t1_min = v_min,
            t1_max = v_max,
            t2_min = 0,
            t2_max = 2*pi
        )
        self.__aperture = aperture
    
    @property
    def aperture(self):
        return self.__aperture