# vector.py

import math

class Vector(object):
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)
    
    def Dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def Cross(self, other):
        return self.x * other.y - self.y * other.x
    
    def Length(self):
        return math.sqrt(self.Dot(self))
    
    def Scale(self, scale):
        return self * scale
    
    def Normalize(self):
        try:
            return self.Scale(1.0 / self.Length())
        except ZeroDivisionError:
            return Vector()
    
    def Rotate(self, angle):
        pass
    
    def Reflect(self, axis):
        pass
    
    def ProjectOnto(self, vector):
        pass
    
    def RejectFrom(self, vector):
        pass
    
    @staticmethod
    def Lerp(self, vectorA, vectorB, value):
        return vectorA + (vectorB - vectorA) * value

    @staticmethod
    def LerpInv(self, vectorA, vectorB, vector):
        vectorC = vectorB - vectorA
        vectorD = vector - vectorA
        # Note that the cross between vectorC and vectorD should be near zero.
        return vectorD.Dot(vectorC) / vectorC.Dot(vectorC)