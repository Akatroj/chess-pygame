import pygame

HEIGHT = 800
WIDTH = 800
FPS = 60

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#BOARD = pygame.image.load('../assets/chessboard.png')


def drawWindow():
    WINDOW.blit(BOARD, (0,0))
    pygame.display.update()

def drawBoard(board):
    pawn = pygame.transform.scale(pygame.image.load('../assets/bp.png'), (SQUARE_WIDTH, SQUARE_WIDTH))
    for i in range(len(board.board)):
        for j in range(len(board.board[0])):
            if (i + j) % 2 == 0:
                color = pygame.Color(240, 217, 181)
            else:
                color = pygame.Color(148, 111, 81)
            x = i * SQUARE_WIDTH
            y = j * SQUARE_WIDTH
            temp = pygame.Rect(x, y, SQUARE_WIDTH, SQUARE_WIDTH)
            pygame.draw.rect(WINDOW, color, temp)
            WINDOW.blit(pawn, (x, y))


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
    print("jebanie")


