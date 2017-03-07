import numpy as np

def init_board():
    # 1 is cross
    # 2 is nought
    print "------------------------"
    print "Playing Tic-tac-toe"
    return np.zeros((3,3))

def fancy_print(board_position):
    def make_symbol_for_print(board_position,x,y):
        if board_position[x,y] == 0:
            return " "
        if board_position[x,y] == 1:
            return "X"
        if board_position[x,y] == 2:
            return "O"
    msfp = make_symbol_for_print
    b    = board_position
    print " ___________ "
    print "| %s | %s | %s |" %(msfp(b,0,0), msfp(b,0,1), msfp(b,0,2))
    print " ___________ "
    print "| %s | %s | %s |" %(msfp(b,1,0), msfp(b,1,1), msfp(b,1,2))
    print " ___________ "
    print "| %s | %s | %s |" %(msfp(b,2,0), msfp(b,2,1), msfp(b,2,2))
    print " ___________ "

def one_move_hh(board_position): # human vs human
    current_player = whos_turn(board_position)
    if current_player == 1:
        print "------------------------\nCurrent player: CROSSES (human 1)"
    else:
        print "------------------------\nCurrent player: NOUGHTS (human 2)"
    fancy_print(board_position)
    while True:
        inp = raw_input("Input move:")
        try:
            y = int(inp[0])
            x = int(inp[1])
        except:
            print "Not valid move, try again!"
            continue
        if y < 0 or y > 2:
            if x < 0 or x > 2:
                "Not valid move, try again!"
                continue
        elif board_position[y,x] != 0:
            "Not valid move, spot already taken!"
            continue
        else:
            break
    board_position[y,x] = current_player # 1 or 2
    return board_position

def whos_turn(board_position):
    b = board_position
    crosses = np.count_nonzero(b == 1)
    noughts = np.count_nonzero(b == 2)
    if crosses <= noughts:
        return 1
    else:
        return 2

def check_for_win(board_position, verbose=True):
    b   = board_position
    win = [np.array([1,1,1]), np.array([2,2,2])]
    xWon = False
    oWon = True
    for i in range(3):
        if np.array_equal(b[:,i], win[0]): # columns
            xWon = True
            if verbose:
                print "CROSSES won!!!"
            return True
        if np.array_equal(b[i,:], win[0]): # rows
            xWon = True
            if verbose:
                print "CROSSES won!!!"
            return True
        if np.array_equal(b[:,i], win[1]): # columns
            oWon = True
            if verbose:
                print "NOUGHTS won!!!"
            return True
        if np.array_equal(b[i,:], win[1]): # rows
            oWon = True
            if verbose:
                print "NOUGHTS won!!!"
            return True
    if np.array_equal(np.array([b[0,0], b[1,1], b[2,2]]), win[0]):
        xWon = True
        if verbose:
            print "CROSSES won!!!"
        return True
    if np.array_equal(np.array([b[2,0], b[1,1], b[0,2]]), win[0]):
        xWon = True
        if verbose:
            print "CROSSES won!!!"
        return True
    if np.array_equal(np.array([b[0,0], b[1,1], b[2,2]]), win[1]):
        oWon = True
        if verbose:
            print "NOUGHTS won!!!"
        return True
    if np.array_equal(np.array([b[2,0], b[1,1], b[0,2]]), win[1]):
        oWon = True
        if verbose:
            print "NOUGHTS won!!!"
        return True
    # Check for tie
    non_empty = np.count_nonzero(b == 0)
    if not non_empty:
        print "Match ended in a tie!!!"; return True
    return False # Board is not won

# -----------------------
# Here starts the AI code
# -----------------------
def one_move_hm(board_position): # human vs human
    current_player = whos_turn(board_position)
    if current_player == 1:
        print "------------------------\nCurrent player: CROSSES (human)"
        fancy_print(board_position)
        while True:
            inp = raw_input("Input move:")
            try:
                y = int(inp[0])
                x = int(inp[1])
            except:
                print "Not valid move, try again!"
                continue
            if y < 0 or y > 2:
                if x < 0 or x > 2:
                    "Not valid move, try again!"
                    continue
            elif board_position[y,x] != 0:
                "Not valid move, spot already taken!"
                continue
            else:
                break
        board_position[y,x] = current_player # 1 or 2
        return board_position
    else:
        print "------------------------\nCurrent player: NOUGHTS (machine)"
        fancy_print(board_position)
        y, x = simple_evaluate(board_position)
        board_position[y,x] = current_player # 1 or 2
        return board_position

def generate_next_moves(board_position):
    l = [] # List of lists with y,x
    for y in range(3):
        for x in range(3):
            if board_position[y,x] == 0:
                l.append([y,x])
    return l

def canIWin(board_position, next_moves, player1or2=2):
    """
    Machine is always player 2 aka noughts, but this function can evaluate for both players
    """
    for y,x in next_moves:
        test      = np.copy(board_position)
        test[y,x] = player1or2
        if check_for_win(test, verbose=False):
            return True, y, x
    return False, None, None # No moves give instant victory

def remove_bad_moves(board_position, next_moves):
    improved_moves = []
    for y,x in next_moves:
        test      = np.copy(board_position)
        test[y,x] = 2 # Machine is always player 2 aka noughts
        next_human_moves = generate_next_moves(test) # Generate next moves of human
        winBool, _, _    = canIWin(test, next_human_moves, player1or2=1) # Check if human can win
        if not winBool:
            improved_moves.append([y,x])
    return improved_moves

def simple_evaluate(board_position):
    next_moves = generate_next_moves(board_position)
    winBool, y, x = canIWin(board_position, next_moves)
    if winBool:
        return y, x
    else:
        not_loosing_moves = remove_bad_moves(board_position, next_moves)
        pssbl_moves = len(not_loosing_moves)
        print not_loosing_moves
        if pssbl_moves > 1:
            y,x = not_loosing_moves[np.random.randint(pssbl_moves)]
            return y, x
        elif pssbl_moves == 1:
            y, x = not_loosing_moves[0]
            return y, x
    # Play a random move (bad as fk)
    y, x = next_moves[np.random.randint(len(next_moves))]
    return y, x

if __name__ == '__main__':
    board = init_board()

    simple_evaluate(board)

    if "human vs human" == True:
        while True:
            board = one_move(board)
            if check_for_win(board):
                break
        fancy_print(board)
    if True:
        "Human vs machine"
        while True:
            board = one_move_hm(board)
            if check_for_win(board):
                break
        fancy_print(board)
