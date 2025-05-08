"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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
    x_count = 0
    o_count = 0

    # Assess state of board
    # Count total number of O's and X's on the board
    for row in board:
        x_count += row.count(X)
        o_count += row.count(O)
    
    if terminal(board):
        return None
    
    # Assuming, or O has just played,
    if x_count == o_count:
        return X

    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Initialize empty set
    possible_actions = set()

    if terminal(board):
        return set()

    # Loop through cells and add cells, (i, j), that have None value
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                possible_actions.add(i, j)
    
    if not len(possible_actions) == 0:
        return possible_actions
    else:
        return set()


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Create new board variables matrix a deep copy of existing
    result_board = deepcopy(board)

    # Determine whos turn it is
    turn = player(board)

    # Check if action is legal
    # If action not in actions(board)
    if action not in actions(board):
        # raise exception
        raise ValueError("Invalid action")
    # Else
    else:
        # Map action to the copy board and return itx = 
        result_board[action[0]][action[2]] = turn

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # Assess the board to check if there are 3 consecutive O's or X's
    # 3 rows, 3 columns, and 2 diagnols, if count of player in any of them is 3!

    # Initialize variable to store potential winner
    won = None

    # Check rows and columns
    for i in range(3):
        row_i = []
        col_i = []
        for j in range(3):
            row_i.append(board[i][j])
            col_i.append(board[j][i])
        
        if row_i.count(O) == 3 or col_i.count(O) == 3:
            won = O 
        elif row_i.count(X) == 3 or col_i.count(X):
            won = X
        else:
            continue
        
    # Check diognals

    # Return winner, or None if no winner
    return won


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # If winner, return true

    # Elif actions(board) is None, return true

    # Else, return False

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # If winner(board) == X, return 1
    # Elif winner == O, return -1
    # Else, return 0

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # if terminal(board), return None


    raise NotImplementedError
