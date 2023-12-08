
class Piece:
    def __init__(self, color, name, img_id):
        self.color = color
        self.name = name
        self.img_id = img_id

    # The __repr__ is used to compute the “official” string representation of an object
    def __repr__(self):
        return str(self)
    
    # The __str__() dunder method returns a reader-friendly string representation of a class object
    def __str__(self):
        return self.color + " " + self.name
    
    def getMoves(self, gameboard, startRow, startCol):
        legalMoves = []
        isCheck = False
        for row in range(8):
            for col in range(8):
                # If move is legal
                if self.moveLogic(gameboard, startRow, startCol, row, col):
                    legalMoves.append((row, col))
                    # If opponent's king is under attack
                    if gameboard[row][col].name == "king":
                        isCheck = True
        print(legalMoves, isCheck)
        return isCheck
    


'''
class Pawn(Piece):
    def __init__(self, color, name):
        super().__init__(color, name)

    def pawnLogic(self, gameBoard, pieceToCapture, startRow, startCol, endRow, endCol):
        # WHITE PAWN LOGIC
        if self.color == "white":
            # Promotion:
            # if pawn is on the 7th rank
            if startRow == 1:
                # TODO: About to promote
                return False

            # Moving one square up:
            # if start and end are on the same file AND end is 1 rank above start AND end square is empty
            elif endCol == startCol and endRow == startRow - 1 and gameBoard[endRow][endCol] == "":
                gameBoard[endRow][endCol] = self
                gameBoard[startRow][startCol] = ""
                return True

            # Moving two squares up:
            # if starting square is on 2nd rank AND start and end are on the same file AND end is 2 ranks above start AND traveled squares are empty
            elif startRow == 6 and endCol == startCol and endRow == startRow - 2 and gameBoard[endRow][endCol] == "" == gameBoard[startRow-1][startCol]:
                gameBoard[endRow][endCol] = self
                gameBoard[startRow][startCol] = ""
                return True
            
            # Capturing a piece (include this in promotion!):
            # if end is 1 rank above start AND end is 1 file next to start AND there is a black piece in end
            elif (startRow-1 == endRow) and (startCol == endCol-1 or startCol == endCol+1) and (pieceToCapture.color == "black"):
                gameBoard[endRow][endCol] = self
                gameBoard[startRow][startCol] = ""
                return True

        # BLACK PAWN LOGIC
        elif self.color == "black":
            # Promotion:
            if startRow == 6:
                # TODO: About to promote
                pass

            # Moving one square down:
            # if start and end are on the same file AND end is 1 rank above start AND end square is empty
            elif endCol == startCol and endRow == startRow + 1 and gameBoard[endRow][endCol] == "":
                gameBoard[endRow][endCol] = self
                gameBoard[startRow][startCol] = ""
                return True

            # Moving two squares down:
            # if starting square is on 2nd rank AND start and end are on the same file AND end is 2 ranks above start AND traveled sqaures are empty
            elif startRow == 1 and endCol == startCol and endRow == startRow + 2 and gameBoard[endRow][endCol] == "" == gameBoard[startRow+1][startCol]:
                gameBoard[endRow][endCol] = self
                gameBoard[startRow][startCol] = ""
                return True
            
            # Capturing a piece (include this in promotion!):
            # if end is 1 rank below start AND end is 1 file next to start AND there is a white piece in end
            elif (startRow+1 == endRow) and (startCol == endCol-1 or startCol == endCol+1) and (pieceToCapture.color == "white"):
                gameBoard[endRow][endCol] = self
                gameBoard[startRow][startCol] = ""
                return True
            
        return False

    def testprint(self):
        print("print from pawn")

class Rook(Piece):
    def __init__(self, color, name):
        super().__init__(color, name)


pawn = Pawn("white", "pawn")
rook = Rook("black", "rook")

board = [[pawn, pawn, pawn, pawn],
         ["", "", "", ""],
         [rook, "", "", ""],
         [pawn, pawn, pawn, pawn]]

print(board[0])
print(board[0][0])

pieceToMove = board[3][1]

startRow = 3
startCol = 1
pieceToCapture = board[2][0]
endRow = 2
endCol = 0

WHITE_PIECES = ["wKing", "wQueen", "wRook", "wBishop", "wKnight", "wPawn"]
BLACK_PIECES = ["bKing", "bQueen", "bRook", "bBishop", "bKnight", "bPawn"]

result = pieceToMove.pawnLogic(board, pieceToCapture, startRow, startCol, endRow, endCol)

print(f"pawnLogic result; move was done? {result}")

'''