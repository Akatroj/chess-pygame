import pygame


# returns a list of 4 pairs (color, border) - one for each side of rectangle
import settings


def colored_rectangle_border(x_start, y_start, width, height, color, thickness):
    result = []

    y_end = y_start + height - thickness
    x_end = x_start + width - thickness

    result.append((color, pygame.Rect(x_start, y_start, width, thickness)))  # left
    result.append((color, pygame.Rect(x_start, y_start, thickness, height)))  # text_surface
    result.append((color, pygame.Rect(x_start, y_end, width, thickness)))  # bottom
    result.append((color, pygame.Rect(x_end, y_start, thickness, height)))  # right

    return result


def make_button_surface(font, button, text):
    result = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA, 32)
    pygame.draw.rect(result, settings.MENU_BUTTON_COLOR, button)
    text_surface = font.render(text, True, pygame.Color('#000000'))
    text_rect = text_surface.get_rect()
    text_rect.center = (button.centerx, button.centery)
    result.blit(text_surface, text_rect)

    temp = colored_rectangle_border(button.x, button.y, button.width, button.height, pygame.Color('Black'), 2)

    for (color, border) in temp:
        pygame.draw.rect(result, color, border)

    return result


def make_gradient_background(color1, color2):
    result = pygame.Surface((4,4))

    result.fill(color1)
    pygame.draw.rect(result, color2, pygame.Rect(1, 1, 2, 2))
    result = pygame.transform.smoothscale(result, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))  # stretch!

    return result

