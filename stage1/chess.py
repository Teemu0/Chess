''' Some explanations of the terms used
    file = vertical strip on a chess board, think as column
    rank = horizontal strip on a chess board, think as row
'''
import pygame
import math
import time
import move_logic
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
bRook = Rook("black", "rook", "bRook")
bQueen = Queen("black", "queen", "bQueen")
bKing = King("black", "king", "bKing")
wPawn = Pawn("white", "pawn", "wPawn")
wKnight = Knight("white", "knight", "wKnight")
wBishop = Bishop("white", "bishop", "wBishop")
wRook = Rook("white", "rook", "wRook")
wQueen = Queen("white", "queen", "wQueen")
wKing = King("white", "king", "wKing")
empty = Empty(None, None, None)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chessboard")

# Initialize board
gameBoard = [
    [bRook,bKnight,bBishop,bQueen,bKing,bBishop,bKnight,bRook],
    [bPawn,bPawn,bPawn,bPawn,bPawn,bPawn,bPawn,bPawn],
    [empty,empty,empty,empty,empty,empty,empty,empty],
    [empty,empty,empty,empty,empty,empty,empty,empty],
    [empty,empty,empty,empty,empty,empty,empty,empty],
    [empty,empty,empty,empty,empty,empty,empty,empty],
    [wPawn,wPawn,wPawn,wPawn,wPawn,wPawn,wPawn,wPawn],
    [wRook,wKnight,wBishop,wQueen,wKing,wBishop,wKnight,wRook]
    ]

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

def draw_chessboard(highlight, hlSquare):
    # Draw empty chess board
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    # Draw highlighted square
    if highlight:
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (hlSquare[1] * SQUARE_SIZE, hlSquare[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    # Draw pieces to the chessboard
    for row in range(len(gameBoard)):
        for col in range(len(gameBoard[row])):
            if gameBoard[row][col] != empty:
                screen.blit(image_dir[gameBoard[row][col].img_id], (col*SQUARE_SIZE + BORDER_WIDTH, row*SQUARE_SIZE + BORDER_WIDTH))

    

def selectSquare(pos):
    rounded_coords = (math.floor(pos[1] / SQUARE_SIZE), math.floor(pos[0] / SQUARE_SIZE))   # values between 0-7, e.g. (7, 0) equals a1
    selected_square = square_dir[rounded_coords]
    selected_piece = gameBoard[rounded_coords[0]][rounded_coords[1]]
    selection = (rounded_coords, selected_piece)
    #print(f"clicked on coordinates {rounded_coords}")
    #print(f'Selected piece is a {selected_piece} on square {selected_square}.')
    return selection


def makeMove(moveStart, moveEnd, gameBoard):
    ''' Checks whether move is legal, and moves the piece if so.
        
        Parameters:
        - moveStart ((Tuple), Piece): The square with the piece to be moved. Tuple=coordinates, String=piece name.
        - moveEnd ((Tuple), Piece): The square where the piece is to be moved.
        
        Returns:
        bool: True if move was made, False otherwise
    '''
    # dismantle parameters
    pieceToMove = moveStart[1]
    startRow = moveStart[0][0]
    startCol = moveStart[0][1]
    pieceToCapture = moveEnd[1]
    endRow = moveEnd[0][0]
    endCol = moveEnd[0][1]

    # If move is legal
    moveIsLegal = pieceToMove.moveLogic(gameBoard, startRow, startCol, endRow, endCol)
    if moveIsLegal:
        movePiece(startRow, startCol, endRow, endCol, gameBoard)
        if selfInCheck(pieceToMove.color, gameBoard):
            reverseMove(startRow, startCol, endRow, endCol, pieceToCapture, gameBoard)
            # Move declined because of a check
            return False   
        else:
            #If a pawn promotes
            if moveIsLegal == 2:
                print("promotion")
                promotePawn(gameBoard, endRow, endCol)
                
            # Move accepted and done
            return True
    else:
        # Move declined
        return False
    
def selfInCheck(color, gameBoard):
    if color == "white":
        for row in range(8):
            for col in range(8):
                if gameBoard[row][col].color =="black":
                    # If black checks white king
                    if gameBoard[row][col].getMoves(gameBoard, row, col)[0]:
                        return True
    elif color == "black":
        for row in range(8):
            for col in range(8):
                if gameBoard[row][col].color == "white":
                    # If white checks black king
                    if gameBoard[row][col].getMoves(gameBoard, row, col)[0]:
                        return True


def movePiece(startRow, startCol, endRow, endCol, gameBoard):
    gameBoard[endRow][endCol] = gameBoard[startRow][startCol]
    gameBoard[startRow][startCol] = empty

def reverseMove(startRow, startCol, endRow, endCol, revivedPiece, gameBoard):
    gameBoard[startRow][startCol] = gameBoard[endRow][endCol]
    gameBoard[endRow][endCol] = revivedPiece

def promotePawn(gameBoard, row, col):
        while True:
            playerInput = input("Choose piece: Q:queen, R:rook, B:bishop, K:knight")
            if playerInput in ["Q", "q", "R", "r", "B", "b", "K", "k"]:
                break
            else:
                print("Invalid input")
        # If player is white    
        if gameBoard[row][col].color == "white":
            if playerInput in ["Q", "q"]:
                newPiece = wQueen
            elif playerInput in ["R", "r"]:
                newPiece = wRook
            elif playerInput in ["B", "b"]:
                newPiece = wBishop
            elif playerInput in ["K", "k"]:
                newPiece = wKnight
        # If player is black
        elif gameBoard[row][col].color == "black":
            if playerInput in ["Q", "q"]:
                newPiece = bQueen
            elif playerInput in ["R", "r"]:
                newPiece = bRook
            elif playerInput in ["B", "b"]:
                newPiece = bBishop
            elif playerInput in ["K", "k"]:
                newPiece = bKnight
        if newPiece != None:
            gameBoard[row][col] = newPiece
            print("Promotion successful")
        else:
            print("Promotion failed")


def minimax(gameBoard, maximizing):
    # Try every legal move
    temp_board = copy.deepcopy(gameBoard)
    # If white to move
    if maximizing:
        for row in range(8):
            for col in range(8):
                if temp_board[row][col].color =="white":
                    moveStart = ((row, col), temp_board[row][col])
                    movesToTry = temp_board[row][col].getMoves(gameBoard, row, col)[1]             
                    for squares in movesToTry:
                        temp_board = copy.deepcopy(gameBoard)
                        moveEnd = (squares, temp_board[squares[0]][squares[1]])
                        print(f"Move: {moveEnd}")
                        makeMove(moveStart, moveEnd, temp_board)
                        Evaluation.eval(temp_board, maximizing)


def main():
    clock = pygame.time.Clock()
    running = True  # is game running?
    highlighted = False # boolean, whether a piece is selected on the board with a mouse click
    whiteToMove = True  # whose turn is it to move
    moveStart = [(0,0), ""]  # initialize variable. uses format: [(7,0), "wRook"]

    while running:

        screen.fill(DARK)
        draw_chessboard(highlighted, moveStart[0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not highlighted:
                    moveStart = selectSquare(event.pos)
                    if whiteToMove and (moveStart[1].color == "white"):
                        highlighted = True
                    elif not whiteToMove and (moveStart[1].color == "black"):
                        highlighted = True
                else:
                    moveEnd = selectSquare(event.pos)
                    highlighted = False
                    print(f"Starting sq: {moveStart}")
                    print(f"Ending sq: {moveEnd}")
                    if makeMove(moveStart, moveEnd, gameBoard):
                        whiteToMove = not whiteToMove
                        # Evaluation.eval(gameBoard, whiteToMove)
                        # minimax(gameBoard, whiteToMove)
                        Evaluation.checkWin(gameBoard, whiteToMove)
    
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()



if __name__ == "__main__":
    main()