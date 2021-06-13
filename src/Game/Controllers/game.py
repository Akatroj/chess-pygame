import os
import time

import pygame
import settings
from Game.utils import is_on_board, LEFT_CLICK, RIGHT_CLICK


from Game.Controllers.gameover import Gameover
from GUI.gamedrawer import GameDrawer
from Game.AI.ai import AI
from Game.Board.board import Board


class Game:
    def __init__(self, window, ai_level=settings.AI_LEVEL):
        self.window = window
        self.board = Board()
        self.game_drawer = GameDrawer(self.board, self.window)
        self.selected = None
        self.selected_move_arr = None
        self.selected_capture_arr = None
        self.selected_piece_original_position = None
        self.dragged = None
        self.mouse_pos = None
        self.converted_pos = None
        self.not_gameover = True
        self.can_be_dropped = False
        self.move_sound = pygame.mixer.Sound(os.path.join(settings.ASSET_FOLDER, 'sounds/Move.ogg'))
        self.capture_sound = pygame.mixer.Sound(os.path.join(settings.ASSET_FOLDER, 'sounds/Capture.ogg'))

        self.clock = pygame.time.Clock()
        self.opponent = AI(self.board, ai_level)

    def start_multiplayer(self):
        pygame.event.clear()
        while self.not_gameover:
            self.redraw()

            self.clock.tick(settings.FPS)
            self.__set_mouse_pos()

            self.__handle_events()

            self.__check_if_game_over()

    def start_against_ai(self):
        pygame.event.clear()
        while self.not_gameover:
            self.redraw()

            self.clock.tick(settings.FPS)
            self.__set_mouse_pos()

            self.__automatic_move('b')
            self.__check_if_game_over()

            if self.not_gameover:
                self.__handle_events()
                self.__check_if_game_over()

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.not_gameover = False
                pygame.event.post(pygame.event.Event(pygame.QUIT))  # propagate event up
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    self.__handle_lmb_pressed()
                elif event.button == RIGHT_CLICK:
                    self.__drop_piece()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT_CLICK:
                self.__handle_lmb_up()
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.board.resign()
                self.not_gameover = False

    def redraw(self):
        self.game_drawer.draw(self.selected, self.selected_move_arr, self.selected_capture_arr,
                              self.dragged, self.mouse_pos, self.board.piece_to_promote)

    def __set_mouse_pos(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.converted_pos = [a // settings.SQUARE_SIZE for a in self.mouse_pos]

    def __handle_lmb_pressed(self):
        # clicking during promotion
        if self.board.piece_to_promote is not None and self.converted_pos[0] == self.board.piece_to_promote.x:
            choice = self.converted_pos[1]
            if choice <= 3 and self.board.current_player == 'w':
                self.board.promote_pawn(self.board.piece_to_promote, choice)
                self.redraw()
            elif choice > 3 and self.board.current_player == 'b':
                self.board.promote_pawn(self.board.piece_to_promote, 7 - choice)
                self.redraw()
        else:
            if is_on_board(*self.converted_pos):
                piece = self.board.get_piece_at_position(self.converted_pos)
                if self.selected == piece:
                    self.dragged = piece
                else:
                    self.__select_piece(piece)

    def __handle_lmb_up(self):
        self.dragged = None  # Stop dragging the piece upon releasing mouse button
        if self.selected is not None:
            # Try to move selected piece to target location
            if self.selected_piece_original_position != self.converted_pos:
                if self.converted_pos in self.selected_capture_arr:
                    self.board.move(self.selected, self.converted_pos)
                    self.capture_sound.play()
                elif self.converted_pos in self.selected_move_arr:
                    self.board.move(self.selected, self.converted_pos)
                    self.move_sound.play()
                self.__drop_piece()  # drop after attempting move, regardless of outcome

            elif self.can_be_dropped:  # protects from dropping instantly after selecting
                self.__drop_piece()
            else:
                self.can_be_dropped = True

    def __select_piece(self, piece):
        if piece is not None and piece.color == self.board.current_player:
            self.selected = self.dragged = piece
            self.selected_move_arr, self.selected_capture_arr = self.board.get_legal_moves(self.selected)
            self.selected_piece_original_position = self.converted_pos
            self.can_be_dropped = False

    def __drop_piece(self):
        self.selected = None
        self.dragged = None
        self.selected_move_arr = None
        self.selected_capture_arr = None
        self.piece_original_position = None

    def __automatic_move(self, player):
        if self.board.current_player == player:
            piece_, best_move = self.opponent.mini_max_first_move(0)

            if self.board.get_piece_at_position(best_move) is not None:
                self.capture_sound.play()
            else:
                self.move_sound.play()

            self.board.move(piece_, best_move)
            if self.board.piece_to_promote is not None:
                self.board.promote_pawn(self.board.piece_to_promote, 0)

    def __check_if_game_over(self):
        if self.board.winner is not None:
            self.not_gameover = False
            self.redraw()
            game_over = Gameover(self.window, self.board.winner)
            time.sleep(2)
            game_over.start()
