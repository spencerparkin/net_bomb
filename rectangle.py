# rectangle.py

from vector import Vector

class Rectangle(object):
    def __init__(self, corner_min, corner_max):
        self.corner_min = corner_min
        self.corner_max = corner_max
    
    def Width(self):
        return self.corner_max.x - self.corner_min.x
    
    def Height(self):
        return self.corner_max.y - self.corner_min.y
    
    def AspectRatio(self):
        return self.Width() / self.Height()
    
    def LinearMap(self, rectangle, position):
        tx = (position.x - self.corner_min.x) / self.Width()
        ty = (position.y - self.corner_min.y) / self.Height()
        result = Vector()
        result.x = rectangle.corner_min.x + tx * rectangle.Width()
        result.y = rectangle.corner_min.y + ty * rectangle.Height()
        return result
    
    def ExpandToMatchAspectRatio(self, rectangle):
        pass
    
    def ShrinkToMatchAspectRatio(self, rectangle):
        rect_aspect_ratio = rectangle.AspectRatio()
        if self.AspectRatio() > rect_aspect_ratio:
            delta = 0.5 * (self.Width() - self.Height() * rect_aspect_ratio)
            self.corner_min.x += delta
            self.corner_max.x -= delta
        else:
            delta = 0.5 * (self.Height() - self.Width() / rect_aspect_ratio)
            self.corner_min.y += delta
            self.corner_min.y -= delta