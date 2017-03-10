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

def evaluate_board_for_win(board,n,m,what_player):
    """
    Need to think how to make this as quick as possible..
    """
    winCross  = np.ones(5)
    winNought = np.ones(5)*2
    for j in range(n-4):
        for i in range(m-4):
            diagM   = board[j:j+5, i:i+5]
            r_fiver = diagM[0,:] # looking for rows
            c_fiver = diagM[:,0] # looking for columns
            d_fiver = np.diag(diagM)            # looking for diagonal --> down
            u_fiver = np.diag(np.fliplr(diagM)) # looking for diagonal --> up

            if what_player == 1:
                cross_win_bools   = [np.array_equal(winCross, fiver)  for fiver in [r_fiver, c_fiver, d_fiver, u_fiver]]
                if np.any(cross_win_bools):
                    print "Crosses won!"
                    return True, 1
            else:
                noughts_win_bools = [np.array_equal(winNought, fiver) for fiver in [r_fiver, c_fiver, d_fiver, u_fiver]]
                if np.any(noughts_win_bools):
                    print "Noughts won!"
                    return True, 2
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

def make_a_move_ai_v0(board,n,m,what_player):
    all_moves  = generate_next_moves(board, n, m)
    y, x       = all_moves[np.random.randint(len(all_moves))] # Choose random move
    board[y,x] = what_player
    return board


if __name__ == '__main__':
    board, n, m, what_player = init_game()

    if False:
        """
        This is human vs human
        """
        while True:
            print_board(board, n, m)
            board = make_a_move(board,n,m, what_player+1)
            if evaluate_board_for_win(board, n, m, what_player+1)[0]:
                print_board(board, n, m)
                break
            what_player = (what_player + 1) % 2 # Next players turn

    if True:
        """
        This is human vs dumb as fk machine
        """
        while True:
            print_board(board, n, m)
            board = make_a_move(board,n,m, what_player+1)
            if evaluate_board_for_win(board, n, m, what_player+1)[0]:
                print_board(board, n, m)
                break
            what_player = (what_player + 1) % 2 # Next players turn
            board = make_a_move_ai_v0(board,n,m, what_player+1)
            if evaluate_board_for_win(board, n, m, what_player+1)[0]:
                print_board(board, n, m)
                break
            what_player = (what_player + 1) % 2 # Next players turn
