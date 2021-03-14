from global_constants import WIDTH, HEIGHT, BG_IMG, pygame, neat, time
from Game_Classes.bird import Bird
from Game_Classes.pipe import Pipe
from Game_Classes.base import Base

pygame.font.init()

STAT_FONT = pygame.font.SysFont("comicsans", 50)

def draw_window(window, bird, pipes, base, score):
    """Draws window for the main loop"""
    window.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(window)
    
    # Score
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(text, (WIDTH - 10 - text.get_width(), 10)) # Accomodate the score to thes screen, no matter how big it is

    base.draw(window)
    bird.draw(window)

    pygame.display.update()


def main():
    """Main Function"""
    my_bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    run = True
    score = 0

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        my_bird.move()
        add_pipe = False
        rem = [] # List of removed pipes
        for pipe in pipes:
            if pipe.collide(my_bird):
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < my_bird.x:
                pipe.passed = True
                add_pipe = True
            
            pipe.move()
        
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        
        for r in rem:
            pipes.remove(r)
        
        if my_bird.y + my_bird.img.get_height() >= 730:
            pass

        base.move()
        draw_window(window, my_bird, pipes, base, score)
    pygame.quit()
    quit()

main()
