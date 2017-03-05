from games.chess.helperFunctions import *
from games.chess.myPiece import *


def generateFen(myGame, move, currPlayerColor):
    """
    Generates a Fen string using the given game state and move to be applied to game state
    :param myGame: Current game state
    :param move: Move to be made
    :param currPlayerColor: Moving players color
    :return: A Fen state string for the move
    """

    fen = getPieceFen(move, myGame)
    fen += " "
    fen += getOppositeColorChar(currPlayerColor)
    fen += getKingQueenCastleFen(move, myGame)

    if currPlayerColor == "White":
        fen += getPassantFen(move, 1)
    else:
        fen += getPassantFen(move, -1)

    return fen


def getPieceFen(move, myGame):
    """
    Generates the piece portion of the Fen string
    :param move: Move to be made
    :param myGame: Current game state
    :return: String containing the Fen state for the pieces
    """
    fen = ""
    # Get list of pieces after the move is applied
    allPieces = getPieceListAfterMove(myGame.whitePlayer.pieces + myGame.blackPlayer.pieces, move)
    for rank in range(8, 0, -1):
        # Counts the blankspaces on the board
        blankSpace = 0

        # Used for counting file
        for file in range(ord("a"), ord("i")):
            piece = getPieceInSquare(rank, chr(file), allPieces)

            if piece is not None:
                # Checks if previous spaces were blank
                if blankSpace > 0:
                    fen += str(blankSpace)
                    blankSpace = 0
                # Add piece found
                fen += getLetterForColor(piece.type, piece.color)

            else:
                blankSpace += 1

        # Made it to the end of file and it was blank
        if blankSpace > 0:
            fen += str(blankSpace)
        fen += "/"
    return fen


def getKingQueenCastleFen(move, myGame):
    """
    Generates the castling portion of the Fen string
    :param move: Move to be made
    :param myGame: Current game state
    :return: Fen string to be used
    """

    fen = " "
    if not myGame.whitePlayer.canKingCastle or (
                        move.piece.type == "Rook" and move.piece.file == "h" and move.piece.rank == 1):
        fen += "-"
    else:
        fen += "K"

    if not myGame.whitePlayer.canQueenCastle or (
                        move.piece.type == "Rook" and move.piece.file == "a" and move.piece.rank == 1):
        fen += "-"
    else:
        fen += "Q"

    if not myGame.blackPlayer.canKingCastle or (
                        move.piece.type == "Rook" and move.piece.file == "h" and move.piece.rank == 8):
        fen += "-"
    else:
        fen += "k"

    if not myGame.blackPlayer.canQueenCastle or (
                        move.piece.type == "Rook" and move.piece.file == "a" and move.piece.rank == 8):
        fen += "-"
    else:
        fen += "q"

    return fen


def getPassantFen(move, rankDirection):
    """
    Generates the En Passant Fen string
    :param move: Move to be made
    :param rankDirection: Rank direction of the move
    :return: Returns the fen for En Passant as either a - or the coordinate for an En Passant move
    """
    fen = " "
    if move.piece.type == "Pawn" and ((move.piece.rank == 7 and move.piece.color == "Black") or (
                    move.piece.rank == 2 and move.piece.color == "White")) and (
                move.piece.rank + rankDirection * 2) == move.rank:

        # Add the rank - rank direction to get the square behind the double move
        fen += (move.file + str(move.rank - rankDirection))
    else:
        fen += "-"
    return fen


def getOppositeColorChar(color):
    """
    Returns single character representation of the opposite color
    :param color: Color as a string White or Black
    :return: The opposite of the color given as b or w
    """
    if color == "White":
        return "b"
    else:
        return "w"


def getLetterForColor(type, color):
    """
    Gets the upper or lowercase letter for the respective piece given the color
    :param type: Type of piece as a string
    :param color: Color of player
    :return: Single character representing the piece given
    """
    if type == "Pawn" and color == "White":
        return "P"
    elif type == "Pawn" and color == "Black":
        return "p"
    elif type == "Rook" and color == "White":
        return "R"
    elif type == "Rook" and color == "Black":
        return "r"
    elif type == "Knight" and color == "White":
        return "N"
    elif type == "Knight" and color == "Black":
        return "n"
    elif type == "Bishop" and color == "White":
        return "B"
    elif type == "Bishop" and color == "Black":
        return "b"
    elif type == "Queen" and color == "White":
        return "Q"
    elif type == "Queen" and color == "Black":
        return "q"
    elif type == "King" and color == "White":
        return "K"
    elif type == "King" and color == "Black":
        return "k"


def getPassantTarget(fen):
    """
    Returns the En Passant part of the Fen
    :param fen: Fen string
    :return: En Passant portion of the Fen String
    """
    fenSplit = fen.split()
    return fenSplit[3]


def getCastlingStr(fen):
    """
    Returns the Castling part of the Fen
    :param fen: Fen string
    :return: Castling portion of the Fen String
    """
    fenSplit = fen.split()
    return fenSplit[2]


def getPiecesFromFen(color, fen):
    """
    Creates list of pieces player owns from Fen String
    :param color: Color of player
    :param fen: Fen string
    :return: List of all pieces that the given colored player owns
    """
    myPieces = []
    rank = 8
    file = "a"
    fenSplit = fen.split()
    for letter in fenSplit[0]:

        if letter == "/":
            rank -= 1
            file = "a"
        elif letter.isdigit():
            file = getNewLetter(file, int(letter))
        else:
            if (letter == "P" and color == "White") or (letter == "p" and color == "Black"):
                myPieces.append(myPiece(file, rank, "Pawn", color))

            elif (letter == "R" and color == "White") or (letter == "r" and color == "Black"):
                myPieces.append(myPiece(file, rank, "Rook", color))

            elif (letter == "N" and color == "White") or (letter == "n" and color == "Black"):
                myPieces.append(myPiece(file, rank, "Knight", color))

            elif (letter == "B" and color == "White") or (letter == "b" and color == "Black"):
                myPieces.append(myPiece(file, rank, "Bishop", color))

            elif (letter == "Q" and color == "White") or (letter == "q" and color == "Black"):
                myPieces.append(myPiece(file, rank, "Queen", color))

            elif (letter == "K" and color == "White") or (letter == "k" and color == "Black"):
                myPieces.append(myPiece(file, rank, "King", color))

            file = getNewLetter(file, 1)
    return myPieces
