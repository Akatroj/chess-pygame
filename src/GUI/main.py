import pygame
import Game.Board.board as Board


WINDOW_HEIGHT = 600
WINDOW_WIDTH = 900
SQUARE_WIDTH = int(WINDOW_HEIGHT / 8)


FPS = 1

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#BOARD = pygame.image.load('../assets/chessboard.png')


def drawWindow(board):
    drawBoard(board)
    pygame.display.update()

def drawBoard(board):
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
            piece = board.get_piece_at_position(j, i)
            if piece is not None:
                #print(piece.spritePath)
                sprite = pygame.transform.scale(pygame.image.load(piece.spritePath), (SQUARE_WIDTH, SQUARE_WIDTH))
                WINDOW.blit(sprite, (x, y))


def main():
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    board = Board.Board()

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)

        drawWindow(board)

    pygame.quit()

if(__name__ == "__main__"):
    main()
    print("jebanie")


