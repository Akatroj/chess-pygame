import Game.Pieces.bishop as Bishop
import Game.Pieces.king as King
import Game.Pieces.pawn as Pawn
import Game.Pieces.knight as Knight
import Game.Pieces.queen as Queen
import Game.Pieces.rook as Rook
import Game.Pieces.piece as Piece
import math

from GUI import settings


class Board:
    def __init__(self):
        self.board_arr = [
             [Rook.Rook('b', 0, 0), Pawn.Pawn('b', 0, 1), None, None, None, None, Pawn.Pawn('w', 0, 6), Rook.Rook('w', 0, 7)],
             [Knight.Knight('b', 1, 0), Pawn.Pawn('b', 1, 1), None, None, None, None, Pawn.Pawn('w', 1, 6), Knight.Knight('w', 1, 7)],
             [Bishop.Bishop('b', 2, 0), Pawn.Pawn('b', 2, 1), None, None, None, None, Pawn.Pawn('w', 2, 6), Bishop.Bishop('w', 2, 7)],
             [Queen.Queen('b', 3, 0), Pawn.Pawn('b', 3, 1), None, None, None, None, Pawn.Pawn('w', 3, 6), Queen.Queen('w', 3, 7)],
             [King.King('b', 4, 0), Pawn.Pawn('b', 4, 1), None, None, None, None, Pawn.Pawn('w', 4, 6), King.King('w', 4, 7)],
             [Bishop.Bishop('b', 5, 0), Pawn.Pawn('b', 5, 1), None, None, None, None, Pawn.Pawn('w', 5, 6), Bishop.Bishop('w', 5, 7)],
             [Knight.Knight('b', 6, 0), Pawn.Pawn('b', 6, 1), None, None, None, None, Pawn.Pawn('w', 6, 6), Knight.Knight('w', 6, 7)],
             [Rook.Rook('b', 7, 0), Pawn.Pawn('b', 7, 1), None, None, None, None, Pawn.Pawn('w', 7, 6), Rook.Rook('w', 7, 7)]
            ]
        self.arr = ['w', 'b']
        # self.current_player = 'w'
        self.move_arr = []
        self.move_counter = 1

    def get_piece_at_position(self, pos):
        return self.board_arr[pos[0]][pos[1]]

    def move_piece(self, piece, position):

        move_arr, capture_arr = piece.possible_move(self)
        legal_move = move_arr + capture_arr
        if self.arr[0] == piece.color:
        # if self.current_player == piece.color:
            for i in legal_move:
                if position == i:
                    if type(piece) == King.King and Board.castle_help(self, piece, position):
                        if position[0] == 2 or position[0] == 6:
                            if position[0] == 2:
                                print("dluga")
                                rook = self.board_arr[0][piece.y]
                                self.move_temp(piece, position)
                                self.board_arr[0][rook.y] = None
                                rook.x = 3
                            else:
                                print("krutka")
                                rook = self.board_arr[7][piece.y]
                                self.move_temp(piece, position)
                                self.board_arr[7][rook.y] = None
                                rook.x = 5
                            rook.last_move = self.move_counter - 1
                            self.board_arr[rook.x][rook.y] = rook
                            self.move_arr[-1][2] = piece.symbol + " C"
                            print(self.move_arr[-1])
                            break
                    elif self.en_passant_help(piece,position) and type(piece) == Pawn.Pawn:
                        self.board_arr[position[0]][piece.y] = None
                        self.move_temp(piece, position)
                        self.move_arr[-1][2] = piece.symbol + " EP"
                        print(self.move_arr[-1])
                        break
                    else:
                        self.move_temp(piece, position)
                        print(self.move_arr[-1])
                        break


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
        self.arr.reverse()
        # self.current_player = 'w' if self.current_player == 'b' else 'b'

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

