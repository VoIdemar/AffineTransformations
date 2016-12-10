class Surface(object):
    
    def __init__(self, x, y, z, t1_min, t1_max, t2_min, t2_max):
        self.__x = x
        self.__y = y
        self.__z = z
        self.__t1_min = t1_min
        self.__t1_max = t1_max
        self.__t2_min = t2_min
        self.__t2_max = t2_max
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    @property
    def z(self):
        return self.__z
    
    @property
    def t1_min(self):
        return self.__t1_min
    
    @property
    def t1_max(self):
        return self.__t1_max
    
    @property
    def t2_min(self):
        return self.__t2_min
    
    @property
    def t2_max(self):
        return self.__t2_max