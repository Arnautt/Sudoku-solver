from sudoku import *


# 1. Create a Sudoku object given a grid -solvable or not-


g1 = np.array([[3, 0, 6, 5, 0, 8, 4, 0, 0],
 [5, 2, 0, 0, 0, 0, 0, 0, 0],
 [0, 8, 7, 0, 0, 0, 0, 3, 1],
 [0, 0, 3, 0, 1, 0, 0, 8, 0],
 [9, 0, 0, 8, 6, 3, 0, 0, 5],
 [0, 5, 0, 0, 9, 0, 6, 0, 0],
 [1, 3, 0, 0, 0, 0, 2, 5, 0],
 [0, 0, 0, 0, 0, 0, 0, 7, 4],
 [0, 0, 5, 2, 0, 6, 3, 0, 0]])

g0 = np.zeros((9,9))
g0[0,0]=g0[1,1]=1

sdk = Sudoku(g1)
sdk.solve()



# 2. Create and solve a random -solvable- Sudoku
# Given that Sudoku is solvable, user can get some hints


"""
Usage::
    >>> sdk = Sudoku()
    >>> nb_values = 10
    >>> sdk.generate(nb_values)

    >>> sdk.get_hint()
    >>> sdk.get_hint()

    >>> sdk.show_solution()
"""
