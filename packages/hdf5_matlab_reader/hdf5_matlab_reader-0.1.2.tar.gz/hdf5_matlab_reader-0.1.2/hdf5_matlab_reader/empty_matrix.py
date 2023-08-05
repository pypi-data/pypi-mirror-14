from __future__ import division, print_function
import numpy as np

class EmptyMatrix():
    def __init__(self, shape=(0, 0), dtype='double'):
        self.shape = tuple(shape)
        self.dtype = dtype

    def __repr__(self):
        if self.shape == (0, 0):
            return '[]'
        else:
            return '<Empty matrix of shape {0}>'.format(self.shape)

    def __int__(self):
        return 0

    #does not use long in python 3, should be fine
    def __long__(self):
        return 0

    def __float__(self):
        return 0.

    def __complex__(self):
        return 0j

    def __add__(self, other):
        return other

    def __radd__(self, other):
        return other

    def __sub__(self, other):
        return -other

    def __rsub__(self, other):
        return other

    def __mul__(self, other):
        return 0

    def __rmul__(self, other):
        return 0
    
    def __div__(self, other):
        return 0

    def __rdiv__(self, other):
        return np.nan

    def __mod__(self, other):
        return 0

    def __rmod__(self, other):
        return np.nan

    def __divmod__(self, other):
        return 0, 0

    def __rdivmod__(self, other): 
        return 0, np.nan

    def __pow__(self, other):
        return 0

    def __rpow__(self, other):
        return 1

    def __lshift__(self, other):
        return 0

    def __rlshift__(self, other):
        return other

    def __rshift__(self, other):
        return 0

    def __rrshift__(self, other):
        return other

    def __and__(self, other):
        return 0

    def __rand__(self, other):
        return 0

    def __or__(self, other):
        return other

    def __ror__(self, other):
        return other

    def __xor__(self, other):
        return other

    def __rxor__(self, other):
        return other

    def __neg__(self, other):
        return 0

    def __pos__(self, other):
        return 0

    def __abs__(self, other):
        return 0

    def __invert__(self, other):
        return -1

    def __oct__(self, other):
        return '0'

    def __hex__(self, other):
        return '0x0'

    def __coerce__(self, other):
        return None

    def __eq__(self, other):
        if other.__class__ != EmptyMatrix:
            return False
        return self.shape == other.shape
        
