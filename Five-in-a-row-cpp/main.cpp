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
#include <algorithm>
#include <map>
#include <omp.h>

using namespace std;

struct Move {
    // This will be a single move on the board
    int row;
    int col;
};

const int BOARD_ROWS        = 7;
const int BOARD_COLS        = 12;
const int MAX_TURNS         = BOARD_ROWS * BOARD_COLS;
const int SET_THREAD_COUNT  = 64;      // Number of OpenMP threads to spawn
const int STARTING_PLAYER   = 1;       // Starting player. The players are always "1" or "2"
const bool LIST_BEST_MOVES  = true;    // Choose whether to print top 5 moves for cpu
const bool LIST_ALL_MOVES   = false;   // ...or print ALL possible moves
const bool AB_PRUNING       = true;    // Choose whether to use alpha-beta-pruning
Move LAST_MOVE;                        // To highlight last move

unsigned SEED = chrono::system_clock::now().time_since_epoch().count();
default_random_engine generator(SEED);

class Board{
public:
    Board();
    char arr_board[BOARD_ROWS][BOARD_COLS];
    vector<Move> get_move_list();
    int moves_left;
    void print_board();
    void make_move(int, int, char &);
    bool legal_move(int, int);
    bool check_game_won(char);
    // string id_for_hash;

private:
    string board_row;
};

Board::Board(){
    // Class constructor
    // Set board to only zeros
    // id_for_hash = "";
    moves_left = MAX_TURNS;
    for (int i = 0; i<BOARD_ROWS; ++i){
        for (int j = 0; j<BOARD_COLS; ++j){
            arr_board[i][j] = '_';
        }
    }
};

vector<Move> Board::get_move_list(){
    Move single_move;
    vector<Move> move_list;
    move_list.reserve(moves_left); // Make room for all pos. moves --> no realloc. of memory later
    // move_list.reserve(MAX_TURNS);
    for (int i = 0; i<BOARD_ROWS; ++i){
        for (int j = 0; j<BOARD_COLS; ++j){
            if (arr_board[i][j] == '_'){
                single_move.row = i;
                single_move.col = j;
                move_list.push_back(single_move);
            }
        }
    }
    return move_list;
}

void Board::print_board(){
    // Extra spacing based on number of rows/cols
    string extra_row_space = "";
    if (BOARD_ROWS > 10){
        extra_row_space = " ";
    }
    // Prints out current board state
    string symbol_to_print = extra_row_space + "  ";
    char player_symbol;
    for (int i=0; i<BOARD_COLS; ++i){
        if (i < 9){
            symbol_to_print += to_string(i) + " ";
        }
        else if (i==9){
            symbol_to_print += to_string(i);
        }
        else if (i%2 == 0){ // Print even numbers white on black
            symbol_to_print += "\033[7;30m" + to_string(i) + "\033[0m";
        }
        else{               // Print odd numbers black on white
            symbol_to_print += to_string(i);
        }
    }
    cout << endl << symbol_to_print << endl;
    cout << " " + extra_row_space + string(BOARD_COLS*2+1, '-') << endl;
    for (int i = 0; i<BOARD_ROWS; ++i){
        if (i < 10){
            board_row = extra_row_space + to_string(i) + "|";
        }
        else{
            board_row = to_string(i) + "|";
        }
        for (int j = 0; j<BOARD_COLS; ++j){
            player_symbol = arr_board[i][j];
            if (player_symbol == '_'){
                symbol_to_print = " ";
            }
            else if (player_symbol == 'X'){
                if (i == LAST_MOVE.row and j == LAST_MOVE.col){
                    symbol_to_print = "\033[7;34mX\033[0m"; // Bold, blue color (inverted background)
                }
                else{
                    symbol_to_print = "\033[1;34mX\033[0m"; // Bold, blue color
                }
            }
            else{
                if (i == LAST_MOVE.row and j == LAST_MOVE.col){
                    symbol_to_print = "\033[7;31mO\033[0m"; // Bold, red color (inverted background)
                }
                else{
                    symbol_to_print = "\033[1;31mO\033[0m"; // Bold, red color
                }
            }
            board_row += symbol_to_print + "|";
        }
        cout << board_row << endl;
        cout << extra_row_space + " " + string(BOARD_COLS*2+1, '-') << endl;
    }
}

void Board::make_move(int r, int c, char &player){
    // Modifies the board. Will overwrite, so legal_move should be checked first.
    arr_board[r][c] = player;
    --moves_left; // Update how many moves left
}

bool Board::legal_move(int move_r, int move_c){
    // Check if a move is valid.
    if (arr_board[move_r][move_c] == '_'){
        return true;
    }
    else{
        return false;
    }
}

bool Board::check_game_won(char player){
    auto &b = arr_board; // Reference to board array
    char &p = player;

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

void get_human_move(Board &board, char &player){
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
                break;
            }
        }
        if (board.legal_move(move_r, move_c)){
            cout << "Player " << player << " made the move " << "(" << move_r << "," << move_c << ")" << endl;
            board.make_move(move_r, move_c, player);
            LAST_MOVE.row = move_r;
            LAST_MOVE.col = move_c;
            break;
        }
    }
}

void weight_function(char &a, char &b, char &c, char &d, char &e, float &valuation, int &search_depth){
    /* Weight function is written out to avoid computing the power function.
       Formula for valuation is:
       valuation += pow(10, (fiver_sum-1)), for fiver_sum > 0            */
    int fiver_sum = 0;
    if (a != '_'){ // chars a-e are only of one type (X or O), but can be also be "open"
      fiver_sum += 1;
    }
    if (b != '_'){
      fiver_sum += 1;
    }
    if (c != '_'){
      fiver_sum += 1;
    }
    if (d != '_'){
      fiver_sum += 1;
    }
    if (e != '_'){
      fiver_sum += 1;
    }
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
       else{ // Game is won! Prefer quick wins over slower!
           float quick_maffs = (1+search_depth);
           valuation += 10000*quick_maffs*quick_maffs;
       }
    }
}

float board_evaluation(Board &board, int &search_depth){
    /* Evaluates the board position for player 1 i.e.
       positive score = good for player 1
       negative score = good for player 2 */
    float valuation = 0;
    auto &b = board.arr_board; // Reference to board array
    char p_char[2] = {'X','O'};

    for (int p = 1; p < 3; ++p){ // p = player
        /* First sum up value for p1, then make negative for sum for p2. Then after p2 sum is
           done, swap sign again (done at return statement)*/
        valuation *= -1.0;
        char np_c = p_char[p%2]; // Opposite player ID from int --> char

        // Check all 2,3 and 4 possibilities (except bottom right corner)
        for (int i=0; i<BOARD_ROWS; ++i){
            for (int j=0; j<BOARD_COLS; ++j){
                // Give value to open 5-ers based on how many player-only spots are taken. Open = taken by player or no player at all.
                if (i < BOARD_ROWS-4 and j < BOARD_COLS-4){
                    if (np_c != b[i][j] and np_c != b[i][j+1] and np_c != b[i][j+2] and np_c != b[i][j+3] and np_c != b[i][j+4]){
                        weight_function(b[i][j], b[i][j+1], b[i][j+2], b[i][j+3], b[i][j+4], valuation, search_depth);
                    }
                    if (np_c != b[i][j] and np_c != b[i+1][j] and np_c != b[i+2][j] and np_c != b[i+3][j] and np_c != b[i+4][j]){
                        weight_function(b[i][j], b[i+1][j], b[i+2][j], b[i+3][j], b[i+4][j], valuation, search_depth);
                    }
                    if (np_c != b[i][j] and np_c != b[i+1][j+1] and np_c != b[i+2][j+2] and np_c != b[i+3][j+3] and np_c != b[i+4][j+4]){
                        weight_function(b[i][j], b[i+1][j+1], b[i+2][j+2], b[i+3][j+3], b[i+4][j+4], valuation, search_depth);
                    }
                    if (np_c != b[i+4][j] and np_c != b[i+3][j+1] and np_c != b[i+2][j+2] and np_c != b[i+1][j+3] and np_c != b[i][j+4]){
                        weight_function(b[i+4][j], b[i+3][j+1], b[i+2][j+2], b[i+1][j+3], b[i][j+4], valuation, search_depth);
                    }
                } // Check bottom right corner/square...
                if (i >= BOARD_ROWS-4 and j < BOARD_COLS-4){
                    if (np_c != b[i][j] and np_c != b[i][j+1] and np_c != b[i][j+2] and np_c != b[i][j+3] and np_c != b[i][j+4]){
                        weight_function(b[i][j], b[i][j+1], b[i][j+2], b[i][j+3], b[i][j+4], valuation, search_depth);
                    }
                }
                if (i < BOARD_ROWS-4 and j >= BOARD_COLS-4){
                    if (np_c != b[i][j] and np_c != b[i+1][j] and np_c != b[i+2][j] and np_c != b[i+3][j] and np_c != b[i+4][j]){
                        weight_function(b[i][j], b[i+1][j], b[i+2][j], b[i+3][j], b[i+4][j], valuation, search_depth);
                    }
                }
            }
        }

    }
    /* Return negative of board score (score is always added to total,
       so for opposing player we first swap sign --> therefore we return negative to undo this.) */
    if (valuation == 0){ // Dont print out negative zero (-0)
      return 0.0;
    }
    else{
      return -valuation;
    }
}

struct Move_with_eval{
    Move move;
    float eval;
};

struct by_eval_min{
    bool operator()(Move_with_eval const &a, Move_with_eval const &b){
        return a.eval < b.eval;
    }
};

struct by_eval_max{
    bool operator()(Move_with_eval const &a, Move_with_eval const &b){
        return a.eval > b.eval;
    }
};

void print_top_moves(bool maximizing, vector<Move_with_eval> top_moves){
    // Sort moves by their evaluation, then print top 5 (and worst for fun)
    if (maximizing){
      sort(top_moves.begin(), top_moves.end(), by_eval_max());
    }
    else{
      sort(top_moves.begin(), top_moves.end(), by_eval_min());
    }

    cout << "Best cpu-moves (from best to worst):" << endl;
    unsigned int stop = 0;
    string print_nmbr = "";
    for (auto &i_move_eval : top_moves){
        ++stop;
        if (stop > 5 and stop != top_moves.size()){
          if (not LIST_ALL_MOVES){
            continue; // Skip 6th --> penultimate
          }
        }
        if (stop < 10){ // Format this bad boi for pretty print
            print_nmbr = "  " + to_string(stop);
        }
        else if (stop < 100){
            print_nmbr = " " + to_string(stop);
        }
        else{
            print_nmbr = to_string(stop);
        }
        cout << " -" << print_nmbr << ": (" << i_move_eval.move.row << "," << i_move_eval.move.col << "). Score: " << i_move_eval.eval << endl;
    }
}

float minimax(Board &board, int search_depth, bool maximizing_player, float alpha, float beta){//, map<string,float> &hash_table){
    // Minimax algorithm with option of alpha-beta-pruning
    bool no_more_moves = false;
    float valuation;
    int best_row = -1;
    int best_col = -1;
    vector<Move> move_list = board.get_move_list();

    if (move_list.size() == 0) {
        no_more_moves = true;
    }

    // Recursive search of optimal play using minimax algorithm
    if (search_depth == 0 or no_more_moves) {
      return board_evaluation(board, search_depth);
    }

    // Check if game over (then dont search tree any further)
    if (board.check_game_won('X') or board.check_game_won('O')){
      return board_evaluation(board, search_depth);
    }

    if (maximizing_player){
        char player = 'X';
        float best_value = -INFINITY;

        for (auto &i_move : move_list){ // move in move_list
            Board node = board;
            node.make_move(i_move.row, i_move.col, player);
            valuation  = minimax(node, search_depth-1, false, alpha, beta);//, hash_table);
            if (valuation >= best_value or best_row == -1){ // The ">=" with multiple threads causes randomization of equally good moves dep. on what thread finishes search last
                best_value = valuation;
                alpha      = valuation;
                best_row   = i_move.row;
                best_col   = i_move.col;
            }
            if (AB_PRUNING and (best_value >= beta)){
                break; // Prune away!!
            }
        }
        board.make_move(best_row, best_col, player);
        return best_value;
    }
    else{
        char player = 'O';
        float best_value = INFINITY;

        for (auto &i_move : move_list){
            Board node = board;
            node.make_move(i_move.row, i_move.col, player);
            valuation  = minimax(node, search_depth-1, true, alpha, beta);//, hash_table);
            if (valuation <= best_value or best_row == -1){
                best_value = valuation;
                beta       = valuation;
                best_row   = i_move.row;
                best_col   = i_move.col;
            }
            if (AB_PRUNING and (best_value <= alpha)){
                break;
            }
        }
        board.make_move(best_row, best_col, player);
        return best_value;
    }
}

float minimax_top_level(Board &board, int search_depth, bool maximizing_player){
    chrono::steady_clock::time_point begin = chrono::steady_clock::now(); // Start timer

    int best_row = -1;
    int best_col = -1;
    vector<Move> move_list = board.get_move_list(); // Get all possible moves
    Move_with_eval temp_move;                       // Move with its evaluation to be filled in vector on next line
    vector<Move_with_eval> top_moves;               // Store best moves (actually all on first level)

    if (maximizing_player){
        char player = 'X';
        float best_value = -INFINITY;

        omp_lock_t writelock; // Create a lock for memory access
        omp_init_lock(&writelock);
        #pragma omp parallel for num_threads(SET_THREAD_COUNT)
        for (unsigned int i = 0; i < move_list.size(); ++i){
            float valuation;
            auto i_move = move_list[i];
            float alpha = -INFINITY;    // Best already explored option along path to the root for maximizer
            float beta  =  INFINITY;    // Best already explored option along path to the root for minimizer
            Board node  = board;
            node.make_move(i_move.row, i_move.col, player);
            valuation   = minimax(node, search_depth-1, false, alpha, beta);//, hash_table);

            omp_set_lock(&writelock);   // Lock access for more than 1 thread at the time
            // cout << "Thread number: " << omp_get_thread_num() << " finished eval. Move (" << i_move.row << "," << i_move.col << "),  Score: " << valuation << endl;
            if (valuation > best_value or best_row == -1){
                best_value = valuation;
                best_row   = i_move.row;
                best_col   = i_move.col;
            }
            if (LIST_BEST_MOVES){
                temp_move.move = i_move;
                temp_move.eval = valuation;
                top_moves.push_back(temp_move);
            }
            omp_unset_lock(&writelock);
        }
        omp_destroy_lock(&writelock);
        board.make_move(best_row, best_col, player);
        LAST_MOVE.row = best_row;
        LAST_MOVE.col = best_col;
        if (LIST_BEST_MOVES){
            print_top_moves(maximizing_player, top_moves);
        }
        chrono::steady_clock::time_point end = chrono::steady_clock::now(); // Stop timer
        unsigned long time_in_ms = chrono::duration_cast<chrono::milliseconds>(end - begin).count();
        cout << "CPU (" << player << ") made the move " << "(" << best_row << "," << best_col << "), " << "with score " << best_value << ". Time [ms]: " << time_in_ms << endl;
        return best_value;
    }
    else{
        char player = 'O';
        float best_value = INFINITY;

        omp_lock_t writelock; // Create a lock for memory access
        omp_init_lock(&writelock);
        #pragma omp parallel for num_threads(SET_THREAD_COUNT)
        for (unsigned int i = 0; i < move_list.size(); ++i){
            float valuation;
            auto i_move = move_list[i];
            float alpha = -INFINITY;
            float beta  =  INFINITY;
            Board node = board;
            node.make_move(i_move.row, i_move.col, player);
            valuation  = minimax(node, search_depth-1, true, alpha, beta);//, hash_table);

            omp_set_lock(&writelock); // Lock access for more than 1 thread at the time
            // cout << "Thread number: " << omp_get_thread_num() << " finished eval. Move (" << i_move.row << "," << i_move.col << "),  Score: " << valuation << endl;
            if (valuation < best_value or best_row == -1){
                best_value = valuation;
                best_row   = i_move.row;
                best_col   = i_move.col;
            }
            if (LIST_BEST_MOVES){
                temp_move.move = i_move;
                temp_move.eval = valuation;
                top_moves.push_back(temp_move);
            }
            omp_unset_lock(&writelock);
        }
        omp_destroy_lock(&writelock);
        board.make_move(best_row, best_col, player);
        LAST_MOVE.row = best_row;
        LAST_MOVE.col = best_col;
        if (LIST_BEST_MOVES){
            print_top_moves(maximizing_player, top_moves);
        }
        chrono::steady_clock::time_point end = chrono::steady_clock::now(); // Stop timer
        unsigned long time_in_ms = chrono::duration_cast<chrono::milliseconds>(end - begin).count();
        cout << "CPU (" << player << ") made the move " << "(" << best_row << "," << best_col << "), " << "with score " << best_value << ". Time [ms]: " << time_in_ms << endl;
        return best_value;
    }
}

void get_cpu_move(Board &board, char &player, int &cpu_level){
    // Do the magic selection of CPU move based on its level (difficulty)
    if (cpu_level == 0){
        vector<Move> move_list = board.get_move_list();
        unsigned int possible_moves = move_list.size();
        uniform_int_distribution<int> distribution(0, possible_moves); // Includes endpoints, so (1,10) can give 1 and 10

        int random_move = distribution(generator);
        int move_r = move_list[random_move].row;
        int move_c = move_list[random_move].col;

        if (board.legal_move(move_r,move_c)){
            cout << "CPU (player " << player << ") made the move " << "(" << move_r << "," << move_c << ") (RNG)" << endl;
            board.make_move(move_r, move_c, player);
        }
        else{
            // This should not be possible, but hey, give a warning anyway!
            cout << "ERROR: CPU MADE ILLEGAL MOVE.\nSolution: Fix source code!" << endl;
        }
    }
    else if (cpu_level > 0){
        // Do MINIMAX search with depth equal to cpu-level/strength/difficulty
        if (player == 'X'){ // Eval function gives score FOR player 1
          minimax_top_level(board, cpu_level, true);
        }
        else{
          minimax_top_level(board, cpu_level, false);
        }
    }
}

int main(int argc, const char * argv[]) {
    cout << "\033[1;31m--------------------\033[0m" << endl;
    cout << "\033[1;31m  GAME: 5-IN-A-ROW  \033[0m" << endl;
    cout << "\033[1;31m--------------------\033[0m" << endl;

    /* Parameters and other choices */
    int turns  = 0;              // Counts the number of turns
    char p_char[2] = {'X','O'};  // Player ID, int --> char, which is used internally
    bool p1_is_cpu = true;       // Choose whether player 2 should be cpu or human
    bool p2_is_cpu = true;      // Choose whether player 2 should be cpu or human
    int cpu1_level = 4;          // Strength of cpu: Search depth. 0 means random moves...
    int cpu2_level = 4;          // If cpu VS cpu, individual level can be set.
    bool setup_position = false; // Set up a position before game starts

    int player = STARTING_PLAYER;
    char p_c   = p_char[player-1];
    Board board;                 // Create the game board

    if (MAX_TURNS > 999) {       // Quit if too big board
        cout << "Board too big, maximum 999 tiles!" << endl;
        return 0;
    }

    /* Set up position: */
    if (setup_position){
      vector<int> start_pos_row = {5,6,7,4,6,4,9,8,5,4}; // Some moves (should be valid..)
      vector<int> start_pos_col = {4,4,6,5,5,3,8,7,6,4};

      for (unsigned int i=0; i<start_pos_row.size(); ++i){
        board.make_move(start_pos_row[i], start_pos_col[i], p_c);

        if (board.check_game_won(p_c)){  // Check if game over
            cout << endl << "GAME WON BY PLAYER " << player << endl;
            break;
        }
        player = player%2 + 1; // Next players turn
        p_c    = p_char[player-1];
        turns++;
      }
  }

    // Lets play 5-in-a-row! :D
    board.print_board(); // Show the board
    while (true){
        cout << "\nTurn " << to_string(turns) << ", PLAYER " << player << " (" << p_c << ")" << endl;

        if (player == 1){
          if (p1_is_cpu){
            // Get a new move from the cpu
            get_cpu_move(board, p_c, cpu1_level);
          }
          else{
            // Get a new move from human
            get_human_move(board, p_c);
          }
        }
        else{
          if (p2_is_cpu){
            get_cpu_move(board, p_c, cpu2_level);
          }
          else{
            get_human_move(board, p_c);
          }
        }

        // Show the board with the new move:
        board.print_board();

        // Check if game over
        if (board.check_game_won(p_c)){
            cout << endl << "GAME WON BY PLAYER " << player << endl;
            break;
        }

        // Next players turn
        player = (player)%2 + 1;
        p_c    = p_char[player-1];
        turns++;
        if (turns == MAX_TURNS) {
            break;
        }
    };
    return 0;
}

/*
Compile command:
g++-7 -std=gnu++14 -fopenmp -O3 -Wall -o main_char.o main_char_arr.cpp
*/
