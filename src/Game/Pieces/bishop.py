from Game.Pieces.piece import Piece

import GUI.piece_sprites as ps
import Game.AI.position_points as pp


class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.symbol = 'b'
        self.sprite = ps.piece_sprites(self)
        self.last_move = None

        self.points = 30 if self.color == 'w' else -30
        self.position_points = pp.get_position_points(self)

    def get_possible_moves(self, board):
        move_arr, capture_arr = self.bishop_move(board)
        return move_arr, capture_arr

    def bishop_move(self, board):
        offsets = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        move_arr, capture_arr = self.generate_moves(board, offsets)
        return move_arr, capture_arr
