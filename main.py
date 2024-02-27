from gomuku import *
from ai import *
import tkinter as tk


def game_loop():
    display_board(board)
    current_player = "B"

    while True:
        if current_player == "W":
            player_move = get_player_move()
            if not player_move:
                print("Invalid input. Please enter two integers separated by a comma.")
                continue
            row, col = player_move
            if not place_piece(board, current_player, row, col):
                print("Invalid input. Space is occupied")
                continue
        else:
            ai_move = ai(board)
            if ai_move is None:
                print("The game is a draw!")
                break
            row, col = ai_move
            place_piece(board, current_player, row, col)
            print(f"{current_player} chose ({row}, {col}).")

        display_board(board)

        game_over, winner = get_winning_condition(board, current_player)
        if game_over:
            print(f"{winner} wins!")
            break

        current_player = "W" if current_player == "B" else "B"


def get_player_move():
    try:
        return map(int, input("W's turn (row, col): ").split(','))
    except ValueError:
        return None

        
game_loop()
