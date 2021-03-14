import pygame 
import os

# pygame.font.init()

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

# STAT_FONT = pygame.font.SysFont("comicsans", 50)