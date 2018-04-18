# game.py

import pygame
import random

from vector import Vector
from rectangle import Rectangle
from node import Node
from spring import Spring

class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.hud_font = pygame.font.SysFont('courier', 14)
        self.game_objects_list = []
        self.space_rect = Rectangle(Vector(-50.0, -50.0), Vector(50.0, 50.0))
        self.origin_mass = 10000.0
        self.air_resistance = 100.0
        self.wind_force_mag = 100.0
        self.kill_radius = 100.0
        self.place_count = 0
        self.game_time_remaining = 2.0 * 60.0
        self.game_over = False
        self.GenerateNextNode()
        pygame.mixer.music.load('sounds/antechamber.mp3')
        pygame.mixer.music.play(-1)
        self.explosion_sound_list = [pygame.mixer.Sound('sounds/explode%d.wav' % i) for i in range(3)]
        self.placement_sound_list = [pygame.mixer.Sound('sounds/placement%d.wav' % i) for i in range(1)]
    
    def GenerateNextNode(self):
        color = (0, 0, 0)
        while color == (0, 0, 0):
            color = (random.randint(0, 1) * 255, random.randint(0, 1) * 255, random.randint(0, 1) * 255)
        mass = float(random.randint(30, 80))
        self.next_node = Node(Vector(), color, mass)
        self.place_count += 1
        if self.place_count % random.randint(3, 5) == 0:
            self.next_node.about_to_explode = True
        self.attachment_count = 2 if random.randint(1, 10) > 7 else 1
    
    def AddObject(self, obj):
        self.game_objects_list.append(obj)
        from explosion import Explosion
        if isinstance(obj, Explosion):
            sound = self.explosion_sound_list[random.randint(0, len(self.explosion_sound_list)-1)]
            sound.play()
    
    def Advance(self, time_delta):
        for obj in self.game_objects_list:
            obj.Reset()
        
        for obj in self.game_objects_list:
            obj.AccumulateForces(self)
        
        # Create a slight breeze that tries to keep everything in view.
        center = Vector()
        count = 0.0
        for obj in self.game_objects_list:
            if isinstance(obj, Node):
                center += obj.position
                count += 1.0
        if count > 0.0:
            center /= count
            wind_force = center.Normalize() * -self.wind_force_mag
            for obj in self.game_objects_list:
                if isinstance(obj, Node):
                    obj.net_force += wind_force
        
        for obj in self.game_objects_list:
            obj.Advance(time_delta, self)
        
        self.game_objects_list = [obj for obj in self.game_objects_list if obj.alive]
        
        if not self.game_over:
            pressed_keys = pygame.key.get_pressed()
            move_rate = 30.0
            if pressed_keys[pygame.K_UP]:
                self.next_node.position.y += move_rate * time_delta
            if pressed_keys[pygame.K_DOWN]:
                self.next_node.position.y -= move_rate * time_delta
            if pressed_keys[pygame.K_LEFT]:
                self.next_node.position.x -= move_rate * time_delta
            if pressed_keys[pygame.K_RIGHT]:
                self.next_node.position.x += move_rate * time_delta
            
            mouse_pos = pygame.mouse.get_pos()
            if 0 <= mouse_pos[0] < self.screen.get_width() and 0 <= mouse_pos[1] < self.screen.get_height():
                space_pos = self.SpaceFromScreen(mouse_pos)
                self.next_node.position = space_pos
        
            self.game_time_remaining -= time_delta
            if self.game_time_remaining <= 0.0:
                self.game_over = True
    
    def HandleEvent(self, event):
        if not self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._ChooseNextNodeLocation()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # This is a left click, but where is the enum for it?
                    self._ChooseNextNodeLocation()
    
    def _ChooseNextNodeLocation(self):
        node_list = self.FindAttachmentNodes()
        for node in node_list:
            self.AddObject(Spring(node, self.next_node))
        self.AddObject(self.next_node)
        self.GenerateNextNode()
        sound = random.choice(self.placement_sound_list)
        sound.play()
    
    def Draw(self, time_elapsed):
        self.screen.fill((0, 0, 0))

        self.game_objects_list.sort(key=lambda obj: obj.DrawSortKey())
        for obj in self.game_objects_list:
            obj.Draw(self)

        self.next_node.Draw(self, True)

        spring_count = 0
        node_count = 0
        for obj in self.game_objects_list:
            if isinstance(obj, Node):
                node_count += 1
            elif isinstance(obj, Spring):
                spring_count += 1

        text = self.hud_font.render('FPS: %f' % (1.0 / time_elapsed), True, (128, 128, 128))
        self.screen.blit(text, (0, 0))

        text = self.hud_font.render('Score: %d' % self.score, True, (255, 255, 255))
        self.screen.blit(text, (0, self.hud_font.get_height()))
        
        text = self.hud_font.render('Nodes: %d' % node_count, True, (255, 255, 255))
        self.screen.blit(text, (0, self.hud_font.get_height() * 2))

        text = self.hud_font.render('Springs: %d' % spring_count, True, (255, 255, 255))
        self.screen.blit(text, (0, self.hud_font.get_height() * 3))
        
        if not self.game_over:
            minutes = int(self.game_time_remaining / 60.0)
            seconds = int(self.game_time_remaining % 60.0)
            text = self.hud_font.render('Time left: %d:%02d' % (minutes, seconds), True, (255, 255, 255))
            self.screen.blit(text, (0, self.hud_font.get_height() * 4))
        else:
            text = 'GAME OVER'
            coords = self._CenterText(text, self.hud_font)
            text = self.hud_font.render(text, True, (255, 255, 255))
            self.screen.blit(text, coords)
    
    def _CenterText(self, text, font):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        text_width, text_height = font.size(text)
        coords = ((screen_width - text_width) // 2, (screen_height - text_height) // 2)
        return coords
    
    def SpaceToScreen(self, position):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        screen_rect = Rectangle(Vector(), Vector(screen_width, screen_height))
        screen_rect.ShrinkToMatchAspectRatio(self.space_rect)
        screen_pos = self.space_rect.LinearMap(screen_rect, position)
        
        x = int(screen_pos.x)
        y = screen_height - int(screen_pos.y)
        
        #x = min(max(x, 0), screen_width - 1)
        #y = min(max(y, 0), screen_height - 1)
        
        return (x, y)

    def SpaceFromScreen(self, coords):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        x = coords[0]
        y = screen_height - coords[1]

        screen_rect = Rectangle(Vector(), Vector(screen_width, screen_height))
        screen_rect.ShrinkToMatchAspectRatio(self.space_rect)
        
        space_pos = screen_rect.LinearMap(self.space_rect, Vector(x, y))
        return space_pos
    
    def FindAttachmentNodes(self):
        node_list = [obj for obj in self.game_objects_list if isinstance(obj, Node)]
        node_list.sort(key=lambda obj: (obj.position - self.next_node.position).Length())
        while len(node_list) > self.attachment_count:
            node_list.pop(-1)
        return node_list