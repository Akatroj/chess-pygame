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



    def possible_move(self, board):

        move_arr = []
        capture_arr = []
        move_arr, capture_arr = Piece.bishop_move(self, board.board_arr)

        return move_arr, capture_arr
