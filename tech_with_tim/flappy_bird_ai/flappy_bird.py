import pygame
import neat
import time
import os
import random
from flappy_classes import Bird, Pipe, Base
from flappy_common import get_image

pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 800
gen = 0
best_score = 0

STAT_FONT = pygame.font.SysFont('consolas', 25)


def draw_window(win, birds, pipes, base, score, generation):
    global best_score
    if score > best_score:
        best_score = score
    win.blit(pygame.transform.scale(get_image('bg'),(WIN_WIDTH,WIN_HEIGHT)), (0,0))
    
    for pipe in pipes:
        pipe.draw(win)
        
    text = STAT_FONT.render('Score: '+str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    
    text = STAT_FONT.render('Best: '+str(best_score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 30))
    
    text = STAT_FONT.render('Generation: '+str(generation), 1, (255,255,255))
    win.blit(text, (10,10))
    
    text = STAT_FONT.render('Alive Birds: '+str(len(birds)), 1, (255,255,255))
    win.blit(text, (10,30))
    
    base.draw(win)
    
    for bird in birds:
        bird.draw(win)
    pygame.display.update()


def main(genomes, config):
    global gen
    gen += 1
    nets = []
    ge = []
    birds = []
    
    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230,350))
        genome.fitness = 0
        ge.append(genome)

    score = 0
    
    base = Base(730)
    pipes = [Pipe(600)]
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break
                
        for x, bird in enumerate(birds):
            bird.move(score)
            ge[x].fitness += 0.1
            
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height),
                                       abs(bird.y - pipes[pipe_ind].bottom)))
            
            if output[0] > 0.5:
                bird.jump(score)

        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                                
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
                
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
                
            pipe.move(score)
                
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600, score, pipes[-1]))
                
        for r in rem:
            pipes.remove(r)
            
        for x, bird in enumerate(birds):   
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
                
        base.move(score)
        draw_window(win, birds, pipes, base, score, gen)
    
    
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)
    
    population = neat.Population(config)
    
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    winner = population.run(main,50)
    
    
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'assets', 'config-feedforward.txt')
    run(config_path)