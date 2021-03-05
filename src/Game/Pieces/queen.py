import pygame

from GUI.settings import SQUARE_SIZE
from Game.Pieces.piece import Piece


class Queen(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        sprite_path = "../assets/{}q.png".format(self.color)
        self.sprite = pygame.transform.scale(pygame.image.load(sprite_path), (SQUARE_SIZE, SQUARE_SIZE))

    def possible_move(self, board):

        move_arr_rook = []
        capture_arr_rook = []
        move_arr_bishop = []
        capture_arr_bishop = []
        move_arr_rook, capture_arr_rook = Piece.rook_move(self, board)
        move_arr_bishop, capture_arr_bishop = Piece.bishop_move(self, board)
        move_arr = move_arr_bishop + move_arr_rook
        capture_arr = capture_arr_bishop + capture_arr_rook


        return move_arr, capture_arr
