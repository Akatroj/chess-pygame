import pygame
from GUI.settings import SQUARE_SIZE
from Game.Pieces.piece import Piece, is_on_board


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        sprite_path = "../assets/{}k.png".format(self.color)
        self.sprite = pygame.transform.scale(pygame.image.load(sprite_path), (SQUARE_SIZE, SQUARE_SIZE))
        self.symbol = 'k'
        self.last_move = None

    def possible_move(self, board):

        move_arr = []
        capture_arr = []
        move_arr_castle = King.castle(self, board.board_arr)

        for i in (-1, 0, 1):
            for j in ( -1, 0, 1):
                newX = self.x + i
                newY = self.y + j
                if (i != 0 or j != 0) and is_on_board(newX, newY):
                    if board.board_arr[newX][newY] is None:
                        move_arr.append([newX, newY])
                    else:
                        if board.board_arr[newX][newY].color != self.color:
                            capture_arr.append([newX, newY])

        move_arr += move_arr_castle
        return move_arr, capture_arr

    def castle(self , board_arr):

        move_arr_castle = []

        if board_arr[0][self.y] != None and self.last_move == None and board_arr[0][self.y].last_move == None and board_arr[1][self.y] == None and board_arr[2][self.y] == None and board_arr[3][self.y] == None:
            move_arr_castle.append([2,self.y])

        if board_arr[7][self.y] != None and self.last_move == None and board_arr[7][self.y].last_move == None and board_arr[5][self.y] == None and board_arr[6][self.y] == None:
            move_arr_castle.append([6,self.y])

        return move_arr_castle