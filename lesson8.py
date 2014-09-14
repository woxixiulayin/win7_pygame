# -*- coding: utf-8 -*-
__author__ = 'gang'

import  pygame
from pygame.locals import *
from sys import exit


fish_image = 'fish.jpg'
back_ground_image = 'fish_background.jpg'

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

fish = pygame.image.load(fish_image).convert()
back_ground = pygame.image.load(back_ground_image)

font = pygame.font.SysFont("simhei", 20)
text_surface = font.render(u"周星驰", True, (0, 255, 255))

clock =  pygame.time.Clock()

move_setp = 170
x = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(back_ground, (0, 0))
    screen.blit(text_surface, (x, 200))

    time_pass_second = clock.tick(30) / 1000.0
    x += move_setp * time_pass_second
    if x > 580 or x < 0:
        move_setp = 0 - move_setp
    pygame.display.update()
