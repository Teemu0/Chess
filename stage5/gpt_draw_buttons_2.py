import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# Button properties
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_GAP = 20  # Gap between buttons
BUTTONS_PER_ROW = 2  # Number of buttons per row
BUTTON_ROWS = 3  # Number of button rows

# Calculate total horizontal and vertical space for buttons
total_horizontal_space = BUTTON_WIDTH * BUTTONS_PER_ROW + BUTTON_GAP * (BUTTONS_PER_ROW - 1)
total_vertical_space = BUTTON_HEIGHT * BUTTON_ROWS + BUTTON_GAP * (BUTTON_ROWS - 1)

# Calculate starting x and y coordinates for the first button
start_x = (SCREEN_WIDTH - total_horizontal_space) // 2
start_y = (SCREEN_HEIGHT - total_vertical_space) // 2

# List to store button rectangles and their text
button_data = []

# Create buttons and store their rectangles and text
for i in range(BUTTON_ROWS * BUTTONS_PER_ROW):
    row = i // BUTTONS_PER_ROW
    col = i % BUTTONS_PER_ROW
    x = start_x + (BUTTON_WIDTH + BUTTON_GAP) * col
    y = start_y + (BUTTON_HEIGHT + BUTTON_GAP) * row
    button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    text = f"Button {i + 1}"
    button_data.append((button_rect, text))

# Font settings
font = pygame.font.Font(None, 36)
font_color = BLACK

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw buttons and text
    screen.fill(WHITE)
    for button_rect, text in button_data:
        pygame.draw.rect(screen, GRAY, button_rect)
        text_surface = font.render(text, True, font_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()