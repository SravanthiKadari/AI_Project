import pygame
import sys
import time

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
LINE_COLOR = (23, 145, 135)  # Color for grid lines
CIRCLE_COLOR = (242, 85, 96)  # Color for 'O'
X_COLOR = (0, 0, 255)  # Color for 'X'
BG_COLOR = (28, 170, 156)  # Background color
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
board = [["_", "_", "_"],
         ["_", "_", "_"],
         ["_", "_", "_"]]

# Game variables
player = 'x'  # Player 1
opponent = 'o'  # Player 2 (AI)
current_player = player
game_over = False

# Score counters
player_1_wins = 0
player_2_wins = 0
ties = 0

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
            if board[row][col] == 'x':
                pygame.draw.line(screen, X_COLOR, 
                                 (col * WIDTH // 3 + X_OFFSET, row * HEIGHT // 3 + X_OFFSET), 
                                 ((col + 1) * WIDTH // 3 - X_OFFSET, (row + 1) * HEIGHT // 3 - X_OFFSET), X_WIDTH)
                pygame.draw.line(screen, X_COLOR, 
                                 ((col + 1) * WIDTH // 3 - X_OFFSET, row * HEIGHT // 3 + X_OFFSET), 
                                 (col * WIDTH // 3 + X_OFFSET, (row + 1) * HEIGHT // 3 - X_OFFSET), X_WIDTH)
            elif board[row][col] == 'o':
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                   (col * WIDTH // 3 + WIDTH // 6, row * HEIGHT // 3 + HEIGHT // 6), 
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

# Check for winner
def check_winner():
    # Check rows, columns, and diagonals for a win
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "_":
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "_":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != "_":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "_":
        return board[0][2]
    return None

# Check for tie
def check_tie():
    for row in range(3):
        for col in range(3):
            if board[row][col] == "_":
                return False
    return True

# Draw the game status
def draw_status():
    if game_over:
        message = "Wins!"
    elif check_tie():
        message = "It's a Tie!"
    else:
        message = f"Player {current_player}'s Turn"

    text = font.render(message, True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

    # Display the total score at the top of the screen
    score_text = font.render(f"Player 1: {player_1_wins}  Player 2: {player_2_wins}  Ties: {ties}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

# Minimax evaluation function
def evaluate(b):
    # Checking for Rows for X or O victory.
    for row in range(3):
        if b[row][0] == b[row][1] == b[row][2] != "_":
            return 10 if b[row][0] == player else -10

    # Checking for Columns for X or O victory.
    for col in range(3):
        if b[0][col] == b[1][col] == b[2][col] != "_":
            return 10 if b[0][col] == player else -10

    # Checking for Diagonals for X or O victory.
    if b[0][0] == b[1][1] == b[2][2] != "_":
        return 10 if b[0][0] == player else -10
    if b[0][2] == b[1][1] == b[2][0] != "_":
        return 10 if b[0][2] == player else -10

    return 0  # No winner

# Check if there are any moves left
def isMovesLeft(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                return True
    return False

# Minimax algorithm to evaluate the best move for the AI
def minimax(board, depth, isMax):
    score = evaluate(board)

    # If Maximizer has won the game return his/her evaluated score
    if score == 10:
        return score

    # If Minimizer has won the game return his/her evaluated score
    if score == -10:
        return score

    # If there are no moves left and no winner, it's a tie
    if not isMovesLeft(board):
        return 0

    # If this is the maximizer's move (AI)
    if isMax:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = player
                    best = max(best, minimax(board, depth + 1, not isMax))
                    board[i][j] = "_"
        return best

    # If this is the minimizer's move (Player)
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = opponent
                    best = min(best, minimax(board, depth + 1, not isMax))
                    board[i][j] = "_"
        return best

# This will return the best possible move for the player
def findBestMove(board):
    bestVal = -1000
    bestMove = (-1, -1)

    # Traverse all cells, evaluate minimax function for all empty cells.
    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                board[i][j] = player  # Make the move
                moveVal = minimax(board, 0, False)
                board[i][j] = "_"

                if moveVal > bestVal:
                    bestMove = (i, j)
                    bestVal = moveVal

    return bestMove

# Reset the game after a win or tie
def reset_game():
    global board, current_player, game_over
    board = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]  # Reset the board
    current_player = player  # Player 1 starts
    game_over = False

# Main game loop
def main():
    global current_player, game_over, player_1_wins, player_2_wins, ties

    screen.fill(BG_COLOR)
    draw_lines()
    draw_symbols()

    # Check for game-over condition before drawing status
    winner = check_winner()
    if winner:
        game_over = True
        if winner == player:
            player_1_wins += 1
        else:
            player_2_wins += 1
    elif check_tie():
        game_over = True
        ties += 1

    draw_status()

    # If the game is over, don't allow further moves
    if not game_over:
        # If it's Player 1's turn (X), calculate the best move for Player 1 (AI)
        if current_player == player:
            time.sleep(1)  # Delay to make the move visible
            best_move = findBestMove(board)
            board[best_move[0]][best_move[1]] = player
            current_player = opponent  # Switch to Player 2 (O)

        # If it's Player 2's turn (O), calculate the best move for Player 2 (AI)
        elif current_player == opponent:
            time.sleep(1)  # Delay to make the move visible
            best_move = findBestMove(board)
            board[best_move[0]][best_move[1]] = opponent
            current_player = player  # Switch to Player 1 (X)

    # After the game ends, pause for 2 seconds before restarting
    if game_over:
        time.sleep(2)
        reset_game()

    pygame.display.update()

# Run the game
while True:
    main()
