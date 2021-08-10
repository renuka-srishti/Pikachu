# pikachu.py : Play the game of Pikachu
#
# Based on skeleton code by D. Crandall, March 2021
#
import sys
import time
import copy

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

class GameState:
    def __init__(self, board, player, N):
        self.board = self.convert_board_2dlist(board, N)
        self.N = N
        self.player = player
        self.player_inverse = {'w':['b', 'B'], 'b':['w','W'], 'W':['b', 'B'], 'B':['w','W']}
        self.opp_pawns = self.player_inverse[player]
        self.curr_pawns = self.player_inverse[self.opp_pawns[0]]
        
    
    def convert_board_2dlist(self, board, N):
        return [list(board[i:i + N]) for i in range(0, len(board), N)]
    
    
    def evaluation(self, board):
        val_white = 0
        val_black = 0
        for row_idx in range(self.N):
            for idx in range(self.N):
                if board[row_idx][idx] == '.':
                    continue
                elif board[row_idx][idx] == 'w':
                    val_white += 1 + (row_idx * 0.05)
                elif board[row_idx][idx] == 'W':
                    val_white += 1.75
                elif board[row_idx][idx] == 'b':
                    val_black += 1 + ((N-row_idx) * 0.05)
                elif board[row_idx][idx] == 'B':
                    val_black += 1.75
        if self.player == 'w':
            return val_white - val_black
        else:
            return val_black - val_white

    def find_valid_pikachu_moves(self, board, idx):
        moves = []
        
        #my logic for this is a bit convoluted
        
        #The order of IFs matter a lot (since short hand in python)
        
        #this no_jump flag says whether your pikachu has not jumped yet (True = pikachu has NOT jumped yet)
        no_jump = True
        
        #not too important to understand but its a flag for resetting and skip one iteration of i
        jumped_at = -1
        
        #Always use a copy cause board is going to be modified when jump occurs (pikachu can also move forward after the jump) 
        board_copy = copy.deepcopy(board)
        
        #MOVING DOWN
        for i in range(1,self.N):
            
            #Basically this if condition is True only when the iteration you jumped over an opponents pawn in which case you won;t be looking at the same position again
            if not no_jump and jumped_at>0:
                #resetting it because you can at max jump over one pawn only
                jumped_at = -1 
                continue
                
            #if the index we are looking at is in bounds and it is an empty space, we could more our pikachu there
            if idx[0] + i < N and board_copy[idx[0]+ i][idx[1]] == '.':
                new_board = copy.deepcopy(board_copy)
                new_board[idx[0]+ i][idx[1]], new_board[idx[0]][idx[1]] = new_board[idx[0]][idx[1]], new_board[idx[0]+ i][idx[1]]
                moves.append(new_board)
                
            #if the index we are looking at is in bounds and it has an opponents pawn and the index where you want to jump over also is in bounds and is empty we can jump over the opponents pawn
            elif idx[0] + i < N and no_jump and (board_copy[idx[0]+ i][idx[1]] in self.player_inverse[board_copy[idx[0]][idx[1]]]) and idx[0] + i + 1 < self.N and board_copy[idx[0]+ i + 1][idx[1]] == '.':
                new_board = copy.deepcopy(board_copy)
                new_board[idx[0]+ i + 1][idx[1]], new_board[idx[0]][idx[1]] = new_board[idx[0]][idx[1]], new_board[idx[0]+ i + 1][idx[1]]
                new_board[idx[0]+ i ][idx[1]] = '.'
                moves.append(new_board)
                #Setting this flag cause more jumps can not happen
                no_jump = False
                #setting this flag so that the next iteration of i can be skipped
                jumped_at = i 
                #removing the opponent's jumped pawn to find valid moves after that point
                board_copy[idx[0]+i][idx[1]] = '.'
                
            # if any of the above conditions go out of bounds, just break/ happens mostly cause of out of bounds check
            else:
                break
        
        
        #Similarly for MOVEMENT UPWARDS
        no_jump = True
        jumped_at = -1
        board_copy = copy.deepcopy(board)
        for i in range(1,self.N):
            if not no_jump and jumped_at>0:
                jumped_at = -1 
                continue
                
            if idx[0] - i >= 0 and board_copy[idx[0]- i][idx[1]] == '.':
                new_board = copy.deepcopy(board_copy)
                new_board[idx[0]- i][idx[1]], new_board[idx[0]][idx[1]] = new_board[idx[0]][idx[1]], new_board[idx[0]- i][idx[1]]
                moves.append(new_board)
            elif idx[0] - i >= 0 and no_jump and board_copy[idx[0]- i][idx[1]] in self.player_inverse[board_copy[idx[0]][idx[1]]] and idx[0] - i - 1 >=0 and board_copy[idx[0]- i - 1][idx[1]] == '.':
                new_board = copy.deepcopy(board_copy)
                new_board[idx[0]- i - 1][idx[1]], new_board[idx[0]][idx[1]] = new_board[idx[0]][idx[1]], new_board[idx[0] - i - 1][idx[1]]
                new_board[idx[0]- i ][idx[1]] = '.'
                moves.append(new_board)
                no_jump = False
                jumped_at = i 
                board_copy[idx[0] - i][idx[1]] = '.'
            else:
                break
                        
            
        #MOVING RIGHT
        no_jump = True
        jumped_at = -1
        board_copy = copy.deepcopy(board)
        for i in range(1,self.N):
            if not no_jump and jumped_at>0:
                jumped_at = -1 
                continue
                
            if idx[1] + i < self.N and board[idx[0]][idx[1]+ i] == '.':
                new_board = copy.deepcopy(board_copy)
                new_board[idx[0]][idx[1]+ i], new_board[idx[0]][idx[1]] = new_board[idx[0]][idx[1]], new_board[idx[0]][idx[1]+ i]
                moves.append(new_board)
            elif idx[1] + i < self.N and no_jump and board[idx[0]][idx[1]+ i] in self.player_inverse[board_copy[idx[0]][idx[1]]] and idx[1] + i + 1 < self.N and board_copy[idx[0]][idx[1]+ i + 1] == '.':
                new_board = copy.deepcopy(board_copy)
                new_board[idx[0]][idx[1]+ i + 1], new_board[idx[0]][idx[1]] = new_board[idx[0]][idx[1]], new_board[idx[0]][idx[1]+ i + 1]
                new_board[idx[0]][idx[1]+ i] = '.'
                moves.append(new_board)
                no_jump = False
                jumped_at = i 
                board_copy[idx[0]][idx[1]+ i] = '.'
            else:
                break
                   
            
        #MOVING LEFT
        no_jump = True
        jumped_at = -1
        board_copy = copy.deepcopy(board)
        for i in range(1,N):
            if not no_jump and jumped_at>0:
                jumped_at = -1 
                continue
                
            if idx[1] - i >= 0 and board[idx[0]][idx[1] - i] == '.':
                new_board = copy.deepcopy(board_copy)
                new_board[idx[0]][idx[1] - i], new_board[idx[0]][idx[1]] = new_board[idx[0]][idx[1]], new_board[idx[0]][idx[1] - i]
                moves.append(new_board)
            elif idx[1] - i >= 0 and no_jump and board[idx[0]][idx[1] - i] in self.player_inverse[board_copy[idx[0]][idx[1]]] and idx[1] - i - 1 >= 0 and board_copy[idx[0]][idx[1] - i - 1] == '.':
                new_board = copy.deepcopy(board_copy)
                new_board[idx[0]][idx[1] - i - 1], new_board[idx[0]][idx[1]] = new_board[idx[0]][idx[1]], new_board[idx[0]][idx[1] - i - 1]
                new_board[idx[0]][idx[1] - i] = '.'
                moves.append(new_board)
                no_jump = False
                jumped_at = i 
                board_copy[idx[0]][idx[1] - i] = '.'
            else:
                break
                        
        return moves

    def game_over(self):
        '''
        Parameters
        ----------
        board : str
            contains the current board state.
        player : str/char
            current player.
    
        Returns
        -------
        Tuple of 2 Boolean 
            First value tells if the game is over.
            Second Value tells if you have won.
    
        '''
        seen_curr_player = False
        seen_opp_player = False
        for row in self.board: 
            for pawn in row:
                if pawn == '.':
                    continue
                elif pawn in self.curr_pawns: 
                    seen_curr_player = True
                elif pawn in self.opp_pawns:
                    seen_opp_player = True
                if seen_curr_player and seen_opp_player:
                    return (False, seen_curr_player)
        
        return (True, seen_curr_player)


    def get_board_positions(self, board, player):
        
        curr_pichu, curr_pikachu, opp_pichu, opp_pikachu = [], [], [], [] 
        opp_pawns = self.player_inverse[player]
        curr_pawns = self.player_inverse[opp_pawns[0]]
        for row_num, row in enumerate(board):    
            for idx, pos in enumerate(row):
                if pos == opp_pawns[0]:
                    opp_pichu.append((row_num,idx))
                elif pos == opp_pawns[1]:
                    opp_pikachu.append((row_num,idx))
                elif pos == curr_pawns[0]:
                    curr_pichu.append((row_num,idx))
                elif pos == curr_pawns[1]:
                    curr_pikachu.append((row_num,idx))
                    
        return curr_pichu, curr_pikachu, opp_pichu, opp_pikachu
    



    
    def find_valid_pichu_moves(self, board, idx):
        
        moves= []
        
        #common 2 degrees movement (left and right)
        neighbors = [(idx[0],idx[1]-1),(idx[0],idx[1]+1)]
        neighbors_j = [ ((idx[0],idx[1]-1),(idx[0],idx[1]-2)), ((idx[0],idx[1]+1),(idx[0],idx[1]+2))]
        
        #if it's a white piece it can also move down so append it to list of possible moves
        if board[idx[0]][idx[1]] == 'w':
            neighbors.append((idx[0]+1,idx[1]))
            neighbors_j.append(((idx[0]+1,idx[1]),(idx[0]+2,idx[1])))
        
        elif board[idx[0]][idx[1]] == 'b':
            neighbors = [(idx[0],idx[1]-1),(idx[0]-1,idx[1]),(idx[0],idx[1]+1)]
            neighbors_j.append(((idx[0]-1,idx[1]),(idx[0]-2,idx[1])))
        
        #keep the list of neighbors that are only in array bounds
        neighbors = [neighbor for neighbor in neighbors if neighbor[0]>=0 and neighbor[0]<self.N and neighbor[1]>=0 and neighbor[1]<self.N]
        neighbors_j = [(j,neighbor) for j,neighbor in neighbors_j if neighbor[0]>=0 and neighbor[0]<self.N and neighbor[1]>=0 and neighbor[1]<self.N]
        #print(neighbors_j)
        
        #check if adjacent moves are possible 
        for neighbor in neighbors:
            
            #if the neighboring cell is empty the pichu can move there
            if board[neighbor[0]][neighbor[1]] == '.':
                #ALWAYS USE DEEPCOPY SINCE LIST OF LISTS 
                new_board = copy.deepcopy(board)
                #swap positions between the empty space and pichu
                new_board[neighbor[0]][neighbor[1]], new_board[idx[0]][idx[1]] = new_board[idx[0]][idx[1]], new_board[neighbor[0]][neighbor[1]] 
                #append the board to the list of moves
                if neighbor[0] == self.N - 1:
                    new_board[neighbor[0]][neighbor[1]] = 'W' if new_board[neighbor[0]][neighbor[1]] == 'w' else 'B'
                moves.append(new_board)
        
        #j holds the index of the opponent pawn that is jumped over
        for j,neighbor in neighbors_j:
            #neighbor holds the idx of the cell that is 2 units away (the position which you land after you jump)
            if board[neighbor[0]][neighbor[1]] == '.' and board[j[0]][j[1]] != '.' and board[j[0]][j[1]] in self.player_inverse[board[idx[0]][idx[1]]]:  
                new_board = copy.deepcopy(board)
                new_board[neighbor[0]][neighbor[1]], new_board[idx[0]][idx[1]] = new_board[idx[0]][idx[1]], new_board[neighbor[0]][neighbor[1]] 
                #assign the jumped position to empty
                new_board[j[0]][j[1]] = '.'
                if neighbor[0] == self.N - 1:
                    new_board[neighbor[0]][neighbor[1]] = 'W' if new_board[neighbor[0]][neighbor[1]] == 'w' else 'B'
                moves.append(new_board)
        
        return moves


    #will get all possible moves
    def possible_moves(self, board, curr_pichu, curr_pikachu):
        
        
        moves = []
        
        #for each pichu index of the current player's generate and add it to our current moveset
        for pichu in curr_pichu:
            #print(pichu)
            moves += self.find_valid_pichu_moves(board, pichu)
            
        #similarly for each pikachu belonging to the current player, generate the set of valid moves
        for pikachu in curr_pikachu:
            #print(pikachu)
            moves += self.find_valid_pikachu_moves(board, pikachu)

        return moves
    
    def minimax(self, board, is_max_player, player, depth, alpha, beta):
    
        curr_pichu, curr_pikachu, opp_pichu, opp_pikachu = self.get_board_positions(board, player)
        # Check if its in the leaf node
        if depth == 0:
            return board, self.evaluation(board)
    
        # If passed player is max player
        if is_max_player:
    
            max_val = float('-inf')
            best_move = None
    
            # get list of valid moves
            
            # generate a list of all possible moves for the current board positions
            pos_moves = self.possible_moves(board, curr_pichu, curr_pikachu)
    
            for move in pos_moves:
                eval_val = self.minimax(move, False, 'b' if player=='w' else 'w', depth - 1, alpha, beta)
                max_val = max(max_val, eval_val[1])
                alpha = max(max_val, alpha)
                if max_val == eval_val[1]:
                    best_move = move

                if beta <= alpha:
                    break
    
            return best_move, max_val

        else:
            min_val = float('inf')
            best_move = None
    
            # get list of valid moves
            #curr_pichu, curr_pikachu, opp_pichu, opp_pikachu = get_board_positions(board, player)
            # generate a list of all possible moves for the current board positions
            pos_moves = self.possible_moves(board, curr_pichu, curr_pikachu)
    
            for move in pos_moves:
                eval_val = self.minimax(move, True, 'b' if player=='w' else 'w', depth - 1, alpha, beta)
                min_val = min(min_val, eval_val[1])
                beta = min(min_val, beta)
                if min_val == eval_val[1]:
                    best_move = move

                if beta <= alpha:
                    break
    
            return best_move, min_val
 
    
 
#print 2d list in a understandable manner
def prprint(board):
    print("\n".join(["".join(row) for row in board]))
    

#format output
def format_output(board):
    return "".join(["".join(row) for row in board])

 
def find_best_move(board, N, player, timelimit):
    game =  GameState(board, player, N)
    depth = 1
    while True:
        yield format_output(game.minimax(game.board, True, game.player, depth, float('-inf'), float('inf'))[0])
        depth += 1

if __name__ == "__main__":
    if len(sys.argv) != 5:
        #print(len(sys.argv))
        raise Exception("Usage: pikachu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
