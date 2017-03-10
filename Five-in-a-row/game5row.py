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
    board = np.random.randint(0,3, size=(n,m))
    board[0:5,0:5] = 0
    return board, n, m

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

def evaluate_board_for_win(board,n,m):
    """
    Need to think how to make this as quick as possible..
    """
    for j in range(n-4):
        for i in range(m-4):
            fiver = board[j,i:i+5] # looking for rows
            print fiver
            raw_input()



if __name__ == '__main__':
    board, n, m = init_game()
    print_board(board, n, m)
    evaluate_board_for_win(board, n, m)
