from Game.Pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.spritePath = "../assets/{}p.png".format(self.color)
