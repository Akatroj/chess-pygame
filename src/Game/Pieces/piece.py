import pygame
import copy

class Piece:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.last_move = None

    def move_piece(self, board, arr):

        move_arr = []
        capture_arr = []

        for i in arr:
            help_arr_move, help_arr_capture = Piece.help_move(self, i[0], i[1], board)
            move_arr = move_arr + help_arr_move
            capture_arr = capture_arr + help_arr_capture

        return move_arr, capture_arr

    def rook_move(self, board):

        move_arr = []
        capture_arr = []
        arr = ((-1, 0), (1, 0), (0, -1), (0, 1))
        move_arr, capture_arr = Piece.move_piece(self, board, arr)
        return move_arr, capture_arr

    def bishop_move(self, board):

        move_arr = []
        capture_arr = []
        arr = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        move_arr, capture_arr = Piece.move_piece(self, board, arr)
        return move_arr, capture_arr

    def help_move(self, change_x , change_y, board):
        move_arr = []
        capture_arr = []
        newX = self.x + change_x
        newY = self.y + change_y

        while is_on_board(newX, newY) and board.board_arr[newX][newY] is None:
            move_arr.append([newX, newY])
            newX += change_x
            newY += change_y
        if is_on_board(newX, newY) and board.board_arr[newX][newY] is not None and board.board_arr[newX][newY].color != self.color:
            capture_arr.append([newX, newY])
        return move_arr, capture_arr

    def position(self):
        return [self.x,self.y]

    def next_step(self, board, newX , newY):
        old_x = self.x
        old_y = self.y
        board.board_arr[self.x][self.y] = None
        self.x= newX
        self.y= newY
        board.board_arr[newX][newY] = self
        checkmate_arr = board.checkmate(board.arr[1])


        for i in range(len(checkmate_arr)):
            if( board.white_king.color == self.color ):
                if board.white_king.position() == checkmate_arr[i]:
                    board.board_arr[old_x][old_y] = self
                    board.board_arr[newX][newY] = None
                    self.x = old_x
                    self.y = old_y
                    return True
            if ( board.black_king.color == self.color ):
                if board.black_king.position() == checkmate_arr[i]:
                    board.board_arr[old_x][old_y] = self
                    board.board_arr[newX][newY] = None
                    self.x = old_x
                    self.y = old_y
                    return True
        board.board_arr[newX][newY] = None
        board.board_arr[old_x][old_y] = self
        self.x = old_x
        self.y = old_y
        return False


def is_on_board(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7

