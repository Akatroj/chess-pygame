import Game.AI.position_points as pp
from Game.Pieces.pawn import Pawn


class AI:
    def __init__(self, board, depth):
        self.depth = depth
        self.board = board

    def mini_max_first_move(self, depth):
        best_move = []
        best = -9999
        piece_ = None
        # checking which player has a move
        if self.board.current_player == 'b':
            is_black_turn = True
        else:
            is_black_turn = False
        if not is_black_turn:
            best = -best
        # checking possible player moves
        # first move performs separately, to know the best starting position
        for row in self.board.board_arr:
            for piece in row:
                if piece is not None and piece.color == self.board.current_player:
                    move, capture = self.board.get_legal_moves(piece, True)
                    array = capture + move
                    for x, y in array:
                        # prevent making the same move 3 times
                        if self.repeated_move(piece, [x, y]):
                            continue
                        # making moves
                        old_position = piece.get_position()
                        piece_none = self.board.fake_move(piece, [x, y])
                        # algorithm invocation alpha-beta
                        val = self.mini_max(depth + 1, not is_black_turn, -10000, 10000)
                        # values for moves with a hidden bonus
                        if type(piece) == Pawn and (y == 7 or y == 0):  # promotion
                            val += 80
                        elif self.board.is_move_en_passant(piece, [x, y]):  # en passant
                            val += 10
                        if not is_black_turn:
                            val = - val
                        if val >= best and is_black_turn:
                            best = val
                            best_move = [x, y]
                            piece_ = piece
                        # undo moves
                        if piece_none is None:
                            self.board.fake_move(piece, old_position)
                        else:
                            self.board.fake_move(piece, old_position)
                            self.board.fake_move(piece_none, [x, y])
        return piece_, best_move

    # mini-max algorithm with alpha-beta pruning
    def mini_max(self, depth, is_black_turn, alpha, beta):
        if self.depth == depth:
            return -self.evaluate_board()
        if is_black_turn:
            best = -9999
            arr = self.possible_move('b', 7)
            for po in range(len(arr) - 1, -1, -1):
                piece = arr[po][1]
                i = arr[po][2]
                old_position = piece.get_position()
                piece_none = self.board.fake_move(piece, i)
                val = self.mini_max(depth + 1, False, alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)
                self.revert_move(piece_none, piece, old_position, i)
                if beta <= alpha:
                    return best
            return best
        else:
            best = 9999
            arr = self.possible_move('w', 0)
            for po in range(len(arr) - 1, -1, -1):
                piece = arr[po][1]
                i = arr[po][2]
                old_position = piece.get_position()
                piece_none = self.board.fake_move(piece, i)
                val = self.mini_max(depth + 1, True, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)
                self.revert_move(piece_none, piece, old_position, i)
                if beta <= alpha:
                    return best
            return best

    # total point value on self.board
    def evaluate_board(self):
        result = 0
        for row in self.board.board_arr:
            for piece in row:
                if piece is not None:
                    arr = pp.get_position_points(piece)
                    r = piece.points + arr[piece.y][piece.x]
                    result += r
        return result

    # prevent making the same move 3 times
    def repeated_move(self, piece, i):
        if self.board.turn_number > 9 and self.board.move_arr[-2][3] == i == self.board.move_arr[-6][3] == \
                self.board.move_arr[-4][4] == self.board.move_arr[-8][4] \
                and self.board.move_arr[-2][5] == self.board.move_arr[-4][5] == piece == self.board.move_arr[-6][5] == \
                self.board.move_arr[-8][5]:
            return True
        return False

    # add higher priority to good moves (pawn promotion, pawn capture)
    def move_priority(self, piece, position):
        arr_better = []
        arr = []
        move_arr, capture_arr = self.board.get_legal_moves(piece, True)
        for x, y in capture_arr:
            if self.board.board_arr[x][y] is not None:
                arr_better.append([10 * self.board.board_arr[x][y].points - piece.points, piece, [x, y]])
                if type(piece) == Pawn and (y == position):
                    arr_better[-1][0] = arr_better[-1][0] + 90
            else:
                arr_better.append([piece.points, piece, [x, y]])
        for i in move_arr:
            if type(piece) == Pawn and (i == position):
                arr_better.append([90, piece, i])
            else:
                arr.append([0, piece, i])
        return arr, arr_better

    def possible_move(self, color, position):
        arr = []
        arr_better = []
        for row in self.board.board_arr:
            for piece in row:
                if piece is not None and piece.color == color:
                    arr_temporary, arr_better_temporary = self.move_priority(piece, position)
                    arr += arr_temporary
                    arr_better += arr_better_temporary
        arr_better.sort(key=lambda key: key[0])
        arr = arr + arr_better
        return arr

    def revert_move(self, piece_none, piece, old_position, i):
        if piece_none is None:
            self.board.fake_move(piece, old_position)
        elif piece_none is not None:
            self.board.fake_move(piece, old_position)
            self.board.fake_move(piece_none, i)
