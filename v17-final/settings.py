### >>> Settings:
# AKA - Global Variables.

import pygame as pg

import os

# Window Size:
WIDTH = 832
HEIGHT = 832
# Window Title:
TITLE = "Snake But Good"

# Frames per Second: 
FPS = 30

# Quick Colors:
BLACK = (0, 0, 0)
WHITE = (250, 251, 226)
RED = (198, 62, 54)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 0, 255)

SNAKEGREEN = (129, 198, 69)
WALLBLACK = (33, 27, 48)

# Tile / Grid Sizing (in px):
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Score (init at 0):
SCORE = 0

### >>> Set Up Asset Access:

# Find the directory where this game is located:
# On my computer, it'll return something like desktop/python-game/v#
vers_game_folder = os.path.dirname(__file__)
# Also, grab its parent, due to the way I'm organizing things:
# On my computer, it'll return something like desktop/python-game
main_game_folder = os.path.abspath(os.path.join(vers_game_folder, os.pardir))

# Use those to find our sprites folder:
# On my computer, it'll return something like desktop/python-game/sprites
sprites_folder = os.path.join(main_game_folder, "sprites")
# And the font folder:
font_folder = os.path.join(main_game_folder, "font")




