import matplotlib.pyplot as plt
import numpy as np

# Define the board
BOARD_SIZE = 15
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def display_board(board):
    """
    Display the board with dots for black and white pieces on a brown background.

    Parameters:
    - board (list of lists): The 2D board to display.
    """
    board_size = len(board)

    # Create a brown background
    brown_background = np.ones((board_size, board_size, 3)) * [0.647, 0.165, 0.165]  # RGB for brown

    # Set color values for black ("B") and white ("W") pieces
    brown_background[board == 'B'] = [0, 0, 0]  # Black
    brown_background[board == 'W'] = [1, 1, 1]  # White

    plt.imshow(brown_background, interpolation='none', extent=[-0.5, board_size - 0.5, -0.5, board_size - 0.5])

    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == 'B':
                plt.plot(col, row, 'ko', markersize=10)
            elif board[row][col] == 'W':
                plt.plot(col, row, 'wo', markersize=10)

    plt.xticks(range(board_size), labels=[str(col) for col in range(board_size)])
    plt.yticks(range(board_size), labels=[str(row) for row in range(board_size)])

    plt.grid(True)
    plt.show()

# Placing and removing pieces 
def place_piece(board, player, row, col):
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == ' ':
        board[row][col] = player
        return True
    else:
        return False
    
def remove_piece(board, player, row, col):
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == player:
        board[row][col] = ' '
        return True
    else:
        return False
    
def get_opponent(player):
    if player == 'B':
        return 'W'
    else:
        return 'B'

# Winning condition
def get_winning_condition(board, player):
    # Check rows
    for row in board:
        if ''.join(row).count(player) > 4:
            return True, player
    # Check columns
    for col in range(len(board[0])):
        column = ''.join(row[col] for row in board)
        if column.count(player) > 4:
            return True, player
    # Check diagonals
    for i in range(len(board) - 4):
        for j in range(len(board[0]) - 4):
            diagonal = ''.join(board[i + k][j + k] for k in range(5))
            anti_diagonal = ''.join(board[i + k][j + 4 - k] for k in range(5))
            if diagonal.count(player) > 4 or anti_diagonal.count(player) > 4:
                return True, player
    return False, None
