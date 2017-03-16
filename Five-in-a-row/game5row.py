from timeit import default_timer as timer # Best timer indep. of system
import sys
import numpy as np

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
    move       = (y,x)
    return board, move

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
    if len(nn_moves) < 1:
        nn_moves = [(n/2+np.random.choice([-1,0,1]),m/2+np.random.choice([-1,0,1]))] # This is the first move
    np.random.shuffle(nn_moves)     # Return moves-list wihtout any pre-determined order
    return nn_moves

def remove_bad_moves_1_step(all_moves,board,n,m,cur_player):
    good_moves = []
    ok_moves   = []
    gc3_board   = -1*np.ones((n+4,m+4)) # With ghost cells outside
    for move in all_moves:
        board_copy       = np.copy(board)
        board_copy[move] = cur_player
        winBool, who_won_or_draw = evaluate_board_for_win(board_copy,n,m,verbose=False,searching_game_tree=True)
        if winBool and who_won_or_draw == cur_player:
            return [move] # If we can win, stop early and simply do this move
        next_moves = generate_next_moves_nn(board_copy, n, m) # Next possible human moves
        move_was_good = True
        for move2 in next_moves:
            board_copy2        = np.copy(board_copy)
            board_copy2[move2] = get_next_player(cur_player)
            winBool, who_won_or_draw = evaluate_board_for_win(board_copy2,n,m,verbose=False,searching_game_tree=True)
            if winBool and who_won_or_draw == get_next_player(cur_player):
                move_was_good = False # If it can lead to loss, not good move!
            gc3_board[1:-3,1:-3] = board_copy2
            for jj in range(n):
                for ii in range(m):
                    j = jj+1; i = ii+1 # Fix indices to ghost cells
                    if gc3_board[j,i] == gc3_board[j+1,i] == gc3_board[j+2,i] == get_next_player(cur_player):
                        if gc3_board[j+3,i] == 0 and gc3_board[j-1,i] == 0:
                            move_was_good = False
                    if gc3_board[j,i] == gc3_board[j,i+1] == gc3_board[j,i+2] == get_next_player(cur_player):
                        if gc3_board[j,i+3] == 0 and gc3_board[j,i-1] == 0:
                            move_was_good = False
                    if gc3_board[j,i] == gc3_board[j+1,i+1] == gc3_board[j+2,i+2] == get_next_player(cur_player):
                        if gc3_board[j+3,i+3] == 0 and gc3_board[j-1,i-1] == 0:
                            move_was_good = False
                    if gc3_board[j,i+2] == gc3_board[j+1,i+1] == gc3_board[j+2,i] == get_next_player(cur_player):
                        if gc3_board[j-1,i+3] == 0 and gc3_board[j+3,i-1] == 0:
                            move_was_good = False
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
    if len(all_moves) < 1:
        all_moves  = generate_next_moves(board, n, m)
    y, x       = all_moves[np.random.randint(len(all_moves))] # Choose random move
    board[y,x] = what_player
    return board

def make_a_move_ai_v2(board,n,m,what_player):
    """
    Computer plays randomly next to another player,
    but checks for easy wins / losses.

    Possible moves: Nearest neighbour moves of already done moves
    Search depth: 1
    """
    all_moves  = generate_next_moves_nn(board, n, m)
    # print "prev.:",all_moves
    good_moves  = remove_bad_moves_1_step(all_moves,board,n,m,what_player)
    # print "after:",good_moves
    if len(good_moves) > 0:
        move = good_moves[np.random.randint(len(good_moves))] # Choose random good move
    else:
        move = all_moves[np.random.randint(len(all_moves))] # Choose random bad move
    print "\nComputer %d chose move:"%what_player,move,""
    board[move] = what_player
    return board


def make_a_move_ai_v3(board,n,m,current_player,max_depth=4,verbose=True):
    """
    Computer plays using minimax algorithm.
    Considered first moves: NN

    Possible moves: Nearest neighbour moves of already done moves
    Search depth: >= 3 (or else it is too dumb)
    """
    if current_player == 1:
        cpu_is_player2 = False
    else:
        cpu_is_player2 = True
    if verbose:
        sys.stdout.write("Computer %d is thinking...\n" %current_player)
        sys.stdout.flush()
    t0 = timer()
    for d in range(1,max_depth+1):
        tt0 = timer()
        score, move = minimax(board, n, m, get_next_player(current_player), 0, d, cpu_is_player2)
        if verbose:
            print "- Search depth: %g, score: %5.2f, move: (%d,%d), time: %.4f sec" %(d,score,move[0],move[1], timer()-tt0)
    if verbose:
        sys.stdout.write("\nComputer %d chose move: (%g,%g). Total time spent: %.2f sec\n" %(current_player, move[0], move[1], timer()-t0))
        sys.stdout.flush()
    board[move] = current_player
    return board

def leaf_score_func(board, n, m, cur_player):
    """
    This function gives a score depending on how many possible winning
    rows of length 2, 3 and 4 it can find.

    If no row(s) of length 5:
    - return SCORE False
    One (or more) rows of length 5:
    - return SCORE True
    """
    ret_score = 0
    cp        = cur_player
    opponent  = get_next_player(cp)
    cp_five   = np.ones(5)*cp
    game_won  = False
    gc_board  = -1*np.ones((n+6,m+6))# With ghost cells outside
    gc_board[1:-5,1:-5] = board
    for jj in range(n):
        for ii in range(m):
            j = jj+1; i = ii+1 # Fix indices to ghost cells
            diagM = gc_board[j:j+6, i:i+6]    # Split board into 6x6
            row   = diagM[0,:]                # looking for rows
            col   = diagM[:,0]                # looking for columns
            d1    = np.diag(diagM)            # looking for diagonal --> down
            d2    = np.diag(np.fliplr(diagM)) # looking for diagonal --> up

            test_list_5 = [row[:-1], col[:-1], d1[:-1], d2[:-1]]
            test_list_6 = [row     , col     , d1     , d2     ]
            for fiver in test_list_5:
                if np.array_equal(fiver, cp_five): # Game is won!
                    ret_score += 400
                    game_won   = True
                if np.count_nonzero(fiver == -1) > 0:
                    continue # If fiver is outside board, try next
                # Look for good 4-combos
                if np.count_nonzero(fiver == opponent) == 0: # Opponent has no spots here
                    if np.count_nonzero(fiver == cp) == 4:
                        ret_score += 4
                    # Look for good 3-combos
                    if np.count_nonzero(fiver == cp) == 3:
                        ret_score += 2
                    # Look for good 2-combos
                    if np.count_nonzero(fiver == cp) == 2:
                        ret_score += 0.1
            # Last out, length 4 with empty board on either side (aka winning)
            for sixer in test_list_6:
                if np.count_nonzero(sixer == -1) > 0:
                    continue # If fiver is outside board, try next
                if np.count_nonzero(sixer == opponent) == 0: # Opponent has no spots here
                    if np.count_nonzero(sixer == cp) == 4: # Four out of six spots belong to player.
                        if sixer[0] == sixer[-1] == 0:
                            ret_score += 50 # Position is won! ..but game not ended
    return ret_score, game_won

def minimax(board, n, m, cur_player, cur_depth, max_depth, cpu_is_player2=True):
    """
    Recursive search for optimal move.

    Search depth: Given as input
    """
    # winBool, player  = evaluate_board_for_win(board,n,m,verbose=False,searching_game_tree=True)
    leaf_score, game_won = leaf_score_func(board,n,m,cur_player) # Not complete / should be optimized (weights)

    # If game is over
    if game_won and cur_player == 2 and     cpu_is_player2:
        return leaf_score - cur_depth*0.1, False
    if game_won and cur_player == 1 and not cpu_is_player2:
        return leaf_score - cur_depth*0.1, False
    if game_won and cur_player == 1 and     cpu_is_player2:
        return cur_depth*0.1 - leaf_score, False
    if game_won and cur_player == 2 and not cpu_is_player2:
        return cur_depth*0.1 - leaf_score, False
    # Game is not over, but max_depth is reached:
    if cur_depth == max_depth:
        if (cpu_is_player2 and cur_player == 2) or (not cpu_is_player2 and cur_player == 1):
            return leaf_score - max_depth*0.1, False
        else:
            return max_depth*0.1 - leaf_score, False

    cur_depth += 1 # We have to go deeper!!!
    scores = []
    moves  = []

    # Fill list of scores, recursively
    all_moves = generate_next_moves_nn(board, n, m)
    for move in all_moves:
        possible_board       = np.copy(board)
        next_player          = get_next_player(cur_player)
        possible_board[move] = next_player
        move_score, _        = minimax(possible_board, n, m, next_player, cur_depth, max_depth, cpu_is_player2)
        scores.append( move_score )
        moves.append(  move )

    # if cur_depth == 1: # Print out possible next moves with score attained (bug fixing)
    #     for i in range(len(scores)):
    #         print scores[i], moves[i]

    if (cpu_is_player2 and next_player == 2) or (not cpu_is_player2 and next_player == 1):
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
    print_board(board, n, m) # First time, before we start.

    """
    Choose the players!
    """
    hmn_vs_hmn = False
    hmn_vs_cpu = False
    cpu_vs_cpu = True
    test_mode  = False

    if hmn_vs_hmn:
        """
        This is human vs human
        """
        while True:
            board = make_a_move(board,n,m, what_player+1)
            if evaluate_board_for_win(board, n, m)[0]:
                print_board(board, n, m)
                break
            what_player = (what_player + 1) % 2 # Next players turn

    if hmn_vs_cpu:
        """
        This is human vs computer.

        - Choose what strength to play against below
          (uncomment the line)!
        """
        # AI_choice = make_a_move_ai_v0 # This plays randomly
        # AI_choice = make_a_move_ai_v1 # Also random, but next to another player
        # AI_choice = make_a_move_ai_v2 # Plays randomly unless it can win, or avoid 1-step-loss
        AI_choice = make_a_move_ai_v3 # This is slow, very slow, but plays very good.

        """
        If AI V3 is used, 'search_depth' can be specified. Higher is better.
        - A value of 3 is good, but it can be fooled by using "multiple lines".
        - A value of 4 is tough to beat, but is starting to be really slow.
        Higher values are ridiculously slow...^^ Happy waiting!
        """
        search_depth = 3

        # Write out what computer is thinking?
        verbose = True

        list_of_human_moves = []
        while True:
            board, move = make_a_move(board,n,m, 1) # Human turn
            list_of_human_moves.append(move)
            if evaluate_board_for_win(board, n, m)[0]:
                print_board(board, n, m)
                break
            print_board(board, n, m)                # AI turn
            board = AI_choice(board,n,m, 2, max_depth=search_depth, verbose=verbose)
            if evaluate_board_for_win(board, n, m)[0]:
                print_board(board, n, m)
                break
            print_board(board, n, m)
        print "List of human moves:", list_of_human_moves

    if cpu_vs_cpu:
        """
        This is computer vs computer.

        - Choose what strength to play against below
          (uncomment the line)!
        """
        # AI_choice = make_a_move_ai_v0 # This plays randomly
        # AI_choice = make_a_move_ai_v1 # Also random, but next to another player
        # AI_choice = make_a_move_ai_v2 # Plays as v1, unless it can win, or avoid 1-step-loss
        # AI_choice = make_a_move_ai_v3 # This is slow, very slow, but plays very good.

        AI_choice1 = make_a_move_ai_v3
        AI_choice2 = make_a_move_ai_v3

        while True:
            board = AI_choice1(board,n,m, 1, max_depth = 2) # CPU 1 turn
            if evaluate_board_for_win(board, n, m)[0]:
                print_board(board, n, m)
                break
            print_board(board, n, m)
            board = AI_choice2(board,n,m, 2, max_depth = 4) # CPU 2 turn
            if evaluate_board_for_win(board, n, m)[0]:
                print_board(board, n, m)
                break
            print_board(board, n, m)

    """
    ##############################
    Below is for testing purposes!
    ##############################
    """
    if test_mode:
        while True:
            print_board(board, n, m)
            swap_player = int(raw_input("1 for human player 1,\n2 for human 2,\n3 for cpu 1\n4 for cpu 4: "))
            if swap_player == 1:
                board, move = make_a_move(board,n,m, 1)
                if evaluate_board_for_win(board, n, m)[0]:
                    print_board(board, n, m)
                    break
            elif swap_player == 2:
                board, move = make_a_move(board,n,m, 2)
                if evaluate_board_for_win(board, n, m)[0]:
                    print_board(board, n, m)
                    break
            elif swap_player == 3:
                board = make_a_move_ai_v3(board,n,m, 1)
                if evaluate_board_for_win(board, n, m)[0]:
                    print_board(board, n, m)
                    break
            else:
                board = make_a_move_ai_v3(board,n,m, 2)
                if evaluate_board_for_win(board, n, m)[0]:
                    print_board(board, n, m)
                    break

# Can loop be done in C?
# (Code below from previous project with laplace equation (aka heat eq.))
# code = """
# int t,i,j;
# for (t=0; t*dt<t_end+dt; t++){
#     for (i=1; i<Nu[0]-1; i++) {
#        for (j=1; j<Nu[1]-1; j++) {
#            UN2(i,j) = U2(i,j) \
#                     + dt*nu*(U2(i-1,j) + U2(i,j-1) - 4*U2(i,j) \
#                     + U2(i,j+1) + U2(i+1,j)) + dt*nu*F2(i,j);
#        }
#     }
#     for (i=1; i<Nu[0]-1; i++) {
#        for (j=1; j<Nu[1]-1; j++) {
#            U2(i,j) = UN2(i,j);
#        }
#     }
# }
# """
#
# weave.inline(code, ['t_end','dt', 'u', 'un','f', 'nu'])
