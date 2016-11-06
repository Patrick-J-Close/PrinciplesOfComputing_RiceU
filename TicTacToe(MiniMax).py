# http://www.codeskulptor.org/#user42_fDR7FvOzzE_3.py

"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    game_state = board.check_win()
    if game_state != None:
        # game is over
        return SCORES[game_state], (-1, -1)
    
    best_move = (-1, (-1, -1)) # min score
    for move in board.get_empty_squares():
        board_clone = board.clone()
        board_clone.move(move[0], move[1], player)
        score = mm_move(board_clone, provided.switch_player(player))[0]
        
        if SCORES[player] * score == 1:
            return score, move
        elif score * SCORES[player] > best_move[0]:
            best_move = (score, move)
        elif best_move[0] == -1:
            best_move = (best_move[0], move)
            
    return best_move[0] * SCORES[player], best_move[1]

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

