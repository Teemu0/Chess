from Piece import Piece

class King(Piece):
    def __init__(self, color, name, img_id):
        super().__init__(color, name, img_id)
        self.value = 0 # King does not count towards material value
        self.canCastle = True

    def moveLogic(self, gameBoard, startRow, startCol, endRow, endCol):
        if startRow == endRow and startCol == endCol:
            return False
        #if vertical move is less than 2 and horizontal is less than 2 and both are not 0
        elif (abs(endRow-startRow) < 2) and (abs(endCol-startCol) < 2) and (abs(endRow-startRow)+abs(endCol-startCol)!=0 ):
            # Checking end square
            if self.color != gameBoard[endRow][endCol].color:    
                return True
        # If move is castle
        elif (self.canCastle == True) and (abs(endCol-startCol) == 2) and (startRow == endRow):
            # King side
            if endCol-startCol == 2:
                if gameBoard[startRow][startCol+1].name == gameBoard[startRow][startCol+2].name == None:
                    if gameBoard[startRow][startCol+3].name == "rook" and gameBoard[startRow][startCol+3].color == self.color:
                        if gameBoard[startRow][startCol+3].canCastle == True:
                            return True
            # Queen side
            elif endCol-startCol == -2:
                if gameBoard[startRow][startCol-1].name == gameBoard[startRow][startCol-2].name == gameBoard[startRow][startCol-3].name == None:
                    if gameBoard[startRow][startCol-4].name == "rook" and gameBoard[startRow][startCol-4].color == self.color:
                        if gameBoard[startRow][startCol-4].canCastle == True:
                            return True

        
        
        # #CASTLING:
        # # Castling king side
        # # If (king can castle) and (endCol - startCol == 2) and (startRow == endRow)
        # elif (self.canCastle == True) and (endCol-startCol == 2) and (startRow == endRow):
        #     if gameBoard[startRow][startCol+1].name == None:
        #         if gameBoard[startRow][startCol+2].name == None:
        #             if gameBoard[startRow][startCol+3].name == "rook" and gameBoard[startRow][startCol+3].color == self.color:
        #                 if gameBoard[startRow][startCol+3].canCastle == True:
        #                     print("Castling king side possible by move logic")

        #                     # Check if opponent is attacking any of the castling squares
        #                     squaresUnderAttack = []
        #                     if self.color == "white":
        #                         for row in range(8):
        #                             for col in range(8):
        #                                 if gameBoard[row][col].color == "black":
        #                                     squaresUnderAttack.append(gameBoard[row][col].getMoves(gameBoard, row, col))
        #                         squaresNeeded = [(7, 4), (7,5), (7,6)]
        #                         for square in squaresNeeded:
        #                             for index in range(len(squaresUnderAttack)):
        #                                 if square in squaresUnderAttack[index]:
        #                                     print("Castling king side impossible; needed squares under attack")
        #                                     return False
        #                         print("Castling king side fully OK")
        #                         return True
                                        
        #                     elif self.color == "black":
        #                         for row in range(8):
        #                             for col in range(8):
        #                                 if gameBoard[row][col].color == "white":
        #                                     squaresUnderAttack.append(gameBoard[row][col].getMoves(gameBoard, row, col))
        #                         squaresNeeded = [(0, 4), (0,5), (0,6)]
        #                         for square in squaresNeeded:
        #                             for index in range(len(squaresUnderAttack)):
        #                                 if square in squaresUnderAttack[index]:
        #                                     print("Castling king side impossible; needed squares under attack")
        #                                     return False
        #                         print("Castling king side fully OK")
        #                         return True
        
        # # Castling queen side
        # # If (king can castle) and (endCol - startCol == -2) and (startRow == endRow)
        # elif (self.canCastle == True) and (endCol-startCol == -2) and (startRow == endRow):
        #     if gameBoard[startRow][startCol-1].name == None:
        #         if gameBoard[startRow][startCol-2].name == None:
        #             if gameBoard[startRow][startCol-3].name == None:
        #                 if gameBoard[startRow][startCol-4].name == "rook" and gameBoard[startRow][startCol+3].color == self.color:
        #                     if gameBoard[startRow][startCol-4].canCastle == True:
        #                         print("Castling queen side possible by move logic")

        #                         # Check if opponent is attacking any of the castling squares
        #                         squaresUnderAttack = []
        #                         if self.color == "white":
        #                             for row in range(8):
        #                                 for col in range(8):
        #                                     if gameBoard[row][col].color == "black":
        #                                         squaresUnderAttack.append(gameBoard[row][col].getMoves(gameBoard, row, col))
        #                             squaresNeeded = [(7, 4), (7,3), (7,2)]
        #                             for square in squaresNeeded:
        #                                 for index in range(len(squaresUnderAttack)):
        #                                     if square in squaresUnderAttack[index]:
        #                                         print("Castling queen side impossible; needed squares under attack")
        #                                         return False
        #                             print("Castling queen side fully OK")
        #                             return True

        #                         elif self.color == "black":
        #                             for row in range(8):
        #                                 for col in range(8):
        #                                     if gameBoard[row][col].color == "white":
        #                                         squaresUnderAttack.append(gameBoard[row][col].getMoves(gameBoard, row, col))
        #                             squaresNeeded = [(0, 4), (0,3), (0,2)]
        #                             for square in squaresNeeded:
        #                                 for index in range(len(squaresUnderAttack)):
        #                                     if square in squaresUnderAttack[index]:
        #                                         print("Castling queen side impossible; needed squares under attack")
        #                                         return False
        #                             print("Castling queen side fully OK")
        #                             return True        
        return False
    
