# -*- coding: utf-8 -*-
__author__ = 'gang'

import  pygame
from pygame.locals import *
from sys import exit


fish_image = 'fish.jpg'
back_ground_image = 'fish_background.jpg'
plane_image = "plane.png"

pygame.init()
try:
    screen = pygame.display.set_mode((640, 480), 0, 32)
except pygame.error, e:
    print "can't creat the display"
    print e
    exit()
try:
    fish = pygame.image.load(fish_image).convert()
except pygame.error, e:
    print "can't creat the display"
    print e
    exit()

back_ground = pygame.image.load(back_ground_image)
plane = pygame.image.load(plane_image).convert_alpha()

font = pygame.font.SysFont("simhei", 50)
text_surface = font.render(u"周星驰", True, (0, 100, 255))

clock =  pygame.time.Clock()

move_setp_x, move_setp_y = 150, 150
x, y = 200., 200.

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
    screen.blit(back_ground, (0, 0))
#    screen.blit(text_surface, (x, 200))
    screen.blit(plane, (x, y))
    time_pass_second = clock.tick(30) / 1000.0
    x += move_setp_x * time_pass_second
    y += move_setp_y *time_pass_second
    if x > (640 - plane.get_width()) or x < 0:
        move_setp_x = 0 - move_setp_x
    if y > (480 - plane.get_height() + 60 ) or y < 0:
        move_setp_y = 0 - move_setp_y
    pygame.display.update()
