import pygame
import math

from GUI.settings import SQUARE_SIZE
from Game.Pieces.piece import Piece, is_on_board


class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        sprite_path = "../assets/{}n.png".format(self.color)
        self.sprite = pygame.transform.scale(pygame.image.load(sprite_path), (SQUARE_SIZE, SQUARE_SIZE))

    def possible_move(self, board):

        move_arr = []
        capture_arr = []

        for i in (-2, -1, 1, 2):
            for j in (-2, -1, 1, 2):
                newX = self.x + i
                newY = self.y + j
                if math.fabs(i) != math.fabs(j) and is_on_board(newX, newY):
                    if board[newX][newY] is None:
                        move_arr.append([newX, newY])
                    else:
                        if board[newX][newY].color != self.color:
                            capture_arr.append([newX, newY])

        return move_arr, capture_arr

