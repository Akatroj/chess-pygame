import math
from Game.Pieces.bishop import Bishop
from Game.Pieces.king import King
from Game.Pieces.knight import Knight
from Game.Pieces.pawn import Pawn
from Game.Pieces.piece import Piece
from Game.Pieces.queen import Queen
from Game.Pieces.rook import Rook


def convert_position(x, y):
    rank = abs(y-8)
    file = chr(ord('a') + x)
    return file + str(rank)


def is_move_castling(king, position):
    return type(king) == King and abs(king.x - position[0]) > 1


class Board:
    def __init__(self):
        self.current_player = 'w'
        self.move_arr = []
        self.turn_number = 1
        self.last_position_check = 0
        self.white_king = King('w', 4, 7)
        self.black_king = King('b', 4, 0)
        self.piece_to_promote = None
        self.check_white_king = False
        self.check_black_king = False
        self.board_arr: list[[Piece]] = [
             [Rook('b', 0, 0),   Pawn('b', 0, 1), None, None, None, None, Pawn('w', 0, 6), Rook('w', 0, 7)],
             [Knight('b', 1, 0), Pawn('b', 1, 1), None, None, None, None, Pawn('w', 1, 6), Knight('w', 1, 7)],
             [Bishop('b', 2, 0), Pawn('b', 2, 1), None, None, None, None, Pawn('w', 2, 6), Bishop('w', 2, 7)],
             [Queen('b', 3, 0),  Pawn('b', 3, 1), None, None, None, None, Pawn('w', 3, 6), Queen('w', 3, 7)],
             [self.black_king,   Pawn('b', 4, 1), None, None, None, None, Pawn('w', 4, 6), self.white_king],
             [Bishop('b', 5, 0), Pawn('b', 5, 1), None, None, None, None, Pawn('w', 5, 6), Bishop('w', 5, 7)],
             [Knight('b', 6, 0), Pawn('b', 6, 1), None, None, None, None, Pawn('w', 6, 6), Knight('w', 6, 7)],
             [Rook('b', 7, 0),   Pawn('b', 7, 1), None, None, None, None, Pawn('w', 7, 6), Rook('w', 7, 7)]
            ]
        self.winner = None

    def get_piece_at_position(self, pos):
        return self.board_arr[pos[0]][pos[1]]

    def next_turn(self):
        self.current_player = 'w' if self.current_player == 'b' else 'b'
        self.is_checkmate()

    def resign(self):
        self.winner = 'w' if self.current_player == 'b' else 'b'

    def last_move(self):
        return None if not self.move_arr else self.move_arr[-1]

    def last_move_positions(self):
        if not self.move_arr:
            return []
        old_position = self.move_arr[-1][3]
        new_position = self.move_arr[-1][4]
        return old_position, new_position

    def get_legal_moves(self, piece, ai=False):
        move_arr, capture_arr = piece.get_possible_moves(self)
        move_arr_legal = self.__get_legal_array(piece, move_arr, ai)
        capture_arr_legal = self.__get_legal_array(piece, capture_arr, ai)
        return move_arr_legal, capture_arr_legal

    def __get_legal_array(self, piece, move_arr, ai):
        result = []
        for move in move_arr:
            if self.__validate_move(piece, move, ai):
                result.append(move)
        return result

    def move(self, piece, position):
        if is_move_castling(piece, position):
            self.castle_king(piece, position)
        elif self.is_move_en_passant(piece, position):
            self.board_arr[position[0]][piece.y] = None
            self.__move_piece(piece, position)
            self.move_arr[-1][2] = piece.symbol + " EP"
        else:
            self.__move_piece(piece, position)

        # dont start next turn if promotion in progress
        if type(piece) == Pawn and (piece.y == 0 or piece.y == 7):
            self.piece_to_promote = piece
        else:
            self.next_turn()
        self.check()

    def __move_piece(self, piece, position):
        self.board_arr[piece.x][piece.y] = None
        old_x = piece.x
        old_y = piece.y
        piece.change_position(position)
        piece.last_move = self.turn_number
        self.board_arr[position[0]][position[1]] = piece
        self.move_arr.append([self.turn_number, piece.color, piece.symbol, [old_x, old_y], [piece.x, piece.y], piece])
        self.turn_number += 1
        self.check_black_king = False
        self.check_white_king = False

    def __get_opponent_captures(self, color):
        captures = []
        for row in self.board_arr:
            for piece in row:
                if piece is not None and piece.color != color:
                    move_arr, capture_arr = piece.get_possible_moves(self)
                    captures = captures + capture_arr
        return captures

    def __validate_move(self, piece, new_position, ai):
        # tries making the move and checks all possible enemy responses to it
        # returns False if enemy can respond by capturing your king
        # this function makes moves on the actual game board and reverts them after it's finished
        new_x = new_position[0]
        new_y = new_position[1]
        old_position = [old_x, old_y] = piece.get_position()
        captured_en_passant = None

        # copy whatever was at this position
        captured_piece = self.board_arr[new_x][new_y]

        # if the move is en passant, copy the captured piece
        if self.is_move_en_passant(piece, new_position):
            captured_en_passant = self.board_arr[new_x][old_y]
            self.board_arr[new_x][old_y] = None

        # simulate a move
        self.board_arr[old_x][old_y] = None
        self.board_arr[new_x][new_y] = piece
        piece.change_position(new_position)

        opponent_captures = self.__get_opponent_captures(self.current_player)

        # if king is trying to castle through attacked position or through check
        if is_move_castling(piece, old_position):
            if math.fabs(new_x - old_x) == 2 and not self.__validate_move(piece, [5, new_y], ai) \
                    or math.fabs(new_x - old_x) == 3 and not self.__validate_move(piece, [3, new_y], ai) \
                    or self.is_in_check(piece):
                self.__revert_move(piece, captured_piece, old_position, new_position)
                return False

        for capture_position in opponent_captures:
            # if king can get captured in response
            if (self.white_king.get_position() == capture_position and piece.color == 'w') \
                    or (self.black_king.get_position() == capture_position and piece.color == 'b'):
                self.__revert_move(piece, captured_piece, old_position, new_position)

                # revert en passant
                if captured_en_passant is not None:
                    self.board_arr[new_x][old_y] = captured_en_passant
                return False

        self.__revert_move(piece, captured_piece, old_position, new_position)
        if captured_en_passant is not None:
            self.board_arr[new_x][old_y] = captured_en_passant
        return True

    def __revert_move(self, piece, captured_piece, old_position, current_position):
        self.board_arr[old_position[0]][old_position[1]] = piece
        self.board_arr[current_position[0]][current_position[1]] = captured_piece
        piece.change_position(old_position)

    def promote_pawn(self, pawn, choice):

        if choice == 0:
            self.board_arr[pawn.x][pawn.y] = Queen(pawn.color, pawn.x, pawn.y)
        elif choice == 1:
            self.board_arr[pawn.x][pawn.y] = Knight(pawn.color, pawn.x, pawn.y)
        elif choice == 2:
            self.board_arr[pawn.x][pawn.y] = Rook(pawn.color, pawn.x, pawn.y)
        elif choice == 3:
            self.board_arr[pawn.x][pawn.y] = Bishop(pawn.color, pawn.x, pawn.y)

        self.next_turn()
        self.check()
        self.piece_to_promote = None

    def castle_king(self, king, position):
        if position[0] == 2 or position[0] == 6:
            if position[0] == 2:
                rook = self.board_arr[0][king.y]
                self.__move_piece(king, position)
                self.board_arr[0][rook.y] = None
                rook.x = 3
            else:
                rook = self.board_arr[7][king.y]
                self.__move_piece(king, position)
                self.board_arr[7][rook.y] = None
                rook.x = 5

            rook.last_move = self.turn_number - 1
            self.board_arr[rook.x][rook.y] = rook
            self.move_arr[-1][2] = king.symbol + " C"

    def is_checkmate(self):
        for row in self.board_arr:
            for piece in row:
                if piece is not None and piece.color == self.current_player:
                    move_arr, capture_arr = self.get_legal_moves(piece)
                    if move_arr or capture_arr:
                        return False
        self.check()
        if self.check_white_king:
            self.winner = 'b'
        elif self.check_black_king:
            self.winner = 'w'
        else:
            self.winner = 'Draw'
        return True

    def check(self):
        if self.current_player == 'w':
            king = self.white_king
        else:
            king = self.black_king
        for row in self.board_arr:
            for piece in row:
                if piece is not None and piece.color != self.current_player:
                    move_arr, capture_arr = self.get_legal_moves(piece)
                    if king.get_position() in capture_arr:
                        if self.current_player == 'b':
                            self.check_black_king = True
                            return
                        else:
                            self.check_white_king = True
                            return

    def is_move_en_passant(self, pawn, new_position):
        if type(pawn) != Pawn:
            return False

        if pawn.color == 'w':
            en_passant_arr = pawn.en_passant(self, -1)
        else:
            en_passant_arr = pawn.en_passant(self, 1)

        return new_position in en_passant_arr

    def fake_move(self, piece, position_new):
        if self.board_arr[position_new[0]] [position_new[1]] is None:
            self.board_arr[piece.x][piece.y] = None
            piece.x = position_new[0]
            piece.y = position_new[1]
            self.board_arr[position_new[0]][position_new[1]] = piece
            return None
        else:
            piece_old = self.board_arr[position_new[0]][position_new[1]]

            self.board_arr[piece.x][piece.y] = None
            piece.x = position_new[0]
            piece.y = position_new[1]
            self.board_arr[position_new[0]][position_new[1]] = piece
            return piece_old

    def is_in_check(self, piece):
        return type(piece) == King and \
               ((piece.color == 'w' and self.check_white_king) or (piece.color == 'b' and self.check_black_king))
