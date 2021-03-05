import pygame


class Piece:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

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

    def help_move(self, change_x , change_y, board ):
        move_arr = []
        capture_arr = []
        newX = self.x + change_x
        newY = self.y + change_y

        while is_on_board(newX, newY) and board[newX][newY] == None:
            move_arr.append([newX, newY])
            newX += change_x
            newY += change_y
        if is_on_board(newX, newY) and board[newX][newY].color != self.color:
            capture_arr.append([newX, newY])

        return move_arr, capture_arr


def is_on_board(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7

