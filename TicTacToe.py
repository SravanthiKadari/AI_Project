import pygame
import sys
import random
import time

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
LINE_COLOR = (28, 170, 156)
CIRCLE_COLOR = (242, 85, 96)
X_COLOR = (0, 0, 255)  # Blue color for Player 1's 'X'
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
X_WIDTH = 25
X_OFFSET = 50
O_OFFSET = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.Font(None, 40)

# The game board
board = [[" ", " ", " "],
         [" ", " ", " "],
         [" ", " ", " "]] 

# Game variables
player_1_symbol = "X"
player_2_symbol = "O"
current_player = player_1_symbol
game_over = False

# Draw grid lines
def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * HEIGHT // 3), (WIDTH, 2 * HEIGHT // 3), LINE_WIDTH)
    
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), LINE_WIDTH)

# Draw X and O symbols
def draw_symbols():
    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                # Draw X for Player 1 (Blue)
                pygame.draw.line(screen, X_COLOR, 
                                 (col * WIDTH // 3 + X_OFFSET, row * HEIGHT // 3 + X_OFFSET), 
                                 ((col + 1) * WIDTH // 3 - X_OFFSET, (row + 1) * HEIGHT // 3 - X_OFFSET), X_WIDTH)
                pygame.draw.line(screen, X_COLOR, 
                                 ((col + 1) * WIDTH // 3 - X_OFFSET, row * HEIGHT // 3 + X_OFFSET), 
                                 (col * WIDTH // 3 + X_OFFSET, (row + 1) * HEIGHT // 3 - X_OFFSET), X_WIDTH)
            elif board[row][col] == "O":
                # Draw O for Player 2 (AI)
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                   (col * WIDTH // 3 + WIDTH // 6, row * HEIGHT // 3 + HEIGHT // 6), 
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

# Check for winner
def check_winner():
    global game_over, current_player
    # Check rows, columns, and diagonals
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != " ":
            pygame.draw.line(screen, (250, 0, 0), 
                             (0, row * HEIGHT // 3 + HEIGHT // 6), 
                             (WIDTH, row * HEIGHT // 3 + HEIGHT // 6), 10)
            game_over = True
            return board[row][0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            pygame.draw.line(screen, (250, 0, 0), 
                             (col * WIDTH // 3 + WIDTH // 6, 0), 
                             (col * WIDTH // 3 + WIDTH // 6, HEIGHT), 10)
            game_over = True
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != " ":
        pygame.draw.line(screen, (250, 0, 0), (0, 0), (WIDTH, HEIGHT), 10)
        game_over = True
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != " ":
        pygame.draw.line(screen, (250, 0, 0), (WIDTH, 0), (0, HEIGHT), 10)
        game_over = True
        return board[0][2]

    return None

# Check for tie
def check_tie():
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                return False
    return True

# Draw the game status
def draw_status():
    if game_over:
        message = f"Player {current_player} Wins!"
    elif check_tie():
        message = "It's a Tie!"
    else:
        message = f"Player {current_player}'s Turn"

    text = font.render(message, True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

# Handle click (for Player 1)
def handle_click(x, y):
    global current_player
    row = y // (HEIGHT // 3)
    col = x // (WIDTH // 3)

    if board[row][col] == " " and not game_over:
        board[row][col] = current_player
        if check_winner() is None and not check_tie():
            current_player = player_2_symbol  # Switch to Player 2's turn (AI)

# AI Move: Player 2 (and Player 1)
def ai_move():
    global current_player
    available_moves = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
    
    if available_moves:
        move = random.choice(available_moves)  # Choose a random available move
        board[move[0]][move[1]] = current_player
        print(f"Player {current_player} chooses position {move}")
        if check_winner() is None and not check_tie():
            # Switch player after AI move
            current_player = player_1_symbol if current_player == player_2_symbol else player_2_symbol

# Main game loop
def main():
    global game_over, current_player
    screen.fill(BG_COLOR)
    draw_lines()
    draw_symbols()
    draw_status()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # AI makes a move if it is Player 1's or Player 2's turn and the game is not over
    if not game_over:
        time.sleep(1)  # AI delay to make the move visible
        ai_move()

    pygame.display.update()

# Run the game
while True:
    main()

