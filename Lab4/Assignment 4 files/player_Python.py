import socket
import numpy as np
import time
from multiprocessing.pool import ThreadPool
import os
import random
import math
import copy


class GameState():
    def __init__(self, player_turn, board):
        self.player = player_turn
        self.board = board
        self.bonus_move = False
        
    # Get all the possible moves
    def findValidMoves(self):
        # Get all possible moves for player 1
        if self.player == 1:
            return [i for i in range(6) if self.board[i] != 0]
        # Get other players possible moves
        else:
            return [i for i in range(7,13) if self.board[i] != 0]

    # Check if the game is over
    def isOver(self):
        over = True

        # Check if player1 still has stones
        for i in range(6):
            if self.board[i] != 0:
                over = False
                break

        # check if player2 still has stones
        if not over: 
            for i in range(7, 13):
                if self.board[i] != 0:
                    return False

            return True
        else:
            return True
    
    # Returns opposite buckets
    def getOpposite(self, x):
        if x == 0 or x == 12:
            return (12,0)
        elif x == 1 or x == 11:
            return (11,1)
        elif x == 2 or x == 10:
            return (10,2)
        elif x == 3 or x == 9:
            return (9,3)
        elif x == 4 or x == 8:
            return (8,4)
        elif x == 5 or x == 7:
            return (7,5)

    # Simulate a player move
    def makeMove(self, bucket):
        self.bonus_move = False

        if self.player == 1:

            # Empty the bucket
            stones = self.board[bucket]
            self.board[bucket] = 0
            change_player = True
            # Index where we start laying down stones
            index = bucket + 1

            while stones > 0:
                # This probably never triggers, but I put it here for safety
                if index == 14:
                    index = 0

                # Check if bonus turn or empty pit
                if stones == 1:
                    # Bonus turn
                    if index == 6:
                        self.player = 1
                        self.board[6] += 1
                        change_player = False
                        break
                    # Take opponents opposing bucket
                    if index in range(6) and self.board[index] == 0:
                        self.board[6] += 1
                        opposing = self.getOpposite(index)
                        self.board[6] += self.board[opposing[0]]
                        self.board[opposing[0]] = 0
                        break

                # We want to skip the opponents basket
                if index == 13:
                    index = 0
                else:
                    self.board[index] += 1
                    index += 1
                    stones -= 1
            if change_player:
                self.player = 2
        else:

            # Empty the bucket
            stones = self.board[bucket]
            self.board[bucket] = 0
            change_player = True
            # Index where we start laying down stones
            index = bucket + 1

            while stones > 0:
                # Check if bonus turn or empty pit
                if index == 14:
                    index = 0

                if stones == 1:
                    # Bonus turn
                    if index == 13:
                        self.board[13] += 1
                        self.player = 1
                        change_player = False
                        self.bonus_move = True
                        break
                    # Take opponents opposing bucket
                    if index in range(7,13) and self.board[index] == 0:
                        self.board[13] += 1
                        opposing = self.getOpposite(index)
                        self.board[13] += self.board[opposing[1]]
                        self.board[opposing[1]] = 0
                        break

                # We want to skip the opponents basket
                if index == 6:
                    index = 7
                else:
                    self.board[index] += 1
                    index += 1
                    stones -= 1
            if change_player:
                self.player = 2

    # Utility function
    def heuristic(self, state):
        score = 0
        '''
           Calculate the total amount of stones on player 2 side of the playing field.
           Multiply stones in the nest with 1.5, since that is valuable to us 
        '''
        player2stones = 0
        for i in range(7,13):
            player2stones += state.board[i]
        player2stones += state.board[13] * 1.5
        '''
            Check if we are on a bonus move, if so add a value to score
        '''
        if self.bonus_move:
            score += 1
        '''
            Return the score
        '''
        return player2stones+score      

# Called from 'main' to start the game
def getBestMove(state):

    valid_moves = state.findValidMoves()

    move_evals = []
    max_val = -math.inf
    best_move = None

    # For every possible move
    for move in valid_moves:
        new_state = copy.deepcopy(state)

        # Simulate move
        new_state.makeMove(move)
        
        # Call the minimax function
        val = minimax(new_state, 2, -math.inf, math.inf)

        # Get best move
        move_evals.append((move, val))
        if val > max_val:
            max_val = val
            best_move = move

    # Make sure that the move is between 1 and 6
    best_move = (best_move+1) % 7
    return best_move

# Minimax function
def minimax(state, depth, alpha, beta):
    
    # Check if game is over or we have reached max-depth
    if state.isOver() or depth == 0:
        return state.heuristic(state)
        
    # For the Maximizing player
    if state.player == 1:
        max_eval = -math.inf
        validMoves = state.findValidMoves()
        
        # For every valid move, simulate a new move, where do i simualate the move though
        for v in validMoves:
            new_board = copy.deepcopy(state)
            new_board.makeMove(v)

            # Alpha Beta pruning to speed up the process
            evaluate = minimax(new_board, depth-1, alpha, beta)
            maxEval = max(max_eval, evaluate)
            alpha = max(alpha, evaluate)

            if beta  <= alpha:
                break
        return maxEval
    # For the Minimun player
    else:
        min_eval = math.inf
        validMoves = state.findValidMoves()

        # For every valid move, simulate a new move, where do i simualate the move though
        for v in validMoves:
            new_board = copy.deepcopy(state)
            new_board.makeMove(v)

            # Alpha Beta pruning to speed up the process
            evaluate = minimax(new_board, depth-1, alpha, beta)
            minEval = min(min_eval, evaluate)
            beta = min(beta, evaluate)

            if beta <= alpha:
                break
            
        return minEval


def receive(socket):
    msg = ''.encode()  # type: str

    try:
        data = socket.recv(1024)  # type: object
        msg += data
    except:
        pass
    return msg.decode()

def send(socket, msg):
    socket.sendall(repr(msg).encode('utf-8'))

# VARIABLES
playerName = 'Madiiboy'
host = '127.0.0.1'
port = 30000  # Reserve a port for your service.
s = socket.socket()  # Create a socket object
pool = ThreadPool(processes=1)
gameEnd = False
MAX_RESPONSE_TIME = 5

print('The player: ' + playerName + ' starts!')
s.connect((host, port))
print('The player: ' + playerName + ' connected!')

while not gameEnd:

    asyncResult = pool.apply_async(receive, (s,))
    startTime = time.time()
    currentTime = 0
    received = 0
    data = []
    while received == 0 and currentTime < MAX_RESPONSE_TIME:
        if asyncResult.ready():
            data = asyncResult.get()
            received = 1
        currentTime = time.time() - startTime

    if received == 0:
        print('No response in ' + str(MAX_RESPONSE_TIME) + ' sec')
        gameEnd = 1

    if data == 'N':
        send(s, playerName)

    if data == 'E':
        gameEnd = 1

    if len(data) > 1:

        # Read the board and player turn
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        playerTurn = int(data[0])
        i = 0
        j = 1
        while i <= 13:
            board[i] = int(data[j]) * 10 + int(data[j + 1])
            i += 1
            j += 2

        # Create a new game state
        state = GameState(playerTurn, board)
        # Start process of selecting move
        move = getBestMove(state)

        send(s, move)
