import pygame
import neat
import time
import os
import random
from flappy_classes import Bird
from flappy_common import get_image


WIN_WIDTH = 600
WIN_HEIGHT = 800

BG_IMAGE = get_image('bg')


def draw_window(win, bird):
    win.blit(BG_IMAGE, (0,0))
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(200,200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            bird.move()
            draw_window(win, bird)

    pygame.quit()
    quit()
    
    
if __name__ == '__main__':
    main()