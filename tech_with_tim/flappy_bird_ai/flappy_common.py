import pygame
import os


def get_image(image_name):
    image_path = os.path.join(os.path.realpath(os.path.dirname(__file__)),
                              'assets',
                              image_name+'.png')
    loaded_image = pygame.image.load(image_path)
    scaled_image = pygame.transform.scale2x(loaded_image)
    return scaled_image