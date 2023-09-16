import numpy as np

# Define the Connect 4 board dimensions
ROWS = 6
COLS = 7

# Constants to represent players
PLAYER_X = 1
PLAYER_O = -1
EMPTY = 0

# Initialize an empty board
board = np.zeros((ROWS, COLS), dtype=int)

# Function to check if a move is valid
def is_valid_move(board, col):
    return board[0][col] == EMPTY

# Function to make a move on the board
def make_move(board, col, player):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = player
            return

# Function to evaluate the current game state
def evaluate(board, player):
    score = 0

    # Check for horizontal wins
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = board[row, col:col+4]
            score += evaluate_window(window, player)

    # Check for vertical wins
    for row in range(ROWS - 3):
        for col in range(COLS):
            window = board[row:row+4, col]
            score += evaluate_window(window, player)

    # Check for diagonal wins (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row-i][col+i] for i in range(4)]
            score += evaluate_window(window, player)

    # Check for diagonal wins (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row+i][col+i] for i in range(4)]
            score += evaluate_window(window, player)

    return score

# Function to evaluate a window of 4 cells
def evaluate_window(window, player):
    score = 0
    opponent = -player

    if window.count(player) == 4:
        score += 1000
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

# Negamax algorithm with alpha-beta pruning
def negamax(board, depth, player, alpha, beta):
    if depth == 0 or is_game_over(board):
        return player * evaluate(board, player)

    max_value = float('-inf')

    for col in range(COLS):
        if is_valid_move(board, col):
            new_board = board.copy()
            make_move(new_board, col, player)
            score = -negamax(new_board, depth - 1, -player, -beta, -alpha)
            
            if score > max_value:
                max_value = score

            alpha = max(alpha, score)
            if alpha >= beta:
                break

    return max_value

# Function to find the best move for the AI
def find_best_move(board, player, depth):
    max_value = float('-inf')
    best_move = None

    for col in range(COLS):
        if is_valid_move(board, col):
            new_board = board.copy()
            make_move(new_board, col, player)
            score = -negamax(new_board, depth - 1, -player, float('-inf'), float('inf'))

            if score > max_value:
                max_value = score
                best_move = col

    return best_move

# Function to check if the game is over
def is_game_over(board):
    return is_winner(board, PLAYER_X) or is_winner(board, PLAYER_O) or is_board_full(board)

# Function to check if a player has won
def is_winner(board, player):
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = board[row, col:col+4]
            if np.array_equal(window, [player, player, player, player]):
                return True

    for row in range(ROWS - 3):
        for col in range(COLS):
            window = board[row:row+4, col]
            if np.array_equal(window, [player, player, player, player]):
                return True

    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row-i][col+i] for i in range(4)]
            if np.array_equal(window, [player, player, player, player]):
                return True

    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row+i][col+i] for i in range(4)]
            if np.array_equal(window, [player, player, player, player]):
                return True

    return False

# Function to check if the board is full (a draw)
def is_board_full(board):
    return np.all(board != EMPTY)

# Example of using the AI to make a move
if __name__ == "__main__":
    while not is_game_over(board):
        # Player X's turn
        print_board(board)
        player_x_col = int(input("Player X, enter column (0-6): "))
        if is_valid_move(board, player_x_col):
            make_move(board, player_x_col, PLAYER_X)

        if is_game_over(board):
            break

        # Player O's turn (AI)
        print_board(board)
        ai_col = find_best_move(board, PLAYER_O, depth=4)  # Adjust the depth as needed
        print(f"AI (Player O) chooses column {ai_col}")
        make_move(board, ai_col, PLAYER_O)

    # Game over
    print_board(board)
    if is_winner(board, PLAYER_X):
        print("Player X wins!")
    elif is_winner(board, PLAYER_O):
        print("Player O (AI) wins!")
    else:
        print("It's a draw!")
