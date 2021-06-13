import pygame
import settings
from Game.Controllers.game import Game
from GUI.menu_drawer import MenuDrawer
from Game.utils import LEFT_CLICK


class Menu:
    def __init__(self, window):
        self.window = window
        self.menu_drawer = MenuDrawer(self.window)

        self.singleplayer_button = self.menu_drawer.singleplayer_button
        self.multiplayer_button = self.menu_drawer.multiplayer_button
        self.quit_button = self.menu_drawer.quit_button

        self.running = True

        self.clock = pygame.time.Clock()

    def start(self):
        while self.running:
            self.menu_drawer.draw()

            self.clock.tick(settings.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT_CLICK:
                    self.__handle_lmb_up()

    def __handle_lmb_up(self):
        game = Game(self.window)
        mouse_pos = pygame.mouse.get_pos()
        if self.singleplayer_button.collidepoint(mouse_pos):
            game.start_against_ai()
        if self.multiplayer_button.collidepoint(mouse_pos):
            game.start_multiplayer()
        if self.quit_button.collidepoint(mouse_pos):
            self.running = False


