import tkinter as tk
import random

# Size of the chessboard
BOARD_SIZE = 8

class EightQueens:
    def __init__(self, root, initial_state=None, final_state=None):
        self.root = root
        root.title("8-Queens Game")

        self.buttons = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.chessboard = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.initial_state = initial_state or [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.final_state = final_state or [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = "white" if (row + col) % 2 == 0 else "black"  # Set background color based on coordinates
                button = tk.Button(
                    root,
                    width=2,
                    height=1,
                    relief=tk.RAISED,
                    bg=color,  # Set the background color
                    command=lambda r=row, c=col: self.place_queen(r, c)
                )
                button.grid(row=row, column=col)
                self.buttons[row][col] = button
               

        self.update_board_state(self.initial_state)

    def place_queen(self, row, col):
        # Check if the cell is already occupied
        if self.chessboard[row][col] == 1:
            return

        # Place the queen on the chessboard
        self.chessboard[row][col] = 1

        # Update the GUI to show the queen
        self.buttons[row][col].configure(text="Q", state=tk.DISABLED)

        # Mark the attacked cells
        self.mark_attacked_cells(row, col)

    def mark_attacked_cells(self, row, col):
        # Mark the attacked cells in the same row
        for c in range(BOARD_SIZE):
            if c != col:
                self.mark_cell(row, c)

        # Mark the attacked cells in the same column
        for r in range(BOARD_SIZE):
            if r != row:
                self.mark_cell(r, col)

        # Mark the attacked cells in the diagonal
        for r, c in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            self.mark_cell(r, c)

        for r, c in zip(range(row + 1, BOARD_SIZE), range(col + 1, BOARD_SIZE)):
            self.mark_cell(r, c)

        for r, c in zip(range(row - 1, -1, -1), range(col + 1, BOARD_SIZE)):
            self.mark_cell(r, c)

        for r, c in zip(range(row + 1, BOARD_SIZE), range(col - 1, -1, -1)):
            self.mark_cell(r, c)

    def mark_cell(self, row, col):
        # Check if the cell is occupied by a queen
        if self.chessboard[row][col] != 1:
            self.chessboard[row][col] = -1
            self.buttons[row][col].configure(state=tk.DISABLED)

    def clear_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.chessboard[row][col] != 0:
                    self.chessboard[row][col] = 0
                    self.buttons[row][col].configure(text="", state=tk.NORMAL)

    def update_board_state(self, state):
        self.clear_board()

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if state[row][col] == 1:
                    self.place_queen(row, col)

    def solve(self):
        self.clear_board()
        self.update_board_state(self.initial_state)

        solutions = self.generate_solutions()
        if solutions:
            self.update_board_state(random.choice(solutions))
            print("Solution found!")
        else:
            print("Solution not found.")
            self.update_board_state(self.final_state)

    def generate_solutions(self):
        solutions = []
        self.backtrack(0, solutions)
        return solutions

    def backtrack(self, col, solutions):
     if col >= BOARD_SIZE:
        solution = [row[:] for row in self.chessboard]
        solutions.append(solution)
        return

     for row in range(BOARD_SIZE):
        if self.is_safe(row, col):
            self.chessboard[row][col] = 1
            self.buttons[row][col].configure(text="Q", state=tk.DISABLED)

            # Apply forward checking
            self.apply_forward_checking(row, col)

            self.backtrack(col + 1, solutions)

            self.chessboard[row][col] = 0
            self.buttons[row][col].configure(text="", state=tk.NORMAL)

    def apply_forward_checking(self, row, col):
    # Reduce the domain of other variables (columns) based on constraints
     for c in range(col + 1, BOARD_SIZE):
        if self.chessboard[row][c] != 1:
            self.chessboard[row][c] = -1  # Mark as attacked
            self.buttons[row][c].configure(state=tk.DISABLED)

    def is_safe(self, row, col):
        for c in range(col):
            if self.chessboard[row][c] == 1:
                return False

        for r, c in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            if self.chessboard[r][c] == 1:
                return False

        for r, c in zip(range(row + 1, BOARD_SIZE), range(col - 1, -1, -1)):
            if self.chessboard[r][c] == 1:
                return False

        return True

if __name__ == "__main__":
    root = tk.Tk()
    game = EightQueens(root)

    solve_button = tk.Button(root, text="Solve", command=game.solve)
    solve_button.grid(row=BOARD_SIZE, columnspan=BOARD_SIZE, pady=10)

    root.mainloop()


