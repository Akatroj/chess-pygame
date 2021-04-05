BOARD_SIZE = 8

LEFT_CLICK = 1
RIGHT_CLICK = 3


def is_on_board(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7


