import Game.Pieces.bishop as Bishop
import Game.Pieces.king as King
import Game.Pieces.pawn as Pawn
import Game.Pieces.knight as Knight
import Game.Pieces.queen as Queen
import Game.Pieces.rook as Rook
import Game.Pieces.piece as Piece
import math
import time

from GUI import settings


class Board:
    def __init__(self):
        self.current_player = 'w'
        self.move_arr = []
        self.move_counter = 1
        self.last_position_check = 0
        self.white_king = King.King('w', 4, 7)
        self.black_king = King.King('b', 4, 0)
        self.board_arr = [
             [Rook.Rook('b', 0, 0), Pawn.Pawn('b', 0, 1), None, None, None, None, Pawn.Pawn('w', 0, 6), Rook.Rook('w', 0, 7)],
             [Knight.Knight('b', 1, 0), Pawn.Pawn('b', 1, 1), None, None, None, None, Pawn.Pawn('w', 1, 6), Knight.Knight('w', 1, 7)],
             [Bishop.Bishop('b', 2, 0), Pawn.Pawn('b', 2, 1), None, None, None, None, Pawn.Pawn('w', 2, 6), Bishop.Bishop('w', 2, 7)],
             [Queen.Queen('b', 3, 0), Pawn.Pawn('b', 3, 1), None, None, None, None, Pawn.Pawn('w', 3, 6), Queen.Queen('w', 3, 7)],
             [self.black_king, Pawn.Pawn('b', 4, 1), None, None, None, None, Pawn.Pawn('w', 4, 6), self.white_king],
             [Bishop.Bishop('b', 5, 0), Pawn.Pawn('b', 5, 1), None, None, None, None, Pawn.Pawn('w', 5, 6), Bishop.Bishop('w', 5, 7)],
             [Knight.Knight('b', 6, 0), Pawn.Pawn('b', 6, 1), None, None, None, None, Pawn.Pawn('w', 6, 6), Knight.Knight('w', 6, 7)],
             [Rook.Rook('b', 7, 0), Pawn.Pawn('b', 7, 1), None, None, None, None, Pawn.Pawn('w', 7, 6), Rook.Rook('w', 7, 7)]
            ]
        self.piece_to_promote = None

    def get_piece_at_position(self, pos):
        return self.board_arr[pos[0]][pos[1]]

    def legal(self, piece):
        move_arr, capture_arr = piece.possible_move(self)
        move_arr_legal = self.legal_help_def(piece, move_arr)
        capture_arr_legal = self.legal_help_def(piece, capture_arr)
        return move_arr_legal, capture_arr_legal

    def legal_help_def(self, piece, arr):
        result = []
        for i in range(len(arr)):
            result_bool = Board.next_step(self, piece, arr[i])
            if not result_bool:
                result.append(arr[i])
        return result

    def move_piece(self, piece, position):

        move_made = False

        move_arr, capture_arr = self.legal(piece)
        legal_move = move_arr + capture_arr
        if self.current_player == piece.color:
            for i in legal_move:
                if position == i:
                    if type(piece) == King.King and self.castle_help(piece, position):
                        if position[0] == 2 or position[0] == 6:
                            if position[0] == 2:
                                rook = self.board_arr[0][piece.y]
                                self.move_temp(piece, position)
                                self.board_arr[0][rook.y] = None
                                rook.x = 3
                                move_made = True
                            else:
                                rook = self.board_arr[7][piece.y]
                                self.move_temp(piece, position)
                                self.board_arr[7][rook.y] = None
                                rook.x = 5
                                move_made = True

                            rook.last_move = self.move_counter - 1
                            self.board_arr[rook.x][rook.y] = rook
                            move_made = True
                            self.move_arr[-1][2] = piece.symbol + " C"
                            break
                    elif type(piece) == Pawn.Pawn and self.en_passant_help(piece, position):
                            self.board_arr[position[0]][piece.y] = None
                            self.move_temp(piece, position)
                            self.move_arr[-1][2] = piece.symbol + " EP"
                            move_made = True
                            break
                    else:
                        self.move_temp(piece, position)
                        move_made = True
                        break
        if type(piece) == Pawn.Pawn and (piece.y == 0 or piece.y == 7):
            self.piece_to_promote = piece
            move_made = False
        if move_made:
            self.next_turn()

    def move_temp(self, piece, position):
        self.board_arr[piece.x][piece.y] = None
        old_x = piece.x
        old_y = piece.y
        piece.x = position[0]
        piece.y = position[1]
        piece.last_move = self.move_counter
        self.board_arr[position[0]][position[1]] = piece
        self.move_arr.append([self.move_counter, piece.color, piece.symbol, (old_x, old_y), (piece.x, piece.y)])
        self.move_counter += 1

    def convert_position(self, x, y):
        rank = abs(y-8)
        file = chr(ord('a') + x)
        return file + str(rank)

    def last_move(self):
        return None if not self.move_arr else self.move_arr[-1]

    def castle_help(self, piece, position):
        return math.fabs(piece.x - position[0]) > 1

    def en_passant_help(self, piece,position ):
        en_passant_arr =[]
        for i in (-1 ,1):
            en_passant_arr.append(Pawn.Pawn.en_passant(piece, self, i))
        for i in en_passant_arr:
            if i == [position]:
                return True
        return False

    def checkmate(self, color):
        checkmate_arr = []
        move_arr = []
        capture_arr = []
        for i in range(len(self.board_arr)):
            for j in range(len(self.board_arr[0])):
                if self.board_arr[i][j] != None and self.board_arr[i][j].color != color:
                    move_arr, capture_arr = self.board_arr[i][j].possible_move(self)
                    checkmate_arr = checkmate_arr + capture_arr
        return checkmate_arr

    def next_step(self, piece, new_position):
        change_position = new_position
        old_position = piece.position()
        temp = self.board_arr[change_position[0]][change_position[1]]
        self.board_arr[old_position[0]][old_position[1]] = None
        self.board_arr[change_position[0]][change_position[1]] = piece
        self.change_position_piece(piece, change_position)
        if type(piece) == Pawn.Pawn and change_position[0]-old_position[0]!=0:
            temp2 = self.board_arr[change_position[0]][old_position[1]]
            self.board_arr[change_position[0]][old_position[1]] = None

        checkmate_arr = self.checkmate(self.current_player)
        for i in range(len(checkmate_arr)):
            if (self.white_king.color == piece.color and self.white_king.position() == checkmate_arr[i]) or \
                    (self.black_king.color == piece.color and self.black_king.position() == checkmate_arr[i]):
                self.old_position_piece(piece , temp , old_position, change_position)
                if type(piece) == Pawn.Pawn and change_position[0]-old_position[0]!=0:
                    self.board_arr[change_position[0]][old_position[1]] = temp2
                return True
        self.old_position_piece(piece , temp , old_position, change_position)
        if type(piece) == Pawn.Pawn and change_position[0] - old_position[0] != 0:
            self.board_arr[change_position[0]][old_position[1]] = temp2
        return False

    def old_position_piece(self , piece , temp , old_position, change_position):
        self.board_arr[old_position[0]][old_position[1]] = piece
        self.board_arr[change_position[0]][change_position[1]] = temp
        self.change_position_piece(piece, old_position)

    def change_position_piece(self, piece, position):
        piece.x = position[0]
        piece.y = position[1]

    def next_turn(self):
        self.current_player = 'w' if self.current_player == 'b' else 'b'

    def promote_pawn(self, pawn, choice):
        if choice == 0:
            self.board_arr[pawn.x][pawn.y] = Queen.Queen(pawn.color, pawn.x, pawn.y)
        elif choice == 1:
            self.board_arr[pawn.x][pawn.y] = Knight.Knight(pawn.color, pawn.x, pawn.y)
        elif choice == 2:
            self.board_arr[pawn.x][pawn.y] = Rook.Rook(pawn.color, pawn.x, pawn.y)
        elif choice == 3:
            self.board_arr[pawn.x][pawn.y] = Bishop.Bishop(pawn.color, pawn.x, pawn.y)

        self.next_turn()
        self.piece_to_promote = None


