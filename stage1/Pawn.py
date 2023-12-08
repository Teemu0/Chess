from Piece import Piece

class Pawn(Piece):
    def __init__(self, color, name, img_id):
        super().__init__(color, name, img_id)

    def moveLogic(self, gameBoard, startRow, startCol, endRow, endCol):
        if startRow == endRow and startCol == endCol:
            return False
        # WHITE PAWN LOGIC
        elif self.color == "white":
            # Promotion:
            # if pawn is on the 7th rank
            if startRow == 1:
                # TODO: About to promote
                return False

            # Moving one square up:
            # if start and end are on the same file AND end is 1 rank above start AND end square is empty
            elif endCol == startCol and endRow == startRow - 1 and gameBoard[endRow][endCol].color == None:
                return True

            # Moving two squares up:
            # if starting square is on 2nd rank AND start and end are on the same file AND end is 2 ranks above start AND traveled squares are empty
            elif startRow == 6 and endCol == startCol and endRow == startRow - 2 and gameBoard[endRow][endCol].color == None == gameBoard[startRow-1][startCol].color:
                return True
            
            # Capturing a piece (include this in promotion!):
            # if end is 1 rank above start AND end is 1 file next to start AND there is a black piece in end
            elif (startRow-1 == endRow) and (startCol == endCol-1 or startCol == endCol+1) and (gameBoard[endRow][endCol].color == "black"):
                return True

        # BLACK PAWN LOGIC
        elif self.color == "black":
            # Promotion:
            if startRow == 6:
                # TODO: About to promote
                pass

            # Moving one square down:
            # if start and end are on the same file AND end is 1 rank above start AND end square is empty
            elif endCol == startCol and endRow == startRow + 1 and gameBoard[endRow][endCol].color == None:
                return True

            # Moving two squares down:
            # if starting square is on 2nd rank AND start and end are on the same file AND end is 2 ranks above start AND traveled sqaures are empty
            elif startRow == 1 and endCol == startCol and endRow == startRow + 2 and gameBoard[endRow][endCol].color == None == gameBoard[startRow+1][startCol].color:
                return True
            
            # Capturing a piece (include this in promotion!):
            # if end is 1 rank below start AND end is 1 file next to start AND there is a white piece in end
            elif (startRow+1 == endRow) and (startCol == endCol-1 or startCol == endCol+1) and (gameBoard[endRow][endCol].color == "white"):
                return True
            
        return False

    def testprint(self):
        print("print from pawn")

# class Rook(Piece):
#     def __init__(self, color, name):
#         super().__init__(color, name)


# pawn = Pawn("white", "pawn")
# rook = Rook("black", "rook")

# board = [[pawn, pawn, pawn, pawn],
#          ["", "", "", ""],
#          [rook, "", "", ""],
#          [pawn, pawn, pawn, pawn]]

# print(board[0])
# print(board[0][0])

# pieceToMove = board[3][1]

# startRow = 3
# startCol = 1
# pieceToCapture = board[2][0]
# endRow = 2
# endCol = 0

# WHITE_PIECES = ["wKing", "wQueen", "wRook", "wBishop", "wKnight", "wPawn"]
# BLACK_PIECES = ["bKing", "bQueen", "bRook", "bBishop", "bKnight", "bPawn"]

# result = pieceToMove.pawnLogic(board, pieceToCapture, startRow, startCol, endRow, endCol)

# print(f"pawnLogic result; move was done? {result}")