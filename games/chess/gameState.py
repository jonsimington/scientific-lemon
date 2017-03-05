from games.chess.helperFunctions import  *

class gameState:
    def __init__(self,fen):
        self.player1 = myPlayer("White", fen)
        self.player2 = myPlayer("Black", fen)
        self.enPassantTarget = self.getPassantTarget(fen)

    def getPassantTarget(self, fen):
        fenSplit = fen.split()
        return fenSplit[3]



class myPlayer:
    def __init__(self, color, fen):
            self.color = color
            self.canQueenCastle = False
            self.canKingCastle = False
            self.myMove = False
            self.rank_direction = getRankDirection(color)
            self.pieces = []

            self.parseFen(fen, color)

    def parseFen(self, fen, color):
        myPieces = []
        rank = 8
        file = "a"

        fenSplit = fen.split()

        for letter in fenSplit[0]:

            if letter == "/":
                rank -= 1
                file = "a"
            elif letter.isdigit():
                file = getNewLetter(file, int(letter))

            elif (letter == "P" and color == "White") or (letter == "p" and color == "Black"):
                myPieces.append(myPiece(file, rank, "Pawn"))
                file = getNewLetter(file, 1)

            elif (letter == "R" and color == "White") or (letter == "r" and color == "Black"):
                myPieces.append(myPiece(file, rank, "Rook"))
                file = getNewLetter(file, 1)

            elif (letter == "N" and color == "White") or (letter == "n" and color == "Black"):
                myPieces.append(myPiece(file, rank, "Knight"))
                file = getNewLetter(file, 1)

            elif (letter == "B" and color == "White") or (letter == "b" and color == "Black"):
                myPieces.append(myPiece(file, rank, "Bishop"))
                file = getNewLetter(file, 1)


            elif (letter == "Q" and color == "White") or (letter == "q" and color == "Black"):
                myPieces.append(myPiece(file, rank, "Queen"))
                file = getNewLetter(file, 1)

            elif (letter == "K" and color == "White") or (letter == "k" and color == "Black"):
                myPieces.append(myPiece(file, rank, "King"))
                file = getNewLetter(file, 1)

        self.pieces = myPieces


        if fenSplit[1] == "w" and color == "White":
            self.myMove = True
        else:
            self.myMove = True

        for letter in fenSplit[2]:
            if (letter == "K" and color == "White") or (letter == "k" and color == "Black"):
                self.canKingCastle = True
            elif (letter == "Q" and color == "White") or (letter == "q" and color == "Black"):
               self.canQueenCastle = True





class myPiece:
    def __init__(self, file, rank, type):
            self.file = file
            self.rank = rank
            self.type = type


def getGameState(fen):
    return (fen)
