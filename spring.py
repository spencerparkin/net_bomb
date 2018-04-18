# spring.py

import pygame

from game_object import GameObject

class Spring(GameObject):
    def __init__(self, nodeA, nodeB):
        super().__init__()
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.equilibrium_length = 15.0
        self.stiffness = 100.0
    
    def Reset(self):
        pass

    def AccumulateForces(self, game):
        if self.nodeA.alive and self.nodeB.alive:
            vector = self.nodeB.position - self.nodeA.position
            current_length = vector.Length()
            vector = vector.Normalize()
            force = vector * -((self.equilibrium_length - current_length) * self.stiffness)
            force = self._CheckForce(force)
            self.nodeA.net_force += force
            self.nodeB.net_force -= force

    def Advance(self, time_delta, game):
        if not self.nodeA.alive or not self.nodeB.alive:
            self.alive = False
    
    def Draw(self, game):
        if self.nodeA.alive and self.nodeB.alive:
            posA = game.SpaceToScreen(self.nodeA.position)
            posB = game.SpaceToScreen(self.nodeB.position)
            color = (128, 128, 128)
            pygame.draw.line(game.screen, color, posA, posB, 2)
    
    def DrawSortKey(self):
        return 1