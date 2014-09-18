import pygame
from  pygame.locals import *
import  math
from gameobjects.vector2 import  Vector2
from sys import exit
from random import randint,choice


class GameEntity(object):
    def __init__(self, name, image):
        #self.world = world
        self.name = name
        self.image = image
        self.location = Vector2(0, 0)
        self.destination = Vector2(0, 0)
        self.speed = 0
        self.brain = StateMachine()
        self.id = 0
    def render(self, surface):
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x-w/2, y-h/2))
    def process(self, time_passed):
        #self.brain.think()
        if self.speed > 0 and self.location != self.destination:
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(self.speed * time_passed, distance_to_destination)
            self.location += travel_distance * heading

def StateMachine():
    pass
pygame.init()
back_ground_image = 'fish_background.jpg'
plane_image = 'plane.png'

screen = pygame.display.set_mode((640, 480), 0, 32)


back_ground = pygame.image.load(back_ground_image).convert()
plane = pygame.image.load(plane_image).convert_alpha()

clock =  pygame.time.Clock()

plane_entity_1 = GameEntity('pl', plane)
plane_entity_1.location = Vector2(50, 50)
plane_entity_1.speed = 40

plane_entity_2 = GameEntity('pl', plane)
plane_entity_2.location = Vector2(450, 450)
plane_entity_2.speed = 40

move_setp_x, move_setp_y = 150, 150


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
    screen.blit(back_ground, (0, 0))
    plane_entity_1.render(screen)
    plane_entity_2.render(screen)

    plane_entity_1.destination = Vector2(*pygame.mouse.get_pos())
    plane_entity_1.process(clock.tick(30)/1000.0)

    plane_entity_2.destination = Vector2(*pygame.mouse.get_pos())
    plane_entity_2.process(clock.tick(30)/1000.0)

    pygame.display.update()