import pygame
import settings


WINDOW = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
pygame.display.set_caption('Chess')
icon = pygame.transform.scale(pygame.image.load(settings.ICON_PATH), (settings.ICON_SIZE, settings.ICON_SIZE))
pygame.display.set_icon(icon)
pygame.font.init()
font = pygame.font.SysFont('Arial', settings.FONT_SIZE)


def draw(board, selected_piece, dragged_piece, mouse_pos):
    draw_board(board, selected_piece)
    if selected_piece is not None:
        moves, captures = selected_piece.possible_move(board)
        draw_possible_moves(moves)
        draw_possible_captures(captures)
    draw_pieces(board, dragged_piece)
    draw_lines()
    if dragged_piece is not None:
        draw_dragged_piece(dragged_piece, mouse_pos)
    draw_coordinates()
    pygame.display.update()


def draw_board(board, selected_piece):
    old_pos = None
    new_pos = None
    temp = board.last_move()

    if temp is not None:
        old_pos = temp[3]
        new_pos = temp[4]
        # print('old: ' + board_arr.convert_position(old_pos[0], old_pos[1]))
        # print('new: ' + board_arr.convert_position(new_pos[0], new_pos[1]))

    for i in range(len(board.board_arr)):
        for j in range(len(board.board_arr[0])):
            x = i * settings.SQUARE_SIZE
            y = j * settings.SQUARE_SIZE
            if selected_piece is not None and selected_piece.x == i and selected_piece.y == j:
                color = settings.SELECTED_PIECE_COLOR
            elif (i + j) % 2 == 0:
                color = settings.BOARD_DARK_SQUARE_COLOR
            else:
                color = settings.BOARD_LIGHT_SQUARE_COLOR
            if temp is not None:
                if (i, j) == old_pos:
                    color = settings.POSITION_PREV_COLOR
                elif (i, j) == new_pos:
                    color = settings.POSITION_CURR_COLOR

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
    for i in range(len(board.board_arr)):
        for j in range(len(board.board_arr[0])):
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


def draw_coordinates():
    # to jest syf
    for i in range(settings.BOARD_SIZE):
        # number
        x = int(settings.RANK_COORDINATE_MARGIN)
        y = int(settings.RANK_COORDINATE_MARGIN + i * settings.SQUARE_SIZE)

        color = settings.BOARD_LIGHT_SQUARE_COLOR if i % 2 == 0 else settings.BOARD_DARK_SQUARE_COLOR
        surface = font.render(str(i+1), True, color)
        WINDOW.blit(surface, (x, y))

        # letter
        x = int(settings.SQUARE_SIZE * (i+1) - settings.FILE_COORDINATE_MARGIN)
        y = int(settings.BOARD_HEIGHT - settings.FONT_SIZE - settings.RANK_COORDINATE_MARGIN)
        color = settings.BOARD_LIGHT_SQUARE_COLOR if i % 2 != 0 else settings.BOARD_DARK_SQUARE_COLOR

        surface = font.render(chr(ord('a') + i), True, color)
        WINDOW.blit(surface, (x, y))
