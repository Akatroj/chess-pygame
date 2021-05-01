import os

from settings import SQUARE_SIZE, ASSET_FOLDER
import pygame

w_rook = pygame.image.load(os.path.join(ASSET_FOLDER, 'wr.png'))
b_rook = pygame.image.load(os.path.join(ASSET_FOLDER, 'br.png'))
w_queen = pygame.image.load(os.path.join(ASSET_FOLDER, 'wq.png'))
b_queen = pygame.image.load(os.path.join(ASSET_FOLDER, 'bq.png'))
w_bishop = pygame.image.load(os.path.join(ASSET_FOLDER, 'wb.png'))
b_bishop = pygame.image.load(os.path.join(ASSET_FOLDER, 'bb.png'))
w_knight = pygame.image.load(os.path.join(ASSET_FOLDER, 'wn.png'))
b_knight = pygame.image.load(os.path.join(ASSET_FOLDER, 'bn.png'))
w_king = pygame.image.load(os.path.join(ASSET_FOLDER, 'wk.png'))
b_king = pygame.image.load(os.path.join(ASSET_FOLDER, 'bk.png'))
w_pawn = pygame.image.load(os.path.join(ASSET_FOLDER, 'wp.png'))
b_pawn = pygame.image.load(os.path.join(ASSET_FOLDER, 'bp.png'))


def piece_sprites(piece):
    if piece.symbol == 'r':
        if piece.color == 'w':
            image = w_rook
        else:
            image = b_rook

    elif piece.symbol == 'q':
        if piece.color == 'w':
            image = w_queen
        else:
            image = b_queen

    elif piece.symbol == 'b':
        if piece.color == 'w':
            image = w_bishop
        else:
            image = b_bishop

    elif piece.symbol == 'n':
        if piece.color == 'w':
            image = w_knight
        else:
            image = b_knight

    elif piece.symbol == 'k':
        if piece.color == 'w':
            image = w_king
        else:
            image = b_king

    else:
        if piece.color == 'w':
            image = w_pawn
        else:
            image = b_pawn

    return pygame.transform.smoothscale(image, (SQUARE_SIZE, SQUARE_SIZE))
