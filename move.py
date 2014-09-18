__author__ = 'gang'

import  pygame
from pygame.locals import *
from sys import exit

pygame.init()

screen = pygame.display.set_mode((640, 480), FULLSCREEN, 32)
pygame.display.set_caption('move picture! made by Master Liu')
back_image = 'ground.jpg'
back_ground = pygame.image.load(back_image).convert()

x, y = 0 , 0
move = 10
fullscreen = True

screen.blit(back_ground, (x, y))
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                x = x - move
            elif event.key == K_RIGHT:
                x = x + move
            elif event.key == K_UP:
                y = y - move
            elif event.key == K_DOWN:
                y = y + move
            elif event.key == K_ESCAPE:
                exit()
            elif event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((640, 480), FULLSCREEN, 32)
                else:
                    screen = pygame.display.set_mode((640, 480), 0, 32)
            screen.fill((0, 0, 0))
            screen.blit(back_ground, (x, y))
            pygame.display.update()