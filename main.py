import sys
import random
from os import path
import pygame

import maploader
from constants import *
from camera import Camera
from player import Player

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
display_surface = pygame.Surface([DS_WIDTH , DS_HEIGHT])
mainclock = pygame.time.Clock()

class Game:
    def __init__(self):
        self.current_level_num = 0
        self.current_level = None
        self.running = False
        print("oui")
        self.run()

    def create_level(self):
        self.current_level = Level(self.current_level_num)
        print("oui")
        self.run()

    def run(self):
        self.create_level()


class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.entities = []
        self.particles = []
        

        self.running = False
        
        #self.map = maploader.Map(path.join(MAP_FOLDER, f"{level_num}.json"))
        #self.map = maploader.Map(path.join(MAP_FOLDER, "test.json"))
        self.width, self.height, entities, self.chunks = maploader.generate_map_data(path.join(MAP_FOLDER, "test.json"), CHUNK_SIZE)
        self.camera = Camera(DS_WIDTH , DS_HEIGHT)
        
        for entity in entities:
            if entity["name"] == "player":
                self.entities.append(Player((entity["x"], entity["y"])))
        self.run()
        
        
    def run(self):
        self.running = True
        # main game loop
        while self.running:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

    def update(self):
        for entity in self.entities:
            entity.update()
            #entity.animate()

        self.camera.focus(self.entities[0])
    
    def draw(self):
             
        display_surface.fill([0,0,0])
        for chunk_data in self.chunks.values():
            for tile in chunk_data[0]:
                display_surface.blit(tile.image, [tile.pos[0] - self.camera.rect.x , tile.pos[1] - self.camera.rect.y])
        
        #for entity in self.entities[1:]:
            #DISPLAY_SURF.blit(entity.image, self.camera.apply(entity.rect))
        
        display_surface.blit(self.entities[0].image, [self.entities[0].rect.x - self.camera.rect.x , self.entities[0].rect.y - self.camera.rect.y])
        screen.blit(pygame.transform.scale(display_surface, (WIDTH,HEIGHT)), (0,0))
        pygame.display.update()



def main():
    game = Game()


if __name__ == "__main__":
    main()