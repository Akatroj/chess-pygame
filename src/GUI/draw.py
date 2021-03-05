import pygame
import settings
import Game.Board.board as Board


WINDOW = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
pygame.display.set_caption('Chess')
icon = pygame.transform.scale(pygame.image.load(settings.ICON_PATH), (settings.ICON_SIZE, settings.ICON_SIZE))
pygame.display.set_icon(icon)


def draw(board, selected_piece, dragged_piece, mouse_pos):
    draw_board(board, selected_piece)
    if selected_piece is not None:
        moves, captures = selected_piece.possible_move(board.board)
        draw_possible_moves(moves)
        draw_possible_captures(captures)
    draw_pieces(board, dragged_piece)
    draw_lines()
    if dragged_piece is not None:
        draw_dragged_piece(dragged_piece, mouse_pos)
    pygame.display.update()


def draw_board(board, selected_piece):
    for i in range(len(board.board)):
        for j in range(len(board.board[0])):
            x = i * settings.SQUARE_SIZE
            y = j * settings.SQUARE_SIZE
            if selected_piece is not None and selected_piece.x == i and selected_piece.y == j:
                color = settings.SELECTED_PIECE_COLOR
            elif (i + j) % 2 == 0:
                color = settings.BOARD_DARK_SQUARE_COLOR
            else:
                color = settings.BOARD_LIGHT_SQUARE_COLOR
            square = pygame.Rect(x, y, settings.SQUARE_SIZE, settings.SQUARE_SIZE)
            pygame.draw.rect(WINDOW, color, square)


def draw_possible_moves(moves):
    for move in moves:
        x = move[0] * settings.SQUARE_SIZE
        y = move[1] * settings.SQUARE_SIZE
        draw_highlighted_border(x, y, settings.SQUARE_SIZE, settings.SQUARE_SIZE, settings.MOVE_COLOR)


def draw_possible_captures(captures):
    for capture in captures:
        x = capture[0] * settings.SQUARE_SIZE
        y = capture[1] * settings.SQUARE_SIZE
        draw_highlighted_border(x, y, settings.SQUARE_SIZE, settings.SQUARE_SIZE, settings.CAPTURE_COLOR)


def draw_highlighted_border(x, y, width, height, color):
    height = height  # - 2
    width = width  # - 2

    x_start = x  # + 1
    y_start = y  # + 1
    y_end = y_start + height - settings.HIGHLIGHTED_BORDER_THICKNESS
    x_end = x_start + width - settings.HIGHLIGHTED_BORDER_THICKNESS

    pygame.draw.rect(WINDOW, color, pygame.Rect(x_start, y_start, width, settings.HIGHLIGHTED_BORDER_THICKNESS))  # left
    pygame.draw.rect(WINDOW, color, pygame.Rect(x_start, y_start, settings.HIGHLIGHTED_BORDER_THICKNESS, height))  # top
    pygame.draw.rect(WINDOW, color, pygame.Rect(x_start, y_end, width, settings.HIGHLIGHTED_BORDER_THICKNESS))  # bottom
    pygame.draw.rect(WINDOW, color, pygame.Rect(x_end, y_start, settings.HIGHLIGHTED_BORDER_THICKNESS, height))  # right


def draw_pieces(board, dragged_piece):
    for i in range(len(board.board)):
        for j in range(len(board.board[0])):
            x = i * settings.SQUARE_SIZE
            y = j * settings.SQUARE_SIZE
            piece = board.get_piece_at_position((i, j))
            if piece is not None and piece != dragged_piece:
                WINDOW.blit(piece.sprite, (x, y))


def draw_dragged_piece(dragged_piece, mouse_pos):
    x = mouse_pos[0] - settings.SQUARE_SIZE//2
    y = mouse_pos[1] - settings.SQUARE_SIZE//2
    WINDOW.blit(dragged_piece.sprite, (x, y))


def draw_lines():
    for i in range(settings.BOARD_SIZE):
        length = i*settings.SQUARE_SIZE-settings.LINE_THICKNESS//2
        vertical_line = pygame.Rect(length, 0, settings.LINE_THICKNESS, settings.BOARD_HEIGHT)
        horizontal_line = pygame.Rect(0, length, settings.BOARD_WIDTH, settings.LINE_THICKNESS)
        pygame.draw.rect(WINDOW, settings.LINE_COLOR, vertical_line)
        pygame.draw.rect(WINDOW, settings.LINE_COLOR, horizontal_line)
