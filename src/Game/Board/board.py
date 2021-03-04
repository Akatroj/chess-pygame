
class Board:
    def __init__(self):
        self.board = [[None for j in range(8)] for i in range(8)]
        print(self.board)

    def get_piece_at_position(self, x, y):
        return self.board[x][y]
