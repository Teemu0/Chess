
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
        ''' Gets a list of all legal moves for a piece. Checks for checks on opponent's king.

            Parameters:
            - self Piece: the piece whose moves to check
            - gameboard array: 8x8 chess board
            - startRow int: self's row index in board array
            - startCol int: self's column index in board array

            Returns:
            bool: True, if one of the legal moves attacks opponents king
                  False, otherwise
        '''
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
        #print(legalMoves, isCheck)
        return (isCheck, legalMoves)
    
