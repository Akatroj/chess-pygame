from Game.Pieces.piece import Piece


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.spritePath = "../assets/{}k.png".format(self.color)

