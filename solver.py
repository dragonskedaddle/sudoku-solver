import numpy as np
import random
import operator as op

class sudoku:
    def __init__(self, board, num_holes):
        self.board = board
        self.num_holes = num_holes

    def board_splitter(self, board): # splits board into 3x3 sections
        return (board.reshape(9//3, 3, -1, 3)).swapaxes(1,2).reshape(-1, 3, 3)

    def is_valid(self):
        for i in self.board: # checks rows for duplicates
            for j in i:
                if j == 0: continue
                if op.countOf(i, j) > 1: # checks count of element in board 
                    return False
        
        for i in list(map(list, zip(*self.board))): # checks columns for duplicates by transposing the board
            for j in i:
                if j == 0: continue
                if op.countOf(i, j) > 1: # checks count of element in board 
                    return False
        
        for i in self.board_splitter(self.board): # checks 3x3 sections
            sub_board = i.flatten() # turns 2D list into 1D
            for j in sub_board:
                if j == 0: continue
                if op.countOf(sub_board, j) > 1: # checks count of element in board 
                    return False
        
        return True

    def is_valid_cell(self, row, col, num):
        if num in self.board[row]: # check row
            return False
        
        if num in self.board[:, col]: # checks column
            return False
        
        # check the 3x3 subgrid
        subgrid_row_start = (row // 3) * 3
        subgrid_col_start = (col // 3) * 3
        subgrid = self.board[subgrid_row_start:subgrid_row_start + 3, subgrid_col_start:subgrid_col_start + 3]
        
        if num in subgrid:
            return False
        
        return True
    
    def fill_diagonal_subgrids(self): # fills diagnal 3x3 subgrids
        for i in range(0, 9, 3): 
            self.fill_subgrid(i, i)
    
    def fill_subgrid(self, row, col): # fills given subgrid
        nums = list(range(1, 10))
        random.shuffle(nums) # randomizes numbers 
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = nums.pop() # sets subgrid to num list
    
    def remove_elements(self): # selctively removes numbers from the board 
        while self.num_holes > 0: # loops for as long as there needs to be holes
            row, col = random.randint(0, 8), random.randint(0, 8) # chooses random row and column 
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                self.num_holes -= 1

    def generate_board(self): # generates board 
        self.board.fill(0)
        self.fill_diagonal_subgrids()
        self.solve_board()
        self.remove_elements()
        return self.board
    
    def solve_board(self):
        def solve():
            possible_nums = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == 0:

                        for num in range(1, 10):
                             if self.is_valid_cell(i, j, num):
                                self.board[i][j] = num

                                if solve():
                                    return True
                                
                                self.board[i][j] = 0
                        return False
            return True
        
        if solve():
            return self.board
        