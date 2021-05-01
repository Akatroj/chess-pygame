from Game.Pieces.piece import Piece
import Game.AI.position_points as pp
import GUI.piece_sprites as ps


class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.symbol = 'r'
        self.sprite = ps.piece_sprites(self)
        self.last_move = None
        self.points = 50 if self.color == 'w' else -50
        self.position_points = pp.get_position_points(self)

    def get_possible_moves(self, board):
        move_arr, capture_arr = self.rook_move(board)
        return move_arr, capture_arr

    def rook_move(self, board):
        offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))
        move_arr, capture_arr = self.generate_moves(board, offsets)
        return move_arr, capture_arr



