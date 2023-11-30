''' Some explanations of the terms used
    file = vertical strip on a chess board, think as column
    rank = horizontal strip on a chess board, think as row
'''
import pygame
import math
import move_logic
from Piece import Piece
from Empty import Empty
from Pawn import Pawn
from Rook import Rook
from Bishop import Bishop

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

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chessboard")

gameBoard = [[Rook("black", "rook", "bRook"),'bKnight',Bishop("black", "bishop", "bBishop"),'bQueen','bKing',Bishop("black", "bishop", "bBishop"),'bKnight',Rook("black", "rook", "bRook")],
          [Pawn("black", "pawn", "bPawn"),Pawn("black", "pawn", "bPawn"),Pawn("black", "pawn", "bPawn"),Pawn("black", "pawn", "bPawn"),
           Pawn("black", "pawn", "bPawn"),Pawn("black", "pawn", "bPawn"),Pawn("black", "pawn", "bPawn"),Pawn("black", "pawn", "bPawn")],
          [Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None)],
          [Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None)],
          [Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None)],
          [Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None),Empty(None, None, None)],
          [Pawn("white", "pawn", "wPawn"),Pawn("white", "pawn", "wPawn"),Pawn("white", "pawn", "wPawn"),Pawn("white", "pawn", "wPawn"),
           Pawn("white", "pawn", "wPawn"),Pawn("white", "pawn", "wPawn"),Pawn("white", "pawn", "wPawn"),Pawn("white", "pawn", "wPawn")],
          [Rook("white", "rook", "wRook"),'wKnight',Bishop("white", "bishop", "wBishop"),'wQueen','wKing',Bishop("white", "bishop", "wBishop"),'wKnight',Rook("white", "rook", "wRook")]
          ]

# load white pieces
wKing = pygame.image.load('wKing.png')
wKing = pygame.transform.scale(wKing, (PIECE_SIZE, PIECE_SIZE))
wQueen = pygame.image.load('wQueen.png')
wQueen = pygame.transform.scale(wQueen, (PIECE_SIZE, PIECE_SIZE))
wRook = pygame.image.load('wRook.png')
wRook = pygame.transform.scale(wRook, (PIECE_SIZE, PIECE_SIZE))
wBishop = pygame.image.load('wBishop.png')
wBishop = pygame.transform.scale(wBishop, (PIECE_SIZE, PIECE_SIZE))
wKnight = pygame.image.load('wKnight.png')
wKnight = pygame.transform.scale(wKnight, (PIECE_SIZE, PIECE_SIZE))
wPawn = pygame.image.load('wPawn.png')
wPawn = pygame.transform.scale(wPawn, (PIECE_SIZE, PIECE_SIZE))
# load black pieces
bKing = pygame.image.load('bKing.png')
bKing = pygame.transform.scale(bKing, (PIECE_SIZE, PIECE_SIZE))
bQueen = pygame.image.load('bQueen.png')
bQueen = pygame.transform.scale(bQueen, (PIECE_SIZE, PIECE_SIZE))
bRook = pygame.image.load('bRook.png')
bRook = pygame.transform.scale(bRook, (PIECE_SIZE, PIECE_SIZE))
bBishop = pygame.image.load('bBishop.png')
bBishop = pygame.transform.scale(bBishop, (PIECE_SIZE, PIECE_SIZE))
bKnight = pygame.image.load('bKnight.png')
bKnight = pygame.transform.scale(bKnight, (PIECE_SIZE, PIECE_SIZE))
bPawn = pygame.image.load('bPawn.png')
bPawn = pygame.transform.scale(bPawn, (PIECE_SIZE, PIECE_SIZE))

image_dir = {
    'wKing' : wKing,
    'wQueen' : wQueen,
    'wRook' : wRook,
    'wBishop' : wBishop,
    'wKnight' : wKnight,
    'wPawn' : wPawn,
    'bKing' : bKing,
    'bQueen' : bQueen,
    'bRook' : bRook,
    'bBishop' : bBishop,
    'bKnight' : bKnight,
    'bPawn' : bPawn
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
            try:
                screen.blit(image_dir[gameBoard[row][col].img_id], (col*SQUARE_SIZE + BORDER_WIDTH, row*SQUARE_SIZE + BORDER_WIDTH))
            # DELETE THIS AFTER ALL PIECES USE THEIR OWN CLASSES
            except AttributeError:
                screen.blit(image_dir[gameBoard[row][col]], (col*SQUARE_SIZE + BORDER_WIDTH, row*SQUARE_SIZE + BORDER_WIDTH))
            except KeyError:
                continue
    

def selectSquare(pos):
    rounded_coords = (math.floor(pos[1] / SQUARE_SIZE), math.floor(pos[0] / SQUARE_SIZE))   # values between 0-7, e.g. (7, 0) equals a1
    selected_square = square_dir[rounded_coords]
    selected_piece = gameBoard[rounded_coords[0]][rounded_coords[1]]
    selection = (rounded_coords, selected_piece)
    print(f"clicked on coordinates {rounded_coords}")
    print(f'Selected piece is a {selected_piece} on square {selected_square}.')
    return selection


def makeMove(moveStart, moveEnd):
    ''' Checks whether move is legal, and moves the piece if so.
        
        Parameters:
        - moveStart ((Tuple), String): The square with the piece to be moved. Tuple=coordinates, String=piece name.
        - moveEnd ((Tuple), String): The square where the piece is to be moved.
        
        Returns:
        bool: True if move was made, False otherwise
    '''
    if (moveStart == moveEnd):
        return False
    
    moveCompleted = False
    # dismantle parameters
    pieceToMove = moveStart[1]
    startRow = moveStart[0][0]
    startCol = moveStart[0][1]
    pieceToCapture = moveEnd[1]
    endRow = moveEnd[0][0]
    endCol = moveEnd[0][1]

    moveCompleted = pieceToMove.moveLogic(gameBoard, pieceToCapture, startRow, startCol, endRow, endCol)

    return moveCompleted

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
                    if makeMove(moveStart, moveEnd):
                        whiteToMove = not whiteToMove
    

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()



if __name__ == "__main__":
    main()