from games.chess.generateMoves import getMove, checkIfInCheck
from games.chess.fenHelper import generateFen


def minimaxMove(myGame, depth, playerColor):

    # List of all possible moves
    moveList = getMove(myGame, playerColor)

    # Final list of possible moves
    validMoves= []

    # Check if any moves put the player in check
    for move in moveList:
        # Creates a FEN based on the move made
        newFen = generateFen(myGame, move, playerColor)

        # Validates no illegal moves are made
        if not checkIfInCheck(newFen, playerColor):
            score = getMaxMove(newFen, depth - 1, playerColor)
            validMoves.append((move, score))

    return validMoves[0][0]

def getMaxMove(fen, depth, playerColor):
    if depth <= 0:
        if playerColor == "Black":
            return


