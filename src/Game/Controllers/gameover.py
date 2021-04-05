import time

import pygame
import settings
from GUI.gameover_drawer import GameoverDrawer
from GUI.menu_drawer import MenuDrawer
from Game.utils import LEFT_CLICK, RIGHT_CLICK


class Gameover:
    def __init__(self, window, winner):
        self.window = window
        self.winner = winner

        if winner == 'b':
            self.gameover_drawer = GameoverDrawer(self.window, 'Black won!')
        elif winner == 'w':
            self.gameover_drawer = GameoverDrawer(self.window, 'White won!')
        else:
            self.gameover_drawer = GameoverDrawer(self.window, 'Draw!')

        self.running = True

        self.clock = pygame.time.Clock()

    def start(self):
        pygame.event.clear()
        while self.running:
            self.gameover_drawer.draw()
            self.clock.tick(settings.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.event.post(pygame.event.Event(pygame.QUIT))  # propagate event up
                elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT_CLICK:
                    self.running = False
