import pygame
import math

from GUI.settings import SQUARE_SIZE
from Game.Pieces.piece import Piece, is_on_board


class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        sprite_path = "../assets/{}p.png".format(self.color)
        self.sprite = pygame.transform.scale(pygame.image.load(sprite_path), (SQUARE_SIZE, SQUARE_SIZE))
        self.symbol = ' '
        self.last_move = None



    def possible_move(self, board):

        #print("test")
        if self.color == 'w':
            change_position = -1
        else:
            change_position = 1

        move_arr = []
        capture_arr = []
        newY = self.y + change_position

        if is_on_board(self.x, newY) and board.board_arr[self.x][newY] is None:
            move_arr.append([self.x, newY])

            if change_position == -1 and self.y == 6 or change_position == 1 and self.y == 1:
                newY = newY + change_position

                if board.board_arr[self.x][newY] is None:
                    move_arr.append([self.x, newY])

        newY = self.y + change_position
        for i in (-1, 1):
            newX = self.x + i
            if is_on_board(newX, newY) and board.board_arr[newX][newY] is not None:
                if board.board_arr[newX][newY].color != self.color:
                    capture_arr.append([newX, newY])

        en_passant_arr = self.en_passant(board, change_position)
        capture_arr += en_passant_arr
        return move_arr, capture_arr

    def en_passant(self, board, change_position):

        en_passant_arr = []
        for i in (-1,1):
            if is_on_board(self.x + i, self.y) and type(board.board_arr[self.x + i][self.y]) == Pawn \
                    and board.move_arr and board.move_arr[-1][2] == self.symbol and\
                    board.move_arr[-1][4][0] == self.x + i and math.fabs(board.move_arr[-1][4][1]- board.move_arr[-1][3][1]) == 2 \
                    and board.board_arr[self.x][self.y].color != board.board_arr[self.x + i][self.y].color :
                en_passant_arr.append([self.x + i , self.y + change_position])
        return en_passant_arr





