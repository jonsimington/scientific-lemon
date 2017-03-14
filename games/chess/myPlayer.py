from games.chess.helperFunctions import *
from games.chess.fenHelper import getCastlingStr, getPiecesFromFen
from games.chess.myPiece import *


class myPlayer:
    """
    Custom built player object containing pieces and values used for tracking the possible moves for a player
    """

    def __init__(self, color, fen):
        # Initialize member values to empty or false before getting data from parseFen Function
        self.canQueenCastle = False
        self.canKingCastle = False
        self.myMove = False
        self.pieces = []
        self.color = color
        self.score = self.calculateScore()
        self.rank_direction = getRankDirection(color)

        # Gets data from Fen and inserts into member variables
        self.parseFen(fen, color)

    def parseFen(self, fen, color):
        """
        Parses the given fen string and gathers information needed for castling, and piece location for given player
        :param fen: The Fen string representing current state
        :param color: Color of player
        :return: Gives values to member variables canQueenCastle, canKingCastle, myMove, and pieces
        """

        self.pieces = getPiecesFromFen(color, fen)

        fenSplit = fen.split()
        # If Player is white and its players move
        if fenSplit[1] == "w" and color == "White":
            self.myMove = True
        else:
            self.myMove = True

        for letter in getCastlingStr(fen):
            if (letter == "K" and color == "White") or (letter == "k" and color == "Black"):
                self.canKingCastle = True
            elif (letter == "Q" and color == "White") or (letter == "q" and color == "Black"):
                self.canQueenCastle = True

    def calculateScore(self):
        score = 0
        for p in self.pieces:
            score += getPieceScore(p.type)
        return score

    def printMe(self):
        """
        Prints color and all pieces player owns
        :return: None
        """
        print(self.color)
        for p in self.pieces:
            print(p.type + ": " + p.file + str(p.rank))
        print()


def getPieceScore(type):
    if type == "Pawn":
        return 1
    elif type == "Knight" or type == "Bishop":
        return 3
    elif type == "Rook":
        return 5
    elif type == "Queen":
        return 9
    # King
    else:
        return 0
