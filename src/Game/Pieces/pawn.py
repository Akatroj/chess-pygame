from Game.Pieces.piece import Piece, is_on_board

import Game.AI.position_points as pp
import GUI.piece_sprites as ps


class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.symbol = ' '
        self.sprite = ps.piece_sprites(self)
        self.last_move = None

        self.points = 10 if self.color == 'w' else -10
        self.position_points = pp.get_position_points(self)

    def get_possible_moves(self, board):
        if self.color == 'w':
            position_change = -1
        else:
            position_change = 1

        move_arr = []
        capture_arr = []
        new_y = self.y + position_change

        # normal moves
        if is_on_board(self.x, new_y) and board.board_arr[self.x][new_y] is None:
            move_arr.append([self.x, new_y])
            if self.last_move is None:
                new_y = new_y + position_change
                if board.board_arr[self.x][new_y] is None:
                    move_arr.append([self.x, new_y])

        # captures
        new_y = self.y + position_change
        for i in (-1, 1):
            new_x = self.x + i
            if is_on_board(new_x, new_y) and board.board_arr[new_x][new_y] is not None:
                if board.board_arr[new_x][new_y].color != self.color:
                    capture_arr.append([new_x, new_y])

        en_passant_arr = self.en_passant(board, position_change)
        capture_arr += en_passant_arr
        return move_arr, capture_arr

    def en_passant(self, board, position_change):
        en_passant_arr = []
        for i in (-1, 1):
            if is_on_board(self.x + i, self.y):
                possible_target = board.board_arr[self.x + i][self.y]
                if type(possible_target) == Pawn and self.color != possible_target.color:
                    last_move = board.last_move()
                    if last_move is not None and last_move[2] == self.symbol and last_move[4][0] == self.x + i \
                            and abs(last_move[4][1] - last_move[3][1]) == 2:
                        en_passant_arr.append([self.x + i, self.y + position_change])

        return en_passant_arr





