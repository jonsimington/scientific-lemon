from games.chess.fenHelper import getPassantTarget

from games.chess.myPlayer import *


class gameState:
    """
    Custom built game state object used for tracking of current adn future game states
    """

    def __init__(self, fen):
        self.whitePlayer = myPlayer("White", fen)
        self.blackPlayer = myPlayer("Black", fen)
        self.enPassantTarget = getPassantTarget(fen)
        self.fen = fen
