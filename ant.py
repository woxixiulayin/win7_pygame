# -*- coding: utf-8 -*-#
import pygame
from  pygame.locals import *
import  math
from gameobjects.vector2 import  Vector2
from sys import exit
from random import randint, choice

SCREENSIZE = (640, 480)
NET_POSITION = (320, 240)
NET_SIZE = 100
ANT_COUNT = 20

class  State(object):
    def __init__(self, name):
        self.name = name
    def do_action(self):
        pass
    def check_conditions(self):
        pass
    def entry_action(self):
        pass
    def exit_action(self):
        pass

class StateMachine(object):
    def __init__(self):
        self.states = {}
        self.active_state = None
    def add_state(self, state):
        self.states[state.name] = state
        print state.name
    def think(self):
        if self.active_state is None:
            return
        self.active_state.do_action()
        new_state = self.active_state.check_conditions()
        if new_state is not None:
            self.set_state(new_state)
    def set_state(self, new_state_name):
        if self.active_state is not None:
            self.active_state.exit_action()
        self.active_state = self.states[new_state_name]
        self.active_state.entry_action()




class GameEntity(object):
    def __init__(self, world, name, image):
        self.world = world
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
        self.brain.think()
        if self.speed > 0 and self.location != self.destination:
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(self.speed * time_passed, distance_to_destination)
            self.location += travel_distance * heading



class World(object):
    def __init__(self):
        self.entities = {}
        self.entity_id = 0
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill((255, 0, 255))
        pygame.draw.circle(self.background, (0, 255, 0), NET_POSITION, int(NET_SIZE))
    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1
    def remove_entity(self, entity):
        del self.entities[entity.id]
    def get(self, entity_id):
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None
    def process(self,time_passed):
        time_pass_seconds = time_passed
        for entity in self.entities.values():
            entity.process(time_pass_seconds)
    def render(self, surface):
        surface.blit(self.background, (0, 0))
        for entity in self.entities.values():
            entity.render(surface)
    def get_close_entity(self, name, location, range = 100):
        location = Vector2(*location)
        for entity in self.entities.values():
            if entity.name == name:
                distance = location.get_distance_to(entity.location)
                if distance < range:
                    return entity
        return None


class Leaf(GameEntity):
    def __init__(self, world, image):
        GameEntity.__init__(self, world, 'leaf', image)

class Ant(GameEntity):
    def __init__(self, world, image):
        GameEntity.__init__(self, world, 'ant', image)
        explor_state = AntExplorState(self)
        seeking_state = AntSeekingState(self)
       # hunting_state = AntHuntingState(self)
        delivering_state = AntDeliveringState(self)
        self.brain.add_state(explor_state)
        self.brain.add_state(seeking_state)
      #  self.brain.add_state(hunting_state)
        self.brain.add_state(delivering_state)
        self.carryimage = None
    def carry(self, image):
        self.carryimage = image
    def drop(self, surface):
        if self.image:
            x, y = self.location
            w, h = self.carryimage.get_size()
            surface.blit(self.carryimage, (x-w, y-h/2))
            self.carryimage = None
    def render(self, surface):
        GameEntity.render(self, surface)
        if self.carryimage:
            x, y = self.location
            w, h = self.carryimage.get_size()
            surface.blit(self.carryimage, (x-w, y-h/2))


class AntExplorState(State):
    def __init__(self, ant):
        State.__init__(self, 'exploring')
        self.ant = ant
    def random_destination(self):
        w, h = SCREENSIZE
        self.ant.destination = Vector2(randint(0, w), randint(0, h))
    def do_action(self):
        if randint(0, 20) == 1:
            self.random_destination()
    def check_conditions(self):
        leaf = self.ant.world.get_close_entity('leaf', self.ant.location)
        if leaf is not None:
            self.ant.leaf_id = leaf.id
            return 'seeking'
       # spinder = self.ant.world.add_entity('spinder', self.ant.location)
       # if spinder is not None:
        #    self.ant.spinder = spinder.id
        #    return  'hunting'
        return None
    def entry_action(self):
        self.ant.speed = 120. + randint(-30, 30)
        self.random_destination()

class AntSeekingState(State):
    def __init__(self, ant):
        State.__init__(self, 'seeking')
        self.ant = ant
        self.leaf_id = None
    def check_conditions(self):
        #判断叶子是否被别的蚂蚁拿走
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf is None:
            return 'exploring'
        #当和叶子的距离小于5时，让蚂蚁背叶子，同时从世界中除去叶子实体
        if self.ant.location.get_distance_to(leaf.location) < 5.0:
            self.ant.carryimage = (leaf.image)
            self.ant.world.remove_entity(leaf)
            return "delivering"
        return None
    def entry_action(self):
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf is not None:
            self.ant.destination = leaf.location
            self.ant.speed = 160. + randint(-20, 20)

class AntDeliveringState(State):
    def __init__(self, ant):
        State.__init__(self, 'delivering')
        self.ant = ant
    def check_conditions(self):
        if self.ant.location.get_distance_to(Vector2(*NET_POSITION)) < NET_SIZE:
            if randint(0, 10) == 1:
                self.ant.drop(self.ant.world.background)
                return 'exploring'
        return None
    def entry_action(self):
        random_offset = Vector2(randint(-20, 20),randint(-20, 20))
        self.ant.destination = Vector2(*NET_POSITION) + random_offset

class AntHuntingState(State):
    pass

back_ground_image = 'fish_background.jpg'
plane_image = 'plane.png'



def run():
    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)
    world = World()
    w, h = SCREENSIZE
    clock =  pygame.time.Clock()
    leaf_image = pygame.image.load('leaf.png').convert_alpha()
    ant_image = pygame.image.load('ant.png').convert_alpha()
    ck_ground = pygame.image.load(back_ground_image).convert()
    for ant_nu in xrange(ANT_COUNT):
        ant = Ant(world, ant_image)
        ant.location = Vector2(randint(0, w), randint(0, h))
        ant.brain.set_state("exploring")
        world.add_entity(ant)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()

        time_passed = clock.tick(30)/1000.0


   #screen.fill((0,255,0))
   #screen.blit(back_ground, (0, 0))
        if randint(0, 20) == 1:
            leaf = Leaf(world, leaf_image)
            leaf.location = Vector2(randint(0, w), randint(0 , h))
            world.add_entity(leaf)

        world.process(time_passed)
        world.render(screen)
        pygame.display.update()

if __name__ == "__main__":
    run()