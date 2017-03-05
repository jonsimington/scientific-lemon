import random
from games.chess.helperFunctions import *
from games.chess.gameState import *

class pieceMove:
    def __init__(self, piece, rank, file, promotion=""):
        self.piece = piece
        self.rank = rank
        self.file = file
        self.promotion = promotion

    def printPiece(self):
        print(self.piece.type, self.rank, self.file, sep="\t")



def getMove(myGame, colorToMove):

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

    # Removes empty list that may be returned if not valid moves were found

    return moveList



def getPawnMove(piece, me, opp, passant):
    myMoves = []

    # Default these moves to None
    forwardMove = False

    # Can move forward
    if not isSquareOccupied(piece.rank + me.rank_direction, piece.file, (me.pieces + opp.pieces)):
        forwardMove = True
        myMoves.append(pieceMove(piece, piece.rank + me.rank_direction, piece.file))

    # Can I double move for first move
    if forwardMove and ((piece.rank == 2 and me.color == "White") or (piece.rank == 7 and me.color == "Black")) and not isSquareOccupied(piece.rank + me.rank_direction * 2, piece.file, (me.pieces + opp.pieces)):
        myMoves.append(pieceMove(piece, piece.rank + me.rank_direction * 2, piece.file))


    # Can attack diagonal
    for p in opp.pieces:
        if piece.rank + me.rank_direction == p.rank and getNewLetter(piece.file, 1) == p.file:
            myMoves.append(pieceMove(piece, piece.rank + me.rank_direction, getNewLetter(piece.file, 1)))
        if piece.rank + me.rank_direction == p.rank and getNewLetter(piece.file, -1) == p.file:
            myMoves.append(pieceMove(piece, piece.rank + me.rank_direction, getNewLetter(piece.file, -1)))

    # Can attack En Passant
    if passant != "-":
        leftPass = getNewLetter(piece.file, -1) + str(piece.rank + me.rank_direction)
        rightPass = getNewLetter(piece.file, 1) + str(piece.rank + me.rank_direction)

        if passant == leftPass:
            myMoves.append(pieceMove(piece, piece.rank + me.rank_direction, getNewLetter(piece.file, -1) ))

        elif passant == rightPass:
            myMoves.append(pieceMove(piece, piece.rank + me.rank_direction, getNewLetter(piece.file, 1)))

    for move in myMoves:
        if move.rank == 1 or move.rank == 8:
            move.promotion = random.choice(["Queen", "Rook", "Bishop", "Knight"])

    return myMoves


def getBishopMove(piece, me, opp):
    myMoves = []
    myPosList = getPieceCoordList(me)
    oppPosList = getPieceCoordList(opp)

    # Flags to indicate if the piece can continue to move in that direction
    # Set to false if a boundary is hit or another piece is hit
    upRight = True
    upLeft = True
    downRight = True
    downLeft = True

    for i in range(1, 8):
        # Check if can still move up and to the right
        if upRight and piece.rank + i != 9 and getNewLetter(piece.file, i) is not "i" and (
                    piece.rank + i, getNewLetter(piece.file, i)) not in myPosList:
            # Check if hitting an opponent piece
            if (piece.rank + i, getNewLetter(piece.file, i)) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank + i, getNewLetter(piece.file, i)))
                upRight = False
            else:
                myMoves.append(pieceMove(piece, piece.rank + i, getNewLetter(piece.file, i)))
        else:
            upRight = False

        # Check if we go too far up or to the left
        # ' is the character that proceeds a in char values
        if upLeft and piece.rank + i != 9 and getNewLetter(piece.file, -i) is not "`" and (
                    piece.rank + i, getNewLetter(piece.file, -i)) not in myPosList:
            # Check if hitting an opponent piece
            if (piece.rank + i, getNewLetter(piece.file, -i)) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank + i, getNewLetter(piece.file, -i)))
                upLeft = False
            else:
                myMoves.append(pieceMove(piece, piece.rank + i, getNewLetter(piece.file, -i)))
        else:
            upLeft = False

        # Check if we go too far down or to the right
        if downRight and piece.rank - i != 0 and getNewLetter(piece.file, i) is not "i" and (
                    piece.rank - i, getNewLetter(piece.file, i)) not in myPosList:
            # Check if hitting an opponent piece
            if (piece.rank - i, getNewLetter(piece.file, i)) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank - i, getNewLetter(piece.file, i)))
                downRight = False
            else:
                myMoves.append(pieceMove(piece, piece.rank - i, getNewLetter(piece.file, i)))
        else:
            downRight = False

        # Check if we go too far down or to the left
        # ' is the character that proceeds a in char values
        if downLeft and piece.rank - i != 0 and getNewLetter(piece.file, -i) is not "`" and (
                    piece.rank - i, getNewLetter(piece.file, -i)) not in myPosList:
            # Check if hitting an opponent piece
            if (piece.rank - i, getNewLetter(piece.file, -i)) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank - i, getNewLetter(piece.file, -i)))
                downLeft = False
            else:
                myMoves.append(pieceMove(piece, piece.rank - i, getNewLetter(piece.file, -i)))
        else:
            downLeft = False

    return myMoves


def getRookMove(piece, me, opp):
    myMoves = []
    myPosList = getPieceCoordList(me)
    oppPosList = getPieceCoordList(opp)

    # Flags to indicate if the piece can continue to move in that direction
    # Set to false if a boundary is hit or another piece is hit
    up = True
    down = True
    right = True
    left = True

    for i in range(1, 8):
        if up and piece.rank + i != 9 and (piece.rank + i, piece.file) not in myPosList:
            # Hit enemy piece
            if (piece.rank + i, piece.file) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank + i, piece.file))
                up = False
            else:
                myMoves.append(pieceMove(piece, piece.rank + i, piece.file))
        else:
            up = False

        if down and piece.rank - i != 0 and (piece.rank - i, piece.file) not in myPosList:
            # Hit enemy piece
            if (piece.rank - i, piece.file) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank - i, piece.file))
                down = False
            else:
                myMoves.append(pieceMove(piece, piece.rank - i, piece.file))
        else:
            down = False

        if right and getNewLetter(piece.file, i) is not "i" and (
                piece.rank, getNewLetter(piece.file, i)) not in myPosList:
            if (piece.rank, getNewLetter(piece.file, i)) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank, getNewLetter(piece.file, i)))
                right = False
            else:
                myMoves.append(pieceMove(piece, piece.rank, getNewLetter(piece.file, i)))
        else:
            right = False

        if left and getNewLetter(piece.file, -i) is not "`" and (
                piece.rank, getNewLetter(piece.file, -i)) not in myPosList:
            # Hit enemy piece
            if (piece.rank, getNewLetter(piece.file, -i)) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank, getNewLetter(piece.file, -i)))
                left = False
            else:
                myMoves.append(pieceMove(piece, piece.rank, getNewLetter(piece.file, -i)))
        else:
            left = False

    return myMoves


def getKnightMove(piece, me, opp):
    myPosList = getPieceCoordList(me)

    possiblePosList = []
    finalResult = []
    possiblePosList.append(pieceMove(piece, piece.rank + 1, getNewLetter(piece.file, 2)))
    possiblePosList.append(pieceMove(piece, piece.rank + 1, getNewLetter(piece.file, -2)))
    possiblePosList.append(pieceMove(piece, piece.rank - 1, getNewLetter(piece.file, 2)))
    possiblePosList.append(pieceMove(piece, piece.rank - 1, getNewLetter(piece.file, -2)))
    possiblePosList.append(pieceMove(piece, piece.rank + 2, getNewLetter(piece.file, 1)))
    possiblePosList.append(pieceMove(piece, piece.rank + 2, getNewLetter(piece.file, -1)))
    possiblePosList.append(pieceMove(piece, piece.rank - 2, getNewLetter(piece.file, 1)))
    possiblePosList.append(pieceMove(piece, piece.rank - 2, getNewLetter(piece.file, -1)))

    for move in possiblePosList:
        rank = move.rank
        file = move.file
        if 1 <= rank <= 8 and ord("a") <= ord(file) <= ord("h") and (rank, file) not in myPosList:
            finalResult.append(move)

    return finalResult


def getQueenMove(piece, me, opp):
    return getBishopMove(piece, me, opp) + getRookMove(piece, me, opp)


def getKingMove(piece, me, opp):
    myPosList = getPieceCoordList(me)
    oppList = getPieceCoordList(opp)

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


    castleMove = getCastleMoves(me, opp, piece, myPosList, oppList )
    for move in castleMove:
        finalResult.append(move)

    return finalResult


def getCastleMoves(me, opp, piece, myPosList, oppList):
    movesToMake = []
    # Check that King has not moved


    kingRook = me.canKingCastle
    queenRook = me.canQueenCastle

    if kingRook:
        kingSideMove = pieceMove(piece, piece.rank, "h")
        movesToMake.append(kingSideMove)
        # Check King is not blocked
        for i in range(1, 3):
            if (piece.rank, getNewLetter(piece.file, i)) in (myPosList + oppList):
                movesToMake.remove(kingSideMove)
                break

    if queenRook:
        queenSideMove = pieceMove(piece, piece.rank, "a")
        movesToMake.append(queenSideMove)

        # Check Queen is not blocked
        for i in range(1, 4):
            if (piece.rank, getNewLetter(piece.file, -i)) in (myPosList + oppList):
                movesToMake.remove(queenSideMove)
                break

    return movesToMake

def isSquareAttacked(player, opp, rank, file, passant=""):
    moveList = []

    for p in player.pieces:
        if p.type == "Pawn":
            result = (getPawnMove(p, player, opp, passant))
            for moves in result:
                moveList.append(moves)

        elif p.type == "Bishop":
            result = getBishopMove(p, player, opp)
            for moves in result:
                moveList.append(moves)

        elif p.type == "Rook":
            result = getRookMove(p, player, opp)
            for moves in result:
                moveList.append(moves)
        elif p.type == "Knight":
            result = getKnightMove(p, player, opp)
            for moves in result:
                moveList.append(moves)
        elif p.type == "Queen":
            result = getQueenMove(p, player, opp)
            for moves in result:
                moveList.append(moves)
        # King
        else:
            result = getKingMove(p, player, opp)
            for moves in result:
                moveList.append(moves)

                # Removes empty list that may be returned if not valid moves were found
    validMoves = [x for x in moveList if x != []]

    for move in validMoves:
        if move.rank == rank and move.file == file:
            return True

    return False

def checkIfInCheck(fen, color):
    myGame = gameState(fen)
    if color == "White":
        me = myGame.whitePlayer
        opp = myGame.blackPlayer
    else:
        me = myGame.blackPlayer
        opp = myGame.whitePlayer

    king = findKing(me.pieces)

    return isSquareAttacked(opp, me, king.rank, king.file)

