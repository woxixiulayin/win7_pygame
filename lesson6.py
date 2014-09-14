__author__ = 'gang'
import pygame
from  pygame.locals import *
from sys import exit

pygame.init()

scree = pygame.display.set_mode((640,480), 0, 32)
plant_image = 'plane.png'

plant = pygame.image.load(plant_image).convert_alpha()
bland_surface = pygame.Surface((256,256), 0, 32)
pygame.Surface((256,256), 0, 32)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    bland_surface.fill((255, 255, 0))
    scree.fill((0, 255, 0))
    pygame.draw.line(scree, (255, 255, 255), (100, 200), (200, 300), 20)
    #scree.blit(bland_surface,(0,0))
    scree.blit(plant, (200, 200))

    pygame.display.update()