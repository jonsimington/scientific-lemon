from copy import deepcopy

def getNewLetter(file, increment):
    return chr(ord(file) + increment)


def getPieceCoordList(player):
    pieceCoordList = []
    for piece in player.pieces:
        pieceCoordList.append((piece.rank, piece.file))

    return pieceCoordList

def isSquareOccupied(rank, file, allPieces):
    for p in allPieces:
        if p.rank == rank and p.file == file:
            return True
    return False

def getRealPiece(piece, player):
    for p in player.pieces:
        if p.rank == piece.rank and p.file == piece.file:
            return p


def getPieceFromList(piece, pieceList):
    for p in pieceList:
        if p.rank == piece.rank and p.file == piece.file:
            return p


def getRankDirection(color):
    if color == "White":
        return 1
    else:
        return -1


def generateFen(myGame, move, currPlayerColor):
    fen = ""
    allPieces = getPieceListAfterMove(myGame.whitePlayer.pieces + myGame.blackPlayer.pieces, move)

    blankSpace = 0

    for rank in range(8,0,-1):
        # Used for letters
        for file in range(ord("a"),ord("i")):
            piece = getPieceInSquare(rank, chr(file), allPieces)

            if piece is not None:
                if blankSpace > 0:
                    fen += str(blankSpace)
                    blankSpace = 0
                fen += getLetterForColor(piece.type, piece.color)

            else:
                blankSpace += 1

        if blankSpace > 0:
            fen += str(blankSpace)
            blankSpace = 0

        fen += "/"
    fen += " "
    fen += getOppositeColorChar(currPlayerColor)
    fen += getKingQueenCastleStr(move, myGame)

    if currPlayerColor == "White":
        fen += getPassantStr(myGame, move, 1)
    else:
        fen += getPassantStr(myGame, move, -1)

    return fen

def getPieceListAfterMove(pieceList, move):
    allPieces = deepcopy(pieceList)
    piece = getPieceFromList(move.piece, allPieces)

    allPieces.remove(piece)
    for p in allPieces:
        if move.rank == p.rank and move.file == p.file:
            allPieces.remove(p)
            break

    piece.rank = move.rank
    piece.file = move.file
    allPieces.append(piece)

    return allPieces



def getKingQueenCastleStr(move, myGame):
    fen = " "

    if myGame.whitePlayer.canKingCastle and move.piece.type != "Rook" and move.piece.file != "h":
        fen += "K"
    else:
        fen += "-"

    if myGame.whitePlayer.canQueenCastle and move.piece.type != "Rook" and move.piece.file != "a":
        fen += "Q"
    else:
        fen += "-"

    if myGame.blackPlayer.canKingCastle and move.piece.type != "Rook" and move.piece.file != "h":
        fen += "k"
    else:
        fen += "-"

    if myGame.blackPlayer.canQueenCastle and move.piece.type != "Rook" and move.piece.file != "a":
        fen += "q"
    else:
        fen += "-"

    return fen

def getPassantStr(myGame,move, rankDirection):
    fen = " "
    if move.piece.type == "Pawn" and ((move.piece.rank == 7 and move.piece.color == "Black") or (move.piece.rank == 2 and move.piece.color == "White")) and (move.piece.rank + rankDirection * 2) == move.rank:
        fen += (move.file  + str(move.rank - rankDirection))
    else:
        fen += "-"
    return fen

def getPieceInSquare(rank,file,allPieces):
    for p in allPieces:
        if p.rank == rank and p.file == file:
            return p
    return None

def getOppositeColorChar(color):
    if color == "White":
        return "b"
    else:
        return "w"

def findKing(pieces):
    for p in pieces:
        if p.type == "King":
            return p


def getLetterForColor(type, color):
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


