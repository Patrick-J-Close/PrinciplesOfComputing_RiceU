# http://www.codeskulptor.org/#user42_4Y4zlpjEBh_10.py

"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 10         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    plays game from given board starting with given player by making 
    random moves
    """
    while board.check_win() == None:
        empty = board.get_empty_squares()
        rand_sq = random.choice(empty)
        board.move(rand_sq[0], rand_sq[1], player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    takes a grid of scores and completed board and updates the scores grid
    """
    winner = board.check_win()
    if winner == player:
        inc = SCORE_CURRENT
    elif winner == provided.DRAW:
        return
    else:
        inc = SCORE_OTHER
        
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            current_square = board.square(row, col)
            if current_square != provided.EMPTY:
                if current_square == winner:
                    scores[row][col] += inc
                else:
                    scores[row][col] -= inc

def get_best_move(board, scores):
    """
    finds the maximum score among the empty squares on a given grid and
    returns square position (row, column)
    """
    max_score = float('-inf')
    max_square = tuple()
    empty = board.get_empty_squares()
    
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if scores[row][col] > max_score and (row, col) in empty:
                max_score = scores[row][col]
                max_square = (row, col)
               
    return(max_square)

def mc_move(board, player, trials):
    """
    generates random move for machine player given current board
    """
    scores = []
    dim = board.get_dim()
    
    while len(scores) < dim:
        scores.append([0]*dim)
    
    counter = 0 
    while counter < trials:
        temp_board = board.clone()
        mc_trial(temp_board, player)
        mc_update_scores(scores, temp_board, player)
        counter += 1
        
    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
