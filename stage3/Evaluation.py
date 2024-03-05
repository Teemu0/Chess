from Piece import Piece
from Empty import Empty
from Pawn import Pawn
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from King import King
import copy
#from chess import makeMove

class Evaluation():
    def __init__(self) -> None:
        pass

    def countMaterial(gameBoard):
        '''
        Returns: materialBalance
        '''
        # 1: Count material
        whiteMaterial = 0
        blackMaterial = 0
        for row in range(8):
            for col in range(8):
                if gameBoard[row][col].color == "white":
                    whiteMaterial += gameBoard[row][col].value
                elif gameBoard[row][col].color == "black":
                    blackMaterial += gameBoard[row][col].value

        print(f"White material count: {whiteMaterial}")
        print(f"Black material count: {blackMaterial}")
        materialBalance = whiteMaterial - blackMaterial
        print(f"Material balance: {materialBalance}")
        return materialBalance
    
    def checkWin(gameBoard, whiteToMove):
        '''
            Returns:
            int 0: no win
            int 1: white wins or stalemates
            int -1: black wins or stalemates
        '''
        pass

    
    # def minimax(gameBoard, maximizing):
    #     # Try every legal move
    #     temp_board = copy.deepcopy(gameBoard)
    #     # If white to move
    #     if maximizing:
    #         for row in range(8):
    #             for col in range(8):
    #                 if temp_board[row][col].color =="white":
    #                     moveStart = ((row, col), temp_board[row][col])
    #                     movesToTry = temp_board[row][col].getMoves[1]                   
    #                     for squares in movesToTry:
    #                         moveEnd = (squares, temp_board[squares[0]][squares[1]])
    #                         makeMove(moveStart, moveEnd, temp_board)
    #                         eval(temp_board, maximizing)


