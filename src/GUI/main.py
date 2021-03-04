import pygame

HEIGHT = 800
WIDTH = 800
FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BOARD = pygame.image.load('../../assets/chessboard.png')


def drawWindow():
    WINDOW.blit(BOARD, (0,0))
    pygame.display.update()

def main():
    pygame.init()
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        drawWindow()

    pygame.quit()

if(__name__ == "__main__"):
    main()