import pygame

from GUI.settings import SQUARE_SIZE
from Game.Pieces.piece import Piece, is_on_board


class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        sprite_path = "../assets/{}p.png".format(self.color)
        self.sprite = pygame.transform.scale(pygame.image.load(sprite_path), (SQUARE_SIZE, SQUARE_SIZE))

    def possible_move(self, board):

        if self.color == 'w':
            change_position = -1
        else:
            change_position = 1

        move_arr = []
        capture_arr = []
        newY = self.y + change_position

        if is_on_board(self.x, newY) and board[self.x][newY] is None:
            move_arr.append([self.x, newY])

            if change_position == -1 and self.y == 6 or change_position == 1 and self.y == 1:
                newY = newY + change_position

                if board[self.x][newY] is None:
                    move_arr.append([self.x, newY])

        newY = self.y + change_position
        for i in (-1, 1):
            newX = self.x + i
            if is_on_board(newX, newY) and board[newX][newY] is not None:
                if board[newX][newY].color != self.color:
                    capture_arr.append([newX, newY])

        return move_arr, capture_arr







