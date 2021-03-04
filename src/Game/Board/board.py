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
            [Rook.Rook('b',0,0),Knight.Knight('b',0,1),Bishop.Bishop('b',0,2),Queen.Queen('b',0,3),
                       King.King('b',0,4),Bishop.Bishop('b',0,5),Knight.Knight('b',0,6),Rook.Rook('b',0,7)],
            [Pawn.Pawn('b',1,i)for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [Pawn.Pawn('w', 6, i) for i in range(8)],
            [Rook.Rook('w', 7, 0), Knight.Knight('w', 7, 1), Bishop.Bishop('w', 7, 2), Queen.Queen('w', 7, 3),
             King.King('w', 7, 4), Bishop.Bishop('w', 7, 5), Knight.Knight('w', 7, 6), Rook.Rook('w', 7, 7)]
            ]
        print(self.board)

    def get_piece_at_position(self, x, y):
        return self.board[x][y]
