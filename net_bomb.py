# net_bomb.py

import time
import sys
import pygame

from game import Game

if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Net Bomb (v1.0)')
    
    game = Game(screen)
    
    time_elapsed = 0.0
    time_last = time.clock()
    time_step = 0.01

    while True:
        
        time_current = time.clock()
        time_elapsed = time_current - time_last
        time_last = time_current
        
        # We want our simulation to advance by a given time step regardless of our frame-rate.
        time_remaining = time_elapsed
        while time_remaining > 0.0:
            time_delta = time_step if time_step < time_remaining else time_remaining
            game.Advance(time_delta)
            time_remaining -= time_delta
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(game.score)
                sys.exit()
            else:
                game.HandleEvent(event)
        
        game.Draw(time_elapsed)
        
        pygame.display.flip()