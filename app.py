from tkinter import *
import argparse
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



    def is_possible(self, row, col, number):
        """Check if it is possible to put 'number' in the position (row,col), i.e can lead to a solution"""
        if (self.is_in_row(row, number) or self.is_in_col(col, number) or self.is_in_square(row, col, number)):
            return False
        else:
            return True



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
        return i,j





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




class SudokuApp():
	"""Simple application to generate and give Sudoku solutions
	:param nb_values: Number of non-zero values in the Sudoku
	"""

	def __init__(self, nb_values):

		self.nb_values = nb_values
		self.sdk = Sudoku()

		self.window = Tk()
		self.window.title('Sudoku generator/solver')

		self.gen_button = Button(self.window)
		self.gen_button.config(text='Generate', command=self.generate)
		self.gen_button.grid(row=0, column=0)


		self.hint_button = Button(self.window)
		self.hint_button.config(text='Get hint', command=self.hint)
		self.hint_button.grid(row=0, column=1)


		self.sol_button = Button(self.window)
		self.sol_button.config(text='Get solution', command=self.solution)
		self.sol_button.grid(row=0, column=2)


		self.labs = {}
		for i in range(9):
			for j in range(9):
				self.labs["lab{}".format(i*9+j)] = Label(self.window, text='0', relief=RIDGE, width = 12, height = 5)
				self.labs["lab{}".format(i*9+j)].grid(row=1+i, column=j, sticky=NSEW)





	def generate(self):
		"""Generate random Sudoku with 'nb_values' initial values"""
		self.sdk.generate(self.nb_values)
		for i in range(9):
			for j in range(9):
				val = str(int(self.sdk.init_grid[i, j]))
				self.labs["lab{}".format(i*9+j)].config(text=val, fg='black')




	def hint(self):
		"""Get hint at random position"""
		i,j = self.sdk.get_hint()
		val = str(int(self.sdk.grid_with_hints[i, j]))
		self.labs["lab{}".format(i*9+j)].config(text=val, fg='red')




	def solution(self):
		"""Give solution to user"""
		for i in range(9):
			for j in range(9):
				val = str(int(self.sdk.grid[i, j]))
				self.labs["lab{}".format(i*9+j)].config(text=val)



	def run(self):
		"""Run app"""
		self.window.mainloop()




if __name__ == '__main__':


	parser = argparse.ArgumentParser()
	parser.add_argument("nb_values", type=int, help="number of values in Sudoku")
	args = parser.parse_args()

	app = SudokuApp(args.nb_values)
	app.run()
