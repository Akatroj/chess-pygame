from Game.utils import is_on_board


class Piece:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.sprite = None
        self.symbol = None
        self.last_move = None

    def get_position(self):
        return [self.x, self.y]

    def change_position(self, position):
        self.x = position[0]
        self.y = position[1]

    def generate_moves(self, board, offsets):
        move_arr = []
        capture_arr = []

        for i in offsets:
            temp_move_arr, temp_capture_arr = self.move_generator(i[0], i[1], board)
            move_arr = move_arr + temp_move_arr
            capture_arr = capture_arr + temp_capture_arr

        return move_arr, capture_arr

    def move_generator(self, change_x, change_y, board):
        move_arr = []
        capture_arr = []
        new_x = self.x + change_x
        new_y = self.y + change_y

        while is_on_board(new_x, new_y) and board.board_arr[new_x][new_y] is None:
            move_arr.append([new_x, new_y])
            new_x += change_x
            new_y += change_y
        if is_on_board(new_x, new_y) and board.board_arr[new_x][new_y] is not None \
                and board.board_arr[new_x][new_y].color != self.color:
            capture_arr.append([new_x, new_y])

        return move_arr, capture_arr
