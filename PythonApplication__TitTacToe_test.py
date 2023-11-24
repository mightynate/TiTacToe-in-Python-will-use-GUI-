import tkinter as tk
import tkinter.messagebox
import random

def on_button_click(button):
    global player
    if mode.get() == "Two Player":
        if button["text"] == "" and player:
            button["text"] = "X"
            player = False
            check_for_winner()
        elif button["text"] == "" and not player:
            button["text"] = "O"
            player = True
            check_for_winner()
    else:
        if button["text"] == "":
            button["text"] = "X"
            if not check_for_winner():
                ai_move()

def ai_move():
    if difficulty.get() == "Easy":
        ai_move_easy()
    elif difficulty.get() == "Intermediate":
        ai_move_intermediate()
    else:
        ai_move_hard()

def ai_move_easy():
    empty_buttons = [button for row in buttons for button in row if button["text"] == ""]
    if empty_buttons:
        random.choice(empty_buttons)["text"] = "O"
        check_for_winner()

def ai_move_intermediate():
    move_made = False

    # Check for AI winning move
    move_made = ai_check_win_or_block("O")

    # Check for blocking player's winning move
    if not move_made:
        move_made = ai_check_win_or_block("X")

    # Take center if available
    if not move_made and buttons[1][1]["text"] == "":
        buttons[1][1]["text"] = "O"
        move_made = True

    # Make a random move if none of the above
    if not move_made:
        ai_move_easy()

def ai_check_win_or_block(mark):
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == mark and buttons[i][2]["text"] == "":
            buttons[i][2]["text"] = "O"
            return True
        elif buttons[i][0]["text"] == buttons[i][2]["text"] == mark and buttons[i][1]["text"] == "":
            buttons[i][1]["text"] = "O"
            return True
        elif buttons[i][1]["text"] == buttons[i][2]["text"] == mark and buttons[i][0]["text"] == "":
            buttons[i][0]["text"] = "O"
            return True

    for j in range(3):
        if buttons[0][j]["text"] == buttons[1][j]["text"] == mark and buttons[2][j]["text"] == "":
            buttons[2][j]["text"] = "O"
            return True
        elif buttons[0][j]["text"] == buttons[2][j]["text"] == mark and buttons[1][j]["text"] == "":
            buttons[1][j]["text"] = "O"
            return True
        elif buttons[1][j]["text"] == buttons[2][j]["text"] == mark and buttons[0][j]["text"] == "":
            buttons[0][j]["text"] = "O"
            return True

    if buttons[0][0]["text"] == buttons[1][1]["text"] == mark and buttons[2][2]["text"] == "":
        buttons[2][2]["text"] = "O"
        return True
    elif buttons[0][0]["text"] == buttons[2][2]["text"] == mark and buttons[1][1]["text"] == "":
        buttons[1][1]["text"] = "O"
        return True
    elif buttons[1][1]["text"] == buttons[2][2]["text"] == mark and buttons[0][0]["text"] == "":
        buttons[0][0]["text"] = "O"
        return True
    elif buttons[0][2]["text"] == buttons[1][1]["text"] == mark and buttons[2][0]["text"] == "":
        buttons[2][0]["text"] = "O"
        return True
    elif buttons[0][2]["text"] == buttons[2][0]["text"] == mark and buttons[1][1]["text"] == "":
        buttons[1][1]["text"] = "O"
        return True
    elif buttons[1][1]["text"] == buttons[2][0]["text"] == mark and buttons[0][2]["text"] == "":
        buttons[0][2]["text"] = "O"
        return True

    return False

def ai_move_hard():
    best_score = float('-inf')
    best_move = None

    for i in range(3):
        for j in range(3):
            if buttons[i][j]["text"] == "":
                buttons[i][j]["text"] = "O"
                score = minimax(buttons, 0, False)
                buttons[i][j]["text"] = ""
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move:
        buttons[best_move[0]][best_move[1]]["text"] = "O"
        check_for_winner()

def minimax(board, depth, is_maximizing):
    winner = check_winner()
    if winner != None:
        return scores[winner]

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j]["text"] == "":
                    board[i][j]["text"] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j]["text"] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j]["text"] == "":
                    board[i][j]["text"] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j]["text"] = ""
                    best_score = min(score, best_score)
        return best_score

def check_winner():
    # Check rows
    for row in range(3):
        if buttons[row][0]["text"] == buttons[row][1]["text"] == buttons[row][2]["text"] != "":
            return buttons[row][0]["text"]

    # Check columns
    for col in range(3):
        if buttons[0][col]["text"] == buttons[1][col]["text"] == buttons[2][col]["text"] != "":
            return buttons[0][col]["text"]

    # Check diagonals
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return buttons[0][0]["text"]
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return buttons[0][2]["text"]

    # Check for draw
    if all(button["text"] != "" for row in buttons for button in row):
        return "Draw"

    return None

def check_for_winner():
    winner = check_winner()
    if winner:
        if winner == "Draw":
            tk.messagebox.showinfo("Tic Tac Toe", "It's a draw!")
        else:
            tk.messagebox.showinfo("Tic Tac Toe", f"Player {winner} wins!")
        reset_game()

def reset_game():
    global player
    player = True
    for row in buttons:
        for button in row:
            button["text"] = ""
    mode.set("Two Player")
    difficulty.set("Easy")

window = tk.Tk()
window.title("Tic Tac Toe")

buttons = [[None, None, None], [None, None, None], [None, None, None]]
player = True  # True for X, False for O

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(window, text="", font=('normal', 40), width=5, height=2,
                                  command=lambda i=i, j=j: on_button_click(buttons[i][j]))
        buttons[i][j].grid(row=i, column=j)

difficulty = tk.StringVar(value="Easy")
difficulty_selector = tk.OptionMenu(window, difficulty, "Easy", "Intermediate", "Hard")
difficulty_selector.grid(row=3, column=0)

mode = tk.StringVar(value="Two Player")
mode_selector = tk.OptionMenu(window, mode, "Single Player", "Two Player")
mode_selector.grid(row=3, column=1)

reset_button = tk.Button(window, text="Reset", font=('normal', 20), command=reset_game)
reset_button.grid(row=3, column=2)

scores = {"X": -1, "O": 1, "Draw": 0}

window.mainloop()
