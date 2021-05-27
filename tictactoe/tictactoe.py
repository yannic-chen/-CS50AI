"""
Tic Tac Toe Player
"""

import math
import copy
import random
import numpy as np

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    #if X starts, when the number of X is the same as O, then its X's turn.
    #if there is more X than O, then its O's turn.
    x = 0
    o = 0
    for row in board:
        for i in row:
            if i == "X":
                x += 1
            elif i == "O":
                o += 1
    if x == o:
        return X
    elif x > o:
        return O
    else:
        return "not a possible if X has the first move" 


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                possible.add(tuple((i,j)))           
    return possible

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    if board_copy[action[0]][action[1]] == None:
        board_copy[action[0]][action[1]] = player(board)
        return board_copy
    else:
        raise Exception ("the move is not possible")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #check for a win across the row
    for row in board:
        if len(set(row)) == 1 and row[0] != None:
            return row[0]

    #check for win on diagonal
    if len(set([board[i][i] for i in range(len(board))])) == 1 and board[0][0] != None:
        return board[0][0]

    elif len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1 and board[0][len(board)-1] != None:
        return board[0][len(board)-1]

    #check for a win on column
    for row in np.transpose(board):
        if len(set(row)) == 1 and row[0] != None:
            return row[0]

    else:
        return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    for row in board:
        for column in row:
            if column == None:
                return False

    return True
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0

def max_value(board):
    if terminal(board) == True:
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board) == True:
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v



def minimax(board):
    """
    Returns the optimal action for the current player on the board. X wants to max, O wants to min
    """
    if player(board) == X:
        #Max
        best_value = max_value(board)
        move = set()
        for action in actions(board):
            v = min_value(result(board, action))
            if v == best_value:
                move.add(action)    #get all the good moves
        optimal_move = random.choice(tuple(move))
        return optimal_move

    elif player(board) == O:
        #Min
        best_value = min_value(board)
        move = set()
        for action in actions(board):
            v = max_value(result(board, action))
            if v == best_value:
                move.add(action)    #get all the good moves
        optimal_move = random.choice(tuple(move))
        return optimal_move