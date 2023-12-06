import matplotlib.pyplot as plt
import numpy as np
import random
board_size = 15

def generate_test_board(board_size):
    # Determine the number of pieces to place on the board (approximately half)
    total_pieces = board_size * board_size // 2

    # Create an empty board
    board = [[' ' for _ in range(board_size)] for _ in range(board_size)]

    # Place black ("B") and white ("W") pieces randomly on the board
    for _ in range(total_pieces):
        row, col = random.randint(0, board_size - 1), random.randint(0, board_size - 1)
        while board[row][col] != ' ':
            row, col = random.randint(0, board_size - 1), random.randint(0, board_size - 1)
        board[row][col] = random.choice(['B', 'W'])

    return board

def display_board(board):
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
                plt.plot(col, board_size - 1 - row, 'ko', markersize=10)
            elif board[row][col] == 'W':
                plt.plot(col, board_size - 1 - row, 'wo', markersize=10)

    plt.xticks(range(board_size), labels=[str(col) for col in range(board_size)])
    plt.yticks(range(board_size), labels=[str(row) for row in range(board_size)])

    plt.gca().invert_yaxis()  # Invert y-axis to match the board orientation
    plt.grid(True)
    plt.show()

def evaluate(board, player):
    # Function to transpose the board (swap rows and columns)
    def transpose(board):
        return list(map(list, zip(*board)))

    # Initialize counts for each pattern
    total_pattern_counts = {}

    # Evaluate rows
    for row in board:
        line = ''.join(row)
        pattern_counts = find_patterns_in_line(line, player)
        update_total_counts(total_pattern_counts, pattern_counts)

    # Evaluate columns
    transposed_board = transpose(board)
    for col in transposed_board:
        line = ''.join(col)
        pattern_counts = find_patterns_in_line(line, player)
        update_total_counts(total_pattern_counts, pattern_counts)

    # Evaluate diagonals
    diagonals = get_diagonals(board)
    for diagonal in diagonals:
        line = ''.join(diagonal)
        pattern_counts = find_patterns_in_line(line, player)
        update_total_counts(total_pattern_counts, pattern_counts)

    # Calculate the score based on the number of patterns
    score = 0

    if total_pattern_counts.get("FiveInRow", 0) != 0:
        score += 100000

    if total_pattern_counts.get("LiveFourRight", 0) == 1 or total_pattern_counts.get("LiveFourLeft", 0) == 1:
        score += 15000

    if (total_pattern_counts.get("LiveThreeRight", 0) >= 2 or total_pattern_counts.get("LiveThreeLeft", 0) >= 2 or
            (total_pattern_counts.get("DeadFour", 0) == 2) or
            (total_pattern_counts.get("DeadFour", 0) == 1 and (total_pattern_counts.get("LiveThreeRight", 0) == 1 or total_pattern_counts.get("LiveThreeLeft", 0) >= 2))):
        score += 10000

    if total_pattern_counts.get("LiveThreeRight", 0) or total_pattern_counts.get("LiveThreeLeft", 0) == 2:
        score += 5000

    if total_pattern_counts.get("DeadFour", 0) != 0:
        score += 1000

    if total_pattern_counts.get("DeadFour", 0) != 0:
        score += 300

    if total_pattern_counts.get("DeadFour", 0) != 0:
        score += total_pattern_counts.get("DeadFour", 0) * 50

    return score

def update_total_counts(total_counts, pattern_counts):
    for pattern, count in pattern_counts.items():
        total_counts[pattern] = total_counts.get(pattern, 0) + count

def get_diagonals(board):
    diagonals = []
    for i in range(len(board)):
        diagonal_up = [board[i + k][k] for k in range(min(len(board) - i, len(board[0])))]
        diagonal_down = [board[k][i + k] for k in range(min(len(board[0]) - i, len(board)))]
        diagonals.extend([diagonal_up, diagonal_down])
    return diagonals


def find_patterns_in_line(line, player):
    patterns = {
        "FiveInRow": "XXXXX",
        "LiveFourRight": "XXXX0",
        "LiveFourLeft": "0XXXX",
        "DeadFour": "1XXXX1",
        "LiveThreeRight": "XXX02",
        "LiveThreeLeft": "20XXX",
        "DeadThree": "1XXX1",
        "LiveTwoRight": "XX022",
        "LiveTwoLeft": "220XX",
        "DeadTwo": "1XX12"
    }

    # Initialize counts for each pattern
    pattern_counts = {pattern: 0 for pattern in patterns}

    # Iterate over each pattern and count occurrences in the line
    for pattern_name, pattern_mask in patterns.items():
        pattern_length = len(pattern_mask)
        i = 0
        while i < len(line) - pattern_length + 1:
            substring = line[i:i + pattern_length]
            if is_match(substring, pattern_mask, player):
                pattern_counts[pattern_name] += 1
                # Remove the matched substring from the line
                line = line[:i] + ' ' * pattern_length + line[i + pattern_length:]
            else:
                i += 1

    return pattern_counts

def is_match(substring, mask, player):
    if len(substring) != len(mask):
        raise ValueError("Length of substring and mask must be the same.")

    # Iterate through each character in the substring and mask
    for sub_char, mask_char in zip(substring, mask):
        if mask_char == 'X':
            # For 'X', check if it matches the current player
            if sub_char != player:
                return False
        elif mask_char == '0':
            # For '0', check if it is an empty space
            if sub_char != ' ':
                return False
        elif mask_char == '1':
            # For '1', check if it matches the opponent
            opponent = "W"
            if sub_char != opponent:
                return False
        else:
            pass
    return True

board = generate_test_board(board_size)
display_board(board)
print(evaluate(board, 'B'))


