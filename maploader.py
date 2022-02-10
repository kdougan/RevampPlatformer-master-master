import json
from pygame import *
import math
from os import path
from functools import cache

@cache
def generate_map_data(level_path, chunk_size):
    chunk_data = {}
    map_data = json.load(open(level_path))
    entities = []
    #gets the index of the tile, object and entity layers
    for index, layer in enumerate(map_data["layers"]):
        if layer["type"] == "tilelayer":
            tile_layer_index = index
        if layer["name"] == "objects":
            object_layer_index = index

        if layer["name"] == "entities":
            entity_layer_index = index

    tile_set = TileSet(path.abspath(path.join(level_path, "..", map_data["tilesets"][0]["source"])))
    
    current_object_index = 0
    max_object_index = len(map_data["layers"][object_layer_index]["objects"]) - 1
    
    #iterate through each chunk in the map and each tile in that chunk
    for chunk_y in range(int(map_data["height"] / chunk_size)):
        for chunk_x in range(int(map_data["width"] / chunk_size)):
            chunk_rect = Rect((chunk_x*chunk_size*16), (chunk_y*chunk_size*16), (chunk_size*16), (chunk_size*16))
            tiles = []
            objects = {}
            for tile_y in range(chunk_size):
                for tile_x in range(chunk_size):
                    #calculate the x and y coordinates of the tile and then get the gid
                    x = (chunk_x * chunk_size) + (tile_x)
                    y = (chunk_y * chunk_size) + (tile_y)
                    tile_index = x + (y*map_data["width"])
                    gid = map_data["layers"][tile_layer_index]["data"][tile_index]
                    

                    if current_object_index <= max_object_index:
                        #get the current object being checked and create a rect from it
                        current_object = map_data["layers"][object_layer_index]["objects"][current_object_index]
                        current_object_rect = Rect(current_object["x"], current_object["y"], current_object["width"], current_object["height"])
                        
                        if chunk_rect.contains(current_object_rect):
                            if current_object["name"] in objects.keys():
                                objects[current_object["name"]].append(current_object_rect)
                            else:
                                objects[current_object["name"]] = [current_object_rect]
                                print(current_object["name"])
                            current_object_index += 1  
                    
                    if gid != 0:    
                        gid -= 1
                        #get the tile image from a tileset
                        image = tile_set.image.subsurface(Rect((gid % tile_set.tileset_width) * (tile_set.tile_width), (math.floor(gid / tile_set.tileset_width)) * (tile_set.tile_height), 16, 16))
                        tiles.append(Tile((x*16, y*16), image))
            
            chunk_data[(chunk_x, chunk_y)] = (tiles, objects)
    for entity in map_data["layers"][entity_layer_index]["objects"]:
        entities.append(entity)
    
    return map_data["width"], map_data["height"], entities, chunk_data




class TileSet:
    def __init__(self, tileset_path):
        with open(tileset_path) as f:
            data = json.load(f)
            self.image = image.load(path.abspath(path.join(tileset_path, "..", data["image"])))
            self.margin = data["margin"]
            self.spacing = data["spacing"]
            self.tile_width = data["tilewidth"]
            self.tile_height = data["tileheight"]
            self.tileset_width = math.floor((data["imagewidth"] - self.margin + self.spacing) / (self.tile_width + self.spacing))

class Tile:
    def __init__(self, pos, image):
        self.pos = pos
        self.image = image
        self.rect = Rect(pos, (16, 16))

class AnimatedTile(Tile):
    def __init__(self, pos, images):
        super().__init__(pos, images)
    
    def update_tile(self):
        pass



 


