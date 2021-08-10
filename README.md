#### This repository contains assignment given by Prof. David Crandall during the Elements of Artificial Intelligence Spring 2021 class.
# Pikachu

## Introduction
Board consisting of a grid of n × n (with n ≥ 7) squares, 2n white stones, and 2n black stones:
- Each stone is also called a Pichu.
- Initially the board starts empty, except for two rows of white Pichus on the second and third row of
  the board, and two rows of black Pichus on rows n − 2 and n − 1.
- Two players alternate turns, with White going first.
- When a Pichu reaches the opposite side of the board then the Pichu is marked with an X and becomes a Pikachu.

Goal is to write a program that plays Pikachu well.

## Approach:

### Alogirithm used:

  We are using Minimax algorithm with aplha beta pruning to find the best move <br/>

        ```
          def minimax(board, N, is_max_player, player, depth):
        
         ```
    
  In that algorithm we are using the current board position and then finding all possible moves for the current board position. <br/>
  
  While calculating all possible moves, we are finding all valid pichu and pikachu moves. <br/>
  
  We are using following evaluation function to decide the best move in minimax algorithm: <br/>
    
    ```
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
        ```
   
 ### Points we discussed before implementing Pikachu
 
 1. What should be the evaluation function.
 
 2. Board size 1D or 2D.
 
 3. Possible moves.
 
 4. How to integrate minimax alpha beta pruning with our program