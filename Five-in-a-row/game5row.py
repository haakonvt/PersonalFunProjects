import sys
import numpy as np
np.random.seed(1)

def init_game():
    if len(sys.argv) == 3:
        n = int(sys.argv[1])
        m = int(sys.argv[2])
    elif len(sys.argv) == 2:
        n = int(sys.argv[1])
        m = n
    else:
        while True:
            n = int(raw_input("Input board hight N: "))
            m = int(raw_input("Input board width M: "))
            if n < 5 or m < 5:
                print "Board must be at least 5 squares long/high, try again."
                continue
            if n > 32 or m > 65:
                print "Board must be equal or smaller than 65x32, try again."
                continue
            if isinstance(n, ( int, long )) and isinstance(n, ( int, long )):
                break
    board = np.zeros((n,m))
    # board = np.random.randint(0,3, size=(n,m))
    starting_player = 0 # This will end up as first person (crosses)
    return board, n, m, starting_player

def print_board(board,n,m):
    cols_index = "   |"
    for j in range(m):
        if j < 10:
            cols_index += " " + str(j) + " |"
        else:
            cols_index += " " + str(j) + "|"
    sys.stdout.write(cols_index + "\n")
    sys.stdout.flush()
    sys.stdout.write("_"*(m*4+4) + "\n")
    sys.stdout.flush()
    for j in range(n):
        if j < 10:
            line_to_print = " " + str(j) + " |"
        else:
            line_to_print = " " + str(j) + "|"
        for i in range(m):
            if board[j,i] == 0:
                line_to_print += "   |"
            elif board[j,i] == 1:
                line_to_print += " X |"
            else: # == 2
                line_to_print += " O |"
        sys.stdout.write(line_to_print)
        sys.stdout.flush()
        sys.stdout.write("\n" + "-"*(m*4+4) + "\n")
        sys.stdout.flush()

def evaluate_board_for_win(board,n,m,verbose=True,searching_game_tree=False):
    """
    Need to think how to make this as quick as possible..

    If somwhow both players have 5 in a row, this func will evaluate victory to crosses
    """
    winCross  = np.ones(5)
    winNought = np.ones(5)*2
    cross_extra_check  = False
    nought_extra_check = False
    for j in range(n-4):
        for i in range(m-4):
            diagM   = board[j:j+5, i:i+5]
            if np.sum(diagM) == 0:
                continue
            r_fiver = diagM[0,:] # looking for rows
            c_fiver = diagM[:,0] # looking for columns
            d_fiver = np.diag(diagM)            # looking for diagonal --> down
            u_fiver = np.diag(np.fliplr(diagM)) # looking for diagonal --> up

            cross_win_bools   = [np.array_equal(winCross, fiver)  for fiver in [r_fiver, c_fiver, d_fiver, u_fiver]]
            noughts_win_bools = [np.array_equal(winNought, fiver) for fiver in [r_fiver, c_fiver, d_fiver, u_fiver]]

            # Diag matrix above doesnt check last 4 rows and cols. Must do manually
            if i == m-5 or j == n-5:
                for ii in range(1,5): # ii = 0 already checked
                    r_fiver = diagM[ii,:] # looking for last 4 rows
                    c_fiver = diagM[:,ii] # looking for last 4 columns
                    if np.array_equal(winCross, r_fiver) or np.array_equal(winCross, c_fiver):
                        cross_extra_check = True
                    if np.array_equal(winNought, r_fiver) or np.array_equal(winNought, c_fiver):
                        nought_extra_check = True

            if np.any(cross_win_bools) or cross_extra_check:
                if verbose:
                    print "Crosses won!"
                return True, 1
            if np.any(noughts_win_bools) or nought_extra_check:
                if verbose:
                    print "Noughts won!"
                return True, 2
    turns_left = np.count_nonzero(board == 0)
    if turns_left == 0 and not searching_game_tree:
        print "Match ended in a draw!"
        print_board(board, n, m)
        sys.exit(0)
    return False, 0

def bad_input_print(spot_taken=False):
    if spot_taken:
        print "Spot already taken! Try again!"
    else:
        print "Not a valid move, try again! (Like this: 5,12 )"

def make_a_move(board,n,m,what_player):
    while True:
        inp = raw_input("Input move: ")
        try:
            y,x = [int(some_input) for some_input in inp.split(',')]
        except:
            bad_input_print()
            continue
        if y < 0 or y > m:
            if x < 0 or x > n:
                bad_input_print()
                continue
        elif board[y,x] != 0:
            bad_input_print(spot_taken=True)
            continue
        else:
            break
    board[y,x] = what_player
    return board

def generate_next_moves(board, n, m):
    moves = [] # List of lists with (y,x)
    for j in range(n):
        for i in range(m):
            if board[j,i] == 0:
                moves.append(  (j,i)  ) # tuple
    return moves

def generate_next_moves_nn(board, n, m):
    ghost_board = np.zeros((n+2,m+2)) - 1 # extra row and col outside
    ghost_board[1:-1,1:-1] = board
    prev_moves  = [] # List of lists with (y,x)
    nn_moves    = []
    for j in range(n):
        for i in range(m):
            if board[j,i] in [1,2]:
                prev_moves.append(  (j,i)  ) # tuple
    for j,i in prev_moves:
        j += 1; i += 1  # Fix indices for ghost board
        if ghost_board[j-1,i] == 0:
            nn_moves.append((j-1,i))
        if ghost_board[j+1,i] == 0:
            nn_moves.append((j+1,i))
        if ghost_board[j,i-1] == 0:
            nn_moves.append((j,i-1))
        if ghost_board[j,i+1] == 0:
            nn_moves.append((j,i+1))
        if ghost_board[j+1,i+1] == 0:
            nn_moves.append((j+1,i+1))
        if ghost_board[j-1,i-1] == 0:
            nn_moves.append((j-1,i-1))
        if ghost_board[j+1,i-1] == 0:
            nn_moves.append((j+1,i-1))
        if ghost_board[j-1,i+1] == 0:
            nn_moves.append((j-1,i+1))
    nn_moves = [(j-1,i-1) for j,i in nn_moves] # Fix indices for ordinary board
    nn_moves = list(set(nn_moves)) # Remove duplicate moves
    return nn_moves

def remove_bad_moves_1_step(all_moves,board,n,m):
    good_moves = []
    for move in all_moves:
        board_copy       = np.copy(board)
        board_copy[move] = 2
        winBool, who_won_or_draw = evaluate_board_for_win(board_copy,n,m,verbose=False,searching_game_tree=True)
        if winBool and who_won_or_draw == 2:
            print "Found a win!"
            return [move] # If we can win, stop early and simply do this move
        next_moves = generate_next_moves_nn(board_copy, n, m) # Next possible human moves
        move_was_good = True
        for move2 in next_moves:
            board_copy2        = np.copy(board_copy)
            board_copy2[move2] = 1
            winBool, who_won_or_draw = evaluate_board_for_win(board_copy2,n,m,verbose=False,searching_game_tree=True)
            if winBool and who_won_or_draw == 1:
                move_was_good = False # If it can lead to loss, not good move!
        if move_was_good:
            good_moves.append(move)
    return good_moves


def make_a_move_ai_v0(board,n,m,what_player):
    """
    Computer plays randomly
    """
    all_moves  = generate_next_moves(board, n, m)
    y, x       = all_moves[np.random.randint(len(all_moves))] # Choose random move
    board[y,x] = what_player
    return board

def make_a_move_ai_v1(board,n,m,what_player):
    """
    Computer plays randomly next to another player
    """
    all_moves  = generate_next_moves_nn(board, n, m)
    y, x       = all_moves[np.random.randint(len(all_moves))] # Choose random move
    board[y,x] = what_player
    return board

def make_a_move_ai_v2(board,n,m,what_player):
    """
    Computer plays randomly next to another player,
    but checks for easy wins / losses.
    Can be fooled by getting three in a row, with empty place on both sides.

    Possible moves: Nearest neighbour moves of already done moves
    Search depth: 1
    """
    all_moves  = generate_next_moves_nn(board, n, m)
    # print "prev.:",all_moves
    good_moves  = remove_bad_moves_1_step(all_moves,board,n,m)
    # print "after:",good_moves
    if len(good_moves) > 0:
        y, x = good_moves[np.random.randint(len(good_moves))] # Choose random good move
    else:
        y, x = all_moves[np.random.randint(len(all_moves))] # Choose random bad move
    board[y,x] = what_player
    return board


def make_a_move_ai_v3(board,n,m,current_player):
    """
    Computer plays using minimax algorithm.
    Considered first moves: NN

    Possible moves: Nearest neighbour moves of already done moves
    Search depth: >= 4
    """
    max_depth   = 4
    score, move = minimax(board, n, m, current_player, 0, max_depth)
    board[move] = current_player
    return board

def minimax_score(board, n, m, depth):
    winBool, player = evaluate_board_for_win(board,n,m,verbose=False,searching_game_tree=True)
    if winBool and player == 2:
        return 100 - depth
    elif winBool and player == 1:
        return depth - 100
    else:
        return 0

def minimax(board, n, m, cur_player, cur_depth, max_depth):
    """
    Recursive search for optimal move.

    Search depth: Given as input
    """
    winBool, player = evaluate_board_for_win(board,n,m,verbose=False,searching_game_tree=True)
    if winBool and player == 2:     # Game is over
        return 100 - cur_depth, None
    elif winBool and player == 1:   # Game is over
        return cur_depth - 100, None
    if cur_depth == max_depth:
        return 0, None              # Max depth is reached, and no player has won.

    cur_depth += 1                  # We have to go deeper!!!
    scores = []
    moves  = []

    # Fill list of scores, recursively
    all_moves = generate_next_moves_nn(board, n, m)
    for move in all_moves:
        possible_board       = np.copy(board)
        possible_board[move] = cur_player
        next_player          = get_next_player(cur_player)
        scores.append( minimax(possible_board, n, m, next_player, cur_depth, max_depth)[0] )
        moves.append( move )

    if cur_player == 2:
        max_score_index = np.argmax(scores) # If multiple candidates, pick first (lazy)
        move = moves[max_score_index]
        return scores[max_score_index], move
    else:
        min_score_index = np.argmin(scores)
        move = moves[min_score_index]
        return scores[min_score_index], move

def get_next_player(current_player):
    if current_player == 1:
        return 2
    elif current_player == 2:
        return 1
    else:
        print "Current player has illegal value", current_player
        print "Exiting..."
        sys.exit(0)


if __name__ == '__main__':
    board, n, m, what_player = init_game()

    if False:
        """
        This is human vs human
        """
        while True:
            print_board(board, n, m)
            board = make_a_move(board,n,m, what_player+1)
            if evaluate_board_for_win(board, n, m)[0]:
                print_board(board, n, m)
                break
            what_player = (what_player + 1) % 2 # Next players turn

    if True:
        """
        This is human vs computer
        """
        AI_choice = make_a_move_ai_v0 # This plays randomly
        AI_choice = make_a_move_ai_v1 # Also random, but next to another player
        AI_choice = make_a_move_ai_v2 # Plays randomly unless it can win, or avoid 1-step-loss
        AI_choice = make_a_move_ai_v3 # This is slow, very slow, but plays very good.
        while True:
            # Human turn
            print_board(board, n, m)
            board = make_a_move(board,n,m, what_player+1)
            if evaluate_board_for_win(board, n, m)[0]:
                print_board(board, n, m)
                break
            # AI turn
            what_player = (what_player + 1) % 2 # Next players turn
            board = AI_choice(board,n,m, what_player+1)
            if evaluate_board_for_win(board, n, m)[0]:
                print_board(board, n, m)
                break
            what_player = (what_player + 1) % 2 # Next players turn
