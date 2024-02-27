from gomuku import *
import math

def evaluate(board):
    # Function to transpose the board (swap rows and columns)
    def transpose(board):
        return list(map(list, zip(*board)))

    # Initialize counts for each pattern
    black_total_pattern_counts = {}
    white_total_pattern_counts = {}

    # Evaluate rows
    for row in board:
        line = ''.join(row)
        black_pattern_counts = find_patterns_in_line(line, "B")
        update_total_counts(black_total_pattern_counts, black_pattern_counts)
        white_pattern_counts = find_patterns_in_line(line, "W")
        update_total_counts(white_total_pattern_counts, white_pattern_counts)
        
    
    # Evaluate columns
    transposed_board = transpose(board)
    for col in transposed_board:
        line = ''.join(col)
        black_pattern_counts = find_patterns_in_line(line, "B")
        update_total_counts(black_total_pattern_counts, black_pattern_counts)
        white_pattern_counts = find_patterns_in_line(line, "W")
        update_total_counts(white_total_pattern_counts, white_pattern_counts)
    
    # Evaluate diagonals
    diagonals = get_diagonals(board)
    for diagonal in diagonals:
        line = ''.join(diagonal)
        black_pattern_counts = find_patterns_in_line(line, "B")
        update_total_counts(black_total_pattern_counts, black_pattern_counts)
        white_pattern_counts = find_patterns_in_line(line, "W")
        update_total_counts(white_total_pattern_counts, white_pattern_counts)

    # Evaluate anti-diagonals
    anti_diagonals = get_anti_diagonals(board)
    for anti_diagonal in anti_diagonals:
        line = ''.join(anti_diagonal)
        black_pattern_counts = find_patterns_in_line(line, "B")
        update_total_counts(black_total_pattern_counts, black_pattern_counts)
        white_pattern_counts = find_patterns_in_line(line, "W")
        update_total_counts(white_total_pattern_counts, white_pattern_counts)


    # Calculate the score based on the number of patterns
    score = 0

    # Five in a row
    if black_total_pattern_counts.get("FiveInRow", 0) > 0:
        score += 100000
    elif white_total_pattern_counts.get("FiveInRow", 0) > 0:
        score -=100000

    # Open four 
    if black_total_pattern_counts.get("OpenFour", 0) > 0:
        score += black_total_pattern_counts.get("OpenFour", 0) * 5000
    elif white_total_pattern_counts.get("OpenFour", 0) > 0:
        score -= white_total_pattern_counts.get("OpenFour", 0) * 5000

    # Live four
    if black_total_pattern_counts.get("LiveFourRight", 0) > 0 or black_total_pattern_counts.get("LiveFourLeft", 0) > 0:
        score += black_total_pattern_counts.get("LiveFourRight", 0) * 1000
        score += black_total_pattern_counts.get("LiveFourLeft", 0) * 1000
    elif white_total_pattern_counts.get("LiveFourRight", 0) > 0 or white_total_pattern_counts.get("LiveFourLeft", 0) > 0:
        score -= white_total_pattern_counts.get("LiveFourRight", 0) * 1000
        score -= white_total_pattern_counts.get("LiveFourLeft", 0) * 1000
    
    # Open three 
    if black_total_pattern_counts.get("OpenThree", 0) > 0:
        score += black_total_pattern_counts.get("OpenThree", 0) * 1300
    elif white_total_pattern_counts.get("OpenThree", 0) > 0:
        score -= white_total_pattern_counts.get("OpenThree", 0) * 1300

    # Open two
    if black_total_pattern_counts.get("OpenTwo", 0) > 0:
        score += black_total_pattern_counts.get("OpenTwo", 0) * 300
    if white_total_pattern_counts.get("OpenTwo", 0) > 0:
        score -= white_total_pattern_counts.get("OpenTwo", 0) * 300
    
    # Live three
    if black_total_pattern_counts.get("LiveThreeRight", 0) > 0 or black_total_pattern_counts.get("LiveThreeLeft", 0) > 0:
        score += black_total_pattern_counts.get("LiveThreeRight", 0) * 100
        score += black_total_pattern_counts.get("LiveThreeLeft", 0) * 100
    elif white_total_pattern_counts.get("LiveThreeRight", 0) > 0 or white_total_pattern_counts.get("LiveThreeLeft", 0) > 0:
        score -= white_total_pattern_counts.get("LiveThreeRight", 0) * 100
        score -= white_total_pattern_counts.get("LiveThreeLeft", 0) * 100

    # Live twos
    if black_total_pattern_counts.get("LiveTwoRight", 0) > 0 or black_total_pattern_counts.get("LiveTwoLeft", 0) > 0:
            score += black_total_pattern_counts.get("LiveTwoRight", 0) * 10
            score += black_total_pattern_counts.get("LiveTwoLeft", 0) * 10
    if white_total_pattern_counts.get("LiveTwoRight", 0) > 0 or white_total_pattern_counts.get("LiveTwoLeft", 0) > 0:
            score -= white_total_pattern_counts.get("LiveTwoRight", 0) * 10
            score -= white_total_pattern_counts.get("LiveTwoLeft", 0) * 10

    return score

def update_total_counts(total_counts, pattern_counts):
    for pattern, count in pattern_counts.items():
        total_counts[pattern] = total_counts.get(pattern, 0) + count

def get_diagonals(board):
    diagonals = []
    for i in range(len(board)):
        diagonal = ''.join(board[i + k][k] for k in range(min(len(board) - i, len(board[0]))))
        diagonals.append(diagonal)
    for j in range(1, len(board[0])):
        diagonal = ''.join(board[k][j + k] for k in range(min(len(board), len(board[0]) - j)))
        diagonals.append(diagonal)
    return diagonals

def get_anti_diagonals(board):
    antidiagonals = []
    for i in range(len(board)):
        antidiagonal = ''.join(board[i - k][k] for k in range(min(i + 1, len(board[0]))))
        antidiagonals.append(antidiagonal)
    for j in range(1, len(board[0])):
        antidiagonal = ''.join(board[len(board) - 1 - k][j + k] for k in range(min(len(board) - j, len(board[0]))))
        antidiagonals.append(antidiagonal)
    return antidiagonals


def find_patterns_in_line(line, player):
    patterns = {
        "FiveInRow": "XXXXX",
        "OpenFour": "0XXXX0",
        "LiveFourRight": "XXXX0",
        "LiveFourLeft": "0XXXX",
        "DeadFour": "1XXXX1",
        "OpenThree": "0XXX0",
        "LiveThreeRight": "XXX0",
        "LiveThreeLeft": "0XXX",
        "DeadThree": "1XXX1",
        "OpenTwo": "0XX0",
        "LiveTwoRight": "XX0",
        "LiveTwoLeft": "0XX",
        "DeadTwo": "1XX1"
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

def find_relevant_area(board, player):
    relevant_moves = []
    
    eval = evaluate(board)
    
    # Check if board is empty
    def is_board_empty(board):
        for row in board:
            for element in row:
                if element != ' ':
                    return False
        return True
    
    # Returns center moves
    def get_center():
        center_row = len(board) // 2
        center_col = len(board[0]) // 2

        center_moves = [
            (center_row - 1, center_col - 1),
            (center_row - 1, center_col),
            (center_row, center_col - 1),
            (center_row, center_col)
        ]

        return center_moves
    
    if is_board_empty(board):
        return get_center()
    else:
        # Only add moves that affect the score along with their impact
        for row in range(len(board)):
            for col in range(len(board[0])):
                if place_piece(board, player, row, col):
                    new_eval = evaluate(board)
                    impact = new_eval - eval
                    if impact != 0:
                        relevant_moves.append(((row, col), impact))
                    remove_piece(board, player, row, col)

        # Sort moves based on their impact (from highest to lowest)
        relevant_moves.sort(key=lambda move: move[1], reverse=True)

        # Extract only the moves without their impact values
        return [move[0] for move in relevant_moves]


def minimax(board, depth, alpha, beta, maximizing_player):

    if depth == 0: #or get_winning_condition
        return evaluate(board)

    relevant_moves = find_relevant_area(board, "B")

    if maximizing_player:
        eval = -math.inf
        for move in relevant_moves:
            row, col = move
            if place_piece(board, "B", row, col):
                eval = max(eval, minimax(board, depth-1, alpha, beta, False))
                remove_piece(board, "B", row, col)
                if eval > beta:
                    break
                alpha = max(alpha, eval)
                
        return eval
            
    else:
        eval = math.inf
        for move in relevant_moves:
            row, col = move
            if place_piece(board, "W", row, col):
                eval = min(eval, minimax(board, depth-1, alpha, beta, True))
                remove_piece(board, "W", row, col)
                if eval < alpha:
                    break
                beta = min(beta, eval)
                
        return eval
            

def ai(board):
    relevant_moves = find_relevant_area(board, "B")
    
    best_move = None
    best_score = -math.inf

    for move in relevant_moves:
        row, col = move
        if place_piece(board, "B", row, col):
            # Use the minimax algorithm for AI's move
            score = minimax(board, 1, -math.inf, math.inf, True)
            remove_piece(board, "B", row, col)
            if score > best_score:
                best_score = score
                best_move = move
              # Undo the move

    return best_move



