
def pawnLogic(gameBoard, pieceToMove, pieceToCapture, startRow, startCol, endRow, endCol, WHITE_PIECES, BLACK_PIECES):
    # WHITE PAWN LOGIC
    if pieceToMove == "wPawn":
        # Promotion:
        # if pawn is on the 7th rank
        if startRow == 1:
            # TODO: About to promote
            return False

        # Moving one square up:
        # if start and end are on the same file AND end is 1 rank above start AND end square is empty
        elif endCol == startCol and endRow == startRow - 1 and gameBoard[endRow][endCol] == "":
            gameBoard[endRow][endCol] = pieceToMove
            gameBoard[startRow][startCol] = ""
            return True

        # Moving two squares up:
        # if starting square is on 2nd rank AND start and end are on the same file AND end is 2 ranks above start AND traveled squares are empty
        elif startRow == 6 and endCol == startCol and endRow == startRow - 2 and gameBoard[endRow][endCol] == "" == gameBoard[startRow-1][startCol]:
            gameBoard[endRow][endCol] = pieceToMove
            gameBoard[startRow][startCol] = ""
            return True
        
        # Capturing a piece (include this in promotion!):
        # if end is 1 rank above start AND end is 1 file next to start AND there is a black piece in end
        elif (startRow-1 == endRow) and (startCol == endCol-1 or startCol == endCol+1) and (pieceToCapture in BLACK_PIECES):
            gameBoard[endRow][endCol] = pieceToMove
            gameBoard[startRow][startCol] = ""
            return True

    # BLACK PAWN LOGIC
    elif pieceToMove == "bPawn":
        # Promotion:
        if startRow == 6:
            # TODO: About to promote
            pass

        # Moving one square down:
        # if start and end are on the same file AND end is 1 rank above start AND end square is empty
        elif endCol == startCol and endRow == startRow + 1 and gameBoard[endRow][endCol] == "":
            gameBoard[endRow][endCol] = pieceToMove
            gameBoard[startRow][startCol] = ""
            return True

        # Moving two squares down:
        # if starting square is on 2nd rank AND start and end are on the same file AND end is 2 ranks above start AND traveled sqaures are empty
        elif startRow == 1 and endCol == startCol and endRow == startRow + 2 and gameBoard[endRow][endCol] == "" == gameBoard[startRow+1][startCol]:
            gameBoard[endRow][endCol] = pieceToMove
            gameBoard[startRow][startCol] = ""
            return True
        
        # Capturing a piece (include this in promotion!):
        # if end is 1 rank below start AND end is 1 file next to start AND there is a white piece in end
        elif (startRow+1 == endRow) and (startCol == endCol-1 or startCol == endCol+1) and (pieceToCapture in WHITE_PIECES):
            gameBoard[endRow][endCol] = pieceToMove
            gameBoard[startRow][startCol] = ""
            return True
        
def rookLogic(gameBoard, pieceToMove, pieceToCapture, startRow, startCol, endRow, endCol, WHITE_PIECES, BLACK_PIECES):
    # Moving vertically:
    #if start and end are in same column
    if (startCol == endCol):
        # if moving up
        if startRow > endRow:
            #if traveled squares are not empty (e.g. rook moves from rank 0 -> 6: checks ranks 1-5)
            for index in range(abs(startRow-endRow)-1):
                if gameBoard[startRow-1-index][startCol] != "":
                    return False
            if pieceToCapture == "":    
                gameBoard[endRow][endCol] = pieceToMove
                gameBoard[startRow][startCol] = ""
                return True
            elif ((pieceToMove == "wRook") and (pieceToCapture in BLACK_PIECES)) or ((pieceToMove == "bRook") and (pieceToCapture in WHITE_PIECES)):
                gameBoard[endRow][endCol] = pieceToMove
                gameBoard[startRow][startCol] = ""
                return True
        # if moving down
        elif startRow < endRow:
            #if traveled squares are not empty (e.g. rook moves from rank 6 -> 0: checks ranks 5-1)
            for index in range(abs(startRow-endRow)-1):
                if gameBoard[startRow+1+index][startCol] != "":
                    return False
            if pieceToCapture == "":    
                gameBoard[endRow][endCol] = pieceToMove
                gameBoard[startRow][startCol] = ""
                return True
            elif ((pieceToMove == "wRook") and (pieceToCapture in BLACK_PIECES)) or ((pieceToMove == "bRook") and (pieceToCapture in WHITE_PIECES)): 
                gameBoard[endRow][endCol] = pieceToMove
                gameBoard[startRow][startCol] = ""
                return True
            
    # Moving horizontally:
    # if start and end are in the same row
    if (startRow == endRow):
        # if moving left
        if startCol > endCol:
            #if traveled squares are not empty (e.g. rook moves from file h -> c: checks ranks g-d)
            for index in range(abs(startCol-endCol)-1):
                if gameBoard[startRow][startCol-1-index] != "":
                    return False
            if pieceToCapture == "":    
                gameBoard[endRow][endCol] = pieceToMove
                gameBoard[startRow][startCol] = ""
                return True
            elif ((pieceToMove == "wRook") and (pieceToCapture in BLACK_PIECES)) or ((pieceToMove == "bRook") and (pieceToCapture in WHITE_PIECES)): 
                gameBoard[endRow][endCol] = pieceToMove
                gameBoard[startRow][startCol] = ""
                return True
        # if moving right
        elif startCol < endCol:
            #if traveled squares are not empty (e.g. rook moves from file h -> c: checks ranks g-d)
            for index in range(abs(startCol-endCol)-1):
                if gameBoard[startRow][startCol+1+index] != "":
                    return False
            if pieceToCapture == "":    
                gameBoard[endRow][endCol] = pieceToMove
                gameBoard[startRow][startCol] = ""
                return True
            elif ((pieceToMove == "wRook") and (pieceToCapture in BLACK_PIECES)) or ((pieceToMove == "bRook") and (pieceToCapture in WHITE_PIECES)): 
                gameBoard[endRow][endCol] = pieceToMove
                gameBoard[startRow][startCol] = ""
                return True

