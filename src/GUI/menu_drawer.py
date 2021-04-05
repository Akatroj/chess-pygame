import random

import pygame
import settings
from GUI.draw_utils import make_button_surface


class MenuDrawer:
    button_font_size = 25
    header_font_size = 90

    def __init__(self, window):
        self.window = window
        self.button_font = pygame.font.SysFont('Comic Sans MS', self.button_font_size)
        self.header_font = pygame.font.SysFont('Calibri', self.header_font_size, bold=True)
        self.sprite_path = 'src/assets/menu-sprite.png'
        self.sprite = None
        self.background_surface = self._make_background()

        self.singleplayer_button = None
        self.singleplayer_button_surface = None
        self.multiplayer_button = None
        self.multiplayer_button_surface = None
        self.quit_button = None
        self.quit_button_surface = None

        self.top = self._make_top()

        self.sprite_offset_x = 0
        self.sprite_offset_y = 0
        self.x_multiplier = 1
        self.y_multiplier = 1

        self._make_buttons()
        self._make_sprite()

    def draw(self):
        self.set_sprite_offset()
        self.window.blit(self.background_surface, (0,0))
        self.window.blit(self.quit_button_surface, (0, 0))
        self.window.blit(self.singleplayer_button_surface, (0, 0))
        self.window.blit(self.multiplayer_button_surface, (0, 0))
        self.window.blit(self.sprite, (self.sprite_offset_x, self.sprite_offset_y))
        self.window.blit(self.top, (0, 0))


        pygame.display.update()


    def _make_buttons(self):
        x = 50
        width = settings.WINDOW_WIDTH // 4
        height = settings.WINDOW_HEIGHT // 8
        # y = settings.WINDOW_HEIGHT - height - 80

        y = settings.WINDOW_HEIGHT // 2 - 80
        self.singleplayer_button = pygame.Rect(x, y, width, height)
        self.singleplayer_button_surface = make_button_surface(self.button_font, self.singleplayer_button, "Singleplayer")

        y += 1.5*height
        self.multiplayer_button = pygame.Rect(x, y, width, height)
        self.multiplayer_button_surface = make_button_surface(self.button_font, self.multiplayer_button, "Multiplayer")

        y += 1.5*height
        self.quit_button = pygame.Rect(x, y, width, height)
        self.quit_button_surface = make_button_surface(self.button_font, self.quit_button, "Quit")

    def _make_sprite(self):
        result = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA, 32)
        sprite = pygame.image.load(self.sprite_path)
        sprite = pygame.transform.smoothscale(sprite, (175, 300))

        result.blit(sprite, (settings.WINDOW_WIDTH - 175 - 50, settings.WINDOW_HEIGHT // 2 - 80))
        self.sprite = result
        pass

    def _make_top(self):
        result = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA, 32)
        text_surface = self.header_font.render("Chess", True, pygame.Color('#FFFFFF'))
        text_rect = text_surface.get_rect()

        pawn_sprite_size = text_rect.height + 10

        top_surface = pygame.Surface(((text_rect.width + pawn_sprite_size), pawn_sprite_size), pygame.SRCALPHA, 32)
        top_rect = top_surface.get_rect()
        top_rect.center = (settings.WINDOW_WIDTH // 2, 90)
        text_rect.center = (((top_rect.width + pawn_sprite_size) // 2), top_rect.height // 2 + 12)

        pawn = pygame.transform.smoothscale(pygame.image.load("src/assets/wp.png"), (pawn_sprite_size, pawn_sprite_size))

        top_surface.blit(pawn, (0, 0))
        top_surface.blit(text_surface, text_rect)
        result.blit(top_surface, top_rect)

        return result

    def _make_background(self):

        blue1 = pygame.Color('#00A2E8')
        blue3= pygame.Color('#1E90FF')
        blue4 = pygame.Color('#00BFFF')
        royalblue = pygame.Color('#4169E1')
        blue2 = pygame.Color(2, 200, 210)
        green = pygame.Color(115, 230, 98)
        orange = pygame.Color(255, 115, 55)

        # result = pygame.Surface((2, 2))  # tiny! 2x2 bitmap
        # pygame.draw.line(result, blue1, (0, 1), (1, 0))  # left colour line
        # pygame.draw.line(result, green, (0, 0), (1, 1))  # right colour line
        #


        #
        result = pygame.Surface((4,4))
        # temp = colored_rectangle_border(0, 0, 3, 3, blue1, 1)
        # for (color, side) in temp:
        #     pygame.draw.rect(result, color, side)
        # pygame.draw.rect(result, green, pygame.Rect(1, 1, 1, 1))

        result.fill(blue2)
        pygame.draw.rect(result, blue1, pygame.Rect(1, 1, 2,2))

        result = pygame.transform.smoothscale(result, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))  # stretch!

        return result

    def set_sprite_offset(self):
        self.sprite_offset_x += self.x_multiplier * random.randrange(0, 3) /2
        self.sprite_offset_y += self.y_multiplier * random.randrange(0, 2) /2
        if abs(self.sprite_offset_x) > 15 or abs(self.sprite_offset_y) > 7:
            self.x_multiplier *= -1
            self.y_multiplier *= -1
