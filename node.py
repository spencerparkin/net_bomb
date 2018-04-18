# node.py

import pygame
import random

from vector import Vector
from game_object import GameObject

class Node(GameObject):
    def __init__(self, position, color, mass=1.0):
        super().__init__()
        self.color = color
        self.position = position
        self.velocity = Vector()
        self.mass = mass
        self.net_force = Vector()
        self.about_to_explode = False
        self.explosion_time_remaining = 2.0
        self.chain_number = 0

    def Reset(self):
        self.net_force = Vector()

    def AccumulateForces(self, game):
        '''
        distance = self.position.Length()
        force = self.position.Normalize() * -(self.mass * game.origin_mass / (distance * distance))
        force = self._CheckForce(force)
        self.net_force += force
        '''
        if self.velocity.Length() > 0.1:
            air_resistance_force = self.velocity.Normalize() * -game.air_resistance
            self.net_force += air_resistance_force

    def Advance(self, time_delta, game):
        acceleration = self.net_force / self.mass
        self.velocity += acceleration * time_delta
        self.position += self.velocity * time_delta
        if self.about_to_explode:
            self.explosion_time_remaining -= time_delta
            if self.explosion_time_remaining <= 0.0:
                self.alive = False
                from explosion import Explosion
                game.AddObject(Explosion(self.position, self.mass / 2.0, self.color, self.chain_number))
                game.score += self.chain_number * int(self.mass)
        if self.position.Length() > game.kill_radius:
            self.alive = False

    def Draw(self, game, placing=False):
        center = game.SpaceToScreen(self.position)
        radius = int(self.mass / 5.0)
        pygame.draw.circle(game.screen, self.color, center, radius)
        if self.about_to_explode:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pygame.draw.circle(game.screen, color, center, radius, 2)
        if placing:
            node_list = game.FindAttachmentNodes()
            for node in node_list:
                posA = game.SpaceToScreen(node.position)
                posB = game.SpaceToScreen(self.position)
                color = (255, 255, 255)
                pygame.draw.line(game.screen, color, posA, posB, 2)
    
    def DrawSortKey(self):
        return 2