#!/usr/bin/python           # This is server.py file

import socket  # Import socket module
import numpy as np
import time
from multiprocessing.pool import ThreadPool
import os
import random
import math
import copy

# TODO:
    # Se över hur spelaren ändras, så borde koden funka sen
    # Kanske döpa om till next_player eller något för att tydligare se vem som spelar nästa runda
    # Fixa move som är helt jävla broken

class GameState():
    def __init__(self, player_turn, board):
        # print(board)
        self.player = player_turn
        self.board = board
        
    # Get all the possible moves
    def findValidMoves(self):
        # print(self.player)
        #Hmm, ska denna vara jag?
        if self.player == 1:
            return [i for i in range(6) if self.board[i] != 0]
        #get other players possible moves
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

    def makeMove(self, bucket):
        '''
            Takes bucket as input
            Simulate move for that bucket
        '''
        # print(self.board)

        # Range 6
        if self.player == 1:

            #Empty the bucket
            stones = self.board[bucket]
            self.board[bucket] = 0
            change_player = True
            #Index where we start laying down stones
            index = bucket + 1

            while stones > 0:

                # This probably never triggers, but I put it here for safety
                if index == 14:
                    index = 0

                # check if bonus turn or empty pit
                if stones == 1:
                    #Bonus turn
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

            #Empty the bucket
            stones = self.board[bucket]
            self.board[bucket] = 0
            change_player = True
            #Index where we start laying down stones
            index = bucket + 1

            while stones > 0:
                # check if bonus turn or empty pit
                if index == 14:
                    index = 0

                if stones == 1:
                    #Bonus turn
                    if index == 13:
                        self.board[13] += 1
                        self.player = 1
                        change_player = False
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

        # print(self.board)
        

# Called from 'main' to start the game
def getBestMove(state):

    # print(state.player)
    valid_moves = state.findValidMoves()
    # print(valid_moves)
    # print(possible_moves)
    move_evals = []
    max_val = -math.inf
    best_move = None
    for move in valid_moves:
        new_state = copy.deepcopy(state)
        new_state.makeMove(move)
        # print(new_state.board)
        val = minimax(new_state, 2, -math.inf, math.inf)

        move_evals.append((move, val))
        if val > max_val:
            max_val = val
            best_move = move

    
    best_move = (best_move+1) % 7
    # print(best_move)
    return best_move



def minimax(state, depth, alpha, beta):
    # print(player)

    if state.isOver() or depth == 0:
        return heuristic(state)
        
    #maximizing player
    if state.player == 1:
        max_eval = -math.inf
        validMoves = state.findValidMoves()
        
        # For every valid move, simulate a new move, where do i simualate the move though
        for v in validMoves:
            new_board = copy.deepcopy(state)
            new_board.makeMove(v)

            evaluate = minimax(new_board, depth-1, alpha, beta)
            maxEval = max(max_eval, evaluate)
            alpha = max(alpha, evaluate)

            if beta  <= alpha:
                break
        return maxEval
    else:
        min_eval = math.inf
        validMoves = state.findValidMoves()

        # For every valid move, simulate a new move, where do i simualate the move though
        for v in validMoves:
            new_board = copy.deepcopy(state)
            new_board.makeMove(v)

            evaluate = minimax(new_board, depth-1, alpha, beta)
            minEval = min(min_eval, evaluate)
            beta = min(beta, evaluate)

            if beta <= alpha:
                break
            
        return minEval
# Calculate the current score of the game, to be used as heuristic value
def heuristic(state):
    
    player1stones = 0
    for i in range(6):
        player1stones += state.board[i]
    player1stones += state.board[6] * 1.5

    player2stones = 0
    for i in range(7,13):
        player2stones += state.board[i]
    player2stones += state.board[13] * 1.5

    return player2stones-player1stones

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

        # board = [0, 0, 0, 0, 10, 0, 0, 4, 4, 4, 4, 4, 4, 0]
        # playerTurn = int(data[0])
        state = GameState(playerTurn, board)
        move = getBestMove(state)
        # print(move)

        # Using your intelligent bot, assign a move to "move"
        #
        # example: move = '1';  Possible moves from '1' to '6' if the game's rules allows those moves.
        # TODO: Change this
        ################
        

        # move = str(r)
        ################
        send(s, move)
