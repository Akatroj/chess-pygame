import pygame

from GUI.settings import SQUARE_SIZE
from Game.Pieces.piece import Piece


class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        sprite_path = "../assets/{}r.png".format(self.color)
        self.sprite = pygame.transform.scale(pygame.image.load(sprite_path), (SQUARE_SIZE, SQUARE_SIZE))
        self.symbol = 'r'
        self.last_move = None

    def get_possible_moves(self, board):
        move_arr, capture_arr = self.rook_move(board)
        return move_arr, capture_arr

    def rook_move(self, board):
        offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))
        move_arr, capture_arr = self.generate_moves(board, offsets)
        return move_arr, capture_arr



