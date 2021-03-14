from global_constants import BIRD_IMGS, pygame

class Bird:
    """Bird Class represeintg The Flappy Bird"""
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        """Initialising Object; params: position x(int) and posiont y(int)"""
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def jump(self):
        """Jump method for the bird"""
        self.vel = -10.5 # To move up negative velocity is need
        self.tick_count = 0 # Keep track when it last jumped
        self.height = self.y

    def move(self):
        """Move method for the bird"""
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
        """Draw method to place the bird on the screen"""
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
        """Gets the mask for the current image of the bird ---> Makes collision possible"""
        return pygame.mask.from_surface(self.img)