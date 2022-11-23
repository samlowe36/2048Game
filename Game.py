import tkinter as tk
import random


class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048: The Cinematic Horror Experience")

        self.grid_main = tk.Frame(self, bg=Game.grid_color, bd=3, width=600, height=600)
        self.grid_main.grid(pady=(125, 0))
        self.gui()
        self.start_game()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        self.mainloop()

    grid_color = "#b8afa9"
    empty_color = "#ffd5b5"
    score_label = ("Chiller", 24, "bold")
    score_font = ("Chiller", 48, "bold")
    game_over_font = ("Chiller", 48, "bold")
    game_over_color = "#ffffff"
    win_background = "#ffcc00"
    lose_background = "#a39489"

    cell_colors = {
        2: "#fcefe6",
        4: "#f2e8cb",
        8: "#f5b882",
        16: "#f29446",
        32: "#ff775c",
        64: "#e64c2e",
        128: "#ede291",
        256: "#fce130",
        512: "#ffdb4a",
        1024: "#f0b922",
        2048: "#fad74d"
    }
    cell_number_colors = {
        2: "#695c57",
        4: "#695c57",
        8: "#ffffff",
        16: "#ffffff",
        32: "#ffffff",
        64: "#ffffff",
        128: "#ffffff",
        256: "#ffffff",
        512: "#ffffff",
        1024: "#ffffff",
        2048: "#ffffff"
    }
    cell_number_font = {
        2: ("Chiller", 40, "bold"),
        4: ("Chiller", 40, "bold"),
        8: ("Chiller", 40, "bold"),
        16: ("Chiller", 40, "bold"),
        32: ("Chiller", 40, "bold"),
        64: ("Chiller", 40, "bold"),
        128: ("Chiller", 40, "bold"),
        256: ("Chiller", 40, "bold"),
        512: ("Chiller", 40, "bold"),
        1024: ("Chiller", 40, "bold"),
        2048: ("Chiller", 40, "bold"),
    }

    def gui(self):
        self.cells = []
        for x in range(4):
            row = []
            for y in range(4):
                cell_frame = tk.Frame(self.grid_main, bg=Game.empty_color, width=150, height=150)
                cell_frame.grid(row=x, column=y, padx=5, pady=5)
                cell_number = tk.Label(self.grid_main, bg=Game.empty_color)
                cell_data = {"frame": cell_frame, "number": cell_number}
                cell_number.grid(row=x, column=y)
                row.append(cell_data)
            self.cells.append(row)

        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=60, anchor="center")
        tk.Label(score_frame, text="Score", font=Game.score_label).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=Game.score_font)
        self.score_label.grid(row=1)

    def start_game(self):
        self.matrix = [[0] * 4 for _ in range(4)]
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=Game.cell_colors[2])
        self.cells[row][col]["number"].configure(
            bg=Game.cell_colors[2],
            fg=Game.cell_number_colors[2],
            font=Game.cell_number_font[2],
            text="2"
        )
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=Game.cell_colors[2])
        self.cells[row][col]["number"].configure(
            bg=Game.cell_colors[2],
            fg=Game.cell_number_colors[2],
            font=Game.cell_number_font[2],
            text="2"
        )
        self.score = 0

    def stack(self):
        matrix1 = [[0] * 4 for _ in range(4)]
        for i in range(4):
            position_fill = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    matrix1[i][position_fill] = self.matrix[i][j]
                    position_fill += 1
        self.matrix = matrix1

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    def reverse(self):
        matrix1 = []
        for i in range(4):
            matrix1.append([])
            for j in range(4):
                matrix1[i].append(self.matrix[i][3 - j])
        self.matrix = matrix1

    def transpose(self):
        matrix1 = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                matrix1[i][j] = self.matrix[j][i]
        self.matrix = matrix1

    def add_tile(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = random.choice([2, 2])

    def gui_update(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=Game.empty_color)
                    self.cells[i][j]["number"].configure(bg=Game.empty_color, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=Game.cell_colors[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=Game.cell_colors[cell_value],
                        fg=Game.cell_number_colors[cell_value],
                        font=Game.cell_number_font[cell_value],
                        text=str(cell_value)
                    )
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_tile()
        self.gui_update()
        self.game_over()

    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_tile()
        self.gui_update()
        self.game_over()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_tile()
        self.gui_update()
        self.game_over()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_tile()
        self.gui_update()
        self.game_over()

    def possible_horizontal(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False

    def possible_vertical(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.grid_main, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="YOU WIN!!",
                bg=Game.win_background,
                fg=Game.game_over_color,
                font=Game.game_over_font
            ).pack()
        elif not any(0 in row for row in self.matrix) and not self.possible_horizontal() and not self.possible_vertical():
            game_over_frame = tk.Frame(self.grid_main, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="GAME OVER!!",
                bg=Game.lose_background,
                fg=Game.game_over_color,
                font=Game.game_over_font
            ).pack()


def main():
    Game()


if __name__ == "__main__":
    main()
