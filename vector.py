"""
vector support library
"""
import math
class Vector(list):
    """vector class that can be accessed by index or vector xyz axis"""
    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        list.__init__(self)
        self.append(x)
        self.append(y)
        self.append(z)

    @property
    def length(self):
        """get the lengths of the vector"""
        return math.sqrt( self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        """normalize the vector in place"""
        length = self.length
        if length:
            inverse = 1.0/length
            self.x = self.x * inverse
            self.y = self.y * inverse
            self.z = self.z * inverse
        return self

    @property
    def x(self):
        """get x (0)"""
        return self[0]

    @property
    def y(self):
        """get y (1)"""
        return self[1]

    @property
    def z(self):
        """get z(2)"""
        return self[2]

    @x.setter
    def x(self, value):
        """set x (0)"""
        self[0] = value

    @y.setter
    def y(self, value):
        """set y (1)"""
        self[1] = value

    @z.setter
    def z(self, value):
        """set z (2)"""
        self[2] = value   

    def __add__(self, other):
        return Vector(self[0] + other[0], self[1] + other[1], self[2] + other[2])

    def __sub__(self, other):
        return Vector(self[0] - other[0], self[1] - other[1], self[2] - other[2])

    def __mul__(self, other): #scale or dot product
        if type(other) == Vector:
            return self[0] * other[0] + self[1] * other[1] + self[2] + other[2]
        else:
            return Vector(self[0] * other, self[1] * other, self[2] * other)

    def __mod__(self, other): #cross product
        return Vector(self[1]*other[2] - self[2]*other[1], self[2]*other[0] - self[0]*other[2], self[0]*other[1] - self[1]*other[0])

    def __pow__(self, other): #raise to power
        if type(other) == Vector:
            raise ValueError('other needs to not be a vector')
        return Vector(self.x**other, self.y**other, self.z**other)