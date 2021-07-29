import random
import tkinter as tk


class Square(tk.Button):
    def __init__(self, master, row_index, col_index, remaining_squares, remaining_mines, *args, **kwargs):
        pixelVirtual = tk.PhotoImage(width=1, height=1)

        super().__init__(master, bd=1, relief="solid", width=2, height=1, bg="#4FB3E8", command=self.reveal,
                         activebackground="#4FB3E8", *args, **kwargs)
        self.bind("<Enter>", lambda event, s=self: s.configure(bg="#4FB"))
        self.bind("<Leave>", lambda event, s=self: s.configure(bg="#4FB3E8"))
        self.bind("<Button-3>", self.flag_toggle)

        self.revealed = False
        self.flagged = False
        self.row_index = row_index
        self.col_index = col_index
        mines = [True] * remaining_mines
        non_mines = [False] * (remaining_squares - remaining_mines)
        square_options = mines + non_mines
        self.is_mine = random.choice(square_options)
        self.number = 0
        self.adjacent_squares = []

    def reveal(self):
        if self.master.revealed_count == 0:
            self.master.fix_start(self)

        self.master.revealed_count += 1
        if self.is_mine:
            self.revealed = True
            self.config(bg="red")
            self.unbind("<Enter>")
            self.unbind("<Leave>")
            self.unbind("<Button-3>")
            self.master.gameover = True
        else:
            self.revealed = True
            self.config(text=self.number, bg="#FFF", state=tk.DISABLED) if self.number > 0 else self.config(bg="#FFF",
                                                                                                            state=tk.DISABLED)
            self.unbind("<Enter>")
            self.unbind("<Leave>")
            self.unbind("<Button-3>")
            [s.reveal() for s in self.adjacent_squares if self.number == 0 and not s.revealed]

    def flag_toggle(self, event):
        w = event.widget
        if w.flagged:
            w.flagged = False
            w.config(bg="#4FB3E8", state=tk.ACTIVE)
            w.bind("<Enter>", lambda event, s=w: s.configure(bg="#4FB"))
            w.bind("<Leave>", lambda event, s=w: s.configure(bg="#4FB3E8"))

        else:
            w.flagged = True
            w.config(bg="yellow", state=tk.DISABLED)
            w.unbind("<Enter>")
            w.unbind("<Leave>")


class Grid(tk.Frame):
    def __init__(self, master, rows: int, columns: int, mines: int, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        if mines > min(rows * columns * 0.8, (rows * columns) - 10):
            raise ValueError(f"Cannot have more than ({min(rows * columns * 0.8, (rows * columns) - 10)}) mines.")
        self.gameover = False
        self.rows = rows
        self.cols = columns
        self.revealed_count = 0
        self.mines = mines
        self.squares = {}
        self.place_mines()
        self.get_adjacency()
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def place_mines(self):
        remaining_squares = self.rows * self.cols
        remaining_mines = self.mines
        for r in range(self.rows):
            for c in range(self.cols):
                self.squares[f"{r}:{c}"] = Square(self, r, c, remaining_squares, remaining_mines)
                remaining_squares -= 1

                if self.squares[f"{r}:{c}"].is_mine:
                    remaining_mines -= 1

    def fix_start(self, start_square: Square):
        if start_square.is_mine or start_square.number > 0:
            for s in start_square.adjacent_squares:
                if s.is_mine:
                    new_s = random.choice(list(self.squares.values()))
                    while new_s in start_square.adjacent_squares or new_s.is_mine:
                        new_s = random.choice(list(self.squares.values()))
                    new_s.is_mine = True
                s.is_mine = False
            self.get_adjacency()

    def get_adjacency(self):
        for s in self.squares.values():
            if s.is_mine:
                continue
            else:
                rows_to_check = list(range(max(s.row_index - 1, 0), min(self.rows, s.row_index + 2)))
                cols_to_check = list(range(max(s.col_index - 1, 0), min(self.cols, s.col_index + 2)))

                for r in rows_to_check:
                    for c in cols_to_check:
                        if self.squares[f"{r}:{c}"].is_mine:
                            s.number += 1
                        s.adjacent_squares.append(self.squares[f"{r}:{c}"])


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Minesweep")
        # self.parent.geometry("400x200")
        self.parent.minsize(500, 200)
        self.frm_1 = tk.Frame()
        self.frm_1.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
        self.frm_2 = tk.Frame()
        self.frm_2.pack(side=tk.TOP, padx=50, pady=5, fill=tk.X)

        # create placeholder attribute for the grid.
        self.frm_grid = None

        # Define variables used for setting up game
        self.grid_rows = tk.IntVar()
        self.grid_cols = tk.IntVar()
        self.grid_mines = tk.IntVar()

        self.grid_rows.set(15)
        self.grid_cols.set(20)
        self.grid_mines.set(150)

        # Define callbacks to trigger when the variables change
        self.grid_rows.trace_add("write", self.enable_start)
        self.grid_cols.trace_add("write", self.enable_start)
        self.grid_mines.trace_add("write", self.enable_start)

        # Create label
        lbl_grid_rows = tk.Label(master=self.frm_1, text="How many rows?", width=7)
        lbl_grid_rows.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=3, pady=3)
        # Create Entry fields and bind to variables
        self.ent_grid_rows = tk.Entry(self.frm_1, width=4, text="10", textvariable=self.grid_rows)
        self.ent_grid_rows.pack(side=tk.LEFT, padx=3, pady=3)

        # Create label
        lbl_grid_cols = tk.Label(master=self.frm_1, text="How many columns?", width=7)
        lbl_grid_cols.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=3, pady=3)
        # Create Entry fields and bind to  variables
        self.ent_grid_cols = tk.Entry(self.frm_1, width=4, text="10", textvariable=self.grid_cols)
        self.ent_grid_cols.pack(side=tk.LEFT, padx=3, pady=3)

        # Create label
        lbl_grid_mines = tk.Label(master=self.frm_1, text="How many mines?", width=7)
        lbl_grid_mines.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=3, pady=3)
        # Create Entry fields and bind to  variables
        self.ent_grid_mines = tk.Entry(self.frm_1, width=4, text="10", textvariable=self.grid_mines)
        self.ent_grid_mines.pack(side=tk.LEFT, padx=3, pady=3)

        # self.wb = None
        # self.ws = None
        # self.cell = dict()
        # self.ent_active = None
        # self.selectable = "both"

        # Load button that starts the game
        self.btn_start = tk.Button(self.frm_2, text="Start", width=10, command=self.start_game)
        self.btn_start.pack(side=tk.TOP, ipadx=10, padx=3, pady=3)

        # self.frm_grid.pack(side=tk.TOP, padx=50, pady=50, fill=tk.BOTH, expand=True)

    def set_active_ent(self, event, selectable):
        self.ent_active = event.widget
        self.selectable = selectable
        self.change_sheet()

    def enable_start(self, var, *args):
        self.btn_start["state"] = "normal" if self.ent_grid_rows.get() else "disabled"

    def start_game(self):
        if self.frm_grid is not None:
            self.frm_grid.pack_forget()
        self.frm_grid = Grid(master=self, rows=self.grid_rows.get(), columns=self.grid_cols.get(),
                             mines=self.grid_mines.get())


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
