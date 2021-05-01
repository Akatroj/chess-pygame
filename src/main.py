import pygame

import settings
from Game.Controllers.menu import Menu


def main():
    pygame.init()
    pygame.font.init()
    window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption('Chess')
    icon = pygame.transform.smoothscale(pygame.image.load(settings.ICON_PATH), (settings.ICON_SIZE, settings.ICON_SIZE))
    pygame.display.set_icon(icon)
    menu = Menu(window)
    menu.start()
    pygame.quit()


if __name__ == "__main__":
    # Paweł 1 : 0 Mariusz
    # Pierwszą gre wygrał Paweł D
    main()


