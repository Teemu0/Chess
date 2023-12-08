from Piece import Piece

class Bishop(Piece):
    def __init__(self, color, name, img_id):
        super().__init__(color, name, img_id)
    
    def moveLogic(self, gameBoard, startRow, startCol, endRow, endCol):
        if startRow == endRow and startCol == endCol:
            return False
        # If moving diagonally
        elif abs(startRow - endRow) == abs(startCol - endCol):
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
            if self.color != gameBoard[endRow][endCol].color:    
                return True
        return False