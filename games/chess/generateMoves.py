import random

class pieceMove:
    def __init__(self, piece, rank, file, promotion=""):
        self.piece = piece
        self.rank = rank
        self.file = file
        self.promotion = promotion

def getNewLetter(file, increment):
    return  chr(ord(file) +  increment)


def getPieceCoordList(player):
    pieceCoordList = []
    for piece in player.pieces:
        pieceCoordList.append((piece.rank, piece.file))

    return pieceCoordList

def getPawnMove(piece, me, opp):
    myMoves = []

    forwardMove = pieceMove(piece, piece.rank + me.rank_direction, piece.file)
    doubleForwardMove = pieceMove(piece, piece.rank + me.rank_direction * 2, piece.file)

    for p in me.pieces + opp.pieces:
        if piece.rank + me.rank_direction == p.rank and piece.file == p.file:
            forwardMove = None
            break

    for p in opp.pieces:
        if piece.rank + me.rank_direction == p.rank and getNewLetter(piece.file,1) == p.file:
            myMoves.append(pieceMove(piece, piece.rank + me.rank_direction, getNewLetter(piece.file,1)))
        if piece.rank + me.rank_direction == p.rank and getNewLetter(piece.file, -1) == p.file:
            myMoves.append(pieceMove(piece, piece.rank + me.rank_direction, getNewLetter(piece.file, -1)))

    # Pawn has not moved from base location
    # And the position immeidately front of the pawn is not blocked
    if piece.rank == 2 and forwardMove is not None:
        for p in me.pieces + opp.pieces:
            if piece.rank + me.rank_direction * 2 == p.rank and piece.file == p.file:
                doubleForwardMove = None
                break
    else:
        doubleForwardMove = None

    if forwardMove is not None:
        myMoves.append(forwardMove)

    if doubleForwardMove is not None:
        myMoves.append(doubleForwardMove)


    for move in myMoves:
        if move.rank == 1 or move.rank == 8:
            move.promotion = random.choice(["Queen","Rook", "Bishop", "Knight"])

    return myMoves

def getBishopMove(piece, me, opp):
    myMoves = []
    myPosList = getPieceCoordList(me)
    oppPosList = getPieceCoordList(opp)

    for i in range(1,8):
        if piece.rank + i == 9 or getNewLetter(piece.file, i) is "i":
            break
        else:
            if (piece.rank + i, getNewLetter(piece.file, i)) in myPosList:
                break
            elif (piece.rank + i, getNewLetter(piece.file, i)) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank + i, getNewLetter(piece.file, i)))
                break
            else:
                myMoves.append(pieceMove(piece, piece.rank + i, getNewLetter(piece.file, i)))

    for i in range(1,8):
        # Check if we go too far up or to the left
        # ' is the character that proceeds a in char values
        if piece.rank + i == 9 or getNewLetter(piece.file, -i) is "`":
            break
        else:
            if (piece.rank + i, getNewLetter(piece.file, -i)) in myPosList:
                break
            elif (piece.rank + i, getNewLetter(piece.file, -i)) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank + i, getNewLetter(piece.file, -i)))
                break
            else:
                myMoves.append(pieceMove(piece, piece.rank + i, getNewLetter(piece.file, -i)))

    for i in range(1,8):
        if piece.rank - i == 0 or getNewLetter(piece.file, i) is "i":
            break
        else:
            if (piece.rank - i, getNewLetter(piece.file, i)) in myPosList:
                break
            elif (piece.rank - i, getNewLetter(piece.file, i)) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank - i, getNewLetter(piece.file, i)))
                break
            else:
                myMoves.append(pieceMove(piece, piece.rank - i, getNewLetter(piece.file, i)))

    for i in range(1,8):
        if piece.rank - i == 0 or getNewLetter(piece.file, -i) is "`":
            break
        else:
            if (piece.rank - i, getNewLetter(piece.file, -i)) in myPosList:
                break
            elif (piece.rank - i, getNewLetter(piece.file, -i)) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank - i, getNewLetter(piece.file, -i)))
                break
            else:
                myMoves.append(pieceMove(piece, piece.rank - i, getNewLetter(piece.file, -i)))
    return myMoves


def getRookMove(piece, me, opp):
    myMoves = []
    myPosList = getPieceCoordList(me)
    oppPosList = getPieceCoordList(opp)

    for i in range(1,8):
        if piece.rank + i == 9:
            break
        else:
            # Collides with ally piece
            if (piece.rank + i, piece.file) in myPosList:
                break
            # Hit enemy piece
            elif (piece.rank + i, piece.file) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank + i, piece.file))
                break
            else:
                myMoves.append(pieceMove(piece, piece.rank + i, piece.file))

    for i in range(1,8):
        if piece.rank - i == 0:
            break
        else:
            # Collides with ally piece
            if (piece.rank - i, piece.file) in myPosList:
                break
            # Hit enemy piece
            elif (piece.rank - i , piece.file) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank - i, piece.file))
                break
            else:
                myMoves.append(pieceMove(piece, piece.rank - i, piece.file))

    for i in range(1,8):
        if getNewLetter(piece.file, i) is "i":
            break
        else:
            # Collides with ally piece
            if (piece.rank, getNewLetter(piece.file, i)) in myPosList:
                break
            # Hit enemy piece
            elif (piece.rank, getNewLetter(piece.file, i)) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank, getNewLetter(piece.file, i)))
                break
            else:
                myMoves.append(pieceMove(piece, piece.rank, getNewLetter(piece.file, i)))

    for i in range(1,8):
        if getNewLetter(piece.file, -i) is "`":
            break
        else:
            # Collides with ally piece
            if (piece.rank, getNewLetter(piece.file, -i)) in myPosList:
                break
            # Hit enemy piece
            elif (piece.rank, getNewLetter(piece.file, -i)) in oppPosList:
                myMoves.append(pieceMove(piece, piece.rank, getNewLetter(piece.file, -i)))
                break
            else:
                myMoves.append(pieceMove(piece, piece.rank, getNewLetter(piece.file, -i)))
    return myMoves

def getKnightMove(piece, me, opp):
    return []

def getQueenMove(piece, me, opp):
    return getBishopMove(piece,me,opp) + getRookMove(piece,me,opp)

def getKingMove(piece, me, opp):
    return []
