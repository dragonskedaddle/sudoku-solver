import eel
import numpy as np
import solver

eel.init('web', allowed_extensions=['.js', '.html'])

@eel.expose
def send_to_solve(array):
    array = np.array(array)
    array[array==None] = 0
    print(np.array([int(j) for j in array]).reshape(9, 9, 1))
    sudoku_board = solver.sudoku(np.array([int(j) for j in array]).reshape(9, 9, 1), 25)
    return sudoku_board.solve_board().flatten().astype(int).tolist()

eel.start('index.html')  