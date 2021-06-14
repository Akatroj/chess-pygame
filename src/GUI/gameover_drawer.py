import pygame

import settings

from GUI.draw_utils import make_gradient_background

BACKGROUND_COLOR_OUTER = pygame.Color('#02C8D2')
BACKGROUND_COLOR_INNER = pygame.Color('#00A2E8')
TEXT_COLOR = pygame.Color('#FFFFFF')
FONT_SIZE = 90


class GameoverDrawer:
    def __init__(self, window, top_text):
        self.window = window
        self.top_text = top_text

        self.font = pygame.font.SysFont('Calibri', FONT_SIZE, bold=True)

        self.background_surface = make_gradient_background(BACKGROUND_COLOR_OUTER, BACKGROUND_COLOR_INNER)

        self.text_surface = self.__make_text_surface()

    def draw(self):
        self.window.blit(self.background_surface, (0, 0))
        self.window.blit(self.text_surface, (0, 0))

        pygame.display.update()

    def __make_text_surface(self):
        result = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA, 32)
        text_surface = self.font.render(self.top_text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = result.get_rect().center
        result.blit(text_surface, text_rect)
        return result
