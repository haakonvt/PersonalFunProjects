//
//  main.cpp
//  five_in_a_row
//
//  Created by Håkon V. Treider on 26/03/2018.
//  Copyright? Nonono, lol
//

#include <iostream>
#include <sstream>
#include <vector>
#include <chrono>
#include <random>

using namespace std;

const int BOARD_ROWS = 5;
const int BOARD_COLS = 8;
const int MAX_TURNS = BOARD_ROWS * BOARD_COLS;
double TIME_SPENT = 0.0;
unsigned seed = chrono::system_clock::now().time_since_epoch().count();
default_random_engine generator(seed);

struct Move {
    // This will be a single move on the board
    int row;
    int col;
};

class Board{
public:
    Board();
    int arr_board[BOARD_ROWS][BOARD_COLS];
    int max_moves = BOARD_ROWS * BOARD_COLS;
    vector<Move> get_move_list();
    void print_board();
    void make_move(int, int, int &);
    bool legal_move(int, int);
    bool check_game_won(int);
    
private:
    string board_row;
};

Board::Board(){
    // Class constructor
    // Set board to only zeros
    for (int i = 0; i<BOARD_ROWS; ++i){
        for (int j = 0; j<BOARD_COLS; ++j){
            arr_board[i][j] = 0;
        }
    }
};

vector<Move> Board::get_move_list(){
    Move single_move;
    vector<Move> move_list;
    move_list.reserve(max_moves); // Make room for all pos. moves --> no realloc. of memory later
    for (int i = 0; i<BOARD_ROWS; ++i){
        for (int j = 0; j<BOARD_COLS; ++j){
            if (arr_board[i][j] == 0){
                single_move.row = i;
                single_move.col = j;
                move_list.push_back(single_move);
            }
        }
    }
    return move_list;
}

void Board::print_board(){
    // Prints out current board state
    string symbol_to_print = "  ";
    int player_symbol;
    for (int i=0; i<BOARD_COLS; ++i){
        symbol_to_print += to_string(i) + " ";
    }
    cout << endl << symbol_to_print << endl;
    cout << " " + string(BOARD_COLS*2+1, '-') << endl;
    for (int i = 0; i<BOARD_ROWS; ++i){
        board_row = to_string(i) + "|";
        for (int j = 0; j<BOARD_COLS; ++j){
            player_symbol = arr_board[i][j];
            if (player_symbol == 0){
                symbol_to_print = " ";
            }
            else if (player_symbol == 1){
                symbol_to_print = "X";
            }
            else{
                symbol_to_print = "O";
            }
            board_row += symbol_to_print + "|";
        }
        cout << board_row << endl;
        cout << " " + string(BOARD_COLS*2+1, '-') << endl;
    }
}

void Board::make_move(int r, int c, int &player){
    // Modifies the board. Will overwrite, so legal_move should be checked first.
    arr_board[r][c] = player;
}

bool Board::legal_move(int move_r, int move_c){
    // Check if a move is valid.
    if (arr_board[move_r][move_c] == 0){
        return true;
    }
    else{
        return false;
    }
}

bool Board::check_game_won(int player){
    auto &b = arr_board; // Reference to board array
    int  &p  = player;
    
    // Check most possibilities (except bottom right corner)
    for (int i=0; i<BOARD_ROWS; ++i){
        for (int j=0; j<BOARD_COLS; ++j){
            if (i < BOARD_ROWS-4 and j < BOARD_COLS-4){
                if (p == b[i][j] and p == b[i][j+1] and p == b[i][j+2] and p == b[i][j+3] and p == b[i][j+4]){
                    return true;
                }
                if (p == b[i][j] and p == b[i+1][j] and p == b[i+2][j] and p == b[i+3][j] and p == b[i+4][j]){
                    return true;
                }
                if (p == b[i][j] and p == b[i+1][j+1] and p == b[i+2][j+2] and p == b[i+3][j+3] and p == b[i+4][j+4]){
                    return true;
                }
                if (p == b[i+4][j] and p == b[i+3][j+1] and p == b[i+2][j+2] and p == b[i+1][j+3] and p == b[i][j+4]){
                    return true;
                }
            } // Check bottom right corner/square...
            if (i >= BOARD_ROWS-4 and j < BOARD_COLS-4){
                if (p == b[i][j] and p == b[i][j+1] and p == b[i][j+2] and p == b[i][j+3] and p == b[i][j+4]){
                    return true;
                }
            }
            if (i < BOARD_ROWS-4 and j >= BOARD_COLS-4){
                if (p == b[i][j] and p == b[i+1][j] and p == b[i+2][j] and p == b[i+3][j] and p == b[i+4][j]){
                    return true;
                }
            }
        }
    }
    // If no 5-in-a-rows are found, return false:
    return false;
}

void get_human_move(Board &board, int &player){
    // Get a valid move from a human
    string user_input = "";
    int move_r = 0; // Row or col
    int move_c = 0;
    
    while (true){ // To check that move is valid on board
        while (true){ // Get the row index
            while (true) {
                cout << "Choose row number: ";
                getline(cin, user_input);
                
                // This code converts from string to number safely.
                stringstream my_stream(user_input);
                if (my_stream >> move_r){
                    break;
                }
                cout << "Invalid number, please try again" << endl;
            }
            if (move_r >= 0 and move_r < BOARD_ROWS){
//                cout << "Row chosen: " << to_string(move_r) << endl;
                break;
            }
        }
        while (true){ // Get the col index
            while (true) {
                cout << "Choose column number: ";
                getline(cin, user_input);
                
                // This code converts from string to number safely.
                stringstream my_stream(user_input);
                if (my_stream >> move_c){
                    break;
                }
                cout << "Invalid number, please try again" << endl;
            }
            if (move_c >= 0 and move_c < BOARD_COLS){
//                cout << "Row chosen: " << to_string(move_c) << endl;
                break;
            }
        }
        if (board.legal_move(move_r,move_c)){
            cout << "Player " << to_string(player) << " made the move " << "(" << to_string(move_r) << "," << to_string(move_c) << ")" << endl;
            board.make_move(move_r, move_c, player);
            break;
        }
    }
}

void weight_function(int &fiver_sum, double &valuation){
    /* Weight function is written out to avoid computing the power function.
       Formula for valuation is:
       valuation += pow(10, (fiver_sum-1)), for fiver_sum > 0            */
    if (fiver_sum > 0) {
        if (fiver_sum == 1){
            valuation += 1;
        }
        else if (fiver_sum == 2){
            valuation += 10;
        }
        else if (fiver_sum == 3){
            valuation += 100;
        }
        else if (fiver_sum == 4){
            valuation += 1000;
        }
        else{ // Game is won!
            valuation += INFINITY;
        }
    }
}

double board_evaluation(Board &board){
    /* Evaluates the board position for player 1 i.e.
       positive score = good for player 1
       negative score = good for player 2 */
    int fiver_sum;
    double valuation = 0;
    auto &b = board.arr_board; // Reference to board array
    
    for (int p = 1; p < 3; ++p){ // p = player
        /* First sum up value for p1, then make negative for sum for p2. Then after p2 sum is
           done, swap sign again (done at return statement)*/
        valuation *= -1.0;
        
        int np = p%2 + 1;       // ID of other player
        
        // Check all 2,3 and 4 possibilities (except bottom right corner)
        for (int i=0; i<BOARD_ROWS; ++i){
            for (int j=0; j<BOARD_COLS; ++j){
                // Give value to open 5-ers based on how many player-only spots are taken. Open = taken by player or no player at all.
                if (i < BOARD_ROWS-4 and j < BOARD_COLS-4){
                    if (np != b[i][j] and np != b[i][j+1] and np != b[i][j+2] and np != b[i][j+3] and np != b[i][j+4]){
                        fiver_sum = (b[i][j] + b[i][j+1] + b[i][j+2] + b[i][j+3] + b[i][j+4]) / p; // Divide by p (1 or 2) to normalize
                        weight_function(fiver_sum, valuation);
                    }
                    if (np != b[i][j] and np != b[i+1][j] and np != b[i+2][j] and np != b[i+3][j] and np != b[i+4][j]){
                        fiver_sum = (b[i][j] + b[i+1][j] + b[i+2][j] + b[i+3][j] + b[i+4][j]) / p;
                        weight_function(fiver_sum, valuation);
                    }
                    if (np != b[i][j] and np != b[i+1][j+1] and np != b[i+2][j+2] and np != b[i+3][j+3] and np != b[i+4][j+4]){
                        fiver_sum = (b[i][j] + b[i+1][j+1] + b[i+2][j+2] + b[i+3][j+3] + b[i+4][j+4]) / p;
                        weight_function(fiver_sum, valuation);
                    }
                    if (np != b[i+4][j] and np != b[i+3][j+1] and np != b[i+2][j+2] and np != b[i+1][j+3] and np != b[i][j+4]){
                        fiver_sum = (b[i+4][j] + b[i+3][j+1] + b[i+2][j+2] + b[i+1][j+3] + b[i][j+4]) / p;
                        weight_function(fiver_sum, valuation);
                    }
                } // Check bottom right corner/square...
                if (i >= BOARD_ROWS-4 and j < BOARD_COLS-4){
                    if (np != b[i][j] and np != b[i][j+1] and np != b[i][j+2] and np != b[i][j+3] and np != b[i][j+4]){
                        fiver_sum = (b[i][j] + b[i][j+1] + b[i][j+2] + b[i][j+3] + b[i][j+4]) / p;
                        weight_function(fiver_sum, valuation);
                    }
                }
                if (i < BOARD_ROWS-4 and j >= BOARD_COLS-4){
                    if (np != b[i][j] and np != b[i+1][j] and np != b[i+2][j] and np != b[i+3][j] and np != b[i+4][j]){
                        fiver_sum = (b[i][j] + b[i+1][j] + b[i+2][j] + b[i+3][j] + b[i+4][j]) / p;
                        weight_function(fiver_sum, valuation);
                    }
                }
            }
        }
        
    }
    /* Return negative of board score (score is always added to total,
       so for opposing player we first swap sign --> therefore we return negative to undo this.) */
//    cout << "POINT H: " << -valuation << endl;
    return -valuation;
}

struct Move_with_eval{
    Move move;
    double eval;
};

struct by_eval{
    bool operator()(Move_with_eval const &a, Move_with_eval const &b){
        return a.eval < b.eval;
    }
};

void print_top_moves(vector<Move_with_eval> top_moves){
    // Sort moves by their evaluation, then print top 5 (and worst for fun)
    
    std::sort(top_moves.begin(), top_moves.end(), by_eval());
    
    cout << "Best cpu-moves (from best to worst):" << endl;
    int stop = 0;
    string print_nmbr = "";
    for (auto &i_move_eval : top_moves){
        ++stop;
        if (stop > 5 and stop != top_moves.size()){
            continue; // Skip 6th --> penultimate
        }
        if (stop < 9){
            print_nmbr = " " + to_string(stop);
        }
        else{
            print_nmbr = to_string(stop);
        }
        cout << " -" << print_nmbr << ": (" << i_move_eval.move.row << "," << i_move_eval.move.col << "). Score: " << i_move_eval.eval << endl;
    }
}

double minimax(Board &board, int search_depth, bool maximizing_player){
    bool NO_MORE_MOVES = false;
    double valuation;
    int best_row = -1;
    int best_col = -1;
    vector<Move> move_list = board.get_move_list();
    
    if (move_list.size() == 0) {
        NO_MORE_MOVES = true;
    }
    
    // Recursive search of optimal play using minimax algorithm
    if (search_depth == 0 or NO_MORE_MOVES) {
        return board_evaluation(board);
    }
    if (maximizing_player){
        int player = 1;
        double best_value = -INFINITY;
        
//        if (board.check_game_won(player)){ // Quit search early if game over
//            return INFINITY;
//        }
        for (auto &i_move : move_list){ // move in move_list
            Board node = board;
            node.make_move(i_move.row, i_move.col, player);
            valuation  = minimax(node, search_depth-1, false);
            if (valuation > best_value or best_row == -1){
                best_value = valuation;
                best_row = i_move.row;
                best_col = i_move.col;
            }
        }
        board.make_move(best_row, best_col, player);
        return best_value;
    }
    else{
        int player = 2;
        double best_value = INFINITY;
        
//        if (board.check_game_won(player)){
//            return -INFINITY;
//        }
        for (auto &i_move : move_list){
            Board node = board;
            node.make_move(i_move.row, i_move.col, player);
            valuation  = minimax(node, search_depth-1, true);
            if (valuation < best_value or best_row == -1){
                best_value = valuation;
                best_row = i_move.row;
                best_col = i_move.col;
            }
        }
        board.make_move(best_row, best_col, player);
        return best_value;
    }
}

double minimax_top_level(Board &board, int search_depth, bool maximizing_player, bool list_top_moves){
    chrono::steady_clock::time_point begin = chrono::steady_clock::now(); // Start timer
    bool NO_MORE_MOVES = false;
    double valuation;            // Store the valuation of node
    int best_row = -1;
    int best_col = -1;
    vector<Move> move_list = board.get_move_list(); // Get open moves
    Move_with_eval temp_move;                       // Move with its evaluation to be filled in vector on next line
    vector<Move_with_eval> top_moves;               // Store best moves (actually all on first level)

    if (move_list.size() == 0) {
        NO_MORE_MOVES = true;
    }
    
    // Recursive search of optimal play using minimax algorithm
    if (search_depth == 0 or NO_MORE_MOVES) {
        return board_evaluation(board);
    }
    if (maximizing_player){
        int player = 1;
        double best_value = -INFINITY;
//        if (board.check_game_won(player)){ // Quit search early if game over
//            return INFINITY;
//        }
        for (auto &i_move : move_list){ // move in move_list
            Board node = board;
            node.make_move(i_move.row, i_move.col, player);
            valuation  = minimax(node, search_depth-1, false);
            if (valuation > best_value or best_row == -1){
                best_value = valuation;
                best_row = i_move.row;
                best_col = i_move.col;
            }
            if (list_top_moves){
                temp_move.move = i_move;
                temp_move.eval = valuation;
                top_moves.push_back(temp_move);
            }
        }
        board.make_move(best_row, best_col, player);
        if (list_top_moves){
            print_top_moves(top_moves);
        }
        chrono::steady_clock::time_point end= std::chrono::steady_clock::now(); // Stop timer
        unsigned long time_in_ms = chrono::duration_cast<chrono::milliseconds>(end - begin).count();
        cout << "CPU made the move " << "(" << to_string(best_row) << "," << to_string(best_col) << "), " << "with score " << best_value << ". Time [ms]: " << time_in_ms << endl;
        return best_value;
    }
    else{
        int player = 2;
        double best_value = INFINITY;
//        if (board.check_game_won(player)){
//            return -INFINITY;
//        }
        for (auto &i_move : move_list){
            Board node = board;
            node.make_move(i_move.row, i_move.col, player);
            valuation  = minimax(node, search_depth-1, true);
            if (valuation < best_value or best_row == -1){
                best_value = valuation;
                best_row = i_move.row;
                best_col = i_move.col;
            }
            if (list_top_moves){
                temp_move.move = i_move;
                temp_move.eval = valuation;
                top_moves.push_back(temp_move);
            }
        }
        board.make_move(best_row, best_col, player);
        if (list_top_moves){
            print_top_moves(top_moves);
        }
        chrono::steady_clock::time_point end= std::chrono::steady_clock::now(); // Stop timer
        unsigned long time_in_ms = chrono::duration_cast<chrono::milliseconds>(end - begin).count();
        cout << "CPU made the move " << "(" << to_string(best_row) << "," << to_string(best_col) << "), " << "with score " << best_value << ". Time [ms]: " << time_in_ms << endl;
        return best_value;
    }
}

void get_cpu_move(Board &board, int &player, int &cpu_level, bool list_top_moves){
    vector<Move> move_list = board.get_move_list();
    int possible_moves = (int) move_list.size(); // Casts unsigned long to int (fine, since it is a small number)
    
    // Do the magic selection of CPU move based on its level (difficulty)
    if (cpu_level == 0){ // IF " or possible_moves+2 > MAX_TURNS" --> computer plays random first move
        uniform_int_distribution<int> distribution(0,possible_moves); // Includes endpoints, so (1,10) can give 1 and 10
        
        int random_move = distribution(generator);
        int move_r = move_list[random_move].row;
        int move_c = move_list[random_move].col;
        
        if (board.legal_move(move_r,move_c)){
            cout << "CPU (player " << to_string(player) << ") made the move " << "(" << to_string(move_r) << "," << to_string(move_c) << ") (RNG)" << endl;
            board.make_move(move_r, move_c, player);
        }
        else{
            // This should not be possible, but hey, give a warning anyway!
            cout << "ERROR: CPU MADE ILLEGAL MOVE.\nSolution: Fix source code!" << endl;
        }
    }
    else if (cpu_level > 0){
        // Do MINIMAX search with depth equal to cpu-level/strength/difficulty
        minimax_top_level(board, cpu_level, false, list_top_moves);
    }
}

int main(int argc, const char * argv[]) {
    int turns = 0;              // Counts the number of turns
    int player = 1;             // The players are always "1" or "2"
    bool play_vs_cpu = true;    // Choose whether player 2 should be cpu or human
    bool list_best_moves = true;// Choose whether to print top 5 moves for cpu
    int cpu_level = 4;          // Strength of cpu: Search depth. 0 means random moves...
                                // Strength of 4 is needed to stop "_XXX_" attacks.
    Board board;                // Create the game board
    
    if (MAX_TURNS > 99) {       // Quit if too big board
        cout << "Board too big, maximum 99 tiles!" << endl;
        return 0;
    }
    
    // Lets play 5-in-a-row! :D
    while (true){
        cout << "\nTurn " << to_string(turns) << ", PLAYER " << player << endl;
        if ((play_vs_cpu and player == 1) or not play_vs_cpu){
            board.print_board();                         // Show the board
        }
        
        if (play_vs_cpu and player == 2) {
//            cout << "CPU MAKING MOVE." << " Player = " << player << endl;
            get_cpu_move(board, player, cpu_level, list_best_moves);  // Get a new move from the cpu
        }
        else{
//            cout << "HMN MAKING MOVE." << " Player = " << player << endl;
            get_human_move(board, player);           // Get a new move from human
        }
        if (board.check_game_won(player)){           // Check if game over
            board.print_board();                     // Show the board
            cout << endl << "GAME WON BY PLAYER " << to_string(player) << endl;
            break;
        }
        
        player = (player)%2 + 1;                     // Next players turn
        turns++;
        if (turns == MAX_TURNS) {
            break;
        }
    };
    return 0;
}













