from Piece import Piece

class Knight(Piece):
    def __init__(self, color, name, img_id):
        super().__init__(color, name, img_id)

    def moveLogic(self, gameBoard, startRow, startCol, endRow, endCol):
        if startRow == endRow and startCol == endCol:
            return False
        #if moving vertically 2 and horizontally 1 or other way around
        elif (abs(endRow-startRow) == 2 and abs(endCol-startCol) == 1) or (abs(endRow-startRow) == 1 and abs(endCol-startCol) == 2):
            # Checking end square
            if self.color != gameBoard[endRow][endCol].color:    
                return True
        else:
            return False
