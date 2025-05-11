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
    
    # If initial state, or or it is X's turn,
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

    # Loop through cells and add cells, (i, j), that have None value
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                possible_actions.add((i, j))
    
    return possible_actions


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
    else:
        # Map action to the resulting board and return it 
        result_board[action[0]][action[1]] = turn

    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

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
        elif row_i.count(X) == 3 or col_i.count(X) == 3:
            won = X
        else:
            continue
        
    # Check diognals
    # Store diagonal lines
    dia_1 = [board[0][0], board[1][1], board[2][2]]
    dia_2 = [board[0][2], board[1][1], board[2][0]]

    if dia_1.count(O) == 3 or dia_2.count(O) == 3:
        won = O

    if dia_1.count(X) == 3 or dia_2.count(X) == 3:
        won = X 

    # Return winner, or None if no winner
    return won


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    
    for row in board:
        if EMPTY in row:
            return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # If winner(board) == X, return 1
    if winner(board) == X:
        return 1

    # Elif winner == O, return -1
    elif winner(board) == O:
        return -1

    # Else, return 0
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if terminal(board), return None
    if terminal(board):
        return None
    
    best_move = None
    
    if player(board) == X:
        best_value = -math.inf
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                best_move = action
        return best_move
    
    else:
        best_value = math.inf
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_move = action
        return best_move

def max_value(board):
    """
        Returns the value of optimal move for the maximizing player, by consiering the oponent's
        optimal moves resulting from each possible action player currently has.
    """
    # Set initial value 
    v = - math.inf

    # If game is finished, give the utility 1, 0, or -1
    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    
    return v


def min_value(board):
    """
    Returns the value of optimal move for the minimizing player, by consiering the oponent's
    optimal moves resulting from each possible action player currently has.

    """
    v = math.inf

    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v
