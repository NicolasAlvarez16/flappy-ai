from global_constants import BASE_IMG, pygame

class Base:
    """Represents the moving floor of the game"""
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """Movement of the floor"""
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
        """Draw floor ---> Two images that move together"""
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))