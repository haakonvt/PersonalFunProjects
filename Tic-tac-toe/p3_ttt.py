import numpy as np
import itertools
import sys

def init_board():
    # 1 is cross
    # 2 is nought
    print("------------------------")
    print("Playing Tic-tac-toe")
    return np.zeros((3,3))

def generate_next_moves(board_position):
    l = [] # List of lists with y,x
    for y in range(3):
        for x in range(3):
            if board_position[y,x] == 0:
                l.append([y,x])
    return l

def whos_turn(board_position):
    b = board_position
    crosses = np.count_nonzero(b == 1)
    noughts = np.count_nonzero(b == 2)
    if crosses <= noughts:
        return 1
    else:
        return 2

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
    print(" ___________ ")
    print("| %s | %s | %s |" %(msfp(b,0,0), msfp(b,0,1), msfp(b,0,2)))
    print(" ___________ ")
    print("| %s | %s | %s |" %(msfp(b,1,0), msfp(b,1,1), msfp(b,1,2)))
    print(" ___________ ")
    print("| %s | %s | %s |" %(msfp(b,2,0), msfp(b,2,1), msfp(b,2,2)))
    print(" ___________ ")

def one_move_hh(board_position): # human vs human
    current_player = whos_turn(board_position)
    if current_player == 1:
        print("------------------------\nCurrent player: CROSSES (human 1)")
    else:
        print("------------------------\nCurrent player: NOUGHTS (human 2)")
    fancy_print(board_position)
    while True:
        inp = input("Input move:")
        try:
            y = int(inp[0])
            x = int(inp[1])
        except:
            bad_input_print(board_position)
            continue
        if y < 0 or y > 2:
            if x < 0 or x > 2:
                bad_input_print(board_position)
                continue
        elif board_position[y,x] != 0:
            bad_input_print(board_position)
            continue
        else:
            break
    board_position[y,x] = current_player # 1 or 2
    return board_position

def check_for_win(board_position, verbose=True):
    b   = board_position
    win = [np.array([1,1,1]), np.array([2,2,2])]
    for i in range(3):
        if np.array_equal(b[:,i], win[0]): # columns
            if verbose:
                print("CROSSES won!!!")
            return True, 1
        if np.array_equal(b[i,:], win[0]): # rows
            if verbose:
                print("CROSSES won!!!")
            return True, 1
        if np.array_equal(b[:,i], win[1]): # columns
            if verbose:
                print("NOUGHTS won!!!")
            return True, 2
        if np.array_equal(b[i,:], win[1]): # rows
            if verbose:
                print("NOUGHTS won!!!")
            return True, 2
    if np.array_equal(np.array([b[0,0], b[1,1], b[2,2]]), win[0]):
        if verbose:
            print("CROSSES won!!!")
        return True, 1
    if np.array_equal(np.array([b[2,0], b[1,1], b[0,2]]), win[0]):
        if verbose:
            print("CROSSES won!!!")
        return True, 1
    if np.array_equal(np.array([b[0,0], b[1,1], b[2,2]]), win[1]):
        if verbose:
            print("NOUGHTS won!!!")
        return True, 2
    if np.array_equal(np.array([b[2,0], b[1,1], b[0,2]]), win[1]):
        if verbose:
            print("NOUGHTS won!!!")
        return True, 2
    # Check for tie
    non_empty = np.count_nonzero(b == 0)
    if not non_empty:
        if verbose:
            print("Match ended in a tie!!!")
        return True, 0
    return False, -1 # Board is not won

def bad_input_print(board_position):
    possible_moves = generate_next_moves(board_position)
    possible_moves = [str(y)+str(x) for y,x in possible_moves]
    p_moves_string = ""
    for move in possible_moves:
        p_moves_string += move + ", "
    print("Not valid move!")
    print("Valid moves:", p_moves_string[:-2])

# -----------------------
# Here starts the AI code
# -----------------------
def one_move_hm(board_position): # human vs machine
    current_player = whos_turn(board_position)
    if current_player == 1:
        print("------------------------\nCurrent player: CROSSES (human)")
        fancy_print(board_position)
        while True:
            inp = input("Input move:")
            try:
                y = int(inp[0])
                x = int(inp[1])
            except:
                bad_input_print(board_position)
                continue
            if y < 0 or y > 2:
                if x < 0 or x > 2:
                    bad_input_print(board_position)
                    continue
            elif board_position[y,x] != 0:
                bad_input_print(board_position)
                continue
            else:
                break
        board_position[y,x] = current_player # 1 or 2
        return board_position
    else:
        print("------------------------\nCurrent player: NOUGHTS (machine)")
        fancy_print(board_position)
        y, x = not_so_simple_evaluate(board_position)
        board_position[y,x] = current_player # 1 or 2
        return board_position

def canIWin(board_position, next_moves, player1or2=2):
    """
    Machine is always player 2 aka noughts, but this function can evaluate for both players
    """
    for y,x in next_moves:
        test      = np.copy(board_position)
        test[y,x] = player1or2
        if check_for_win(test, verbose=False)[0]:
            return True, y, x
    return False, None, None # No moves give instant victory

def canIDraw(board_position, next_moves):
    y1, x1 = next_moves[0]
    y2, x2 = next_moves[1]

    test1      = np.copy(board_position)
    test1[y1,x1] = 2
    test1[y2,x2] = 1
    t1_winBool, t1_player = check_for_win(test1, verbose=False)
    if t1_winBool and t1_player == 2:
        return y1, x1
    test2      = np.copy(board_position)
    test2[y1,x1] = 1
    test2[y2,x2] = 2
    t2_winBool, t2_player = check_for_win(test2, verbose=False)
    if t2_winBool and t2_player == 2:
        return y1, x1
    if t1_player == 0: # This means draw
        return y1, x1
    elif t2_player == 0:
        return y2, x2
    else:
        print("This should never happen lulz")

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

def not_idiot_move(board_position, not_loosing_moves):
    np.random.shuffle(not_loosing_moves) # Make the machine not predictable, but still flawless
    for y,x in not_loosing_moves:
        test      = np.copy(board_position)
        test[y,x] = 2 # Machine is always player 2 aka noughts
        next_human_moves = generate_next_moves(test) # Generate next moves of human
        winBool, _, _    = canIWin(test, next_human_moves, player1or2=2) # If I could place two, could I win?
        if winBool:
            return y,x
    return not_loosing_moves[0] # If all equally bad, return random

def not_so_simple_evaluate(board_position):
    b             = board_position
    corners_rand  = [[0,0], [0,2], [2,0], [2,2]]
    edges_rand    = [[0,1], [1,2], [2,1], [1,0]]
    next_moves    = generate_next_moves(b)
    winBool, y, x = canIWin(b, next_moves)
    if winBool:
        return y, x
    else:
        not_loosing_moves = remove_bad_moves(b, next_moves)
        pssbl_moves = len(not_loosing_moves)
        np.random.shuffle(corners_rand)
        np.random.shuffle(edges_rand)
        if pssbl_moves == 0:
            y, x = canIDraw(b, next_moves)
            return y, x
        elif pssbl_moves == 1:
            y, x = not_loosing_moves[0]
            return y, x
        else: # This means pssbl_moves > 1:
            if [1,1] in not_loosing_moves: # Pick center if possible
                return 1, 1
            if b[1,1] == 2: # Machine control center
                if (b[0,0] == 1 and b[2,2] == 1) or (b[0,2] == 1 and b[2,0] == 1):
                    for move in edges_rand:
                        if move in not_loosing_moves:
                            return move
                if (b[0,1] == 1 and b[2,1] == 1) or (b[1,0] == 1 and b[1,2] == 1):
                    for move in corners_rand:
                        if move in not_loosing_moves:
                            return move
                if b[1,0] == 1 and b[0,1]:
                    if [0,0] in not_loosing_moves:
                        return 0,0
                if b[0,1] == 1 and b[1,2]:
                    if [0,2] in not_loosing_moves:
                        return 0,2
                if b[1,2] == 1 and b[2,1]:
                    if [2,2] in not_loosing_moves:
                        return 2,2
                if b[2,1] == 1 and b[1,0]:
                    if [2,0] in not_loosing_moves:
                        return 2,0
                return not_idiot_move(b, not_loosing_moves)
            if b[1,1] == 1: # Human control center
                for move in corners_rand:
                    if move in not_loosing_moves:
                        return move # Pick random corner
                for move in edges_rand:
                    if move in not_loosing_moves:
                        return move # Pick random edge if all corners are gone


if __name__ == '__main__':
    # Initiate empty board
    board = init_board()

    # Choose opponent, machine or human!
    PvP_bool = False
    PvM_bool = True

    if PvP_bool:
        "This is PvP"
        while True:
            board = one_move(board)
            if check_for_win(board)[0]:
                break
        fancy_print(board)

    if PvM_bool:
        "Human vs perfect AI"
        while True:
            board = one_move_hm(board)
            if check_for_win(board)[0]:
                break
        fancy_print(board)
