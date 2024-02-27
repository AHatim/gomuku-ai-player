from gomuku import *
from ai import *
import tkinter as tk

def display_board(board):
    # Print column numbers
    print("   " + "   ".join(str(i) for i in range(len(board[0]))))
    print("  " + "----" * len(board[0]))

    for i, row in enumerate(board):
        # Print row number
        print(f"{i} |", end=" ")

        # Print board elements
        print(" | ".join(map(str, row)))

        # Print separator
        print("  " + "----" * len(row))


def display_board_with_relevant_moves(board, relevant_moves=None):
    # Print column numbers
    print("   " + "   ".join(str(i) for i in range(len(board[0]))))
    print("  " + "----" * len(board[0]))

    for i, row in enumerate(board):
        # Print row number
        print(f"{i} |", end=" ")

        # Print board elements with 'R' for relevant moves
        for j, element in enumerate(row):
            if (i, j) in relevant_moves:
                print(f"R{element}", end=" | ")
            else:
                print(f" {element} ", end=" | ")

        # Print separator
        print("\n  " + "----" * len(row))

def display_board_with_eval_diff(board, current_player):
    # Print column numbers
    print("   " + "   ".join(str(i) for i in range(len(board[0]))))
    print("  " + "----" * len(board[0]))

    for i, row in enumerate(board):
        # Print row number
        print(f"{i} |", end=" ")

        for j, cell in enumerate(row):
            # Print board elements
            print(f" {cell} ", end="")

            # Print evaluation difference for each empty move
            if cell == ' ':
                board_copy = [row.copy() for row in board]
                board_copy[i][j] = current_player
                eval_before = evaluate(board)
                eval_after = evaluate(board_copy)
                eval_diff = eval_after - eval_before
                print(f"({eval_diff:+})", end="")
            else:
                print("   ", end="")

            # Print separator
            if j < len(row) - 1:
                print("|", end="")

        print()

        # Print separator
        if i < len(board) - 1:
            print("  " + "----" * len(row))



def testminimax(board, depth, alpha, beta, maximizing_player):

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


def testai(board):
    relevant_moves = find_relevant_area(board, "B")
    
    best_move = None
    best_score = -math.inf

    for move in relevant_moves:
        row, col = move
        if place_piece(board, "B", row, col):
            # Use the minimax algorithm for AI's move
            score = minimax(board, 3, -math.inf, math.inf, True)
            remove_piece(board, "B", row, col)
            if score > best_score:
                best_score = score
                best_move = move
              # Undo the move

    return best_move

root = tk.Tk()

def display_board(board):
    for i, row in enumerate(board):
        for j, elem in enumerate(row):
            label = tk.Label(root, text=elem, width=4, height=2, relief="ridge", borderwidth=2)
            label.grid(row=i, column=j)

testboard = [[' ' for _ in range(10)] for _ in range(10)]



testdisplay_board(testboard)
root.mainloop()
