import random
from games.chess.gameState import *


class pieceMove:
    """
    Possible move that could be made
    Contains piece, the new rank, new file and promotion of the move
    """

    def __init__(self, piece, rank, file, promotion=""):
        self.piece = piece
        self.rank = rank
        self.file = file
        self.promotion = promotion

    def printPiece(self):
        """
        Prints the Type, new rank, new file and promotion
        :return:
        """
        print(self.piece.type, self.rank, self.file, self.promotion, sep="\t")

    def __lt__(self, other):
        """
        Added less than operator for priority queue always return true 
        This is because the operator is only used with a priority queue and the priorirty queue
        is sorting based on move history score
        :param other: Other move
        :return: True
        """
        return True

def getMove(myGame, colorToMove):
    """
    Gets a list of all possible moves that can me made at a given turn

    :param myGame: Current game state
    :param colorToMove: Color player to move
    :return: List of all possible moves that can be made
    """

    moveList = []

    if colorToMove == "White":
        pieces = myGame.whitePlayer.pieces
        player = myGame.whitePlayer
        opponent = myGame.blackPlayer

    else:
        pieces = myGame.blackPlayer.pieces
        player = myGame.blackPlayer
        opponent = myGame.whitePlayer

    for p in pieces:
        if p.type == "Pawn":
            result = getPawnMove(p, player, opponent, myGame.enPassantTarget)
            for moves in result:
                moveList.append(moves)

        elif p.type == "Bishop":
            result = getBishopMove(p, player, opponent)
            for moves in result:
                moveList.append(moves)

        elif p.type == "Rook":
            result = getRookMove(p, player, opponent)
            for moves in result:
                moveList.append(moves)
        elif p.type == "Knight":
            result = getKnightMove(p, player, opponent)
            for moves in result:
                moveList.append(moves)
        elif p.type == "Queen":
            result = getQueenMove(p, player, opponent)
            for moves in result:
                moveList.append(moves)
        # King
        else:
            result = getKingMove(p, player, opponent)
            for moves in result:
                moveList.append(moves)

            castleMove = getCastleMoves(p, player, opponent)
            for move in castleMove:
                moveList.append(move)

    return moveList


def getPawnMove(piece, me, opp, passant):
    """
    Gets all moves for a given pawn
    :param piece: Pawn to moves
    :param me: The myPlayer object of the moving
    :param opp: The myPlayer object of the opponent of the moving player
    :param passant: The passant string from the Fen
    :return: List of all possible movements for the pawn
    """
    myMoves = []

    # Default these moves to None
    forwardMove = False

    # Can move forward
    if not isSquareOccupied(piece.rank + me.rank_direction, piece.file, (me.pieces + opp.pieces)):
        forwardMove = True
        myMoves.append(pieceMove(piece, piece.rank + me.rank_direction, piece.file))

    # Check for ability to double move for first time
    if forwardMove and ((piece.rank == 2 and me.color == "White") or (piece.rank == 7 and me.color == "Black")) \
            and not isSquareOccupied(piece.rank + me.rank_direction * 2, piece.file, (me.pieces + opp.pieces)):
        myMoves.append(pieceMove(piece, piece.rank + me.rank_direction * 2, piece.file))

    # Can attack diagonal
    for p in opp.pieces:
        # Check if piece is diagonal right
        if piece.rank + me.rank_direction == p.rank and getNewLetter(piece.file, 1) == p.file:
            myMoves.append(pieceMove(piece, piece.rank + me.rank_direction, getNewLetter(piece.file, 1)))
        # Check if piece is diagonal left
        if piece.rank + me.rank_direction == p.rank and getNewLetter(piece.file, -1) == p.file:
            myMoves.append(pieceMove(piece, piece.rank + me.rank_direction, getNewLetter(piece.file, -1)))

    # Can attack En Passant
    if passant != "-":
        leftPass = getNewLetter(piece.file, -1) + str(piece.rank + me.rank_direction)
        rightPass = getNewLetter(piece.file, 1) + str(piece.rank + me.rank_direction)

        if passant == leftPass:
            myMoves.append(pieceMove(piece, piece.rank + me.rank_direction, getNewLetter(piece.file, -1)))

        elif passant == rightPass:
            myMoves.append(pieceMove(piece, piece.rank + me.rank_direction, getNewLetter(piece.file, 1)))

    finalMoves = []
    # Adds promotion tag as necessary
    for move in myMoves:
        if move.rank == 1 or move.rank == 8:
            finalMoves.append(pieceMove(move.piece,move.rank, move.file, "Queen"))
            finalMoves.append(pieceMove(move.piece, move.rank, move.file, "Rook"))
            finalMoves.append(pieceMove(move.piece, move.rank, move.file, "Bishop"))

            move.promotion = "Knight"
            finalMoves.append(move)
        else:
            finalMoves.append(move)

    return finalMoves


def getBishopMove(piece, me, opp):
    """
    Gets all moves for the given bishop piece
    :param piece: Pawn to moves
    :param me: The myPlayer object of the moving
    :param opp: The myPlayer object of the opponent of the moving player
    :return: List of all possible movements for the bishop
    """
    myMoves = []

    # Flags to indicate if the piece can continue to move in that direction
    # Set to false if a boundary is hit or another piece is hit
    upRight = True
    upLeft = True
    downRight = True
    downLeft = True

    for i in range(1, 8):
        # Check if can still move up and to the right, and not hit ourselves,
        if upRight and piece.rank + i != 9 and getNewLetter(piece.file, i) is not "i" \
                and not isSquareOccupied(piece.rank + i, getNewLetter(piece.file, i), me.pieces):
            myMoves.append(pieceMove(piece, piece.rank + i, getNewLetter(piece.file, i)))

            # Check if hitting an opponent piece
            if isSquareOccupied(piece.rank + i, getNewLetter(piece.file, i), opp.pieces):
                upRight = False
        else:
            upRight = False

        # Check if we go too far up, hit ourselves, or to the left
        # ' is the character that proceeds a in char values
        if upLeft and piece.rank + i != 9 and getNewLetter(piece.file, -i) is not "`" \
                and not isSquareOccupied(piece.rank + i, getNewLetter(piece.file, -i), me.pieces):
            myMoves.append(pieceMove(piece, piece.rank + i, getNewLetter(piece.file, -i)))
            # Check if hitting an opponent piece
            if isSquareOccupied(piece.rank + i, getNewLetter(piece.file, -i), opp.pieces):
                upLeft = False
        else:
            upLeft = False

        # Check if we go too far down, hit ourselves, or to the right
        if downRight and piece.rank - i != 0 and getNewLetter(piece.file, i) is not "i" \
                and not isSquareOccupied(piece.rank - i, getNewLetter(piece.file, i), me.pieces):
            myMoves.append(pieceMove(piece, piece.rank - i, getNewLetter(piece.file, i)))

            # Check if hitting an opponent piece
            if isSquareOccupied(piece.rank - i, getNewLetter(piece.file, i), opp.pieces):
                downRight = False
        else:
            downRight = False

        # Check if we go too far down or to the left
        # ' is the character that proceeds a in char values
        if downLeft and piece.rank - i != 0 and getNewLetter(piece.file, -i) is not "`" \
                and not isSquareOccupied(piece.rank - i, getNewLetter(piece.file, -i), me.pieces):
            myMoves.append(pieceMove(piece, piece.rank - i, getNewLetter(piece.file, -i)))

            # Check if hitting an opponent piece
            if isSquareOccupied(piece.rank - i, getNewLetter(piece.file, -i), opp.pieces):
                downLeft = False
        else:
            downLeft = False

    return myMoves


def getRookMove(piece, me, opp):
    """
    Gets all the moves that a rook can make
    :param piece: Rook to mve
    :param me: The myPlayer object of the moving
    :param opp: The myPlayer object of the opponent of the moving player
    :return: List of all possible movements for the Rook
    """

    myMoves = []
    # Flags to indicate if the piece can continue to move in that direction
    # Set to false if a boundary is hit or another piece is hit
    up = True
    down = True
    right = True
    left = True

    for i in range(1, 8):
        # Can move up without hitting top or ally piece
        if up and piece.rank + i != 9 and not isSquareOccupied(piece.rank + i, piece.file, me.pieces):
            myMoves.append(pieceMove(piece, piece.rank + i, piece.file))
            # Hit enemy piece
            if isSquareOccupied(piece.rank + i, piece.file, opp.pieces):
                up = False

        else:
            up = False

        # Can move down without hitting bottom or ally piece
        if down and piece.rank - i != 0 and not isSquareOccupied(piece.rank - i, piece.file, me.pieces):
            myMoves.append(pieceMove(piece, piece.rank - i, piece.file))
            # Hit enemy piece
            if isSquareOccupied(piece.rank - i, piece.file, opp.pieces):
                down = False
        else:
            down = False

        # Can move right without hitting side or ally piece
        if right and getNewLetter(piece.file, i) is not "i" and not isSquareOccupied(piece.rank,
                                                                                     getNewLetter(piece.file, i),
                                                                                     me.pieces):
            myMoves.append(pieceMove(piece, piece.rank, getNewLetter(piece.file, i)))
            # Hit enemy piece
            if isSquareOccupied(piece.rank, getNewLetter(piece.file, i), opp.pieces):
                right = False
        else:
            right = False

        # Can move left without hitting side or ally piece
        if left and getNewLetter(piece.file, -i) is not "`" and not isSquareOccupied(piece.rank,
                                                                                     getNewLetter(piece.file, -i),
                                                                                     me.pieces):
            myMoves.append(pieceMove(piece, piece.rank, getNewLetter(piece.file, -i)))
            # Hit enemy piece
            if isSquareOccupied(piece.rank, getNewLetter(piece.file, -i), opp.pieces):
                left = False
        else:
            left = False

    return myMoves


def getKnightMove(piece, me, opp):
    """
    Get list of all possible knight moves
    :param piece: Knight to move
    :param me: Player moving knight
    :param opp: Opponent player, this variable is unused but added for future improvements on knight capture logic
    :return: List of all possible moves
    """
    myPosList = getPieceCoordList(me)

    possiblePosList = [pieceMove(piece, piece.rank + 1, getNewLetter(piece.file, 2)),
                       pieceMove(piece, piece.rank + 1, getNewLetter(piece.file, -2)),
                       pieceMove(piece, piece.rank - 1, getNewLetter(piece.file, 2)),
                       pieceMove(piece, piece.rank - 1, getNewLetter(piece.file, -2)),
                       pieceMove(piece, piece.rank + 2, getNewLetter(piece.file, 1)),
                       pieceMove(piece, piece.rank + 2, getNewLetter(piece.file, -1)),
                       pieceMove(piece, piece.rank - 2, getNewLetter(piece.file, 1)),
                       pieceMove(piece, piece.rank - 2, getNewLetter(piece.file, -1))]

    # Generates all possible coordinates for the knight


    finalResult = []
    # Checks if a move is valid from list of possible moves
    for move in possiblePosList:
        rank = move.rank
        file = move.file
        if 1 <= rank <= 8 and ord("a") <= ord(file) <= ord("h") and (rank, file) not in myPosList:
            finalResult.append(move)

    return finalResult


def getQueenMove(piece, me, opp):
    """
    Gets list of all possible queen moves
    :param piece: Queen to move
    :param me: Player moving the queen
    :param opp: Opponent of player
    :return: List of all possible moves
    """

    # Queens move as a rook and bishop so call those function
    return getBishopMove(piece, me, opp) + getRookMove(piece, me, opp)


def getKingMove(piece, me, opp):
    """
    Gets all possible moves for king
    Does not check if the move puts the king into check because of a recursive call issue with checking if in check
    :param piece: King to move
    :param me: The myPlayer object of the moving
    :param opp: The myPlayer object of the opponent of the moving player
    :return: List of all possible movements for the King
    """
    myPosList = getPieceCoordList(me)

    possiblePosList = []
    finalResult = []
    possiblePosList.append(pieceMove(piece, piece.rank + 1, getNewLetter(piece.file, 1)))
    possiblePosList.append(pieceMove(piece, piece.rank + 1, getNewLetter(piece.file, 0)))
    possiblePosList.append(pieceMove(piece, piece.rank + 1, getNewLetter(piece.file, -1)))
    possiblePosList.append(pieceMove(piece, piece.rank - 1, getNewLetter(piece.file, 1)))
    possiblePosList.append(pieceMove(piece, piece.rank - 1, getNewLetter(piece.file, 0)))
    possiblePosList.append(pieceMove(piece, piece.rank - 1, getNewLetter(piece.file, -1)))
    possiblePosList.append(pieceMove(piece, piece.rank, getNewLetter(piece.file, 1)))
    possiblePosList.append(pieceMove(piece, piece.rank, getNewLetter(piece.file, -1)))

    for move in possiblePosList:
        rank = move.rank
        file = move.file
        if 1 <= rank <= 8 and ord("a") <= ord(file) <= ord("h") and (rank, file) not in myPosList:
            finalResult.append(move)

    return finalResult


def getCastleMoves(piece, me, opp):
    """
    Gets the list of all possble castle moves
    :param piece: King to castle
    :param me: The myPlayer object of the moving
    :param opp: The myPlayer object of the opponent of the moving player
    :return: List of all possible castle movements for the King, an empty list is possible
    """
    movesToMake = []

    myPosList = getPieceCoordList(me)
    oppList = getPieceCoordList(opp)

    if me.canKingCastle:
        kingSideMove = pieceMove(piece, piece.rank, "h")
        movesToMake.append(kingSideMove)
        # Check King is not blocked
        for i in range(1, 3):
            if ((piece.rank, getNewLetter(piece.file, i)) in (myPosList + oppList)) or (
                    isSquareAttacked(me, opp, piece.rank, getNewLetter(piece.file, i))):
                movesToMake.remove(kingSideMove)
                break

    if me.canQueenCastle:
        queenSideMove = pieceMove(piece, piece.rank, "a")
        movesToMake.append(queenSideMove)

        # Check Queen is not blocked
        for i in range(1, 4):
            if ((piece.rank, getNewLetter(piece.file, -i)) in (myPosList + oppList)) or (
                    isSquareAttacked(me, opp, piece.rank, getNewLetter(piece.file, -i))):
                movesToMake.remove(queenSideMove)
                break

    return movesToMake


def isSquareAttacked(player, opp, rank, file, passant=""):
    """
    Checks if a specified square is under attack
    :param player: Player about to attack
    :param opp: Opponent about to be attacked
    :param rank: Rank to check
    :param file: File to check
    :param passant: Passant flag for checking En Passant
    :return: Returns true if a piece can attack the square
    """
    for p in player.pieces:
        if p.type == "Pawn":
            result = (getPawnMove(p, player, opp, passant))
            for move in result:
                if move.rank == rank and move.file == file:
                    return True


        elif p.type == "Bishop":
            result = getBishopMove(p, player, opp)
            for move in result:
                if move.rank == rank and move.file == file:
                    return True


        elif p.type == "Rook":
            result = getRookMove(p, player, opp)
            for move in result:
                if move.rank == rank and move.file == file:
                    return True

        elif p.type == "Knight":
            result = getKnightMove(p, player, opp)
            for move in result:
                if move.rank == rank and move.file == file:
                    return True

        elif p.type == "Queen":
            result = getQueenMove(p, player, opp)
            for move in result:
                if move.rank == rank and move.file == file:
                    return True

        # King
        else:
            result = getKingMove(p, player, opp)
            for move in result:
                if move.rank == rank and move.file == file:
                    return True

    return False


def checkIfInCheck(fen, color):
    """
    Checks if the colored player is in check
    :param fen: Fen string for the game state
    :param color: Color of player to check if in check
    :return: Returns True if player is in check for the given state
    """
    myGame = gameState(fen)
    if color == "White":
        me = myGame.whitePlayer
        opp = myGame.blackPlayer
    else:
        me = myGame.blackPlayer
        opp = myGame.whitePlayer

    king = findKing(me.pieces)

    # This is used to prevent trying to peer into a future state where the king is already captured
    if king is None:
        return True
    else:
        return isSquareAttacked(opp, me, king.rank, king.file)
