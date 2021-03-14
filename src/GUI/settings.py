import pygame

# General
FPS = 60
WINDOW_HEIGHT = 900
WINDOW_WIDTH = 900
BOARD_HEIGHT = BOARD_WIDTH = min(WINDOW_WIDTH, WINDOW_HEIGHT)
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_HEIGHT//BOARD_SIZE
ICON_PATH = '../assets/wp.png'
ICON_SIZE = 32
FONT_SIZE = int(SQUARE_SIZE * 0.27)
RANK_COORDINATE_MARGIN = SQUARE_SIZE * 0.075
FILE_COORDINATE_MARGIN = SQUARE_SIZE * 0.15

# Visual
BOARD_LIGHT_SQUARE_COLOR = pygame.Color('#946F51')
BOARD_DARK_SQUARE_COLOR = pygame.Color('#F0D9B5')

MOVE_COLOR = pygame.Color('#00FF00')
CAPTURE_COLOR = pygame.Color('#FF0000')

LINE_COLOR = pygame.Color('#000000')
LINE_THICKNESS = 2

SELECTED_PIECE_COLOR = pygame.Color('#2CBA41')
HIGHLIGHTED_BORDER_THICKNESS = 5

POSITION_PREV_COLOR = pygame.Color('#FFFF3D')
POSITION_CURR_COLOR = pygame.Color('#FFD700')
