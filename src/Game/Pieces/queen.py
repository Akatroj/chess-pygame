import pygame

from GUI.settings import SQUARE_SIZE
from Game.Pieces.bishop import Bishop
from Game.Pieces.piece import Piece
from Game.Pieces.rook import Rook


class Queen(Rook, Bishop, Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        sprite_path = "../assets/{}q.png".format(self.color)
        self.sprite = pygame.transform.scale(pygame.image.load(sprite_path), (SQUARE_SIZE, SQUARE_SIZE))
        self.symbol = 'q'
        self.last_move = None

    def get_possible_moves(self, board):
        move_arr_rook, capture_arr_rook = self.rook_move(board)
        move_arr_bishop, capture_arr_bishop = self.bishop_move(board)
        move_arr = move_arr_bishop + move_arr_rook
        capture_arr = capture_arr_bishop + capture_arr_rook

        return move_arr, capture_arr
