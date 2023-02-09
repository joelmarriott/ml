import pygame
import os


def get_image(image_name):
    image_path = os.path.join(os.path.realpath(os.path.dirname(__file__)),
                              'assets',
                              image_name+'.png')
    loaded_image = pygame.image.load(image_path)
    scaled_image = pygame.transform.scale2x(loaded_image)
    return scaled_image


WIN_WIDTH = 600
WIN_HEIGHT = 800

PIPE_IMAGE = get_image('pipe')
BASE_IMAGE = get_image('base')
BG_IMAGE = get_image('bg')