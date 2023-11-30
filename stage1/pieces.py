import pygame

pieces = {
    "wp": pygame.image.load("wPawn.png"),
    #"wr": pygame.image.load("wr.png"),
    # ... Load images for other pieces
}


# Define constants
WIDTH, HEIGHT = 480, 480
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
LIGHT = (232, 194, 145)
DARK = (113, 74, 46)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chessboard")

screen.fill(DARK)
draw_chessboard()
pygame.display.flip()