from games.chess.generateMoves import getMove, checkIfInCheck
from games.chess.fenHelper import generateFen
from games.chess.gameState import *
import random


class moveScore:
    def __init__(self, move, score):
        self.myMove = move
        self.myScore = score

def minimaxMove(myGame, depth, playerMoveColor, changeCount, moveHistory, turnNum):
    """
    The minimax calculation of the game at the current state
    :param myGame: The current game state
    :param depth: Depth to traverse
    :param playerMoveColor: Player that is moving
    :param changeCount: How many turns since the last change of pawn or capture
    :param moveHistory: Move history used for checking for a similar state
    :param turnNum: Current overall turn number
    :return: Best possible move to be made to maximize heuristic value
    """

    # Reset alpha beta values for pruning
    alpha = -999
    beta = 999

    # List of all possible moves
    moveList = getMove(myGame, playerMoveColor)

    # Final list of possible moves
    validMoves = []

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

            score = getMinMove(newFen, depth - 1, getOppositeColorStr(playerMoveColor), playerMoveColor,
                               tempChangeCount, newMoveHistory, tempTurnNum, alpha, beta)

            if score is not None:
                if score > alpha:
                    alpha = score
                    # Empty list of moves worse than current move score
                    validMoves = []
                    validMoves.append(moveScore(move, score))
                elif score == alpha:
                    validMoves.append(moveScore(move, score))

    return random.choice(validMoves).myMove, alpha


def getMaxMove(fen, depth, playerMoveColor, myColor, changeCount, moveHistory, turnNum, alpha, beta):
    """
    Gets the max possible move for the passed FEN state
    :param fen: FEN state to create moves for
    :param depth: How much further to evaluated
    :param playerMoveColor: Player to move for this turn
    :param myColor: My actual color
    :param changeCount: How many turns since a change has occured
    :param moveHistory: History of all moves made in the last 8 turns
    :param turnNum: Current turn number
    :return: Best possible move to make
    """
    # Ignores moves where the game has ended
    if "K" in fen and "k" in fen:
        highscore = None

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

            # Check if any moves put the player in check
            for move in moveList:
                # Creates a FEN based on the move made
                newFen = generateFen(myGame, move, playerMoveColor)

                if not checkIfInCheck(newFen, playerMoveColor):
                    # Create a copy of move history
                    newMoveHistory = deepcopy(moveHistory)
                    tempTurnNum = turnNum + 1
                    # Add newly made move to history
                    newMoveHistory[tempTurnNum % 8] = createMoveTuple(move)
                    # Updates change count
                    tempChangeCount = updateChangeCount(changeCount, move, myGame)

                    score = getMinMove(newFen, depth - 1, getOppositeColorStr(playerMoveColor), myColor,
                                       tempChangeCount, newMoveHistory, tempTurnNum, alpha, beta)

                    # Make sure a value is returned
                    if score is not None:
                        # Fail High Prune
                        if score >= beta:
                            print("BETA PRUNE: "+ str(beta) + "\t" + str(score))
                            return score
                        # Update alpha value
                        elif score > alpha:
                            alpha = score

                        # Set new best score found
                        if highscore is None or score > highscore :
                            highscore = score

        return highscore
    else:
        return None


def getMinMove(fen, depth, playerMoveColor, myColor, changeCount, moveHistory, turnNum, alpha, beta):
    """
    Gets the min possible move for the passed FEN state
    :param fen: FEN state to create moves for
    :param depth: How much further to evaluated
    :param playerMoveColor: Player to move for this turn
    :param myColor: My actual color
    :param changeCount: How many turns since a change has occured
    :param moveHistory: History of all moves made in the last 8 turns
    :param turnNum: Current turn number
    :return: Best possible move to make for MIN player
    """
    # Ignores moves where the game has ended
    if "K" in fen and "k" in fen:
        highscore = None

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

                    score = getMaxMove(newFen, depth - 1, getOppositeColorStr(playerMoveColor), myColor,
                                       tempChangeCount, newMoveHistory, tempTurnNum, alpha, beta)

                    if score is not None:
                        if score <= alpha:
                            print("ALPHA PRUNE: " + str(alpha) + "\t" + str(score))
                            return score
                        elif score < beta:
                            beta = score

                        if highscore is None or score > highscore :
                            highscore = score
        return  highscore
    else:
        return None


def heuristicScore(blackScore, whiteScore, myColor):
    """
    Calculates the heuristic score at state
    :param blackScore: Score of black player
    :param whiteScore: Score of the white player
    :param myColor: My color
    :return: Score as an int
    """
    if myColor == "Black":
        return blackScore - whiteScore
    else:
        return whiteScore - blackScore


def checkForDraw(changeCount, moveHistory):
    """
    Checks for a draw state
    :param changeCount: How many moves since last state change
    :param moveHistory: History of 8 moves
    :return: Returns true if the state will end in a draw
    """
    if changeCount == 8:
        return True

    # Check that movehistory has 8 moves
    for i in moveHistory:
        if i is None:
            return False

    # Check if the last moves 8 are all equal
    if moveHistory[0] == moveHistory[4] and \
                    moveHistory[1] == moveHistory[5] and \
                    moveHistory[2] == moveHistory[6] and \
                    moveHistory[3] == moveHistory[7]:
        return True

    return False


def createMoveTuple(move):
    """
    Creates a movement tuple for the tuple in form (old position, new position)
    :param move: Move to make as a myMove object
    :return: String tuple of move
    """
    # Store the move into move history table
    oldPos = move.piece.file + str(move.piece.rank)
    newPos = move.file + str(move.rank)
    pieceType = move.piece.type

    return (oldPos, newPos, pieceType)


def createMoveTupleFromGame(game):
    """
    Creates a movement tuple in form (old position, new position)
    :param game: MegaMiner game object
    :return: String tuple of move
    """
    # Store my opponents move in history
    oldPos = game.moves[-1].from_file + str(game.moves[-1].from_rank)
    newPos = game.moves[-1].to_file + str(game.moves[-1].to_rank)
    pieceType = game.moves[-1].piece.type
    return (oldPos, newPos, pieceType)


def updateChangeCount(changeCount, move, myGame):
    """
    Updates the change count counter
    :param changeCount: Current change count value
    :param move: Move object to be made as
    :param myGame: A myGame object of the current state
    :return: Updated change count as int
    """
    if move.piece.type == "Pawn" or myMoveCapture(move, myGame):
        return 0
    else:
        return changeCount + 1


def updateChangeCountFromGame(game, turnWithoutChange):
    """
    Updates the change count counter
    :param game: Megaminer game object
    :param turnWithoutChange: turns without a change
    :return: Updated change count as int
    """
    # Checks if a capture or panw movement occured
    if game.moves[-1].piece == "Pawn" or game.moves[-1].captured is not None or game.moves[-1].promotion is not "":
        return 0
    else:
        return turnWithoutChange + 1
