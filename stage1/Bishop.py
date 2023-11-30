from Piece import Piece
from Empty import Empty

class Bishop(Piece):
    def __init__(self, color, name, img_id):
        super().__init__(color, name, img_id)
    
    def moveLogic(self, gameBoard, pieceToCapture, startRow, startCol, endRow, endCol):
        # If moving diagonally
        if abs(startRow - endRow) == abs(startCol - endCol):
            # If moving up left
            if (startRow - endRow) == (startCol - endCol) > 0:
                for index in range(abs(startRow-endRow)-1):
                        if gameBoard[startRow-1-index][startCol-1-index].color != None:
                            return False
            # If moving down right
            elif (startRow - endRow) == (startCol - endCol) < 0:
                for index in range(abs(startRow-endRow)-1):
                        if gameBoard[startRow+1+index][startCol+1+index].color != None:
                            return False
            # If moving up right
            elif (startRow - endRow) == (startCol - endCol) * (-1) > 0:
                for index in range(abs(startRow-endRow)-1):
                        if gameBoard[startRow-1-index][startCol+1+index].color != None:
                            return False
            # If moving down left
            elif (startRow - endRow) == (startCol - endCol) * (-1) < 0:
                for index in range(abs(startRow-endRow)-1):
                        if gameBoard[startRow+1+index][startCol-1-index].color != None:
                            return False
            # Checking end square
            if self.color != pieceToCapture.color:    
                gameBoard[endRow][endCol] = self
                gameBoard[startRow][startCol] = Empty()
                return True
        else:
            return False