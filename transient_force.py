# transient_force.py

from game_object import GameObject
from node import Node

class TransientForce(GameObject):
    def __init__(self, target, force):
        super().__init__()
        self.target = target
        self.force = force

    def AccumulateForces(self, game):
        if isinstance(self.target, Node):
            self.target.net_force += self.force
        self.alive = False