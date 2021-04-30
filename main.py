from global_constants import WIDTH, HEIGHT, BG_IMG, pygame, neat, time
from Game_Classes.bird import Bird
from Game_Classes.pipe import Pipe
from Game_Classes.base import Base
import os

pygame.font.init()

STAT_FONT = pygame.font.SysFont("comicsans", 50)

def draw_window(window, birds, pipes, base, score):
    """Draws window for the main loop"""
    window.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(window)
    
    # Score
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(text, (WIDTH - 10 - text.get_width(), 10)) # Accomodate the score to thes screen, no matter how big it is

    base.draw(window)
    for bird in birds:
        bird.draw(window)
    pygame.display.update()


def main(genomes, config):
    """Main Function"""
    nets = []
    ge = []
    my_birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        my_birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

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
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(my_birds) > 0: 
            if len(pipes) > 1 and my_birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break
        
        for x, bird in enumerate(my_birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()
        
        # my_bird.move()
        add_pipe = False
        rem = [] # List of removed pipes
        for pipe in pipes:
            for x, bird in enumerate(my_birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    my_birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
                
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            pipe.move()
        
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))
        
        for r in rem:
            pipes.remove(r)
        
        for x, bird in enumerate(my_birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                my_birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(window, my_birds, pipes, base, score)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)    
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    winner = population.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)