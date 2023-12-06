import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Define the board
BOARD_SIZE = 7
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Displaying the board
CELL_SIZE = 40
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def display_board(board):
    BOARD_SIZE = len(board)
    brown_background = np.ones((BOARD_SIZE, BOARD_SIZE, 3)) * [0.647, 0.165, 0.165]  # RGB for brown
    brown_background[board == 'B'] = [0, 0, 0]  # Black
    brown_background[board == 'W'] = [1, 1, 1]  # White

    plt.imshow(brown_background, interpolation='none', extent=[-0.5, BOARD_SIZE - 0.5, -0.5, BOARD_SIZE - 0.5])

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'B':
                plt.plot(col, BOARD_SIZE - 1 - row, 'ko', markersize=10)
            elif board[row][col] == 'W':
                plt.plot(col, BOARD_SIZE - 1 - row, 'wo', markersize=10)

    plt.xticks(range(BOARD_SIZE), labels=[str(col) for col in range(BOARD_SIZE)])
    plt.yticks(range(BOARD_SIZE), labels=[str(row) for row in range(BOARD_SIZE)])

    plt.gca().invert_yaxis()
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

# Player selection 
def player_selection():
    while True:
        choice = input("Select your color (B for Black, W for White): ").upper()
        if choice == 'B':
            return 'B', 'W'
        elif choice == 'W':
            return 'W', 'B'
        else:
            print("Invalid choice. Please enter 'B' or 'W'.")

human_player, ai_player = player_selection()   

# AI opponent functions

# Evaluate board
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
            opponent = get_opponent(player)
            if sub_char != opponent:
                return False
        else:
            pass
    return True

# Find possible moves
def get_possible_moves(board):
    possible_moves = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == ' ':
                possible_moves.append((row, col))
    return possible_moves

# Minimax algorithm
def minimax(board, depth, alpha, beta, maximizing_player, player):
    game_over, winner = get_winning_condition(board, player)

    if depth == 0 or game_over:
        return evaluate(board, player)

    relevant_moves = find_relevant_area(board)
    random.shuffle(relevant_moves)

    if maximizing_player:
        max_eval = -math.inf
        for move in relevant_moves:
            row, col = move
            if place_piece(board, player, row, col):
                eval = minimax(board, depth - 1, alpha, beta, False, player)
                remove_piece(board, player, row, col) # Undo the move
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for move in relevant_moves:
            row, col = move
            if place_piece(board, player, row, col):
                eval = minimax(board, depth - 1, alpha, beta, True, player)
                remove_piece(board, player, row, col)  # Undo the move
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def get_opponent(player):
    return human_player if player == ai_player else ai_player

# Find relevant area
def find_relevant_area(board):
    occupied_positions = [(r, c) for r in range(len(board)) for c in range(len(board[0])) if board[r][c] != ' ']

    if not occupied_positions:
        # Default 3x3 area around the center
        center_row, center_col = len(board) // 2, len(board[0]) // 2
        min_row, max_row = max(0, center_row - 1), min(len(board) - 1, center_row + 1)
        min_col, max_col = max(0, center_col - 1), min(len(board[0]) - 1, center_col + 1)
        return [(r, c) for r in range(min_row, max_row + 1) for c in range(min_col, max_col + 1)]

    min_row = max(0, min(r for r, _ in occupied_positions) - 1)
    max_row = min(len(board) - 1, max(r for r, _ in occupied_positions) + 1)
    min_col = max(0, min(c for _, c in occupied_positions) - 1)
    max_col = min(len(board[0]) - 1, max(c for _, c in occupied_positions) + 1)

    return [(r, c) for r in range(min_row, max_row + 1) for c in range(min_col, max_col + 1)]

# AI move with relevant area
def ai(board, player):
    relevant_moves = find_relevant_area(board)
    random.shuffle(relevant_moves)
    
    best_move = None
    best_score = -math.inf

    for move in relevant_moves:
        row, col = move
        if place_piece(board, player, row, col):
            score = minimax(board, 3, -math.inf, math.inf, False, player)
            remove_piece(board, player, row, col)  # Undo the move

            if score > best_score:
                best_score = score
                best_move = move

    return best_move

# Game logic
def game_loop():
    display_board(board)

    turn = human_player
    for player in (human_player,ai_player):
        if player == 'B':
            turn = player

    while True:
        if turn == human_player:
            try:
                row, col = map(int, input(f"{turn}'s turn (row, col): ").split(','))
            except ValueError:
                print("Invalid input. Please enter two integers separated by a comma.")
                continue
            if not place_piece(board, turn, row, col):
                print("Invalid input. Space is occupied")
                
        else:
            ai_move = ai(board, turn)
            if ai_move is None:
                print("The game is a draw!")
                break
            else:
                row, col = ai_move
                place_piece(board, turn, row, col)
                print(f"{turn} chose ({row}, {col}).")
        
        display_board(board)
        
        game_over, winner = get_winning_condition(board, turn)
        if game_over:
            print(f"{winner} wins!")
            break
        else:
            turn = human_player if turn == ai_player else ai_player

        
        


# Test
game_loop()