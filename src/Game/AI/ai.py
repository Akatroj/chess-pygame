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
                    capture, move = self.board.get_legal_moves(piece, True)
                    array = capture + move
                    for i in array:
                        # the prevention of the same movement 3rd time
                        if AI.repeated_move(self, piece, i):
                            continue
                        # making movements
                        old_position = piece.get_position()
                        piece_none = self.board.fake_move(piece, i)
                        # algorithm invocation alpha-beta
                        val = AI.mini_max(self, depth + 1, not is_black_turn, -10000, 10000)
                        # values for moves with a hidden bonus
                        if type(piece) == Pawn and (i[1] == 7 or i[1] == 0):  # promotion
                            val += 80
                        elif self.board.is_move_en_passant(piece, i):  # en passant
                            val += 10
                        if not is_black_turn:
                            val = - val
                        if val >= best and is_black_turn:
                            best = val
                            best_move = i
                            piece_ = piece
                        # undo moves
                        if piece_none is None:
                            self.board.fake_move(piece, old_position)
                        else:
                            self.board.fake_move(piece, old_position)
                            self.board.fake_move(piece_none, i)
        return piece_, best_move

    # mini-max algorithm with alpha-beta pruning
    def mini_max(self, depth, is_black_turn, alpha, beta):
        if self.depth == depth:
            return -AI.evaluate_board(self)
        if is_black_turn:
            arr = []
            arr_better = []
            best = -9999
            for row in self.board.board_arr:
                for piece in row:
                    if piece is not None and piece.color == 'b':
                        arr_temporary, arr_better_temporary = AI.sort_legal_move(self, piece, 7)
                        arr += arr_temporary
                        arr_better += arr_better_temporary
            arr_better.sort(key=lambda key: key[0])
            arr = arr + arr_better
            for po in range(len(arr) - 1, -1, -1):
                piece = arr[po][1]
                i = arr[po][2]
                old_position = piece.get_position()
                piece_none = self.board.fake_move(piece, i)
                val = AI.mini_max(self, depth + 1, False, alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)
                if piece_none is None:
                    self.board.fake_move(piece, old_position)
                elif piece_none is not None:
                    self.board.fake_move(piece, old_position)
                    self.board.fake_move(piece_none, i)
                if beta <= alpha:
                    return best
            return best
        else:
            arr = []
            arr_better = []
            best = 9999
            for row in self.board.board_arr:
                for piece in row:
                    if piece is not None and piece.color == 'w':
                        arr_temporary, arr_better_temporary = AI.sort_legal_move(self, piece, 0)
                        arr += arr_temporary
                        arr_better += arr_better_temporary
            arr_better.sort(key=lambda key: key[0])
            arr = arr + arr_better
            for po in range(len(arr) - 1, -1, -1):
                piece = arr[po][1]
                i = arr[po][2]
                old_position = piece.get_position()
                piece_none = self.board.fake_move(piece, i)
                val = AI.mini_max(self, depth + 1, True, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)
                if piece_none is None:
                    self.board.fake_move(piece, old_position)
                elif piece_none is not None:
                    self.board.fake_move(piece, old_position)
                    self.board.fake_move(piece_none, i)
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

    # possible moves for the piece
    def sort_legal_move(self, piece, position):
        # czemu ta funkcja ma w nazwie sort jezeli nic nie sortuje????
        arr_better = []
        arr = []
        move, capture = self.board.get_legal_moves(piece, True)
        # !unpack tuple in loop
        for i in capture:
            if self.board.board_arr[i[0]][i[1]] is not None:
                arr_better.append([10 * self.board.board_arr[i[0]][i[1]].points - piece.points, piece, i])
                if type(piece) == Pawn and (i[1] == position):
                    arr_better[-1][0] = arr_better[-1][0] + 90
            else:
                arr_better.append([piece.points, piece, i])
        for i in move:
            if type(piece) == Pawn and (i[1] == position):
                arr_better.append([90, piece, i])
            else:
                arr.append([0, piece, i])
        return arr, arr_better

