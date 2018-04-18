# explosion.py

import pygame
import random

from vector import Vector
from game_object import GameObject
from node import Node
from transient_force import TransientForce

class Explosion(GameObject):
    def __init__(self, position, blast_radius, color, chain_number=0):
        super().__init__()
        self.color = color
        self.position = position
        self.blast_radius = blast_radius
        self.current_radius = 0.0
        self.blast_rate = 50.0
        self.chain_number = chain_number

    def Advance(self, time_delta, game):
        self.current_radius += self.blast_rate * time_delta
        if self.current_radius >= self.blast_radius:
            self.current_radius = self.blast_radius
            self.alive = False
        for obj in game.game_objects_list:
            if isinstance(obj, Node) and (obj.position - self.position).Length() <= self.current_radius:
                if obj.color == self.color:
                    obj.about_to_explode = True
                    obj.explosion_time_remaining = 0.0
                    obj.chain_number = self.chain_number + 1
                elif obj.alive:
                    force = (obj.position - self.position).Normalize() * 10000.0 * (1.0 - self.current_radius / self.blast_radius)
                    game.AddObject(TransientForce(obj, force))

    def Draw(self, game):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        center = game.SpaceToScreen(self.position)
        circle_point = self.position + Vector(self.current_radius, 0.0)
        coords = game.SpaceToScreen(circle_point)
        radius = coords[0] - center[0]
        pygame.draw.circle(game.screen, color, center, radius, min(radius, 4))