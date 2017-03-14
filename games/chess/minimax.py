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
            score = getMinMove(newFen, depth - 1, playerMoveColor, myColor)
            validMoves.append(moveScore(move, score))

    # Best possible move
    bestMove = []
    currScore = -999
    for move in validMoves:
        if move.myScore > currScore:
            bestMove= [move.myMove]
            currScore = move.myScore

        elif move.myScore == currScore:
            bestMove.append(move.myMove)

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
            if move.myScore > currScore:
                currScore = move.myScore

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
        currScore = 999
        for move in validMoves:
            if move.myScore < currScore:
                currScore = move.myScore

        return currScore
