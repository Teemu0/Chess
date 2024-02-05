#TODO: check en passant; implemented quickly, can contain bugs.

import pygame
import math
import time
from Piece import Piece
from Empty import Empty
from Pawn import Pawn
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from King import King
from Evaluation import Evaluation
import copy

# Define constants
WIDTH, HEIGHT = 480, 480
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
BORDER_WIDTH = SQUARE_SIZE * 0.1
PIECE_SIZE = SQUARE_SIZE - 2*BORDER_WIDTH
WHITE_PIECES = ["wKing", "wQueen", "wRook", "wBishop", "wKnight", "wPawn"]
BLACK_PIECES = ["bKing", "bQueen", "bRook", "bBishop", "bKnight", "bPawn"]
# Colors
LIGHT = (232, 194, 145)
DARK = (113, 74, 46)
HIGHLIGHT_COLOR = (255, 209, 0)
# Initialize pieces
bPawn = Pawn("black", "pawn", "bPawn")
bKnight = Knight("black", "knight", "bKnight")
bBishop = Bishop("black", "bishop", "bBishop")
bRook_1 = Rook("black", "rook", "bRook")
bRook_2 = Rook("black", "rook", "bRook")
bQueen = Queen("black", "queen", "bQueen")
bKing = King("black", "king", "bKing")
wPawn = Pawn("white", "pawn", "wPawn")
wKnight = Knight("white", "knight", "wKnight")
wBishop = Bishop("white", "bishop", "wBishop")
wRook_1 = Rook("white", "rook", "wRook")
wRook_2 = Rook("white", "rook", "wRook")
wQueen = Queen("white", "queen", "wQueen")
wKing = King("white", "king", "wKing")
empty = Empty(None, None, None)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chessboard")

# Initialize board
gameBoard = [
    [bRook_1,bKnight,bBishop,bQueen,bKing,bBishop,bKnight,bRook_2],
    [bPawn,bPawn,bPawn,bPawn,bPawn,bPawn,bPawn,bPawn],
    [empty,empty,empty,empty,empty,empty,empty,empty],
    [empty,empty,empty,empty,empty,empty,empty,empty],
    [empty,empty,empty,empty,empty,empty,empty,empty],
    [empty,empty,empty,empty,empty,empty,empty,empty],
    [wPawn,wPawn,wPawn,wPawn,wPawn,wPawn,wPawn,wPawn],
    [wRook_1,wKnight,wBishop,wQueen,wKing,wBishop,wKnight,wRook_2]
    ]

enPassantSquare = (None, None)  # type (row, col)

# load white piece images
wKingImg = pygame.image.load('wKing.png')
wKingImg = pygame.transform.scale(wKingImg, (PIECE_SIZE, PIECE_SIZE))
wQueenImg = pygame.image.load('wQueen.png')
wQueenImg = pygame.transform.scale(wQueenImg, (PIECE_SIZE, PIECE_SIZE))
wRookImg = pygame.image.load('wRook.png')
wRookImg = pygame.transform.scale(wRookImg, (PIECE_SIZE, PIECE_SIZE))
wBishopImg = pygame.image.load('wBishop.png')
wBishopImg = pygame.transform.scale(wBishopImg, (PIECE_SIZE, PIECE_SIZE))
wKnightImg = pygame.image.load('wKnight.png')
wKnightImg = pygame.transform.scale(wKnightImg, (PIECE_SIZE, PIECE_SIZE))
wPawnImg = pygame.image.load('wPawn.png')
wPawnImg = pygame.transform.scale(wPawnImg, (PIECE_SIZE, PIECE_SIZE))
# load black piece images
bKingImg = pygame.image.load('bKing.png')
bKingImg = pygame.transform.scale(bKingImg, (PIECE_SIZE, PIECE_SIZE))
bQueenImg = pygame.image.load('bQueen.png')
bQueenImg = pygame.transform.scale(bQueenImg, (PIECE_SIZE, PIECE_SIZE))
bRookImg = pygame.image.load('bRook.png')
bRookImg = pygame.transform.scale(bRookImg, (PIECE_SIZE, PIECE_SIZE))
bBishopImg = pygame.image.load('bBishop.png')
bBishopImg = pygame.transform.scale(bBishopImg, (PIECE_SIZE, PIECE_SIZE))
bKnightImg = pygame.image.load('bKnight.png')
bKnightImg = pygame.transform.scale(bKnightImg, (PIECE_SIZE, PIECE_SIZE))
bPawnImg = pygame.image.load('bPawn.png')
bPawnImg = pygame.transform.scale(bPawnImg, (PIECE_SIZE, PIECE_SIZE))

image_dir = {
    'wKing' : wKingImg,
    'wQueen' : wQueenImg,
    'wRook' : wRookImg,
    'wBishop' : wBishopImg,
    'wKnight' : wKnightImg,
    'wPawn' : wPawnImg,
    'bKing' : bKingImg,
    'bQueen' : bQueenImg,
    'bRook' : bRookImg,
    'bBishop' : bBishopImg,
    'bKnight' : bKnightImg,
    'bPawn' : bPawnImg
}

square_dir = {
    (7,0) : 'a1',
    (6,0) : 'a2',
    (5,0) : 'a3',
    (4,0) : 'a4',
    (3,0) : 'a5',
    (2,0) : 'a6',
    (1,0) : 'a7',
    (0,0) : 'a8',
    (7,1) : 'b1',
    (6,1) : 'b2',
    (5,1) : 'b3',
    (4,1) : 'b4',
    (3,1) : 'b5',
    (2,1) : 'b6',
    (1,1) : 'b7',
    (0,1) : 'b8',
    (7,2) : 'c1',
    (6,2) : 'c2',
    (5,2) : 'c3',
    (4,2) : 'c4',
    (3,2) : 'c5',
    (2,2) : 'c6',
    (1,2) : 'c7',
    (0,2) : 'c8',
    (7,3) : 'd1',
    (6,3) : 'd2',
    (5,3) : 'd3',
    (4,3) : 'd4',
    (3,3) : 'd5',
    (2,3) : 'd6',
    (1,3) : 'd7',
    (0,3) : 'd8',
    (7,4) : 'e1',
    (6,4) : 'e2',
    (5,4) : 'e3',
    (4,4) : 'e4',
    (3,4) : 'e5',
    (2,4) : 'e6',
    (1,4) : 'e7',
    (0,4) : 'e8',
    (7,5) : 'f1',
    (6,5) : 'f2',
    (5,5) : 'f3',
    (4,5) : 'f4',
    (3,5) : 'f5',
    (2,5) : 'f6',
    (1,5) : 'f7',
    (0,5) : 'f8',
    (7,6) : 'g1',
    (6,6) : 'g2',
    (5,6) : 'g3',
    (4,6) : 'g4',
    (3,6) : 'g5',
    (2,6) : 'g6',
    (1,6) : 'g7',
    (0,6) : 'g8',
    (7,7) : 'h1',
    (6,7) : 'h2',
    (5,7) : 'h3',
    (4,7) : 'h4',
    (3,7) : 'h5',
    (2,7) : 'h6',
    (1,7) : 'h7',
    (0,7) : 'h8',
}

inCheck = {
    "white" : False,
    "black" : False
}

def draw_chessboard(highlight, hlRow, hlCol):
    # Draw empty chess board
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    # Draw highlighted square
    if highlight:
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (hlCol * SQUARE_SIZE, hlRow * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    # Draw pieces to the chessboard
    for row in range(len(gameBoard)):
        for col in range(len(gameBoard[row])):
            if gameBoard[row][col] != empty:
                screen.blit(image_dir[gameBoard[row][col].img_id], (col*SQUARE_SIZE + BORDER_WIDTH, row*SQUARE_SIZE + BORDER_WIDTH))

def selectSquare(pos):
    row = math.floor(pos[1] / SQUARE_SIZE)
    col = math.floor(pos[0] / SQUARE_SIZE)
    return row, col

def make_move(gameBoard, startRow, startCol, endRow, endCol):
    moveType = move_logic(gameBoard, startRow, startCol, endRow, endCol) # True(normal move), False(illegal move), 2(promotion)
    if moveType != False:
        if check_logic(gameBoard, startRow, startCol, endRow, endCol):
            #move_is_promotion
            if moveIsPromotion(gameBoard, startRow, startCol):
                promotePawn(gameBoard, startRow, startCol, endRow, endCol) 
            else:
                movePiece(startRow, startCol, endRow, endCol, gameBoard)
            return True              
    return False

def processMove(gameBoard, startRow, startCol, endRow, endCol):
    if moveIsLegal(gameBoard, startRow, startCol, endRow, endCol):
        makeTheMove(startRow, startCol, endRow, endCol, gameBoard)
        return True
    else:
        return False

def moveIsLegal(gameBoard, startRow, startCol, endRow, endCol):
    if move_logic(gameBoard, startRow, startCol, endRow, endCol) or moveIsEnPassant(gameBoard, startRow, startCol, endRow, endCol):
        if check_logic(gameBoard, startRow, startCol, endRow, endCol):
            if moveIsCastle(gameBoard, startRow, startCol, endRow, endCol):
                if castling_logic(gameBoard, startRow, startCol, endRow, endCol):
                    return True
            else:
                return True
    return False

def makeTheMove(startRow, startCol, endRow, endCol, gameBoard):
    if moveIsPromotion(gameBoard, startRow, startCol):
        promotePawn(gameBoard, startRow, startCol, endRow, endCol)
    elif moveIsCastle(gameBoard, startRow, startCol, endRow, endCol):
        castle(gameBoard, startRow, startCol, endRow, endCol)
    elif moveIsEnPassant(gameBoard, startRow, startCol, endRow, endCol):
        moveEnPassant(gameBoard, startRow, startCol, endRow, endCol)
    else:
        movePiece(startRow, startCol, endRow, endCol, gameBoard)
    updateEnPassantSquare(startRow, startCol, endRow, endCol, gameBoard)

def moveIsCastle(gameBoard, startRow, startCol, endRow, endCol):
    '''
        Checks whether the about to be made move is a castle. 
        Assumes that the move has already gone through move_logic().
    '''
    if gameBoard[startRow][startCol].name == "king" and (abs(endCol - startCol) == 2):
        return True
    else:
        return False

def moveIsPromotion(gameBoard, startRow, startCol):
    '''
        Checks whether the about to be made move is a pawn promotion.
    
        Returns:
        bool: True if move is a promotion
        bool: False if move is not a promotion
    '''
    if gameBoard[startRow][startCol].name == "pawn":
        if gameBoard[startRow][startCol].color == "white" and startRow == 1:
            return True
        elif gameBoard[startRow][startCol].color == "black" and startRow == 6:
            return True
    else:
        return False

# TODO:
#Functions needed for en passant:

# DONE update enpassantsquare: stores the "enpassable" square in a global variable
# DONE moveIsEnPassant(): checks from user input if move is en passant
# DONE MoveEnPassant: moves the pieces
#

def moveIsEnPassant(gameBoard, startRow, startCol, endRow, endCol):
    #if enpassantsquare[0] != None
    if enPassantSquare != (None, None):
        #For white pawn
        if gameBoard[startRow][startCol].color == "white" and (gameBoard[startRow][startCol].name == "pawn"):
            # if startRow is on rank 5 AND endRow is on rank 6 AND endCol is 1 file from startCol
            if (startRow == 3) and (endRow == 2) and (abs(startCol - endCol) == 1):
                # if endSquare is enpassantSquare
                if (endRow, endCol) == enPassantSquare:
                    print("moveIsEnPassant(): attempted to make en passant")
                    return True
        # For black pawn
        elif gameBoard[startRow][startCol].color == "black" and (gameBoard[startRow][startCol].name == "pawn"):
            if (startRow == 4) and (endRow == 5) and (abs(startCol - endCol) == 1):
                if (endRow, endCol) == enPassantSquare:
                    print("moveIsEnPassant(): attempted to make en passant")
                    return True
    return False

def moveEnPassant(gameBoard, startRow, startCol, endRow, endCol):
    gameBoard[endRow][endCol] = gameBoard[startRow][startCol]
    gameBoard[startRow][startCol] = empty
    gameBoard[startRow][endCol] = empty

def updateEnPassantSquare(startRow, startCol, endRow, endCol, gameBoard):
    global enPassantSquare
    if gameBoard[endRow][endCol].name == "pawn" and abs(startRow - endRow) == 2:
        enPassantSquare = (int(startRow - (startRow - endRow) / 2), startCol)
    else: 
        enPassantSquare = (None, None)
    print(f"updateEnPassantSquare(): en passant square (row, col) = {enPassantSquare}")
    


def move_logic(gameBoard, startRow, startCol, endRow, endCol):
    '''
        Returns:
        bool True: if move is allowed by piece's logic
        bool False: otherwise
    '''
    return gameBoard[startRow][startCol].moveLogic(gameBoard, startRow, startCol, endRow, endCol)

def check_logic(gameBoard, startRow, startCol, endRow, endCol):
    ''' 
        Checks if a move does not lead to a self check.
        Returns:
        bool True: if move does not lead to self check
        bool False: otherwise
    '''
    tempBoard = copy.deepcopy(gameBoard)
    movePiece(startRow, startCol, endRow, endCol, tempBoard)
    # If moving player is white: get all moves for black
    if tempBoard[endRow][endCol].color == "white":
        startCoords, endCoords = getAllMoves(tempBoard, "black")
    else:
        startCoords, endCoords = getAllMoves(tempBoard, "white")
    for coords in endCoords:
        for index in range(len(coords)):
            if tempBoard[coords[index][0]][coords[index][1]].name == "king":
                # Move leads to a self check
                return False
    # Move does not lead to a self check
    return True

def castling_logic(gameBoard, startRow, startCol, endRow, endCol):
    color = gameBoard[startRow][startCol].color
    # Castling king side:  
    if endCol-startCol == 2:
        if gameBoard[startRow][startCol+1].name == None:
            if gameBoard[startRow][startCol+2].name == None:
                if gameBoard[startRow][startCol+3].name == "rook" and gameBoard[startRow][startCol+3].color == color:
                    if gameBoard[startRow][startCol+3].canCastle == True:
                        print("Castling king side possible by move logic")
                        # Check if opponent is attacking any of the castling squares
                        squaresUnderAttack = []
                        # For white
                        if color == "white":
                            for row in range(8):
                                for col in range(8):
                                    if gameBoard[row][col].color == "black":
                                        squaresUnderAttack.append(gameBoard[row][col].getMoves(gameBoard, row, col))
                            squaresNeeded = [(7, 4), (7,5), (7,6)]
                            for square in squaresNeeded:
                                for index in range(len(squaresUnderAttack)):
                                    if square in squaresUnderAttack[index]:
                                        print("Castling king side impossible; needed squares under attack")
                                        return False
                            print("Castling king side fully OK")
                            return True
                        # For black            
                        elif color == "black":
                            for row in range(8):
                                for col in range(8):
                                    if gameBoard[row][col].color == "white":
                                        squaresUnderAttack.append(gameBoard[row][col].getMoves(gameBoard, row, col))
                            squaresNeeded = [(0, 4), (0,5), (0,6)]
                            for square in squaresNeeded:
                                for index in range(len(squaresUnderAttack)):
                                    if square in squaresUnderAttack[index]:
                                        print("Castling king side impossible; needed squares under attack")
                                        return False
                            print("Castling king side fully OK")
                            return True
    # Castling queen side:  
    elif endCol-startCol == -2:
        if gameBoard[startRow][startCol-1].name == None:
            if gameBoard[startRow][startCol-2].name == None:
                if gameBoard[startRow][startCol-3].name == None:
                    if gameBoard[startRow][startCol-4].name == "rook" and gameBoard[startRow][startCol-4].color == color:
                        if gameBoard[startRow][startCol-4].canCastle == True:
                            print("Castling queen side possible by move logic")
                            # Check if opponent is attacking any of the castling squares
                            squaresUnderAttack = []
                            # For white
                            if color == "white":
                                for row in range(8):
                                    for col in range(8):
                                        if gameBoard[row][col].color == "black":
                                            squaresUnderAttack.append(gameBoard[row][col].getMoves(gameBoard, row, col))
                                squaresNeeded = [(7, 4), (7,3), (7,2)]
                                for square in squaresNeeded:
                                    for index in range(len(squaresUnderAttack)):
                                        if square in squaresUnderAttack[index]:
                                            print("Castling queen side impossible; needed squares under attack")
                                            return False
                                print("Castling queen side fully OK")
                                return True
                            # For black
                            elif color == "black":
                                for row in range(8):
                                    for col in range(8):
                                        if gameBoard[row][col].color == "white":
                                            squaresUnderAttack.append(gameBoard[row][col].getMoves(gameBoard, row, col))
                                squaresNeeded = [(0, 4), (0,3), (0,2)]
                                for square in squaresNeeded:
                                    for index in range(len(squaresUnderAttack)):
                                        if square in squaresUnderAttack[index]:
                                            print("Castling queen side impossible; needed squares under attack")
                                            return False
                                print("Castling queen side fully OK")
                                return True
    else:
        return False
               
def getAllMoves(gameBoard, color):
    '''
        Gets all moves by color allowed by moveLogic.
        Returns:
        startCoords e.g. [(startRow1, startCol1), (startRow2, startCol2)]

    '''
    startCoords = []
    endCoords = []
    for row in range(8):
        for col in range(8):
            if gameBoard[row][col].color == color:
                startCoords.append((row, col))
                endCoords.append(gameBoard[row][col].getMoves(gameBoard, row, col))
    return startCoords, endCoords

def movePiece(startRow, startCol, endRow, endCol, gameBoard):
    if gameBoard[startRow][startCol].name in  ("rook", "king"):
        gameBoard[startRow][startCol].canCastle = False
    gameBoard[endRow][endCol] = gameBoard[startRow][startCol]
    gameBoard[startRow][startCol] = empty

def reverseMove(startRow, startCol, endRow, endCol, revivedPiece, gameBoard):
    gameBoard[startRow][startCol] = gameBoard[endRow][endCol]
    gameBoard[endRow][endCol] = revivedPiece

def promotePawn(gameBoard, startRow, startCol, endRow, endCol):
    '''
    Replaces movePiece() in case of a pawn promotion.
    '''
    while True:
        playerInput = input("Choose piece: Q:queen, R:rook, B:bishop, K:knight")
        if playerInput in ["Q", "q", "R", "r", "B", "b", "K", "k"]:
            break
        else:
            print("Invalid input")
    # If player is white    
    if gameBoard[startRow][startCol].color == "white":
        if playerInput in ["Q", "q"]:
            newPiece = wQueen
        elif playerInput in ["R", "r"]:
            newPiece = Rook("white", "rook", "wRook")
            newPiece.canCastle = False
        elif playerInput in ["B", "b"]:
            newPiece = wBishop
        elif playerInput in ["K", "k"]:
            newPiece = wKnight
    # If player is black
    elif gameBoard[startRow][startCol].color == "black":
        if playerInput in ["Q", "q"]:
            newPiece = bQueen
        elif playerInput in ["R", "r"]:
            newPiece = Rook("black", "rook", "bRook")
            newPiece.canCastle = False
        elif playerInput in ["B", "b"]:
            newPiece = bBishop
        elif playerInput in ["K", "k"]:
            newPiece = bKnight
    if newPiece != None:
        gameBoard[endRow][endCol] = newPiece
        gameBoard[startRow][startCol] = empty
        print("Promotion successful")
    else:
        print("Promotion failed")

def castle(gameBoard, startRow, startCol, endRow, endCol):
    gameBoard[endRow][endCol] = gameBoard[startRow][startCol]
    gameBoard[startRow][startCol] = empty
    gameBoard[endRow][endCol].canCastle = False
    # king side
    if startCol-endCol < 0:
        gameBoard[startRow][startCol+1] = gameBoard[startRow][startCol+3]
        gameBoard[startRow][startCol+3] = empty
    # queen side
    else:
        gameBoard[startRow][startCol-1] = gameBoard[startRow][startCol-4]
        gameBoard[startRow][startCol-4] = empty


def isGameOver(gameBoard, whiteToMove):
    '''
        Checks if the game is over.
        Returns:
        int -1: game is not over
        int 0: stalemate
        int 1: white wins
        int 2: black wins
    '''
    # 1. Get all moves
    if whiteToMove:
        startCoords, endCoords = getAllMoves(gameBoard, "white")
    else:
        startCoords, endCoords = getAllMoves(gameBoard, "black")

    # 2. Try all the moves
    for startIndex in range(len(startCoords)):
         for endIndex in range(len(endCoords[startIndex])):
            tempBoard = copy.deepcopy(gameBoard)
            startRow = startCoords[startIndex][0]
            startCol = startCoords[startIndex][1]
            endRow = endCoords[startIndex][endIndex][0]
            endCol = endCoords[startIndex][endIndex][1]
            if moveIsLegal(tempBoard, startRow, startCol, endRow, endCol):
                # Found a legal move -> game is not over
                return -1
            
    # No legal moves found. Game is over. Is it a checkmate, or a stalemate?
    # 3. Is own king in check?
    if whiteToMove:
        startCoords, endCoords = getAllMoves(gameBoard, "black")
    else:
        startCoords, endCoords = getAllMoves(gameBoard, "white")
    
    for coords in endCoords:
        for index in range(len(coords)):
            if tempBoard[coords[index][0]][coords[index][1]].name == "king":
                # Own king is in check -> opponent has a checkmate
                if whiteToMove:
                    return 2
                else:
                    return 1
    # Stalemate
    return 0

def printResult(result):
    if result == 0:
        print("Draw! It is a stalemate.")
    elif result == 1:
        print("White wins!")
    elif result == 2:
        print("Black wins!")

# DELETE THIS
# def minimax(gameBoard, maximizing):
#     # Try every legal move
#     temp_board = copy.deepcopy(gameBoard)
#     # If white to move
#     if maximizing:
#         for row in range(8):
#             for col in range(8):
#                 if temp_board[row][col].color =="white":
#                     moveStart = ((row, col), temp_board[row][col])
#                     movesToTry = temp_board[row][col].getMoves(gameBoard, row, col)[1]             
#                     for squares in movesToTry:
#                         temp_board = copy.deepcopy(gameBoard)
#                         moveEnd = (squares, temp_board[squares[0]][squares[1]])
#                         print(f"Move: {moveEnd}")
#                         makeMove(moveStart, moveEnd, temp_board)
#                         Evaluation.eval(temp_board, maximizing)


def main():
    clock = pygame.time.Clock()
    running = True  # is game running?
    highlighted = False # boolean, whether a piece is selected on the board with a mouse click
    whiteToMove = True  # whose turn is it to move
    startRow = 0 # Initialize for draw_chessboard(). Will not be used before getting real values
    startCol = 0
    result = -1 # -1(game not over), 0(stalemate), 1(white wins), 2(black wins)

    while running:

        screen.fill(DARK)
        draw_chessboard(highlighted, startRow, startCol)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not highlighted:
                    startRow, startCol = selectSquare(event.pos)
                    if whiteToMove and (gameBoard[startRow][startCol].color == "white"):
                        highlighted = True
                    elif not whiteToMove and (gameBoard[startRow][startCol].color == "black"):
                        highlighted = True
                else:
                    endRow, endCol = selectSquare(event.pos)
                    highlighted = False
                    if processMove(gameBoard, startRow, startCol, endRow, endCol):
                        whiteToMove = not whiteToMove
                        # If game is over
                        result = isGameOver(gameBoard, whiteToMove)
                        if result != -1:
                            printResult(result)

    
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()