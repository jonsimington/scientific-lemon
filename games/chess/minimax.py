from games.chess.generateMoves import getMove, checkIfInCheck
from games.chess.fenHelper import generateFen
from games.chess.gameState import *
import random

class moveScore:
    def __init__(self, move,score):
        self.myMove = move
        self.myScore = score

def minimaxMove(myGame, depth, playerMoveColor, changeCount, moveHistory, turnNum):

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

            # Create a copy of move history
            newMoveHistory = deepcopy(moveHistory)
            tempTurnNum = turnNum + 1
            # Add newly made move to history
            newMoveHistory[tempTurnNum % 8] = createMoveTuple(move)
            # Updates change count
            tempChangeCount = updateChangeCount(changeCount, move, myGame)


            score = getMinMove(newFen, depth - 1, getOppositeColorStr(playerMoveColor), playerMoveColor, tempChangeCount, newMoveHistory, tempTurnNum)
            validMoves.append(moveScore(move, score))

    # Best possible move
    bestMove = []

    # Default the score to really low value
    currScore = -999
    for move in validMoves:
        if move.myScore is not None and move.myScore > currScore:
            bestMove = [move.myMove]
            currScore = move.myScore
        elif move.myScore == currScore:
                bestMove.append(move.myMove)

    return random.choice(bestMove), currScore


def getMaxMove(fen, depth, playerMoveColor, myColor, changeCount, moveHistory, turnNum):
    # Ignores moves where the game has ended
    if "K" in fen and "k" in fen:
        myGame = gameState(fen)

        # Check if this move creates a draw
        if checkForDraw(changeCount, moveHistory):
            return 0

         # Recursive base case
        if depth <= 0:
            return heuristicScore(myGame.blackPlayer.score, myGame.whitePlayer.score, myColor)

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

                # Create a copy of move history
                newMoveHistory = deepcopy(moveHistory)
                tempTurnNum = turnNum + 1
                # Add newly made move to history
                newMoveHistory[tempTurnNum % 8] = createMoveTuple(move)
                # Updates change count
                tempChangeCount = updateChangeCount(changeCount, move, myGame)

                if not checkIfInCheck(newFen, playerMoveColor):
                    score = getMinMove(newFen, depth - 1, getOppositeColorStr(playerMoveColor), playerMoveColor, tempChangeCount, newMoveHistory, tempTurnNum)
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
    else:
        return None


def getMinMove(fen, depth, playerMoveColor, myColor, changeCount, moveHistory, turnNum):
    # Ignores moves where the game has ended
    if "K" in fen and "k" in fen:

        myGame = gameState(fen)

        # Check if this move creates a draw
        if checkForDraw(changeCount, moveHistory):
            return 0

        # Recursive base case
        elif depth <= 0:
            return heuristicScore(myGame.blackPlayer.score, myGame.whitePlayer.score, myColor)

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

                    # Create a copy of move history
                    newMoveHistory = deepcopy(moveHistory)
                    tempTurnNum = turnNum + 1
                    # Add newly made move to history
                    newMoveHistory[tempTurnNum % 8] = createMoveTuple(move)
                    # Updates change count
                    tempChangeCount = updateChangeCount(changeCount, move, myGame)

                    score = getMaxMove(newFen, depth - 1, getOppositeColorStr(playerMoveColor), playerMoveColor,
                                       tempChangeCount, newMoveHistory, tempTurnNum)
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
    else:
        return None


def heuristicScore(blackScore, whiteScore, myColor):
    if myColor == "Black":
        return blackScore - whiteScore
    else:
        return whiteScore - blackScore


def checkForDraw(changeCount, moveHistory):
    if changeCount == 8:
        return True

    # Check that movehistory has 8 moves
    for i in moveHistory:
        if i is None:
            return False

    # Check if the last moves 8 are all equal
    if moveHistory[0][0] == moveHistory[4][0] and moveHistory[0][1] == moveHistory[4][1] and \
        moveHistory[1][0] == moveHistory[5][0] and moveHistory[1][1] == moveHistory[5][1] and \
        moveHistory[2][0] == moveHistory[6][0] and moveHistory[2][1] == moveHistory[6][1] and \
        moveHistory[3][0] == moveHistory[7][0] and moveHistory[3][1] == moveHistory[7][1]:
        return True

    return False


def createMoveTuple(move):
    # Store the move into move history table
    oldPos = move.piece.file + str(move.piece.rank)
    newPos = move.file + str(move.rank)

    return (oldPos, newPos)

def createMoveTupleFromGame(game):
    # Store my opponents move in history
    oldPos = game.moves[-1].from_file + str(game.moves[-1].from_rank)
    newPos = game.moves[-1].to_file + str(game.moves[-1].to_rank)

    return (oldPos,newPos)

def updateChangeCount(changeCount, move, myGame):
    if move.piece.type == "Pawn" or myMoveCapture(move, myGame):
        return 0
    else:
        return  changeCount + 1