import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import solver


app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template('index.html') # displays the html gui

@socketio.on("empty-board") # will solve board when signal is emitted 
def update(data):
    array = np.array(data['data'])
    array[array == None] = 0
    sudoku_board = solver.sudoku(np.array([int(j) for j in array]).reshape(9, 9, 1)) # makes the board into a 2D array 
    emit("filled-board", sudoku_board.solve_board().flatten().astype(int).tolist()) # flattens and ensures datatypes match for display

@socketio.on("generate-board") # will generate board when signal is emitted 
def generate(data):
    array = np.array(data['data'])
    array[array == None] = 0
    sudoku_board = solver.sudoku(np.array([int(j) for j in array]).reshape(9, 9, 1)) # makes the board into a 2D array 
    emit("filled-board", sudoku_board.generate_board().flatten().astype(int).tolist()) # flattens and ensures datatypes match for display


if __name__ == "__main__": 
    socketio.run(app, debug=True)