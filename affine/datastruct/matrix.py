import numpy as np

class Matrix(object):

    __TYPE_ERROR_MSG = 'Incompatible types: Matrix and '
    __NON_INT_POWER_MSG = 'Power must be a positive integer. Current value: '
    
    def __init__(self, n=1, m=1):
        self.__elems = np.zeros((n, m))
        
    @staticmethod
    def from_array(array_like):
        matr = Matrix(0, 0)
        numpyElems = np.array(array_like)
        if not (numpyElems is None):
            matr.__elems = numpyElems
        return matr
        
    def __getitem__(self, index):
        i, j = index
        return self.__elems[i, j]
    
    def __setitem__(self, index, value):
        i, j = index
        self.__elems[i, j] = value
        
    def dot(self, matr):
        return Matrix.from_array(np.dot(self.__elems, matr.__elems))
    
    def transpose(self):
        self.__elems = np.transpose(self.__elems)
    
    def __add__(self, matr):
        if type(self) <> type(matr):
            raise TypeError(Matrix.__TYPE_ERROR_MSG + type(matr).__name__) 
        res = Matrix(0, 0)
        res.__elems = self.__elems + matr.__elems
        return res
    
    def __radd__(self, matr):
        if type(self) <> type(matr):
            raise TypeError(Matrix.__TYPE_ERROR_MSG + type(matr).__name__) 
        return matr.__add__(self)
    
    def __sub__(self, matr):
        if type(self) <> type(matr):
            raise TypeError(Matrix.__TYPE_ERROR_MSG + type(matr).__name__)
        return self.__elems - matr.__elems
    
    def __rsub__(self, matr):
        if type(self) <> type(matr):
            raise TypeError(Matrix.__TYPE_ERROR_MSG + type(matr).__name__) 
        return matr.__sub__(self)
        
    def __pow__(self, power):
        if type(power) == int and power > 0:
            res = self
            for y in range(1, power):
                res = res.dot(self)
            return res
        else:
            raise TypeError(Matrix.__NON_INT_POWER_MSG + str(power))
    
    def __eq__(self, matrix):
        if type(self) <> type(matrix):
            return False
        return np.array_equal(self.__elems, matrix.__elems)
        
    def __str__(self):
        return self.__elems.__str__()