import os
import random

import pygame
import settings
from GUI.draw_utils import make_button_surface, make_gradient_background
import GUI.piece_sprites as piece_sprites

BACKGROUND_COLOR_OUTER = pygame.Color('#02C8D2')
BACKGROUND_COLOR_INNER = pygame.Color('#00A2E8')
BUTTON_COLOR = pygame.Color('#2BB14C')


class MenuDrawer:
    button_font_size = 25
    header_font_size = 90

    def __init__(self, window):
        self.window = window
        self.button_font = pygame.font.SysFont('Comic Sans MS', self.button_font_size)
        self.header_font = pygame.font.SysFont('Calibri', self.header_font_size, bold=True)
        self.sprite_path = os.path.join(settings.ASSET_FOLDER, 'menu-sprite.png')
        self.sprite = None
        self.background_surface = make_gradient_background(BACKGROUND_COLOR_OUTER, BACKGROUND_COLOR_INNER)

        self.singleplayer_button = None
        self.singleplayer_button_surface = None
        self.multiplayer_button = None
        self.multiplayer_button_surface = None
        self.quit_button = None
        self.quit_button_surface = None

        self.top = self.__make_top()

        self.sprite_offset_x = 0
        self.sprite_offset_y = 0
        self.x_multiplier = 1
        self.y_multiplier = 1

        self.__make_buttons()
        self.__make_sprite()

    def draw(self):
        self.set_sprite_offset()
        self.window.blit(self.background_surface, (0, 0))
        self.window.blit(self.quit_button_surface, (0, 0))
        self.window.blit(self.singleplayer_button_surface, (0, 0))
        self.window.blit(self.multiplayer_button_surface, (0, 0))
        self.window.blit(self.sprite, (self.sprite_offset_x, self.sprite_offset_y))
        self.window.blit(self.top, (0, 0))

        pygame.display.update()

    def __make_buttons(self):
        x = 50
        width = settings.WINDOW_WIDTH // 4
        height = settings.WINDOW_HEIGHT // 8
        # y = settings.WINDOW_HEIGHT - height - 80

        y = settings.WINDOW_HEIGHT // 2 - 80
        self.singleplayer_button = pygame.Rect(x, y, width, height)
        self.singleplayer_button_surface = \
            make_button_surface(self.button_font, self.singleplayer_button, "Singleplayer", BUTTON_COLOR)

        y += 1.5*height
        self.multiplayer_button = pygame.Rect(x, y, width, height)
        self.multiplayer_button_surface = \
            make_button_surface(self.button_font, self.multiplayer_button, "Multiplayer", BUTTON_COLOR)

        y += 1.5*height
        self.quit_button = pygame.Rect(x, y, width, height)
        self.quit_button_surface = \
            make_button_surface(self.button_font, self.quit_button, "Quit", BUTTON_COLOR)

    def __make_sprite(self):
        result = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA, 32)
        sprite = pygame.image.load(self.sprite_path)
        sprite = pygame.transform.smoothscale(sprite, (175, 300))

        result.blit(sprite, (settings.WINDOW_WIDTH - 175 - 50, settings.WINDOW_HEIGHT // 2 - 80))
        self.sprite = result
        pass

    def __make_top(self):
        result = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA, 32)
        text_surface = self.header_font.render("Chess", True, pygame.Color('#FFFFFF'))
        text_rect = text_surface.get_rect()

        pawn_sprite_size = text_rect.height + 10

        top_surface = pygame.Surface(((text_rect.width + pawn_sprite_size), pawn_sprite_size), pygame.SRCALPHA, 32)
        top_rect = top_surface.get_rect()
        top_rect.center = (settings.WINDOW_WIDTH // 2, 90)
        text_rect.center = (((top_rect.width + pawn_sprite_size) // 2), top_rect.height // 2 + 12)

        pawn = pygame.transform.smoothscale(piece_sprites.w_pawn, (pawn_sprite_size, pawn_sprite_size))

        top_surface.blit(pawn, (0, 0))
        top_surface.blit(text_surface, text_rect)
        result.blit(top_surface, top_rect)

        return result

    def set_sprite_offset(self):
        # bouncing:

        if random.choice((True, False)):
            self.sprite_offset_x += self.x_multiplier
            if (self.sprite_offset_x > 15 and self.x_multiplier > 0) \
                    or (self.sprite_offset_x < -15 and self.x_multiplier < 0):
                self.x_multiplier *= -1
        if random.choice((True, False)):
            self.sprite_offset_y += self.y_multiplier
            if (self.sprite_offset_y > 7 and self.y_multiplier > 0) \
                    or (self.sprite_offset_y < -7 and self.y_multiplier < 0):
                self.y_multiplier *= -1

        # # parabola:
        # self.sprite_offset_x += self.x_multiplier * 0.6
        # self.sprite_offset_y = -(self.sprite_offset_x ** 2) * 13/225
        # if abs(self.sprite_offset_x) > 15:
        #     self.x_multiplier *= -1

