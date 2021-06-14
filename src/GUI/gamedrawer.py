import pygame
import settings
from Game.Pieces.bishop import Bishop
from Game.Pieces.knight import Knight
from Game.Pieces.queen import Queen
from Game.Pieces.rook import Rook
from GUI.draw_utils import colored_rectangle_border
from Game.utils import BOARD_SIZE

# arrays with 'fake pieces' used during pawn promotion
PROMOTION_ARRAY_WHITE = [
    Queen('w', 0, 0), Knight('w', 0, 1), Rook('w', 0, 2), Bishop('w', 0, 3)
]

PROMOTION_ARRAY_BLACK = [
    Bishop('b', 0, 4), Rook('b', 0, 5), Knight('b', 0, 6), Queen('b', 0, 7)
]

# Constants
# Empty board surface
BOARD_LIGHT_SQUARE_COLOR = pygame.Color('#946F51')
BOARD_DARK_SQUARE_COLOR = pygame.Color('#F0D9B5')
LINE_COLOR = pygame.Color('#000000')
LINE_THICKNESS = 2

# Coordinates
FONT_SIZE = int(settings.SQUARE_SIZE * 0.27)
COORDINATE_MARGIN = settings.SQUARE_SIZE * 0.075
LETTER_WIDTH = FONT_SIZE * 0.58  # this is just an estimate


# Special squares colors
POSITION_PREV_COLOR = pygame.Color('#FFFF3D')
POSITION_CURR_COLOR = pygame.Color('#FFD700')
SELECTED_PIECE_COLOR = pygame.Color('#2CBA41')
CHECK_COLOR = pygame.Color('#FF0000')

# Squares with colored outline
HIGHLIGHTED_BORDER_THICKNESS = 5
MOVE_COLOR = pygame.Color('#00FF00')
CAPTURE_COLOR = pygame.Color('#FF0000')

# Promotion window
PROMOTION_WINDOW_COLOR = pygame.Color("#FFFFFF")
PROMOTION_WINDOW_WIDTH = settings.SQUARE_SIZE
PROMOTION_WINDOW_HEIGHT = settings.SQUARE_SIZE * 4


# returns a surface of an empty chessboard (only alternating light/dark squares)
def _prepare_empty_board_surface():
    result = pygame.Surface((settings.BOARD_WIDTH, settings.BOARD_HEIGHT), pygame.SRCALPHA, 32)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            x = i * settings.SQUARE_SIZE
            y = j * settings.SQUARE_SIZE
            if (i + j) % 2 == 0:
                color = BOARD_DARK_SQUARE_COLOR
            else:
                color = BOARD_LIGHT_SQUARE_COLOR
            pygame.draw.rect(result, color, pygame.Rect(x, y, settings.SQUARE_SIZE, settings.SQUARE_SIZE))
    return result


# returns a transparent surface with chessboard coordinates (letters for columns, numbers for rows)
def _prepare_coordinates_surface(font):
    result = pygame.Surface((settings.BOARD_WIDTH, settings.BOARD_HEIGHT), pygame.SRCALPHA, 32)
    for i in range(BOARD_SIZE):

        # number
        x = int(COORDINATE_MARGIN)
        y = int(COORDINATE_MARGIN + i * settings.SQUARE_SIZE)
        color = BOARD_LIGHT_SQUARE_COLOR if i % 2 == 0 else BOARD_DARK_SQUARE_COLOR

        surface = font.render(str(8-i), True, color)
        result.blit(surface, (x, y))

        # letter
        x = int(settings.SQUARE_SIZE * (i + 1) - LETTER_WIDTH)
        y = int(settings.BOARD_HEIGHT - FONT_SIZE - COORDINATE_MARGIN)
        color = BOARD_LIGHT_SQUARE_COLOR if i % 2 != 0 else BOARD_DARK_SQUARE_COLOR

        surface = font.render(chr(ord('a') + i), True, color)
        result.blit(surface, (x, y))

    return result


# returns a transparent surface with intersecting black lines
def _prepare_line_surface():
    result = pygame.Surface((settings.BOARD_WIDTH, settings.BOARD_HEIGHT), pygame.SRCALPHA, 32)
    for i in range(BOARD_SIZE):
        length = i * settings.SQUARE_SIZE - LINE_THICKNESS // 2
        vertical_line = pygame.Rect(length, 0, LINE_THICKNESS, settings.BOARD_HEIGHT)
        horizontal_line = pygame.Rect(0, length, settings.BOARD_WIDTH, LINE_THICKNESS)
        pygame.draw.rect(result, LINE_COLOR, vertical_line)
        pygame.draw.rect(result, LINE_COLOR, horizontal_line)
    return result


class GameDrawer:
    def __init__(self, board, window):
        self.board = board
        self.window = window
        self.coordinates_font = pygame.font.SysFont('Arial', FONT_SIZE)

        # surfaces
        self.base_surface = pygame.Surface((settings.BOARD_WIDTH, settings.BOARD_HEIGHT), pygame.SRCALPHA, 32)
        self._coordinates_surface = _prepare_coordinates_surface(self.coordinates_font)
        self._empty_board_surface = _prepare_empty_board_surface()
        self._line_surface = _prepare_line_surface()

        # cache
        self.cached_selected_piece = "default"  # can't be initialised as None
        self.cached_turn_number = board.turn_number
        self.cached_board_surface = None
        self.cached_piece_to_promote = board.piece_to_promote

    def draw(self, selected_piece, moves, captures, dragged_piece, mouse_pos, piece_to_promote):
        # refresh cache if needed
        if selected_piece != self.cached_selected_piece\
                or self.board.turn_number != self.cached_turn_number \
                or self.cached_piece_to_promote != self.board.piece_to_promote:
            # print("refreshing cache")
            self.__cache_full_board_surface(selected_piece, moves, captures, dragged_piece)

        self.window.blit(self.cached_board_surface, (0, 0))
        if dragged_piece is not None:
            self.__draw_dragged_piece(dragged_piece, mouse_pos)
        elif selected_piece is not None:
            x = selected_piece.x * settings.SQUARE_SIZE
            y = selected_piece.y * settings.SQUARE_SIZE
            self.window.blit(selected_piece.sprite, (x, y))
        if piece_to_promote is not None:
            self.draw_promotion_window(piece_to_promote)
        pygame.display.update()

    def draw_promotion_window(self, piece_to_promote):
        if piece_to_promote.color == 'w':
            x = piece_to_promote.x * settings.SQUARE_SIZE
            y = piece_to_promote.y * settings.SQUARE_SIZE
            pygame.draw.rect(self.window, PROMOTION_WINDOW_COLOR,
                             pygame.Rect(x, y, PROMOTION_WINDOW_WIDTH, PROMOTION_WINDOW_HEIGHT))
            for i in range(len(PROMOTION_ARRAY_WHITE)):
                piece = PROMOTION_ARRAY_WHITE[i]
                self.window.blit(piece.sprite, (x, i * settings.SQUARE_SIZE))
                y_bottom = i * settings.SQUARE_SIZE - LINE_THICKNESS // 2
                pygame.draw.rect(self.window, LINE_COLOR,
                                 pygame.Rect(x, y_bottom, settings.BOARD_WIDTH, LINE_THICKNESS))
        else:
            x = piece_to_promote.x * settings.SQUARE_SIZE
            y = (piece_to_promote.y - 3) * settings.SQUARE_SIZE
            pygame.draw.rect(self.window, PROMOTION_WINDOW_COLOR,
                             pygame.Rect(x, y,
                                         PROMOTION_WINDOW_WIDTH, PROMOTION_WINDOW_HEIGHT))
            for i in range(len(PROMOTION_ARRAY_BLACK)):
                piece = PROMOTION_ARRAY_BLACK[i]
                self.window.blit(piece.sprite, (x, (i+4) * settings.SQUARE_SIZE))
                y_bottom = (i+4) * settings.SQUARE_SIZE - LINE_THICKNESS // 2
                pygame.draw.rect(self.window, LINE_COLOR,
                                 pygame.Rect(x, y_bottom, settings.BOARD_WIDTH, LINE_THICKNESS))

    def __draw_dragged_piece(self, dragged_piece, mouse_pos):
        x = mouse_pos[0] - settings.SQUARE_SIZE // 2
        y = mouse_pos[1] - settings.SQUARE_SIZE // 2
        self.window.blit(dragged_piece.sprite, (x, y))

    # creates a surface of a full chessboard:
    # alternating light/dark squares, colored special squares, piece sprites, lines between squares, coordinates
    # and stores it into cache.
    def __cache_full_board_surface(self, selected_piece, moves, captures, dragged_piece):
        result = self._empty_board_surface.copy()
        result.blit(self.__highlighted_squares_surface(selected_piece, moves, captures), (0, 0))
        result.blit(self.__piece_sprites_surface(dragged_piece), (0, 0))
        result.blit(self._line_surface, (0, 0))
        result.blit(self._coordinates_surface, (0, 0))

        self.cached_board_surface = result
        self.cached_selected_piece = selected_piece
        self.cached_turn_number = self.board.turn_number
        self.cached_piece_to_promote = self.board.piece_to_promote

    # returns a transparent surface with all piece sprites, except for the dragged piece
    def __piece_sprites_surface(self, dragged_piece):
        result = pygame.Surface((settings.BOARD_WIDTH, settings.BOARD_HEIGHT), pygame.SRCALPHA, 32)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x = i * settings.SQUARE_SIZE
                y = j * settings.SQUARE_SIZE
                piece = self.board.board_arr[i][j]
                if piece is not None and piece != dragged_piece:
                    result.blit(piece.sprite, (x, y))
        return result

    # returns a transparent surface with colored special squares
    # (last move, selected square, possible moves and possible captures)
    def __highlighted_squares_surface(self, selected_piece, moves, captures):
        result = pygame.Surface((settings.BOARD_WIDTH, settings.BOARD_HEIGHT), pygame.SRCALPHA, 32)
        special_squares = []
        last_move = self.board.last_move_positions()
        first = True
        for (i, j) in last_move:
            x = i * settings.SQUARE_SIZE
            y = j * settings.SQUARE_SIZE
            color = POSITION_PREV_COLOR if first else POSITION_CURR_COLOR
            square = pygame.Rect(x, y, settings.SQUARE_SIZE, settings.SQUARE_SIZE)
            special_squares.append((color, square))
            first = False

        if selected_piece is not None:
            x = selected_piece.x * settings.SQUARE_SIZE
            y = selected_piece.y * settings.SQUARE_SIZE
            color = SELECTED_PIECE_COLOR
            square = pygame.Rect(x, y, settings.SQUARE_SIZE, settings.SQUARE_SIZE)
            special_squares.append((color, square))
            for move in moves:
                x = move[0] * settings.SQUARE_SIZE
                y = move[1] * settings.SQUARE_SIZE
                special_squares += colored_rectangle_border(x, y, settings.SQUARE_SIZE, settings.SQUARE_SIZE,
                                                            MOVE_COLOR, HIGHLIGHTED_BORDER_THICKNESS)
            for capture in captures:
                x = capture[0] * settings.SQUARE_SIZE
                y = capture[1] * settings.SQUARE_SIZE
                special_squares += colored_rectangle_border(x, y, settings.SQUARE_SIZE, settings.SQUARE_SIZE,
                                                            CAPTURE_COLOR, HIGHLIGHTED_BORDER_THICKNESS)

        king = None
        if self.board.check_white_king:
            king = self.board.white_king
        elif self.board.check_black_king:
            king = self.board.black_king

        if king is not None:
            color = CHECK_COLOR
            square = pygame.Rect(king.x * settings.SQUARE_SIZE, king.y * settings.SQUARE_SIZE,
                                 settings.SQUARE_SIZE, settings.SQUARE_SIZE)
            special_squares.append((color, square))

        for (color, square) in special_squares:
            pygame.draw.rect(result, color, square)

        return result
