# Q-Learning in Reinforcement Learning

## Project Overview

This project demonstrates the implementation of **Q-Learning**, a model-free reinforcement learning (RL) algorithm, applied to a **Tic-Tac-Toe** game. In this project, the AI learns to play Tic-Tac-Toe optimally by using the Q-learning algorithm, progressively improving through multiple training episodes. The game is simulated, and the AI's performance improves by interacting with the game environment, making decisions based on the rewards received during gameplay.

## Q-Learning Overview

Q-learning is a reinforcement learning algorithm used to find the optimal action-selection policy for a given finite Markov decision process (MDP). The core idea of Q-learning is to learn a policy that tells an agent what action to take under certain conditions (states) based on maximizing the expected reward over time.

- **Learning Rate (α):** Controls how much newly acquired information overrides old information. A value of 0.1 is used in this implementation.
- **Discount Factor (γ):** Represents the importance of future rewards, with a value of 0.9.
- **Exploration Rate (ε):** The probability of taking a random action instead of following the learned policy. In this case, it's set to 0.2.

## Project Features

- **Tic-Tac-Toe Game**: A 3x3 grid-based game between two players, where Player 1 is human-controlled and Player 2 is AI-controlled.
- **Q-Learning AI**: The AI uses Q-learning to decide the next optimal move based on the current state of the game board.
- **Training Phase**: The AI undergoes a training process over several episodes to learn the best strategies by interacting with the game environment.
- **Game Outcomes**: Tracks the number of wins, ties, and losses throughout the gameplay.

## Requirements

- Python 3.x
- Pygame library (for game rendering)

You can install the required dependencies using `pip`:

```bash
pip install pygame
```

## How to Run the Project

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/SravanthiKadari/AI_Project.git
```

### 2. Navigate to the Project Directory

After cloning, navigate to the directory containing the project:

```bash
cd AI_Project
```

### 3. Run the Python Script

Run the `Q_learninginRL.py` script using Python:

```bash
python Q_learninginRL.py
```

### 4. Gameplay Instructions

- **Player 1**: The human player uses 'X' and interacts with the game by clicking on the grid.
- **Player 2 (AI)**: The AI-controlled player uses 'O'. The AI decides its next move using the Q-learning algorithm.
- The game will continue until one player wins, the board is full resulting in a tie, or the user quits.

## Key Functions and Methods

### 1. `initialize_q_table()`
- Initializes the Q-table, which holds the Q-values for each state-action pair. The Q-table starts with all values set to 0.

### 2. `state_to_number(state)`
- Converts the current game board state into a unique numeric representation used for the Q-table lookup.

### 3. `number_to_state(num)`
- Converts a numeric representation of the board back to a 3x3 board configuration.

### 4. `draw_lines()`
- Draws the grid lines on the Pygame window.

### 5. `draw_symbols()`
- Draws 'X' and 'O' symbols on the board.

### 6. `check_winner()`
- Checks if there is a winner by evaluating rows, columns, or diagonals for three matching symbols.

### 7. `check_tie()`
- Checks if the board is full and there is no winner, resulting in a tie.

### 8. `handle_click(x, y)`
- Handles the player’s click to make a move (Player 1's turn).

### 9. `ai_move()`
- The AI chooses its move using Q-learning. It either explores (chooses a random move) or exploits (chooses the best-known move based on Q-values).

### 10. `main()`
- The main game loop that runs the game, with the AI playing against the human player.

## Training the AI

The AI is trained over several **episodes**, where it plays against itself. During each episode, the AI explores different moves, learns from the outcomes, and updates its Q-table. This training process helps the AI to improve its decision-making strategy, eventually making the AI an effective opponent.

### Q-Table Update Rule

- **Exploration:** With probability ε, the AI chooses a random action (move).
- **Exploitation:** With probability (1 - ε), the AI chooses the action that maximizes the expected future reward, which is stored in the Q-table.
- **Q-value Update Formula:**
  
  \[
  Q(s, a) \leftarrow Q(s, a) + \alpha \cdot \left( r + \gamma \cdot \max_a Q(s', a) - Q(s, a) \right)
  \]

Where:
- \(s\) is the current state
- \(a\) is the action taken
- \(r\) is the immediate reward received
- \(\alpha\) is the learning rate
- \(\gamma\) is the discount factor
- \(\max_a Q(s', a)\) is the maximum expected future reward from the next state \(s'\)

## Project Structure

```
AI_Project/
│
├── Q_learninginRL.py        # Main script for the Tic-Tac-Toe Q-learning game
│
└── README.md                # Project documentation
```

## Acknowledgements

- **Pygame**: A set of Python modules designed for writing video games, used to render the graphical interface of the game.
- **Q-Learning**: A popular reinforcement learning algorithm, applied here to teach an AI to play Tic-Tac-Toe.
