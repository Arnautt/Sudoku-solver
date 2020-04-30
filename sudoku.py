import numpy as np
import pandas as pd



class Sudoku:
    """Simple class to solve -if possible- any Sudoku by using backtracking
    It can be used by passing an initial Sudoku grid or by generating a random
    feasible one.

    :param grid: An array, the initial Sudoku (optional).
    """
    def __init__(self, grid = np.zeros((9,9))):
        self.init_grid = grid
        self.grid = grid
        self.hints_nb = 0
        self.grid_with_hints = grid
        self.nb_init_values = 0

        if not self.is_valid(): raise ValueError("You need to pass a valid Sudoku")



    def is_valid(self):
        """Check is the Sudoku is valid by checking row, columns and every sub-square"""

        # 1) Check row
        for row in range(9):
            vals, counts = np.unique(self.init_grid[row,:], return_counts=True)
            zero_idx = (vals==0)
            counts = counts[~zero_idx]
            if (np.any(counts > 1)): return False


        # 2) Check col
        for col in range(9):
            vals, counts = np.unique(self.init_grid[:,col], return_counts=True)
            zero_idx = (vals==0)
            counts = counts[~zero_idx]
            if (np.any(counts > 1)): return False


        # 3) Check sub_square
        for square_nb_col in range(3):
            for square_nb_row in range(3):
                sub_square = self.get_square(square_nb_col, square_nb_row)
                vals, counts = np.unique(sub_square, return_counts=True)
                zero_idx = (vals==0)
                counts = counts[~zero_idx]
                if (np.any(counts > 1)): return False

        # If none of the above return False, Sudoku is correct
        return True



    def generate(self, nb_init_values):
        '''
        Generate a random Sudoku by following these rules :
        - Start by putting n random numbers between 1-9 at random index
        (to introduce some alea and avoid getting always the same grid)
        - Generate a feasible Sudoku with these n numbers
        - Remove some numbers to have grid with 'nb_init_values' values
        '''
        self.nb_init_values = nb_init_values
        while True:
            n = 3
            rnd_nb = np.random.choice(np.arange(1,10), n, replace = False)
            grid = np.zeros((9,9))
            to_sample = [(i,j) for i in range(9) for j in range(9)]
            idx_to_feed = np.random.choice(np.arange(0,81), n, replace = False)
            for i,idx in enumerate(idx_to_feed):
                grid[to_sample[idx][0], to_sample[idx][1]] = rnd_nb[i]

            self.grid = grid
            if self.is_solvable():
                break


        grid_copy = np.copy(self.grid)
        zeros_idx = np.random.choice(np.arange(0,81), 81-nb_init_values, replace = False)
        to_sample = [(i,j) for i in range(9) for j in range(9)]
        for idx in zeros_idx:
            grid_copy[to_sample[idx][0], to_sample[idx][1]] = 0
        self.init_grid = grid_copy
        self.grid_with_hints = np.copy(grid_copy)
        print("Your solvable Sudoku is : ")
        self.show_init_grid()



    def solve(self):
        """Solve current Sudoku if possible"""

        print("Your initial Sudoku was : ")
        self.show_init_grid()

        if (self.is_solvable()):
            print("And one possible solution is : ")
            self.show_solution()
        else:
            print("And this Sudoku doesn't have any solution")



    def is_possible(self, row, col, number):
        """Check if it is possible to put 'number' in the position (row,col), i.e can lead to a solution"""
        if (self.is_in_row(row, number) or self.is_in_col(col, number) or self.is_in_square(row, col, number)):
            return False
        else:
            return True



    def show_init_grid(self):
        """Show initial Sudoku"""
        df = pd.DataFrame(self.init_grid, columns = ['','','','','','','','',''], index = ['','','','','','','','',''])
        print(df)


    def show_solution(self):
        """Show the solution of Sudoku"""
        df = pd.DataFrame(self.grid, columns = ['','','','','','','','',''], index = ['','','','','','','','',''])
        print(df)

    def show_hint(self):
        """Show Sudoku with hints"""
        df = pd.DataFrame(self.grid_with_hints, columns = ['','','','','','','','',''], index = ['','','','','','','','',''])
        print(df)


    def is_in_row(self, row, number):
        """Check if 'number' is in the row 'row' of the Sudoku"""
        return np.any(self.grid[row,:] == number)


    def is_in_col(self, col, number):
        """Check if 'number' is in the column 'col' of the Sudoku"""
        return np.any(self.grid[:,col] == number)


    def is_in_square(self, row, col, number):
        """Check if 'number' is in the sub-square given row and col"""
        square_nb_col = int(col/3)
        square_nb_row = int(row/3)
        sub_grid = self.get_square(square_nb_col, square_nb_row)
        return np.any(sub_grid == number)



    def get_square(self, square_nb_col, square_nb_row):
        '''
        Get one of the 9 Sudoku sub-square
        :param square_nb_col: Column block index, must be between 0 and 2
        :param square_nb_row: Row block index, must be between 0 and 2
        :returns: A sub-array of the Sudoku
        '''
        return self.grid[(square_nb_row*3):(square_nb_row*3+3), (square_nb_col*3):(square_nb_col*3+3)]



    def get_hint(self):
        '''
        Give 1 hint to user if needed, i.e give one more number of the solution
        Use only if Sudoku was generated by method generate().
        '''
        to_sample = [(i,j) for i in range(9) for j in range(9) if self.grid_with_hints[i,j] == 0]
        idx = np.random.randint(0, 81-(self.nb_init_values+self.hints_nb), 1)[0]
        i,j = to_sample[idx]
        self.grid_with_hints[i, j] = self.grid[i, j]
        self.hints_nb += 1
        print("Grid with {} hints : ".format(self.hints_nb))
        self.show_hint()





    def is_solvable(self):
        """Check if the Sudoku is solvable by using backtracking"""

        for row in range(9):
            for col in range(9):

                if (self.grid[row,col] == 0):
                    possible_values = [nb for nb in range(1,10) if self.is_possible(row, col, nb)]

                    for value in possible_values:
                        self.grid[row,col] = value
                        if self.is_solvable():
                            return True

                    self.grid[row,col] = 0
                    return False


        # If we go to all the lines/columns and we never got a 0 ;
        # Algorithm succeed and we got a solution
        return True
