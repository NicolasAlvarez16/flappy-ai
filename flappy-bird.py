import pygame
import neat
import time
import os 
import random

# Constants
WIDTH = 500
HEIGHT = 800

# Images Constants
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))), 
             pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def jump(self):
        self.vel = -10.5 # To move up negative velocity is need
        self.tick_count = 0 # Keep track when it last jumped
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count**2 # Number of pixels bird moves up or down
        if d >= 16:
            # If bird is down more than 16 pixels, stop accelerating
            d = 16  
        
        if d < 0:
            d -= 2
        
        self.y = self.y + d 
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    def draw(self, window):
        self.img_count += 1
        
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2
        
        # Tilting bird properly --> Rotates the image around the center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = (self.x, self.y))
        window.blit(pygame.transform.rotate(self.img, self.tilt), (self.x, self.y))
    
    def get_mask(self):
        """Collision"""
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL
    
    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    def collide(self, bird):
        """Returns wether the bird collided with the pipe or not ---> Using mask for an accurate collision"""
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # How far away the two top-left hand corners are from each other
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_point = bird.mask.overlap(bottom_mask, bottom_offset) # Collision point for the bottom pipe (Return none)
        top_point = bird.mask.overlap(top_mask, top_offset) # Collision point for the top pipe (Retur none)

        if top_point or bottom_point:
            return True
        return False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        # Two ground images created
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            # Check if images is off the screen completely
            self.x1 = self.x2 + self.WIDTH # Move it back again
        
        if self.x2 + self.WIDTH < 0:
            # Check if images is off the screen completely
            self.x2 = self.x1 + self.WIDTH # Move it back again

    def draw(self, window):
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))

def draw_window(window, bird, pipes, base):
    window.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(window)
    
    base.draw(window)
    bird.draw(window)
    pygame.display.update()


def main():
    my_bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # my_bird.move()
        for pipe in pipes:
            pipe.move()
            
        base.move()
        draw_window(window, my_bird, pipes, base)
    pygame.quit()
    quit()

main()
