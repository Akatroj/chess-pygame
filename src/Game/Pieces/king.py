import pygame
from GUI.settings import SQUARE_SIZE
from Game.Pieces.piece import Piece, is_on_board


def can_castle(rook):
    return (rook is not None) and (rook.last_move is None)


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        sprite_path = "../assets/{}k.png".format(self.color)
        self.sprite = pygame.transform.scale(pygame.image.load(sprite_path), (SQUARE_SIZE, SQUARE_SIZE))
        self.symbol = 'k'
        self.last_move = None

    def get_possible_moves(self, board):
        move_arr = []
        capture_arr = []
        castle_move_array = self.castle(board.board_arr)

        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                new_x = self.x + i
                new_y = self.y + j
                if (i != 0 or j != 0) and is_on_board(new_x, new_y):
                    if board.board_arr[new_x][new_y] is None:
                        move_arr.append([new_x, new_y])
                    else:
                        if board.board_arr[new_x][new_y].color != self.color:
                            capture_arr.append([new_x, new_y])

        move_arr += castle_move_array
        return move_arr, capture_arr

    def castle(self, board_arr):
        castle_move_arr = []
        left_rook = board_arr[0][self.y]
        right_rook = board_arr[7][self.y]

        if self.last_move is None:
            if can_castle(left_rook) and (board_arr[1][self.y] is None and board_arr[2][self.y] is None
                                          and board_arr[3][self.y] is None):
                castle_move_arr.append([2, self.y])
            if can_castle(right_rook) and (board_arr[5][self.y] is None and board_arr[6][self.y] is None):
                castle_move_arr.append([6, self.y])

        return castle_move_arr
