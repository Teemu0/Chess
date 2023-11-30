from Piece import Piece
from Empty import Empty

class Rook(Piece):
    def __init__(self, color, name, img_id):
        super().__init__(color, name, img_id)

    def moveLogic(self, gameBoard, pieceToCapture, startRow, startCol, endRow, endCol,):
        # Moving vertically:
        #if start and end are in same column
        if (startCol == endCol):
            # if moving up
            if startRow > endRow:
                #if traveled squares are not empty (e.g. rook moves from rank 0 -> 6: checks ranks 1-5)
                for index in range(abs(startRow-endRow)-1):
                    if gameBoard[startRow-1-index][startCol].color != None:
                        return False
            # if moving down
            elif startRow < endRow:
                #if traveled squares are not empty (e.g. rook moves from rank 6 -> 0: checks ranks 5-1)
                for index in range(abs(startRow-endRow)-1):
                    if gameBoard[startRow+1+index][startCol].color != None:
                        return False
            if self.color != pieceToCapture.color:    
                gameBoard[endRow][endCol] = self
                gameBoard[startRow][startCol] = Empty()
                return True
                
        # Moving horizontally:
        # if start and end are in the same row
        elif (startRow == endRow):
            # if moving left
            if startCol > endCol:
                #if traveled squares are not empty (e.g. rook moves from file h -> c: checks ranks g-d)
                for index in range(abs(startCol-endCol)-1):
                    if gameBoard[startRow][startCol-1-index].color != None:
                        return False
            # if moving right
            elif startCol < endCol:
                #if traveled squares are not empty (e.g. rook moves from file h -> c: checks ranks g-d)
                for index in range(abs(startCol-endCol)-1):
                    if gameBoard[startRow][startCol+1+index].color != None:
                        return False
            if self.color != pieceToCapture.color:    
                gameBoard[endRow][endCol] = self
                gameBoard[startRow][startCol] = Empty()
                return True
        else:
            return False