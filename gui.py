import eel
import numpy as np
import solver

eel.init('web', allowed_extensions=['.js', '.html'])

@eel.expose
def send_to_solve(array):
    array = np.array(array)
    array[array==None] = 0
    return solver.solve_sudoku(array).flatten().astype(int).tolist()

eel.start('index.html')  