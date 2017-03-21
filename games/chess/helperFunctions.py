from copy import deepcopy


def getNewLetter(file, increment):
    """
    Finds the next letter character used for incrementing file
    :param file: Current file of a piece [a-h]
    :param increment: Positive or negative integer
    :return: Character that is incremented by new letter
             Can return any value is not limited to [a-h]
    """
    return chr(ord(file) + increment)


def getPieceCoordList(player):
    """
    Returns a list of rank, file of all pieces for a given player
    :param player: Player or myPlayer class
    :return: A list with tuples of form (rank, file)
    """
    pieceCoordList = []
    for piece in player.pieces:
        pieceCoordList.append((piece.rank, piece.file))

    return pieceCoordList


def isSquareOccupied(rank, file, allPieces):
    """
    Checks is a square has a piece in it
    :param rank: Rank to check
    :param file: File to check
    :param allPieces: List of pieces to check
    :return: True if rank and file are found in all pieces False if not
    """
    for p in allPieces:
        if p.rank == rank and p.file == file:
            return True
    return False


def getRealPiece(piece, player):
    """
    Used for getting the MegaMiner AI Piece object for calling the move function
    :param piece: myPiece object that a match is to be found for
    :param player: MegaMiner AI Player class who owns the piece
    :return: The matching piece in the pieceList
    """
    return getPieceFromList(piece, player.pieces)


def getPieceFromList(piece, pieceList):
    """
        Used for getting a specified Piece object from a Piece list
        Used for the interchange of pieces between myPlayer and Player classes
        :param piece: myPiece object that a match is to be found for
        :param pieceList: List of all pieces to find
        :return: The matching piece in the pieceList
    """
    for p in pieceList:
        if p.rank == piece.rank and p.file == piece.file:
            return p


def getRankDirection(color):
    """
    Returns integer value specifying which way the rank moves for a color
    :param color: White or Black
    :return: 1 or -1 based on color
    """
    if color == "White":
        return 1
    else:
        return -1


def getPieceListAfterMove(pieceList, move):
    """
    Updated list of pieces after a move is made
    :param pieceList: A list of pieces for both players
    :param move: A pieceMove object that was made
    :return: Updated list, with any captured pieces removed
    """
    allPieces = deepcopy(pieceList)
    piece = getPieceFromList(move.piece, allPieces)

    allPieces.remove(piece)
    for p in allPieces:
        if move.rank == p.rank and move.file == p.file:
            # Check for King moving into its own rook for castling
            if p.type == "Rook" and p.color == move.piece.color:
                # Update rooks position
                if p.file == "h":
                    p.file = "g"
                elif p.file == "a":
                    p.file = "b"

            else:
                allPieces.remove(p)

            break

    piece.rank = move.rank
    piece.file = move.file

    if move.promotion != "" and piece.type == "Pawn":
        piece.type = move.promotion

    allPieces.append(piece)

    return allPieces


def getPieceInSquare(rank, file, allPieces):
    """
    Gets the piece located at a specific rank and file
    :param rank: The rank of the piece
    :param file: The file of the piece
    :param allPieces: List of all pieces to look for
    :return: Returns a piece if found or None if there is no piece at that location
    """
    for p in allPieces:
        if p.rank == rank and p.file == file:
            return p
    return None


def findKing(pieces):
    """
    Return of the king
    :param pieces: List of pieces for a single player
    :return: The king is returned
    """
    for p in pieces:
        if p.type == "King":
            return p


def getOppositeColorStr(color):
    """
    Returns the opposite color of the string
    :param color: Color as a string
    :return: Color as a string
    """
    if color == "White":
        return "Black"
    else:
        return "White"


def myMoveCapture(move, myGame):
    """
    Returns if the move made captured a piece
    :param move: Move to be made
    :param myGame: The game state before the move is made
    :return: True if a piece is captured
    """
    for p in myGame.whitePlayer.pieces + myGame.blackPlayer.pieces:
        # Check if a piece was captured and ignores castling
        if p.rank == move.rank and p.file == move.file and p.color != move.piece.color:
            return True
    return False
