
import pygame
import math
import time
import random
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
gameTypes = ("playerVsPlayer", "playerVsAI")

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

# def make_move(gameBoard, startRow, startCol, endRow, endCol):
#     moveType = move_logic(gameBoard, startRow, startCol, endRow, endCol) # True(normal move), False(illegal move), 2(promotion)
#     if moveType != False:
#         if check_logic(gameBoard, startRow, startCol, endRow, endCol):
#             #move_is_promotion
#             if moveIsPromotion(gameBoard, startRow, startCol):
#                 promotePawn(gameBoard, startRow, startCol, endRow, endCol) 
#             else:
#                 movePiece(startRow, startCol, endRow, endCol, gameBoard)
#             return True              
#     return False

def processMove(gameBoard, startRow, startCol, endRow, endCol, moveByComputer=True):
    if moveIsLegal(gameBoard, startRow, startCol, endRow, endCol):
        makeTheMove(startRow, startCol, endRow, endCol, gameBoard, moveByComputer, False)
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

def makeTheMove(startRow, startCol, endRow, endCol, gameBoard, moveByComputer, usingTempBoard):
    if moveIsPromotion(gameBoard, startRow, startCol):
        promotePawn(gameBoard, startRow, startCol, endRow, endCol, moveByComputer)
    elif moveIsCastle(gameBoard, startRow, startCol, endRow, endCol):
        castle(gameBoard, startRow, startCol, endRow, endCol)
    elif moveIsEnPassant(gameBoard, startRow, startCol, endRow, endCol):
        moveEnPassant(gameBoard, startRow, startCol, endRow, endCol)
    else:
        movePiece(startRow, startCol, endRow, endCol, gameBoard)
    updateEnPassantSquare(startRow, startCol, endRow, endCol, gameBoard)
    if not usingTempBoard:
        updateDevelopmentTable(startRow, startCol, endRow, endCol, gameBoard)

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
    #print(f"updateEnPassantSquare(): en passant square (row, col) = {enPassantSquare}")
    


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
        possibleMoves = getAllMoves(tempBoard, "black")
    else:
        possibleMoves = getAllMoves(tempBoard, "white")
    for move in possibleMoves:
        if tempBoard[move[2]][move[3]].name == "king":
            # Move leads to a self check
            return False
    # Move does not lead to a self check
    return True

def castling_logic(gameBoard, startRow, startCol, endRow, endCol):
    color = gameBoard[startRow][startCol].color
    # Castling king side:  
    if endCol-startCol == 2:
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
    return False
               
def getAllMoves(gameBoard, color):
    '''
        Gets all moves by color allowed by moveLogic only!!; Does not account for check logic!
        #TODO: mistake: counts castling even when castling is not possible
                check if counts en passant
        Returns:
        a list of moves [(startRow, startCol, endRow, endCol)]

    '''

    possibleMoves = []
    for row in range(8):
        for col in range(8):
            if gameBoard[row][col].color == color:
                endCoords = gameBoard[row][col].getMoves(gameBoard, row, col)
                if endCoords:
                    for coords in endCoords:
                        possibleMoves.append((row, col, coords[0], coords[1]))

    #print(f"getAllMoves: possible moves for {color}: possibleMoves = {possibleMoves}")
    return possibleMoves

def movePiece(startRow, startCol, endRow, endCol, gameBoard):
    # castling rights
    if gameBoard[startRow][startCol].name in  ("rook", "king"):
        gameBoard[startRow][startCol].canCastle = False
    # moving piece
    gameBoard[endRow][endCol] = gameBoard[startRow][startCol]
    gameBoard[startRow][startCol] = empty
    

def updateDevelopmentTable(startRow, startCol, endRow, endCol, gameBoard):
    '''
    Updates the Evaluation.developmentBooleans table regarding bishops and knights. 
    Called in makeTheMove after a piece has already been moved.
    '''
    startSquare = (startRow, startCol)
    name = gameBoard[endRow][endCol].name
    color = gameBoard[endRow][endCol].color

    if name == "knight":

        if color == "white":
            if startSquare == (7, 1):
                Evaluation.developmentBooleans["whiteKnight1"] = True
            elif startSquare == (7, 6):
                Evaluation.developmentBooleans["whiteKnight2"] = True

        elif color == "black":
            if startSquare == (0, 1):
                Evaluation.developmentBooleans["blackKnight1"] = True
            elif startSquare == (0, 6):
                Evaluation.developmentBooleans["blackKnight2"] = True

    
    elif name == "bishop":

        if color == "white":
            if startSquare == (7, 2):
                Evaluation.developmentBooleans["whiteBishop1"] = True
            elif startSquare == (7, 5):
                Evaluation.developmentBooleans["whiteBishop2"] = True

        elif color == "black":
            if startSquare == (0, 2):
                Evaluation.developmentBooleans["blackBishop1"] = True
            elif startSquare == (0, 5):
                Evaluation.developmentBooleans["blackBishop2"] = True
    # Castling
    elif moveIsCastle(gameBoard, startRow, startCol, endRow, endCol):
        if color == "white":
            Evaluation.developmentBooleans["whiteCastle"] = True
        else:
            Evaluation.developmentBooleans["blackCastle"] = True



def reverseMove(startRow, startCol, endRow, endCol, revivedPiece, gameBoard):
    gameBoard[startRow][startCol] = gameBoard[endRow][endCol]
    gameBoard[endRow][endCol] = revivedPiece

def promotePawn(gameBoard, startRow, startCol, endRow, endCol, moveByComputer=True):
    '''
    Replaces movePiece() in case of a pawn promotion.
    '''
    # If computer makes promotion it will always choose queen
    if moveByComputer:
        if gameBoard[startRow][startCol].color == "white":
            newPiece = wQueen
        elif gameBoard[startRow][startCol].color == "black":
            newPiece = bQueen
    else:
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
        possibleMoves = getAllMoves(gameBoard, "white")
    else:
        possibleMoves = getAllMoves(gameBoard, "black")

    # 2. Try all the moves
    for move in possibleMoves:
        tempBoard = copy.deepcopy(gameBoard)
        startRow = move[0]
        startCol = move[1]
        endRow = move[2]
        endCol = move[3]
        if moveIsLegal(tempBoard, startRow, startCol, endRow, endCol):
            # Found a legal move -> game is not over
            return -1
            
    # No legal moves found. Game is over. Is it a checkmate, or a stalemate?
    # 3. Is own king in check?
    if whiteToMove:
        possibleMoves = getAllMoves(gameBoard, "black")
    else:
        possibleMoves = getAllMoves(gameBoard, "white")
    
    for move in possibleMoves:
        if tempBoard[move[2]][move[3]].name == "king":
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

def getBestMove(gameBoard, whiteToMove, depth=10):
    # possibleMoves : pass move logic
    # allMoves : pass move logic and check logic
    bestMaterialCount = Evaluation.countMaterial(gameBoard)
    if depth == 0:
        return [None, None, None, None, bestMaterialCount]
    allMoves = []
    bestMove = None #type [startRow, startCol, endRow, endCol, materialBalance]
    #1. get all moves
    if whiteToMove:
        possibleMoves = getAllMoves(gameBoard, "white")
    else:
        possibleMoves = getAllMoves(gameBoard, "black")

    # 2. Try all the moves and count their material balance
    for move in possibleMoves:
        tempBoard = copy.deepcopy(gameBoard)
        startRow = move[0]
        startCol = move[1]
        endRow = move[2]
        endCol = move[3]
        if moveIsLegal(tempBoard, startRow, startCol, endRow, endCol):
            makeTheMove(startRow, startCol, endRow, endCol, tempBoard, True, True)
            possibleMove = [startRow, startCol, endRow, endCol]
            tempMaterialCount = Evaluation.countMaterial(tempBoard)
            possibleMove.append(tempMaterialCount)
            allMoves.append(possibleMove)


            if whiteToMove:
                if tempMaterialCount > bestMaterialCount:
                    if getBestMove(tempBoard, not whiteToMove, depth=(depth-1))[4] >= bestMaterialCount:
                        bestMaterialCount = tempMaterialCount
                        bestMove = possibleMove
            elif not whiteToMove:
                if tempMaterialCount < bestMaterialCount:                  
                    if getBestMove(tempBoard, not whiteToMove, depth=(depth-1))[4] <= bestMaterialCount:
                        bestMaterialCount = tempMaterialCount
                        bestMove = possibleMove
    print(f"possibleMoves = {possibleMoves}")
    
    # 3. Return the move with the best material balance.

    # If no moves are available, return final material count
    if not allMoves:
        return [None, None, None, None, bestMaterialCount]
    # Select random move
    if bestMove == None:
        randomIndex = random.randint(0, len(allMoves)-1)
        bestMove = allMoves[randomIndex]
    print(f"bestMove = {bestMove}")
    return bestMove

boardCounter = 0
def minimax(gameboard, whitetomove, depth, canIncreaseDepth):
    '''
    Returns:
        eval: int
        move: (startRow, startCol, endRow, endCol)
        boardsAnalyzed: int  # number of boards created using copy.deepcopy
    '''
    print("_______________________")
    print(f"minimax: depth = {depth}")
    global boardCounter
    boardCounter += 1

    case = isGameOver(gameboard, whitetomove)

    # if white wins
    if case == 1:
        return 100, None
    
    # if black wins
    if case == 2:
        return -100, None
    
    # if draw
    if case == 0:
        return 0, None
    
    
    
    if depth == 0:
        materialCount = Evaluation.countMaterial(gameboard)
        return materialCount, None

    if whitetomove:
        max_eval = -100
        best_moves = []
        all_moves = getAllMoves(gameboard, "white") # moves accepted by move_logic
        possible_moves = [] # moves accepted by move_logic and check_logic

        for move in all_moves:
            if moveIsLegal(gameboard, move[0], move[1], move[2], move[3]):
                possible_moves.append(move)
        
        for move in possible_moves:
            temp_board = copy.deepcopy(gameboard)
            materialCountBefore = Evaluation.countMaterial(temp_board)
            makeTheMove(move[0], move[1], move[2], move[3], temp_board, True, True)
            materialCountAfter = Evaluation.countMaterial(temp_board)
            if materialCountAfter == materialCountBefore:
                canIncreaseDepth = False
            if materialCountAfter > materialCountBefore+1 and canIncreaseDepth:
                depth += 1
                canIncreaseDepth = False
            eval = minimax(temp_board, not whitetomove, depth-1, canIncreaseDepth and depth == 1)[0]
            if eval == max_eval:
                best_moves.append(move)
            elif eval > max_eval:
                max_eval = eval
                best_moves = []
                best_moves.append(move)
        # print(f"White's turn: max_eval = {max_eval}, best_moves = {best_moves}")
        return max_eval, best_moves

    elif not whitetomove:
        min_eval = 100
        best_moves = []
        all_moves = getAllMoves(gameboard, "black") # moves accepted by move_logic
        possible_moves = [] # moves accepted by move_logic and check_logic

        for move in all_moves:
            if moveIsLegal(gameboard, move[0], move[1], move[2], move[3]):
                possible_moves.append(move)
        
        for move in possible_moves:
            temp_board = copy.deepcopy(gameboard)
            materialCountBefore = Evaluation.countMaterial(temp_board)
            makeTheMove(move[0], move[1], move[2], move[3], temp_board, True, True)
            materialCountAfter = Evaluation.countMaterial(temp_board)
            if materialCountAfter == materialCountBefore:
                canIncreaseDepth = False
            if materialCountAfter < materialCountBefore-1 and canIncreaseDepth and depth == 1:
                depth += 1
            eval = minimax(temp_board, not whitetomove, depth-1, canIncreaseDepth)[0]
            if eval == min_eval:
                best_moves.append(move)
            elif eval < min_eval:
                min_eval = eval
                best_moves = []
                best_moves.append(move)
        # print(f"Black's turn: min_eval = {min_eval}, best_moves = {best_moves}")
        return min_eval, best_moves

def minimax_v2(gameboard, whitetomove, depth, canIncreaseDepth):
    '''
    Returns:
        eval: int
        move: (startRow, startCol, endRow, endCol)
        boardsAnalyzed: int  # number of boards created using copy.deepcopy
    '''
    print("_______________________")
    print(f"minimax: depth = {depth}")
    global boardCounter
    boardCounter += 1

    case = isGameOver(gameboard, whitetomove)

    # if white wins
    if case == 1:
        return 100, None
    
    # if black wins
    if case == 2:
        return -100, None
    
    # if draw
    if case == 0:
        return 0, None
    
    
    
    if depth == 0:
        evaluation = Evaluation.getEvaluation(gameboard)
        return evaluation, None

    if whitetomove:
        max_eval = -100
        best_moves = []
        all_moves = getAllMoves(gameboard, "white") # moves accepted by move_logic
        possible_moves = [] # moves accepted by move_logic and check_logic

        for move in all_moves:
            if moveIsLegal(gameboard, move[0], move[1], move[2], move[3]):
                possible_moves.append(move)
        
        for move in possible_moves:
            temp_board = copy.deepcopy(gameboard)
            evaluationBefore = Evaluation.getEvaluation(temp_board)
            makeTheMove(move[0], move[1], move[2], move[3], temp_board, True, True)
            evaluationAfter = Evaluation.getEvaluation(temp_board)

            if depth == 2 and abs(evaluationAfter - evaluationBefore) < 3:
                canIncreaseDepth = False

            if depth == 1 and canIncreaseDepth and (isMoveCheck(temp_board, move[2], move[3]) or (abs(evaluationAfter - evaluationBefore) > 2)):
                depth += 1
                canIncreaseDepth = False
            eval = minimax_v2(temp_board, not whitetomove, depth-1, canIncreaseDepth)[0]
            if eval == max_eval:
                best_moves.append(move)
            elif eval > max_eval:
                max_eval = eval
                best_moves = []
                best_moves.append(move)
        # print(f"White's turn: max_eval = {max_eval}, best_moves = {best_moves}")
        return max_eval, best_moves

    elif not whitetomove:
        min_eval = 100
        best_moves = []
        all_moves = getAllMoves(gameboard, "black") # moves accepted by move_logic
        possible_moves = [] # moves accepted by move_logic and check_logic

        for move in all_moves:
            if moveIsLegal(gameboard, move[0], move[1], move[2], move[3]):
                possible_moves.append(move)
        
        for move in possible_moves:
            temp_board = copy.deepcopy(gameboard)
            evaluationBefore = Evaluation.getEvaluation(temp_board)
            makeTheMove(move[0], move[1], move[2], move[3], temp_board, True, True)
            evaluationAfter = Evaluation.getEvaluation(temp_board)

            if depth == 2 and abs(evaluationAfter - evaluationBefore) < 3:
                canIncreaseDepth = False

            if depth == 1 and  canIncreaseDepth and (isMoveCheck(temp_board, move[2], move[3]) or (abs(evaluationAfter - evaluationBefore) > 2)):
                depth += 1
                canIncreaseDepth = False
            eval = minimax_v2(temp_board, not whitetomove, depth-1, canIncreaseDepth)[0]
            if eval == min_eval:
                best_moves.append(move)
            elif eval < min_eval:
                min_eval = eval
                best_moves = []
                best_moves.append(move)
        # print(f"Black's turn: min_eval = {min_eval}, best_moves = {best_moves}")
        return min_eval, best_moves

def minimaxBasic(gameboard, whitetomove, depth, canIncreaseDepth):
    '''
    Basic minimax algorithm based on getEvaluation. Depth cannot be adjusted.
    Returns:
        eval: int
        move: (startRow, startCol, endRow, endCol)
        boardsAnalyzed: int  # number of boards created using copy.deepcopy
    '''
    print("_______________________")
    print(f"minimax: depth = {depth}")
    global boardCounter
    boardCounter += 1

    case = isGameOver(gameboard, whitetomove)

    # if white wins
    if case == 1:
        return 100, None
    
    # if black wins
    if case == 2:
        return -100, None
    
    # if draw
    if case == 0:
        return 0, None
    
    
    
    if depth == 0:
        evaluation = Evaluation.getEvaluation(gameboard)
        return evaluation, None

    if whitetomove:
        max_eval = -100
        best_moves = []
        all_moves = getAllMoves(gameboard, "white") # moves accepted by move_logic
        possible_moves = [] # moves accepted by move_logic and check_logic

        for move in all_moves:
            if moveIsLegal(gameboard, move[0], move[1], move[2], move[3]):
                possible_moves.append(move)
        
        for move in possible_moves:
            temp_board = copy.deepcopy(gameboard)
            makeTheMove(move[0], move[1], move[2], move[3], temp_board, True, True)
            eval = minimaxBasic(temp_board, not whitetomove, depth-1, False)[0]
            if eval == max_eval:
                best_moves.append(move)
            elif eval > max_eval:
                max_eval = eval
                best_moves = []
                best_moves.append(move)
        # print(f"White's turn: max_eval = {max_eval}, best_moves = {best_moves}")
        return max_eval, best_moves

    elif not whitetomove:
        min_eval = 100
        best_moves = []
        all_moves = getAllMoves(gameboard, "black") # moves accepted by move_logic
        possible_moves = [] # moves accepted by move_logic and check_logic

        for move in all_moves:
            if moveIsLegal(gameboard, move[0], move[1], move[2], move[3]):
                possible_moves.append(move)
        
        for move in possible_moves:
            temp_board = copy.deepcopy(gameboard)
            makeTheMove(move[0], move[1], move[2], move[3], temp_board, True, True)
            eval = minimaxBasic(temp_board, not whitetomove, depth-1, canIncreaseDepth)[0]
            if eval == min_eval:
                best_moves.append(move)
            elif eval < min_eval:
                min_eval = eval
                best_moves = []
                best_moves.append(move)
        # print(f"Black's turn: min_eval = {min_eval}, best_moves = {best_moves}")
        return min_eval, best_moves

def call_minimax(gameboard, whitetomove, depth, canIncreaseDepth):
    global boardCounter
    startTime = time.time()

    evaluation, best_moves = minimaxBasic(gameboard, whitetomove, depth, canIncreaseDepth)
    if len(best_moves) > 1:
            randomIndex = random.randint(0, len(best_moves)-1)
            best_move = best_moves[randomIndex]
    else:
        best_move = best_moves[0]

    endTime = time.time()
    totalTime = round((endTime - startTime), 2)
    print(f"call_minimax: minimax went through {boardCounter} boards and it took {totalTime} seconds")
    boardCounter = 0
    print(f"call_minimax: Computer evaluates the position as {evaluation}")
    print(f"call_minimax: Computer thinks the best moves is {best_move}")
    print(f"call_minimax: Evaluation.developmentBooleans = {Evaluation.developmentBooleans}")

    return best_move

def isMoveCheck(gameBoard, endRow, endCol):
    '''
    Called after the move has been made
    '''
    if gameBoard[endRow][endCol].color == "white":
        possibleMoves = getAllMoves(gameBoard, "white")
        for move in possibleMoves:
            if gameBoard[move[2]][move[3]].name == "king" and gameBoard[move[2]][move[3]].color == "black":
                # Move leads to a check
                return True
    elif gameBoard[endRow][endCol].color == "black":
        possibleMoves = getAllMoves(gameBoard, "black")
        for move in possibleMoves:
            if gameBoard[move[2]][move[3]].name == "king" and gameBoard[move[2]][move[3]].color == "white":
                # Move leads to a check
                return True
        
    # Move does not lead to a self check
    return False


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
    setting_up = True
    running = False # is game running?
    state_playerVsPlayer = False
    state_playerVsAI = False

    highlighted = False # boolean, whether a piece is selected on the board with a mouse click
    whiteToMove = True  # whose turn is it to move
    gameType = gameTypes[1] # gameTypes[0] = playerVsPlayer, gameTypes[1] = playerVsAI
    startRow = 0 # Initialize for draw_chessboard(). Will not be used before getting real values
    startCol = 0
    result = -1 # -1(game not over), 0(stalemate), 1(white wins), 2(black wins)
    while setting_up:
        user_input = input("Select color [W] for white or [B] for black or [P] for practice board")
        if user_input in ["p", "P"]:
            setting_up = False
            state_playerVsPlayer = True
            running = True
        elif user_input in ["w", "W"]:
            setting_up = False
            state_playerVsAI = True
            running = True

    while running and state_playerVsPlayer:

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
                    if processMove(gameBoard, startRow, startCol, endRow, endCol, moveByComputer=False):
                        whiteToMove = not whiteToMove
                        # If game is over
                        result = isGameOver(gameBoard, whiteToMove)
                        if result != -1:
                            printResult(result)
                        Evaluation.countMaterial(gameBoard)
                        minimax(gameBoard, whiteToMove, 10)
        pygame.display.flip()
        clock.tick(30)

    while running and state_playerVsAI:
        screen.fill(DARK)
        draw_chessboard(highlighted, startRow, startCol)
        if whiteToMove:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not highlighted:
                        startRow, startCol = selectSquare(event.pos)
                        if (gameBoard[startRow][startCol].color == "white"):
                            highlighted = True
                    else:
                        endRow, endCol = selectSquare(event.pos)
                        highlighted = False
                        if processMove(gameBoard, startRow, startCol, endRow, endCol, moveByComputer=False):
                            whiteToMove = not whiteToMove
                            result = isGameOver(gameBoard, whiteToMove)
                            if result != -1:
                                printResult(result)
                                running = False
        screen.fill(DARK)
        draw_chessboard(highlighted, startRow, startCol)
        pygame.display.flip()

        if not whiteToMove and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            bestMove = call_minimax(gameBoard, whiteToMove, 2, True)
            startRow = bestMove[0]
            startCol = bestMove[1]
            endRow = bestMove[2]
            endCol = bestMove[3]
            if processMove(gameBoard, startRow, startCol, endRow, endCol, moveByComputer=True):
                whiteToMove = not whiteToMove
                result = isGameOver(gameBoard, whiteToMove)
                if result != -1:
                    printResult(result)
            else:
                print("main: error: best move is not playable")

        screen.fill(DARK)
        draw_chessboard(highlighted, startRow, startCol)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()