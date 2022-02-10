import pygame
from os import path

WIDTH, HEIGHT = 720, 480
DS_WIDTH , DS_HEIGHT = 360, 240
FPS = 60
CHUNK_SIZE = 3
GAME_FOLDER = path.dirname(__file__)
ASSETS_FOLDER = path.join(GAME_FOLDER, "assets")
MAP_FOLDER = path.join(ASSETS_FOLDER, "maps")
PLAYER_FOLDER = path.join(ASSETS_FOLDER, "player")