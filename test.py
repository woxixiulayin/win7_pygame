#!/usr/bin/python
import pygame
from pygame.locals import *
from sys import exit 

pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption("Hello World!")


back_imgae = 'ground.jpg'
fish_image = 'fish.png'
back_ground = pygame.image.load(back_imgae).convert()
mouse_cursor = pygame.image.load(fish_image).convert_alpha()

while True:
    for event in  pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(back_ground, (0, 0))
    x, y = pygame.mouse.get_pos()
    x-= mouse_cursor.get_width() / 2
    y-= mouse_cursor.get_height() / 2
    screen.blit(mouse_cursor, (x, y))
    pygame.display.update()





