from settings import SQUARE_SIZE
import pygame

w_root = pygame.image.load("src/assets/wr.png")
b_root = pygame.image.load("src/assets/br.png")
w_queen = pygame.image.load("src/assets/wq.png")
b_gueen = pygame.image.load("src/assets/bq.png")
w_bishop = pygame.image.load("src/assets/wb.png")
b_biskop = pygame.image.load("src/assets/bb.png")
w_knight = pygame.image.load("src/assets/wn.png")
b_knight = pygame.image.load("src/assets/bn.png")
w_king = pygame.image.load("src/assets/wk.png")
b_king = pygame.image.load("src/assets/bk.png")
w_pawn = pygame.image.load("src/assets/wp.png")
b_pawn = pygame.image.load("src/assets/bp.png")


def piece_sprites(piece):
    if piece.symbol == 'r':
        if piece.color == 'w':
            image = w_root
        else:
            image = b_root

    elif piece.symbol == 'q':
        if piece.color == 'w':
            image = w_queen
        else:
            image = b_gueen

    elif piece.symbol == 'b':
        if piece.color == 'w':
            image = w_bishop
        else:
            image = b_biskop

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
