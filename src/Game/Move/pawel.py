import pygame
pygame.init()

HEIGHT = 800
WIDTH = 800

screen=pygame.display.set_mode((WIDTH, HEIGHT))


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if(__name__ == "__main__"):
    main()



pygame.quit()