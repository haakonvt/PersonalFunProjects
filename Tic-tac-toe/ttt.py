import numpy as np

def init_board():
    # 1 is cross
    # 2 is nought
    print "------------------------"
    print "Playing Tic-tac-toe"
    return np.zeros((3,3))

def evaluate(board_position):
    pass

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

def one_move(board_position):
    current_player = whos_turn(board_position)
    if current_player == 1:
        print "------------------------\nCurrent player: CROSSES"
    else:
        print "------------------------\nCurrent player: NOUGHTS"
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

def check_for_win(board_position):
    b   = board_position
    win = [np.array([1,1,1]), np.array([2,2,2])]
    for i in range(3):
        if np.array_equal(b[:,i], win[0]): # columns
            print "CROSSES won!!!"; return True
        if np.array_equal(b[i,:], win[0]): # rows
            print "CROSSES won!!!"; return True
        if np.array_equal(b[:,i], win[1]): # columns
            print "NOUGHTS won!!!"; return True
        if np.array_equal(b[i,:], win[1]): # rows
            print "NOUGHTS won!!!"; return True
    if np.array_equal(np.array([b[0,0], b[1,1], b[2,2]]), win[0]):
        print "CROSSES won!!!"; return True
    if np.array_equal(np.array([b[2,0], b[1,1], b[0,2]]), win[0]):
        print "CROSSES won!!!"; return True
    if np.array_equal(np.array([b[0,0], b[1,1], b[2,2]]), win[1]):
        print "NOUGHTS won!!!"; return True
    if np.array_equal(np.array([b[2,0], b[1,1], b[0,2]]), win[1]):
        print "NOUGHTS won!!!"; return True
    # Check for tie
    non_empty = np.count_nonzero(b == 0)
    if not non_empty:
        print "Match ended in a tie!!!"; return True
    return False # Board is not won

if __name__ == '__main__':
    board = init_board()
    while True:
        board = one_move(board)
        if check_for_win(board):
            break
    fancy_print(board)
