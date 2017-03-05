

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


def getRankDirection(color):
    if color == "White":
        return 1
    else:
        return -1

