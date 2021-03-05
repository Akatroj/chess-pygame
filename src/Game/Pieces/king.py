import pygame
from GUI.settings import SQUARE_SIZE
from Game.Pieces.piece import Piece, is_on_board


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        sprite_path = "../assets/{}k.png".format(self.color)
        self.sprite = pygame.transform.scale(pygame.image.load(sprite_path), (SQUARE_SIZE, SQUARE_SIZE))

    def possible_move(self, board):

        move_arr = []
        capture_arr = []

        for i in (-1, 0, 1):
            for j in ( -1, 0, 1):
                newX = self.x + i
                newY = self.y + j
                if (i != 0 or j != 0) and is_on_board(newX, newY):
                    if board[newX][newY] is None:
                        move_arr.append([newX, newY])
                    else:
                        if board[newX][newY].color != self.color:
                            capture_arr.append([newX, newY])

        return move_arr, capture_arr

