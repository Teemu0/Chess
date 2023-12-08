from Piece import Piece

class King(Piece):
    def __init__(self, color, name, img_id):
        super().__init__(color, name, img_id)

    def moveLogic(self, gameBoard, startRow, startCol, endRow, endCol):
        if startRow == endRow and startCol == endCol:
            return False
        #if vertical move is less than 2 and horizontal is less than 2 and both are not 0
        elif (abs(endRow-startRow) < 2) and (abs(endCol-startCol) < 2) and (abs(endRow-startRow)+abs(endCol-startCol)!=0 ):
            # Checking end square
            if self.color != gameBoard[endRow][endCol].color:    
                return True
        else:
            return False
    
