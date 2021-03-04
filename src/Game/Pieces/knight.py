from Game.Pieces.piece import Piece


class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.spritePath = "../assets/{}n.png".format(self.color)

