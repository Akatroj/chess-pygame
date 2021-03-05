import pygame
import settings
import Game.Board.board as Board

from draw import draw

board = Board.Board()


def main():
    selected = None
    dragged = None
    mouse_pos = None
    board_pos = None
    piece_original_position = None
    running = True
    pygame.init()
    clock = pygame.time.Clock()
    draw(board, selected, dragged, mouse_pos)
    while running:
        clock.tick(settings.FPS)
        mouse_pos = pygame.mouse.get_pos()
        board_pos = [mouse_pos[0]//settings.SQUARE_SIZE, mouse_pos[1]//settings.SQUARE_SIZE]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Highlight and start dragging piece upon clicking
                if selected is None:
                    piece = board.get_piece_at_position(board_pos)
                    if piece is not None and piece.color == board.current_player:
                        selected = dragged = piece
                        piece_original_position = board_pos
                    # Drop the piece upon clicking on it again
                elif selected is not None and board_pos == piece_original_position:
                    selected = None

                draw(board, selected, dragged, mouse_pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                dragged = None  # Stop dragging the piece upon releasing mouse button
                if selected is not None:
                    # Try to move selected piece to target location
                    if piece_original_position != board_pos:
                        board.move_piece(selected, board_pos)
                        selected = None

                draw(board, selected, dragged, mouse_pos)

            elif event.type == pygame.MOUSEMOTION:
                # Drop the piece upon dragging it out of bounds
                if mouse_pos[0] > settings.BOARD_WIDTH or mouse_pos[1] > settings.BOARD_HEIGHT:
                    dragged = None
                    selected = None
                draw(board, selected, dragged, mouse_pos)

    pygame.quit()


if __name__ == "__main__":
    main()


