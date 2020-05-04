from tkinter import *
from sudoku2 import *
import argparse



class SudokuApp():
	'''Simple application to generate and give Sudoku solutions
	:param nb_values: Number of non-zero values in the Sudoku
	'''

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
		'''Generate random Sudoku with 'nb_values' initial values'''
		self.sdk.generate(self.nb_values)
		for i in range(9):
			for j in range(9):
				val = str(int(self.sdk.init_grid[i, j]))
				self.labs["lab{}".format(i*9+j)].config(text=val)




	def hint(self):
		'''Get hint at random position'''
		i,j = self.sdk.get_hint()
		val = str(int(self.sdk.grid_with_hints[i, j]))
		self.labs["lab{}".format(i*9+j)].config(text=val, fg='red')




	def solution(self):
		'''Give solution to user'''
		for i in range(9):
			for j in range(9):
				val = str(int(self.sdk.grid[i, j]))
				self.labs["lab{}".format(i*9+j)].config(text=val)



	def run(self):
		'''Run app'''
		self.window.mainloop()




if __name__ == '__main__':


	parser = argparse.ArgumentParser()
	parser.add_argument("nb_values", type=int, help="nb of values in Sudoku")
	args = parser.parse_args()

	app = SudokuApp(args.nb_values)
	app.run()
