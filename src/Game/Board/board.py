import Game.Pieces.bishop as Bishop
import Game.Pieces.king as King
import Game.Pieces.pawn as Pawn
import Game.Pieces.knight as Knight
import Game.Pieces.queen as Queen
import Game.Pieces.rook as Rook
import Game.Pieces.piece as Piece


class Board:
    def __init__(self):
        self.board = [
             [Rook.Rook('b', 0, 0), Pawn.Pawn('b', 0, 1), None, None, None, None, Pawn.Pawn('w', 0, 6), Rook.Rook('w', 0, 7)],
             [Knight.Knight('b', 1, 0), Pawn.Pawn('b', 1, 1), None, None, None, None, Pawn.Pawn('w', 1, 6), Knight.Knight('w', 1, 7)],
             [Bishop.Bishop('b', 2, 0), Pawn.Pawn('b', 2, 1), None, None, None, None, Pawn.Pawn('w', 2, 6), Bishop.Bishop('w', 2, 7)],
             [Queen.Queen('b', 3, 0), Pawn.Pawn('b', 3, 1), None, None, None, None, Pawn.Pawn('w', 3, 6), Queen.Queen('w', 3, 7)],
             [King.King('b', 4, 0), Pawn.Pawn('b', 4, 1), None, None, None, None, Pawn.Pawn('w', 4, 6), King.King('w', 4, 7)],
             [Bishop.Bishop('b', 5, 0), Pawn.Pawn('b', 5, 1), None, None, None, None, Pawn.Pawn('w', 5, 6), Bishop.Bishop('w', 5, 7)],
             [Knight.Knight('b', 6, 0), Pawn.Pawn('b', 6, 1), None, None, None, None, Pawn.Pawn('w', 6, 6), Knight.Knight('w', 6, 7)],
             [Rook.Rook('b', 7, 0), Pawn.Pawn('b', 7, 1), None, None, None, None, Pawn.Pawn('w', 7, 6), Rook.Rook('w', 7, 7)]
            ]
        # self.arr = ['w', 'b']
        self.current_player = 'w'

    def get_piece_at_position(self, pos):
        return self.board[pos[0]][pos[1]]

    def move_piece(self, piece, position):

        move_arr, capture_arr = piece.possible_move(self.board)
        legal_move = move_arr + capture_arr
        #if self.arr[0] == piece.color:
        if self.current_player == piece.color:
            for i in legal_move:
                if position == i:
                    self.board[piece.x][piece.y] = None
                    piece.x = position[0]
                    piece.y = position[1]
                    self.board[position[0]][position[1]] = piece
                    #self.arr.reverse()
                    self.current_player = 'w' if self.current_player == 'b' else 'b'
                    break
