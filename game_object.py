# game_object.py

class GameObject(object):
    def __init__(self):
        self.alive = True
    
    def Reset(self):
        pass
    
    def AccumulateForces(self, game):
        pass
    
    def Advance(self, time_delta, game):
        pass

    def Draw(self, game):
        pass
    
    def DrawSortKey(self):
        return 0
    
    def _CheckForce(self, force, max_mag=1000.0):
        mag = force.Length()
        if mag > max_mag:
            force = force.Scale(max_mag / mag)
        return force