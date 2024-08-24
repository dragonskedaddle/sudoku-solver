import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import solver


app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template('index.html')

@socketio.on("empty-board")
def update(data):
    array = np.array(data['data'])
    array[array==None] = 0
    sudoku_board = solver.sudoku(np.array([int(j) for j in array]).reshape(9, 9, 1), 25)
    emit("filled-board", sudoku_board.solve_board().flatten().astype(int).tolist())

if __name__ == "__main__": 
    socketio.run(app, debug=True)