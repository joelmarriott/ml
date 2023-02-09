from flappy_common import get_image
import pygame

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
        
        
    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y
        
        
    def move(self):
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