#TODO: Add game modes as black; Draw chess board upside down
#TODO: updateDevelopmentTable() has a bug. Evaluation.developmentBooleans is not accurate.
#TODO: Evaluation: add a list that tracks controlled squares, squares under attack, pieces under attack, etc.
#TODO: Rework drawing main menu and end menu (the code is messy). 
#TODO: Rethink code structure; Add more classes, for example GameBoard, AI
#TODO: Add more documentation

import pygame
import sys
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
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 480
ROWS, COLS = 8, 8
SQUARE_SIZE = SCREEN_WIDTH // COLS
BORDER_WIDTH = SQUARE_SIZE * 0.1
PIECE_SIZE = SQUARE_SIZE - 2*BORDER_WIDTH
WHITE_PIECES = ["wKing", "wQueen", "wRook", "wBishop", "wKnight", "wPawn"]
BLACK_PIECES = ["bKing", "bQueen", "bRook", "bBishop", "bKnight", "bPawn"]

# Colors
MENU_COLOR = (234,210,162)
BUTTON_COLOR = (255, 255, 255)
LIGHT = (232, 194, 145)
DARK = (113, 74, 46)
HIGHLIGHT_COLOR = (255, 209, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREY = (230, 230, 230)
GREY = (40, 40, 40)
GREEN = (50,205,50)
CYAN = (0,255,255)
BLUE = (0,0,255)
YELLOW = (255,255,0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chessboard")

# Main menu properties
BUTTON_WIDTH = 8*(SCREEN_WIDTH/20)
BUTTON_HEIGHT = 3*(SCREEN_HEIGHT/20)

BUTTON_GAP = SCREEN_WIDTH/20  # Gap between buttons
BUTTONS_PER_ROW = 2  # Number of buttons per row
BUTTON_ROWS = 3  # Number of button rows

# Font settings
font_normal = pygame.font.Font(None, 30)
font_small = pygame.font.Font(None, 22)
font_big = pygame.font.Font(None, 48)
font_color = BLACK

def init_mainMenuButtons():
    '''
    Make a list of buttons needed for the main menu.
    Returns: a list of buttons [(button_rect, text), ]
    '''
    # Calculate total horizontal and vertical space for buttons
    total_horizontal_space = BUTTON_WIDTH * BUTTONS_PER_ROW + BUTTON_GAP * (BUTTONS_PER_ROW - 1)
    total_vertical_space = BUTTON_HEIGHT * BUTTON_ROWS + BUTTON_GAP * (BUTTON_ROWS - 1)

    # Calculate starting x and y coordinates for the first button
    start_x = (SCREEN_WIDTH - total_horizontal_space) // 2
    start_y = (SCREEN_HEIGHT - total_vertical_space) - BUTTON_GAP

    # List to store button rectangles and their text
    button_data = []
    button_text = [("White vs. Easy Bot", "Bot takes ~ 5 s per move"), 
                   ("Black vs. Easy Bot", "Not available"), 
                   ("White vs. Hard Bot", "Bot takes ~ 20 s per move"), 
                   ("Black vs. Hard Bot", "Not available"), 
                   ("White and Black", "Control both colors"), 
                    ("Quit Game", "Close window")]

    # Create buttons and store their rectangles and text
    for index in range(BUTTON_ROWS * BUTTONS_PER_ROW):
        row = index // BUTTONS_PER_ROW
        col = index % BUTTONS_PER_ROW
        x = start_x + (BUTTON_WIDTH + BUTTON_GAP) * col
        y = start_y + (BUTTON_HEIGHT + BUTTON_GAP) * row
        button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        text = button_text[index]
        button_data.append((button_rect, text))

    return button_data
        
# Initialize main menu button data   
mainMenu_buttonData = init_mainMenuButtons()  # type [(button_rect, button_text), ]

# Initialize pieces
global bPawn
global bKnight
global bBishop
global bRook_1
global bRook_2 
global bQueen
global bKing
global wPawn
global wKnight
global wBishop
global wRook_1
global wRook_2
global wQueen
global wKing
global empty

# Initialize board
global gameBoard
# Other game variables
global enPassantSquare
global boardCounter

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
# load teemunshakkibotti logo
logoImg = pygame.image.load('Logo.png')

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

def draw_mainMenu():

    # Draw background
    screen.fill(MENU_COLOR)

    # Draw logo
    screen.blit(logoImg, (0, 0))

    # Draw "Play as"
    text_surface = font_normal.render("Play as", True, font_color)
    screen.blit(text_surface, (mainMenu_buttonData[0][0][0], mainMenu_buttonData[0][0][1] - BUTTON_GAP))    # screen.blit(text_surface, (x, y))

    # Draw buttons
    for button_rect, text in mainMenu_buttonData:
        pygame.draw.rect(screen, WHITE, button_rect)
        text_surface = font_normal.render(text[0], True, font_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        # Add explanation texts
        text_surface = font_small.render(text[1], True, font_color)
        coords = button_rect.center
        x, y = coords[0]-94, coords[1]+20
        screen.blit(text_surface, (x, y))

def draw_endMenu(gameResult):
    '''
    Draws game result and a button to return to main menu.
    Returns: button_rect
    '''

    if gameResult == 1:
        text_result = "Checkmate, white wins!"
    elif gameResult == 2:
        text_result = "Checkmate, black wins!"
    else:
        text_result = "Stalemate, draw!"

    # Draw game result
    text_surface = font_big.render(text_result, True, BLACK)
    screen.blit(text_surface, (BORDER_WIDTH*10, SCREEN_HEIGHT/2))    # screen.blit(text_surface, (x, y))

    # Draw "back to main menu" button
    button_rect = pygame.Rect(SCREEN_WIDTH/3, SCREEN_HEIGHT/2+40, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, WHITE, button_rect)

    # Draw text inside button
    text_surface = font_normal.render("Back to main menu", True, font_color)
    coords = button_rect.center
    x, y = coords[0]-94, coords[1]-10
    screen.blit(text_surface, (x, y))

    # Return clickable button
    return button_rect

def resetGlobalVariables():
    '''
    Initializes pieces, game board, and other global variables.
    '''
    global bPawn
    global bKnight
    global bBishop
    global bRook_1
    global bRook_2 
    global bQueen
    global bKing
    global wPawn
    global wKnight
    global wBishop
    global wRook_1
    global wRook_2
    global wQueen
    global wKing
    global empty

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

    global gameBoard
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
    
    global enPassantSquare
    enPassantSquare = (None, None)

    global boardCounter
    boardCounter = 0

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
    '''
    Handle mouse input when clicking on chess board.
    '''
    row = math.floor(pos[1] / SQUARE_SIZE)
    col = math.floor(pos[0] / SQUARE_SIZE)
    return row, col

def processMove(gameBoard, startRow, startCol, endRow, endCol, moveByComputer=True):
    '''
    Makes a move with given parameters.
    Returns:
        True if move was succesful
        False if move was denied
    '''
    if moveIsLegal(gameBoard, startRow, startCol, endRow, endCol):
        makeTheMove(startRow, startCol, endRow, endCol, gameBoard, moveByComputer, False)
        return True
    else:
        return False

def moveIsLegal(gameBoard, startRow, startCol, endRow, endCol):
    '''
    Checks if a move is possible to be made according to the rules of chess.
    '''
    # if move follows piece movement rules
    if move_logic(gameBoard, startRow, startCol, endRow, endCol) or moveIsEnPassant(gameBoard, startRow, startCol, endRow, endCol):
        # if move does not lead to a self check (self check = own king is in danger)
        if check_logic(gameBoard, startRow, startCol, endRow, endCol):
            if moveIsCastle(gameBoard, startRow, startCol, endRow, endCol):
                if castling_logic(gameBoard, startRow, startCol, endRow, endCol):
                    # move can be done
                    return True
            else:
                # move can be done
                return True
    # move cannot be done
    return False

def makeTheMove(startRow, startCol, endRow, endCol, gameBoard, moveByComputer, usingTempBoard):
    '''
    Moves the pieces on the chess board.
    '''
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
        #TODO: updateDevelopmentTable() not working as intended.
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

def moveIsEnPassant(gameBoard, startRow, startCol, endRow, endCol):
    '''
    Checks if a move is an en passant.
    '''
    if enPassantSquare != (None, None):
        #For white pawn
        if gameBoard[startRow][startCol].color == "white" and (gameBoard[startRow][startCol].name == "pawn"):
            # if startRow is on rank 5 AND endRow is on rank 6 AND endCol is 1 file from startCol
            if (startRow == 3) and (endRow == 2) and (abs(startCol - endCol) == 1):
                # if endSquare is enpassantSquare
                if (endRow, endCol) == enPassantSquare:
                    return True
        # For black pawn
        elif gameBoard[startRow][startCol].color == "black" and (gameBoard[startRow][startCol].name == "pawn"):
            if (startRow == 4) and (endRow == 5) and (abs(startCol - endCol) == 1):
                if (endRow, endCol) == enPassantSquare:
                    return True
    return False

def moveEnPassant(gameBoard, startRow, startCol, endRow, endCol):
    '''
    Moves the pieces on the chess board.
    '''
    gameBoard[endRow][endCol] = gameBoard[startRow][startCol]
    gameBoard[startRow][startCol] = empty
    gameBoard[startRow][endCol] = empty

def updateEnPassantSquare(startRow, startCol, endRow, endCol, gameBoard):
    '''
    Keeps track of the en passant square.
    '''
    global enPassantSquare
    if gameBoard[endRow][endCol].name == "pawn" and abs(startRow - endRow) == 2:
        enPassantSquare = (int(startRow - (startRow - endRow) / 2), startCol)
    else: 
        enPassantSquare = (None, None)
    
def move_logic(gameBoard, startRow, startCol, endRow, endCol):
    '''
        Returns:
        bool True: if move is allowed by piece's move logic
        bool False: otherwise
    '''
    return gameBoard[startRow][startCol].moveLogic(gameBoard, startRow, startCol, endRow, endCol)

def check_logic(gameBoard, startRow, startCol, endRow, endCol):
    ''' 
        Checks if a move does not lead to a self check (self check = own king is under attack).
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
    '''
    Checks if castling is possible in the current position according to the rules of chess.
    Returns:
        True: if castling is possible
        False: if castling is not possible
    '''
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
                        return False
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
                        return False
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
                        return False
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
                        return False
            return True
    return False
               
def getAllMoves(gameBoard, color):
    '''
        Gets all moves by color allowed by moveLogic only!!; Does not account for check logic!
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
    '''
    Moves the pieces on the chess board.
    '''
    # updating castling rights
    if gameBoard[startRow][startCol].name in  ("rook", "king"):
        gameBoard[startRow][startCol].canCastle = False
    # moving piece
    gameBoard[endRow][endCol] = gameBoard[startRow][startCol]
    gameBoard[startRow][startCol] = empty
    
def updateDevelopmentTable(startRow, startCol, endRow, endCol, gameBoard):
    '''
    Note! Does not work as intended!

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
    '''
    Reverses the previous move.
    '''
    gameBoard[startRow][startCol] = gameBoard[endRow][endCol]
    gameBoard[endRow][endCol] = revivedPiece

def promotePawn(gameBoard, startRow, startCol, endRow, endCol, moveByComputer=True):
    '''
    Replaces movePiece() in case of a pawn promotion. Moves pieces on the chess board.
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
    '''
    Moves pieces on the chess board.
    '''
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
    # Own king is not in check -> Stalemate
    return 0

def printResult(result):
    '''
    Prints the result of the game.
    '''
    if result == 0:
        print("Draw! It is a stalemate.")
    elif result == 1:
        print("White wins!")
    elif result == 2:
        print("Black wins!")

def minimaxAdvanced(gameboard, whitetomove, depth, canIncreaseDepth, startTime):
    '''
    Minimax algorithm to search for the best move. Uses recursion to go through all the moves and to get their evaluations.
    Selects best move according to Evaluation.getEvaluation().
    Time limit is set to 30 seconds, after which recurison is stopped. 
    (Without time limit and depth=2+1 recursion can take up to 4 minutes depending on the position.)

    Returns:
        eval: int
        best_moves: [(startRow, startCol, endRow, endCol), ] # a list of best moves which share the same eval.
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
    
    # if move takes over 20 seconds -> limit depth
    timeTaken = time.time() - startTime
    if timeTaken > 20:
        canIncreaseDepth = False
        if timeTaken > 30:
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
            materialBefore = Evaluation.countMaterial(temp_board)
            makeTheMove(move[0], move[1], move[2], move[3], temp_board, True, True)
            materialAfter = Evaluation.countMaterial(temp_board)
            
            if depth == 1 and canIncreaseDepth and (isMoveCheck(temp_board, move[2], move[3]) or (abs(materialAfter - materialBefore) > 2)):
                depth += 1
                canIncreaseDepth = False

            eval = minimaxAdvanced(temp_board, not whitetomove, depth-1, canIncreaseDepth, startTime)[0]
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
            materialBefore = Evaluation.countMaterial(temp_board)
            makeTheMove(move[0], move[1], move[2], move[3], temp_board, True, True)
            materialAfter = Evaluation.countMaterial(temp_board)

            if depth == 1 and  canIncreaseDepth and (isMoveCheck(temp_board, move[2], move[3]) or (abs(materialAfter - materialBefore) > 2)):
                depth += 1
                canIncreaseDepth = False

            eval = minimaxAdvanced(temp_board, not whitetomove, depth-1, canIncreaseDepth, startTime)[0]
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
    Basic minimax algorithm to get the best move according to Evaluation.getEvaluation(). 
    Depth cannot be adjusted.

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

def call_minimax(gameboard, whitetomove, depth, canIncreaseDepth, advancedMode):
    '''
    Calls minimax algorithm. Selects one move from the list of best_moves.

    Returns:
        best_move: (startRow, startCol, endRow, endCol)
    '''
    global boardCounter
    startTime = time.time()

    if advancedMode:
        evaluation, best_moves = minimaxAdvanced(gameboard, whitetomove, depth, canIncreaseDepth, startTime)

    else:
        evaluation, best_moves = minimaxBasic(gameboard, whitetomove, depth, canIncreaseDepth)

    # if more than one best move -> pick one randomly
    if len(best_moves) > 1:
            randomIndex = random.randint(0, len(best_moves)-1)
            best_move = best_moves[randomIndex]
    else:
        best_move = best_moves[0]

    # get the time it took to get the move
    endTime = time.time()
    totalTime = round((endTime - startTime), 2)

    print(f"call_minimax: minimax went through {boardCounter} boards and it took {totalTime} seconds")
    print(f"call_minimax: Computer evaluates the position as {evaluation}")

    # reset boardCounter
    boardCounter = 0

    return best_move

def isMoveCheck(gameBoard, endRow, endCol):
    '''
    Checks if a move attacks the opponent's king. Called AFTER the move has been made.
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
        
    # Move does not lead to a check
    return False

def main():
    # Initialize main variables
    clock = pygame.time.Clock()
    highlighted = False # boolean, whether a piece is selected on the board with a mouse click
    whiteToMove = True  # whose turn it is to move
    startRow = 0 # Initialize for draw_chessboard(). Will not be used before getting real values
    startCol = 0 # Initialize for draw_chessboard(). Will not be used before getting real values
    result = -1 # Initialize. -1(game not over), 0(stalemate), 1(white wins), 2(black wins)
    game_state = "main_menu"
    game_mode = None
    # Initialize global variables
    resetGlobalVariables()

    # infinite loop
    while True:

        while game_state == "main_menu":

            draw_mainMenu()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If mouse click coordinates collide with button surface area
                    if mainMenu_buttonData[0][0].collidepoint(event.pos):
                        print("White vs. Easy Bot")
                        game_mode = "whiteVsEasyBot"
                        game_state = "game_ongoing"

                    elif mainMenu_buttonData[1][0].collidepoint(event.pos):
                        print("Black vs. Easy Bot; Not available")
                        # game_mode = "blackVsEasyBot"
                        # game_state = "game_ongoing"

                    elif mainMenu_buttonData[2][0].collidepoint(event.pos):
                        print("White vs. Hard Bot")
                        game_mode = "whiteVsHardBot"
                        game_state = "game_ongoing"

                    elif mainMenu_buttonData[3][0].collidepoint(event.pos):
                        print("Black vs. Hard Bot; Not available")
                        # game_mode = "blackVsHardBot"
                        # game_state = "game_ongoing"

                    elif mainMenu_buttonData[4][0].collidepoint(event.pos):
                        print("White and Black")
                        game_mode = "whiteAndBlack"
                        game_state = "game_ongoing"

                    elif mainMenu_buttonData[5][0].collidepoint(event.pos):
                        print("Quit Game")
                        pygame.quit()
                        sys.exit()

            clock.tick(30)

        while game_state == "game_ongoing":

            if game_mode == "whiteAndBlack":

                screen.fill(DARK)
                draw_chessboard(highlighted, startRow, startCol)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
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
                                    game_state = "game_over"
            
            elif game_mode == "whiteVsEasyBot":

                screen.fill(DARK)
                draw_chessboard(highlighted, startRow, startCol)
                pygame.display.flip()
                if whiteToMove:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

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
                                        game_state = "game_over"
                screen.fill(DARK)
                draw_chessboard(highlighted, startRow, startCol)
                pygame.display.flip()

                if not whiteToMove and game_state == "game_ongoing":

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    bestMove = call_minimax(gameBoard, whiteToMove, 2, True, False)
                    startRow = bestMove[0]
                    startCol = bestMove[1]
                    endRow = bestMove[2]
                    endCol = bestMove[3]
                    if processMove(gameBoard, startRow, startCol, endRow, endCol, moveByComputer=True):
                        whiteToMove = not whiteToMove
                        result = isGameOver(gameBoard, whiteToMove)
                        if result != -1:
                            printResult(result)
                            game_state = "game_over"
                    else:
                        print("main: error: best move is not playable")
            
            elif game_mode == "whiteVsHardBot":

                screen.fill(DARK)
                draw_chessboard(highlighted, startRow, startCol)
                pygame.display.flip()
                if whiteToMove:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

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
                                        game_state = "game_over"
                screen.fill(DARK)
                draw_chessboard(highlighted, startRow, startCol)
                pygame.display.flip()

                if not whiteToMove and game_state == "game_ongoing":

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    bestMove = call_minimax(gameBoard, whiteToMove, 2, True, True)
                    startRow = bestMove[0]
                    startCol = bestMove[1]
                    endRow = bestMove[2]
                    endCol = bestMove[3]
                    if processMove(gameBoard, startRow, startCol, endRow, endCol, moveByComputer=True):
                        whiteToMove = not whiteToMove
                        result = isGameOver(gameBoard, whiteToMove)
                        if result != -1:
                            printResult(result)
                            game_state == "game_over"
                    else:
                        print("main: error: best move is not playable")
        
            clock.tick(30)
        
        while game_state == "game_over":
            
            # Draw chess board
            draw_chessboard(highlighted, startRow, startCol)
            # Draw end menu
            button_rect = draw_endMenu(result)  # get "Back to main menu" button rect
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If mouse click coordinates collide with button surface area
                    if button_rect.collidepoint(event.pos):
                        print("Back to main menu")

                        # Reset main variables.
                        highlighted = False # boolean, whether a piece is selected on the board with a mouse click
                        whiteToMove = True  # whose turn is it to move
                        startRow = 0 # Initialize for draw_chessboard(). Will not be used before getting real values
                        startCol = 0
                        result = -1 # -1(game not over), 0(stalemate), 1(white wins), 2(black wins)
                        game_state = "main_menu"
                        game_mode = None
                        # Reset global variables.
                        resetGlobalVariables()
            
            clock.tick(30)

if __name__ == "__main__":
    main()