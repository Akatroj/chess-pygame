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
    draw(board, selected, dragged, mouse_pos, board.piece_to_promote)
    while running:
        clock.tick(settings.FPS)
        mouse_pos = pygame.mouse.get_pos()
        board_pos = [mouse_pos[0]//settings.SQUARE_SIZE, mouse_pos[1]//settings.SQUARE_SIZE]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if board.piece_to_promote is not None:
                    if board_pos[0] == board.piece_to_promote.x:
                        choice = board_pos[1]
                        if choice < 3 and board.current_player == 'w':
                            choice = choice
                            board.promote_pawn(board.piece_to_promote, choice)
                        elif choice > 3 and board.current_player == 'b':
                            choice = 7 - choice
                            board.promote_pawn(board.piece_to_promote, choice)

                else:
                    # print(board_arr.convert_position(board_pos[0], board_pos[1]))
                    # Highlight and start dragging piece upon clicking
                    if selected is None:
                        if board_pos[0] >= settings.BOARD_SIZE or board_pos[1] >= settings.BOARD_SIZE:
                            piece = None
                        else:
                            piece = board.get_piece_at_position(board_pos)
                        # if piece is not None and piece.color == board_arr.current_player:
                        if piece is not None and piece.color == board.current_player:
                            selected = dragged = piece
                            piece_original_position = board_pos
                        # Drop the piece upon clicking on it again
                    elif selected is not None and board_pos == piece_original_position:
                        selected = None

                draw(board, selected, dragged, mouse_pos, board.piece_to_promote)

            elif event.type == pygame.MOUSEBUTTONUP:
                dragged = None  # Stop dragging the piece upon releasing mouse button
                if selected is not None:
                    # Try to move selected piece to target location
                    if piece_original_position != board_pos:
                        board.move_piece(selected, board_pos)
                        selected = None

                draw(board, selected, dragged, mouse_pos, board.piece_to_promote)

            elif event.type == pygame.MOUSEMOTION:
                if dragged is not None:
                    # Drop the piece upon dragging it out of bounds
                    if mouse_pos[0] > settings.BOARD_WIDTH or mouse_pos[1] > settings.BOARD_HEIGHT:
                        dragged = None
                        selected = None

                    draw(board, selected, dragged, mouse_pos, board.piece_to_promote)

    pygame.quit()


if __name__ == "__main__":
    # Paweł 1 : 0 Mariusz
    # Pierwszą gre wygrał Paweł D
    main()


