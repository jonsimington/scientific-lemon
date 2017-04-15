# This is where you build your AI for the Chess game.
from joueur.base_ai import BaseAI
from games.chess.generateMoves import *
from games.chess.fenHelper import generateFen

from games.chess.minimax import *
import datetime
import random

# Global depth limit
DEPTHLIMIT = 999
# Global time limit per turn in microseconds
TIMELIMIT = 1000000

# Last 8 turns
moveHistory = [None] * 8
# Current turn number for myself
turnNum = 0
# Track turns without pawn, promotions or capture for 8 turn tie rule
turnWithoutChange = 0

class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    def get_name(self):
        """ This is the name you send to the server so your AI will control the
		player named this string.

		Returns
			str: The name of your Player.
		"""

        return "Tim Buesking"  # REPLACE THIS WITH YOUR TEAM NAME

    def start(self):
        """ This is called once the game starts and your AI knows its playerID
		and game. You can initialize your AI here.
		"""

    # replace with your start logic

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are
		tracking anything you can update it here.
		"""

    # replace with your game updated logic

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and
		dump files here if need be.

		Args:
			won (bool): True means you won, False means you lost.
			reason (str): The human readable string explaining why you won or
						  lost.
		"""

    # replace with your end logic
    def print_current_board(self):
        """Prints the current board using pretty ASCII art
		Note: you can delete this function if you wish
		"""

        # iterate through the range in reverse order
        for r in range(9, -2, -1):
            output = ""
            if r == 9 or r == 0:
                # then the top or bottom of the board
                output = "   +------------------------+"
            elif r == -1:
                # then show the ranks
                output = "     a  b  c  d  e  f  g  h"
            else:  # board
                output = " " + str(r) + " |"
                # fill in all the files with pieces at the current rank
                for file_offset in range(0, 8):
                    # start at a, with with file offset increasing the char
                    f = chr(ord("a") + file_offset)
                    current_piece = None
                    for piece in self.game.pieces:
                        if piece.file == f and piece.rank == r:
                            # then we found the piece at (file, rank)
                            current_piece = piece
                            break

                    code = "."  # default "no piece"
                    if current_piece:
                        # the code will be the first character of their type
                        # e.g. 'Q' for "Queen"
                        code = current_piece.type[0]

                        if current_piece.type == "Knight":
                            # 'K' is for "King", we use 'N' for "Knights"
                            code = "N"

                        if current_piece.owner.id == "1":
                            # the second player (black) is lower case.
                            # Otherwise it's uppercase already
                            code = code.lower()

                    output += " " + code + " "

                output += "|"
            print(output)

    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

		Returns:
			bool: Represents if you want to end your turn. True means end your
				  turn, False means to keep your turn going and re-call this
				  function.
		"""

        # Used to track states persistently from my and opponents move
        global turnWithoutChange
        global turnNum

        # print the board to the console

        # print the opponent's last move to the console
        if len(self.game.moves) > 0:

            # Adds the previously made opponent move to history
            moveHistory[turnNum % 8] = createMoveTupleFromGame(self.game)
            turnNum += 1

            # Checks for the number of turns without change form opponent
            turnWithoutChange = updateChangeCountFromGame(self.game, turnWithoutChange)

        # Generate a game state
        myGame = gameState(self.game.fen)
        startTime = datetime.datetime.now()

        # History table of moves
        historyTable = {}
        for i in range(0, DEPTHLIMIT):
            # Calculate time spent searching in microseconds
            timeSpent = (datetime.datetime.now() - startTime)
            timeInMicro = timeSpent.seconds * 1000000 + timeSpent.microseconds

            if timeInMicro < TIMELIMIT:
                # Select the move to make
                moveToMake, score = minimaxMove(myGame, i, self.player.color, turnWithoutChange, moveHistory, turnNum, historyTable, 2)
            else:
                print(str(i-1))
                break


        # Gets the Megaminer piece that is equivalent to my piece
        piece = getRealPiece(moveToMake.piece, self.player)

        # Update move history
        moveHistory[turnNum % 8] = createMoveTuple(moveToMake)
        turnNum += 1

        # Update no change turn count
        turnWithoutChange = updateChangeCount(turnWithoutChange, moveToMake, myGame)

        # Make the piece move
        piece.move(moveToMake.file, moveToMake.rank, moveToMake.promotion)

        return True  # to signify we are done with our turn.
