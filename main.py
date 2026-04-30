import tkinter as tk
from tkinter import messagebox
import random


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Pro")

        # Game state
        self.current_player = "X"
        self.winner = False
        self.vs_computer = False
        self.score_x = 0
        self.score_o = 0

        self.buttons = []

        self.create_ui()

    # ---------------- UI ---------------- #
    def create_ui(self):
        self.status_label = tk.Label(
            self.root,
            text=f"Player {self.current_player}'s Turn",
            font=("Arial", 16, "bold"),
            fg="blue"
        )
        self.status_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Board
        for i in range(9):
            btn = tk.Button(
                self.root,
                text="",
                font=("Arial", 24, "bold"),
                width=5,
                height=2,
                bg="#222",
                fg="white",
                activebackground="#444",
                relief="flat",
                command=lambda i=i: self.handle_click(i)
            )
            btn.grid(row=(i // 3) + 1, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        # Score
        self.score_label = tk.Label(
            self.root,
            text="Score - X: 0 | O: 0",
            font=("Arial", 14)
        )
        self.score_label.grid(row=4, column=0, columnspan=3, pady=5)

        # Result log
        self.result_label = tk.Label(
            self.root,
            text="Last Result: None",
            font=("Arial", 12),
            fg="gray"
        )
        self.result_label.grid(row=5, column=0, columnspan=3)

        # Buttons
        tk.Button(self.root, text="Play Again", command=self.reset_game).grid(row=6, column=0, columnspan=3, pady=5)

        tk.Button(self.root, text="2 Player Mode", command=lambda: self.set_mode(False)).grid(row=7, column=0, columnspan=1)
        tk.Button(self.root, text="Vs Computer", command=lambda: self.set_mode(True)).grid(row=7, column=1, columnspan=2)

        # Menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        game_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Restart", command=self.reset_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)

    # ---------------- GAME LOGIC ---------------- #
    def handle_click(self, index):
        if self.buttons[index]["text"] == "" and not self.winner:
            self.buttons[index]["text"] = self.current_player
            self.check_winner()

            if not self.winner and not self.check_draw():
                self.toggle_player()

                if self.vs_computer and self.current_player == "O":
                    self.root.after(400, self.computer_move)

    def computer_move(self):
        empty = [i for i, b in enumerate(self.buttons) if b["text"] == ""]
        if empty and not self.winner:
            move = random.choice(empty)
            self.buttons[move]["text"] = "O"
            self.check_winner()

            if not self.winner and not self.check_draw():
                self.toggle_player()

    def toggle_player(self):
        self.current_player = "X" if self.current_player == "O" else "O"
        self.status_label.config(
            text=f"Player {self.current_player}'s Turn",
            fg="blue" if self.current_player == "X" else "red"
        )

    def check_winner(self):
        combos = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]

        for combo in combos:
            b1, b2, b3 = combo
            if self.buttons[b1]["text"] == self.buttons[b2]["text"] == self.buttons[b3]["text"] != "":
                self.highlight_winner(combo)
                self.winner = True
                winner = self.buttons[b1]["text"]

                if winner == "X":
                    self.score_x += 1
                else:
                    self.score_o += 1

                self.update_score()
                self.result_label.config(text=f"Last Winner: {winner}")
                messagebox.showinfo("Game Over", f"Player {winner} Wins!")

                self.disable_buttons()
                return

    def check_draw(self):
        if all(btn["text"] != "" for btn in self.buttons) and not self.winner:
            messagebox.showinfo("Game Over", "It's a Draw!")
            self.result_label.config(text="Last Result: Draw")
            self.disable_buttons()
            return True
        return False

    def highlight_winner(self, combo):
        for i in combo:
            self.buttons[i].config(bg="green")

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    # ---------------- UTILITIES ---------------- #
    def reset_game(self):
        self.current_player = "X"
        self.winner = False

        self.status_label.config(text="Player X's Turn", fg="blue")

        for btn in self.buttons:
            btn.config(text="", state="normal", bg="#222")

    def update_score(self):
        self.score_label.config(text=f"Score - X: {self.score_x} | O: {self.score_o}")

    def set_mode(self, mode):
        self.vs_computer = mode
        mode_text = "Computer" if mode else "2 Player"
        messagebox.showinfo("Mode Changed", f"Switched to {mode_text} Mode")
        self.reset_game()


# ---------------- RUN ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()