# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class Square:
    def __init__(self, grid, row_index, col_index, remaining_squares, remaining_mines):
        self.revealed = False;
        self.row_index = row_index
        self.col_index = col_index
        mines = [True] * remaining_mines
        non_mines = [False] * (remaining_squares - remaining_mines)
        square_options = mines + non_mines
        self.is_mine = random.choice(square_options)
        self.number = 0
        self.adjacent_squares = []
        self.grid = grid

    def reveal(self):
        if self.is_mine:
            self.revealed = True
            self.grid.gameover = True
        else:
            self.revealed = True
            [s.reveal() for s in self.adjacent_squares if self.number == 0 and not s.revealed]

    def __str__(self):

        return "X" if self.is_mine else str(self.number) if self.number > 0 else " "


class Grid:
    def __init__(self, rows: int, columns: int, mines: int):

        if mines >= rows * columns:
            raise ValueError(f"Cannot have more mines ({mines}) than squares ({rows * columns})!")
        self.gameover = False
        self.rows = rows
        self.cols = columns
        self.mines = mines
        self.squares = {}
        self.place_mines()
        self.get_adjacency()
        print(self)

    def place_mines(self):
        remaining_squares = self.rows * self.cols
        remaining_mines = self.mines
        for r in range(self.rows):
            for c in range(self.cols):
                self.squares[f"{r}:{c}"] = Square(self, r, c, remaining_squares, remaining_mines)
                remaining_squares -= 1

                if self.squares[f"{r}:{c}"].is_mine:
                    remaining_mines -= 1

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

    def __str__(self):
        max_row_digits = len(str(self.rows))
        first_row = " " * (max_row_digits + 2)
        first_row += " ".join([str(i + 1) for i in range(0, self.cols)])
        output = first_row + "\n"
        output += "-" * (len(output) -1)
        output += "\n"
        for row in range(0, self.rows):

            a = [str(row + 1).rjust(max_row_digits) + "|"]
            for col in range(self.cols):
                if self.squares[f"{row}:{col}"].revealed:
                    a.append(str(self.squares[f"{row}:{col}"]))
                else:
                    a.append("#")
            output += " ".join(a) + "\n"
        output = output.rstrip()
        return output

    def reveal(self, coordinates):
        c, r = coordinates.split(":")
        c = int(c) - 1
        r = int(r) - 1
        self.squares[f"{r}:{c}"].reveal()
        print(self)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game = Grid(17, 10, 5)
    while not game.gameover:
        game.reveal(input("Enter coord (column:row): "))
    print("Game Over")
