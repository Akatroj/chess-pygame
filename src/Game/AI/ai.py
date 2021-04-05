import Game.AI.position_points as pp
import Game.Pieces.pawn as Pawn


class AI:
    def __init__(self, board, depth):
        self.depth = depth
        self.board = board

    def mini_max_first_move(self, depth):
        best_move = []
        best = -9999
        piece_ = None
        #checking which player has a move
        if self.board.current_player == 'b':
            player = True
        else:
            player = False
        if not player:
            best = -best
        #checking possible player moves
        #first move performs separately, to know the best starting position
        for row in self.board.board_arr:
            for piece in row:
                if piece is not None and piece.color == self.board.current_player:
                    capture, move = self.board.get_legal_moves(piece, True)
                    array = capture + move
                    for i in array:
                        #the prevention of the same movement 3rd time
                        if AI.repeated_move(self, piece, i):
                            continue
                        #making movements
                        old_position = piece.get_position()
                        piece_none = self.board.fake_move(piece, i)
                        #algorithm invocation alpha-betha
                        val = AI.mini_max(self, depth + 1, not player, -1000, 1000)
                        #values for movements with a hidden bonus
                        if type(piece) == Pawn.Pawn and (i[1] == 7 or i[1] == 0):
                            val += 80
                        if self.board._is_move_en_passant(piece, i):
                            val += 10
                        if not player:
                            val = - val
                        if val >= best and player:
                            best = val
                            best_move = i
                            piece_ = piece
                        #undo movements
                        if piece_none is None:
                            self.board.fake_move(piece, old_position)
                        else:
                            self.board.fake_move(piece, old_position)
                            self.board.fake_move(piece_none, i)
        return piece_, best_move

    #mini-max algoithm in version alpha-betha
    def mini_max(self, depth, player, alpha, beta):
        if self.depth == depth:
            return -AI.situation_on_self(self)
        if player:
            arr = []
            arr_better = []
            best = - 9999
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

    #point value on the self.board
    def situation_on_self(self):
        result = 0
        for row in self.board.board_arr:
            for piece in row:
                if piece is not None:
                    arr = pp.get_position_points(piece)
                    r = piece.points + arr[piece.y][piece.x]
                    result += r
        return result

    # the prevention of the same movement 3rd time
    def repeated_move(self, piece, i):
        if self.board.turn_number > 9 and self.board.move_arr[-2][3] == i == self.board.move_arr[-6][3] == \
                self.board.move_arr[-4][4] == self.board.move_arr[-8][4] \
                and self.board.move_arr[-2][5] == self.board.move_arr[-4][5] == piece == self.board.move_arr[-6][5] == \
                self.board.move_arr[-8][5]:
            return True
        return False

    #possible moves for the piece
    def sort_legal_move(self, piece, position):
        arr_better = []
        arr = []
        move, capture = self.board.get_legal_moves(piece, True)
        for i in capture:
            if self.board.board_arr[i[0]][i[1]] is not None:
                arr_better.append([10 * self.board.board_arr[i[0]][i[1]].points - piece.points, piece, i])
                if type(piece) == Pawn.Pawn and (i[1] == position):
                    arr_better[-1][0] = arr_better[-1][0] + 90
            else:
                arr_better.append([piece.points, piece, i])
        for i in move:
            if type(piece) == Pawn.Pawn and (i[1] == position):
                arr_better.append([90, piece, i])
            else:
                arr.append([0, piece, i])
        return arr, arr_better

