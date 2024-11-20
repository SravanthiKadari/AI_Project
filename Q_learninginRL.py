import pygame
import sys
import random
import time
import numpy as np

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
LINE_COLOR = (23, 145, 135)  # Black color for grid lines
CIRCLE_COLOR = (242, 85, 96)
X_COLOR = (0, 0, 255)  # Blue color for Player 1's 'X'
BG_COLOR = (28, 170, 156)
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

# Score counters
player_1_wins = 0
player_2_wins = 0
ties = 0

# Q-learning constants
ALPHA = 0.1      # Learning rate
GAMMA = 0.9      # Discount factor
EPSILON = 0.2   # Exploration rate
NUM_EPISODES = 10  # Number of games to train the AI

# Define Q-table: flatten the board, so there are 3^9 possible states
Q_table = {}

# Initialize Q-table
def initialize_q_table():
    for i in range(3**9):
        Q_table[i] = [0] * 9  # 9 actions (corresponding to positions 0 to 8)

# Convert the board state to a unique number for Q-table lookup
def state_to_number(state):
    mapping = {' ': 0, 'X': 1, 'O': 2}
    num = 0
    for i, row in enumerate(state):
        for j, cell in enumerate(row):
            num += mapping[cell] * (3 ** (i * 3 + j))
    return num

# Convert a Q-table state number back to the board representation
def number_to_state(num):
    mapping = {0: ' ', 1: 'X', 2: 'O'}
    state = [[' ' for _ in range(3)] for _ in range(3)]
    for i in range(9):
        state[i // 3][i % 3] = mapping[num % 3]
        num //= 3
    return state

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
                pygame.draw.line(screen, X_COLOR, 
                                 (col * WIDTH // 3 + X_OFFSET, row * HEIGHT // 3 + X_OFFSET), 
                                 ((col + 1) * WIDTH // 3 - X_OFFSET, (row + 1) * HEIGHT // 3 - X_OFFSET), X_WIDTH)
                pygame.draw.line(screen, X_COLOR, 
                                 ((col + 1) * WIDTH // 3 - X_OFFSET, row * HEIGHT // 3 + X_OFFSET), 
                                 (col * WIDTH // 3 + X_OFFSET, (row + 1) * HEIGHT // 3 - X_OFFSET), X_WIDTH)
            elif board[row][col] == "O":
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
    
    # Display the total score at the top of the screen
    score_text = font.render(f"Player 1: {player_1_wins}  Player 2: {player_2_wins}  Ties: {ties}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

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

    # Get all available moves (empty spots on the board)
    available_moves = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
    
    # If there are no available moves, the game is over (just return)
    if not available_moves:
        return

    # Convert board to number representation (state number)
    state_num = state_to_number(board)
    
    if random.random() < EPSILON:
        # Exploration: Choose random move
        move = random.choice(available_moves)
    else:
        # Exploitation: Choose the best move based on Q-table
        # First, collect the Q-values for the available moves
        q_values = [Q_table[state_num][r * 3 + c] for r, c in available_moves]
        
        # Ensure that q_values is not empty
        if q_values:
            max_q_value = max(q_values)  # Get the max Q-value
            best_moves = [available_moves[i] for i in range(len(available_moves)) if q_values[i] == max_q_value]
            move = random.choice(best_moves)  # Pick a random best move from the options
        else:
            # If no valid Q-values exist, choose a random move
            move = random.choice(available_moves)
    
    # Perform the move
    board[move[0]][move[1]] = current_player

    # Check for terminal state (game over) and calculate reward
    winner = check_winner()
    reward = 0
    if winner == player_2_symbol:  # AI wins
        reward = 1
    elif winner == player_1_symbol:  # Player 1 wins
        reward = -1
    elif check_tie():  # Tie
        reward = 0

    # Update the Q-table
    new_state_num = state_to_number(board)
    
    if winner or check_tie():
        # If the game ends, no future states, so use reward directly
        Q_table[state_num][move[0] * 3 + move[1]] += ALPHA * (reward - Q_table[state_num][move[0] * 3 + move[1]])
        draw_symbols()
        draw_status()
    else:
        # If not game over, we update based on the next best state
        future_q_value = max(Q_table[new_state_num]) if new_state_num in Q_table else 0
        Q_table[state_num][move[0] * 3 + move[1]] += ALPHA * (reward + GAMMA * future_q_value - Q_table[state_num][move[0] * 3 + move[1]])
        draw_symbols()
        
    pygame.display.update()
    print(f"Player {current_player} chooses position {move} with reward {reward}")
    

    # Switch players after the move
    if not game_over:
        current_player = player_1_symbol if current_player == player_2_symbol else player_2_symbol

    # Update the win/tie counters
    if winner == player_1_symbol:
        global player_1_wins
        player_1_wins += 1
    elif winner == player_2_symbol:
        global player_2_wins
        player_2_wins += 1
    elif check_tie():
        global ties
        ties += 1

# Main game loop
def main():
    initialize_q_table() 
    pygame.display.update()

# Initialize Q-table and start training
initialize_q_table()

for episode in range(NUM_EPISODES):
    board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    screen.fill(BG_COLOR)
    draw_lines()

    game_over = False

    while not game_over:
        time.sleep(1)
        draw_symbols()
        ai_move()

        if check_winner() or check_tie():
            draw_symbols()
            game_over = True

    if episode % 1 == 0:
        print(f"Episode {episode+1}/{NUM_EPISODES}")

# Run the game after training
while True:
    main()