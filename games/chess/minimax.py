from games.chess.generateMoves import getMove, checkIfInCheck
from games.chess.fenHelper import generateFen
from games.chess.gameState import *
import random

class moveScore:
    def __init__(self, move,score):
        self.myMove = move
        self.myScore = score

def minimaxMove(myGame, depth, playerMoveColor, myColor):

    # List of all possible moves
    moveList = getMove(myGame, playerMoveColor)

    # Final list of possible moves
    validMoves= []

    # Check if any moves put the player in check
    for move in moveList:
        # Creates a FEN based on the move made
        newFen = generateFen(myGame, move, playerMoveColor)

        # Validates no illegal moves are made
        if not checkIfInCheck(newFen, playerMoveColor):
            score = getMinMove(newFen, depth, playerMoveColor, myColor)
            validMoves.append(moveScore(move, score))

    # Best possible move
    bestMove = []

    # Default the score to really low value
    currScore = -999
    allScore = ""
    for move in validMoves:
        allScore += ", " + str(move.myScore)

        if move.myScore is not None and move.myScore > currScore:
            bestMove = [move.myMove]
            currScore = move.myScore

        elif move.myScore == currScore:
                bestMove.append(move.myMove)

    print("MINIMAX Score:    " + str(allScore))
    print("MINIMAX RESULT:    " + str(currScore))

    return random.choice(bestMove)


def getMaxMove(fen, depth, playerMoveColor, myColor):
    myGame = gameState(fen)

    if depth <= 0:
        if myColor == "Black":
            return myGame.blackPlayer.score - myGame.whitePlayer.score
        else:
            return myGame.whitePlayer.score - myGame.blackPlayer.score

    else:
        # List of all possible moves
        moveList = getMove(myGame, playerMoveColor)

        # Final list of possible moves
        validMoves= []

        # Check if any moves put the player in check
        for move in moveList:
            # Creates a FEN based on the move made
            newFen = generateFen(myGame, move, playerMoveColor)

            # Validates no illegal moves are made
            if not checkIfInCheck(newFen, playerMoveColor):
                score = getMinMove(newFen, depth - 1, getOppositeColorStr(playerMoveColor), myColor)
                validMoves.append(moveScore(move, score))

        # Best possible score
        currScore = -999
        for move in validMoves:
            # Check that the move has a score, it will not if the game ends
            if move.myScore is not None and move.myScore > currScore:
                currScore = move.myScore

        # Default the score to really low value
        if currScore == -999:
            return None
        else:
            return currScore


def getMinMove(fen, depth, playerMoveColor, myColor):
    myGame = gameState(fen)

    if depth <= 0:
        if myColor == "Black":
            return myGame.blackPlayer.score - myGame.whitePlayer.score
        else:
            return myGame.whitePlayer.score - myGame.blackPlayer.score


    else:
        # List of all possible moves
        moveList = getMove(myGame, playerMoveColor)

        # Final list of possible moves
        validMoves= []

        # Check if any moves put the player in check
        for move in moveList:
            # Creates a FEN based on the move made
            newFen = generateFen(myGame, move, playerMoveColor)

            # Validates no illegal moves are made
            if not checkIfInCheck(newFen, playerMoveColor):
                score = getMaxMove(newFen, depth - 1, getOppositeColorStr(playerMoveColor), myColor)
                validMoves.append(moveScore(move, score))

        # Best possible score
        # Default the score to really largevalue
        currScore = 999
        for move in validMoves:
            # Check that the move has a score, it will not if the game ends
            if move.myScore is not None and move.myScore < currScore:
                currScore = move.myScore

        if currScore == 999:
            return None
        else:
            return currScore
