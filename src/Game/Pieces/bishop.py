import pygame

from GUI.settings import SQUARE_SIZE
from Game.Pieces.piece import Piece


class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        sprite_path = "../assets/{}b.png".format(self.color)
        self.sprite = pygame.transform.scale(pygame.image.load(sprite_path), (SQUARE_SIZE, SQUARE_SIZE))
        self.symbol = 'b'
        self.last_move = None

    def get_possible_moves(self, board):
        move_arr, capture_arr = self.bishop_move(board)
        return move_arr, capture_arr

    def bishop_move(self, board):
        offsets = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        move_arr, capture_arr = self.generate_moves(board, offsets)
        return move_arr, capture_arr
