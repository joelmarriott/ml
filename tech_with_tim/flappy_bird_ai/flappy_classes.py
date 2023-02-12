from flappy_common import get_image
import pygame
import random

class Bird:
    BIRD_IMAGES = [ get_image('bird1'), get_image('bird2'), get_image('bird3') ]
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5
    
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.image_count = 0
        self.image = self.BIRD_IMAGES[0]
        
        
    def jump(self, score):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y
        
        
    def move(self, score):
        self.tick_count += 1

        direction = (self.velocity * self.tick_count) + (1.5 * self.tick_count ** 2)
        
        if direction >= 16:
            direction = 16
            
        if direction < 0:
            direction -= 2
            
        self.y = self.y + direction
        
        if direction < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY
                
                
    def draw(self, win):
        self.image_count += 1
        
        if self.tilt <= -80:
            self.image = self.BIRD_IMAGES[1]
            self.image_count = self.ANIMATION_TIME*2
            self.set_tilt(win)
            return
        
        if self.image_count < self.ANIMATION_TIME:
            self.image = self.BIRD_IMAGES[0]
        elif self.image_count <= self.ANIMATION_TIME*2:
            self.image = self.BIRD_IMAGES[1]
        elif self.image_count <= self.ANIMATION_TIME*3:
            self.image = self.BIRD_IMAGES[2]
        elif self.image_count <= self.ANIMATION_TIME*4:
            self.image = self.BIRD_IMAGES[1]
        elif self.image_count == self.ANIMATION_TIME*4 + 1:
            self.image = self.BIRD_IMAGES[0]
            self.image_count = 0
        self.set_tilt(win)
        
        
    def set_tilt(self, win):
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        top_left = (self.x, self.y)
        center = self.image.get_rect(topleft = top_left).center
        new_rect = rotated_image.get_rect(center=center)
        win.blit(rotated_image, new_rect.topleft)
            
        
    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
    
class Pipe:
    PIPE_IMAGE = get_image('pipe')
    GAP = 200
    VELOCITY = 5
    
    def __init__(self, x, score=0, last_pipe=None):
        self.x = x
        self.height = 0
        
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(self.PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = self.PIPE_IMAGE
        
        self.last_pipe = last_pipe
        
        self.passed = False
        self.set_height(score)
        
    
    def set_height(self, score):
        self.height = random.randrange(50, 450)
        max_distance = 250
        if self.last_pipe:
            max_distance = 250 - (score * 3)
        
            if self.height > self.last_pipe.height + max_distance:
                self.height = self.last_pipe.height + max_distance
                if self.height > 450:
                    self.height = 450
                
            if self.height < self.last_pipe.height - max_distance:
                self.height = self.last_pipe.height - max_distance
                if self.height < 50:
                    self.height = 50
            
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
        
        
    def move(self, score):
        self.x -= self.VELOCITY + (score / 1.5)
        
        
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        
        
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        
        return False
    
    
class Base:
    BASE_IMAGE = get_image('base')
    VELOCITY = 5
    WIDTH = BASE_IMAGE.get_width()
    
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        
        
    def move(self, score):
        self.x1 -= self.VELOCITY + (score / 1.5)
        self.x2 -= self.VELOCITY + (score / 1.5)
        
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
            
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
            
            
    def draw(self, win):
        win.blit(self.BASE_IMAGE, (self.x1, self.y))
        win.blit(self.BASE_IMAGE, (self.x2, self.y))