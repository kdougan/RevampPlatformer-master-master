import pygame

from pygame.locals import *
from constants import *

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.direction = pygame.math.Vector2(0,0)

        self.image = pygame.Surface((8,12))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=pos)

    def event_handler(self):
        keys = pygame.key.get_pressed()

        if keys[K_RIGHT]:
            self.direction.x = 1
        if keys[K_LEFT]:
            self.direction.x = -1
        if keys[K_SPACE]:
            pass
        

    def update(self): 
        self.event_handler()
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y
    