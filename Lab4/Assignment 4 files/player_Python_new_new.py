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

class GameState():
    def __init__(self, player_turn, board):
        # print(board)
        self.player = player_turn
        self.board = board
        
    # Get all the possible moves
    def findValidMoves(self):
        # print(self.player)
        #Hmm, ska denna vara jag?
        if self.player == 2:
            return [i for i in range(6) if self.board[i] != 0]
        #get other players possible moves
        else:
            return [i for i in range(7,14) if self.board[i] != 0]

    #Get the total score of player 1
    def getScore(self):
        score = 0
        for i in range(7):
            score += self.board[i]
        return score

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
            for i in range(7, 14):
                if self.board[i] != 0:
                    return False

            return True
        else:
            return True
    
    # Simulates the move
    def makeMove(self, bucket):

        # TODO: Check if player will get a bonus move

        # get the amount of stones that is in chosen bucket
        stones = self.board[bucket]

        #If the player is me, I want to be able to put stone in index 6
        if self.player == 2:
            #take all stones from the current bucket
            self.board[bucket] = 0
            availble_stones = stones
            index = bucket
            last_index = 0
            while availble_stones > 0:
                #Skip if opponents pit
                if availble_stones == 1:
                    last_index = index

                if index == 14:
                    index = 0

                #Skip the enemy pit
                if index == 13:
                    index += 1
                else:
                    self.board[index+1] += 1
                    index += 1
                    availble_stones -= 1
            if last_index == 6:
                self.player = 1
            else:
                self.player = 2
            return

        elif self.player == 1:
            self.board[bucket] = 0
            availble_stones = stones
            index = bucket
            last_index = 0
            while availble_stones > 0:
                if availble_stones == 1:
                    last_index = index
                #Skip if opponents pit
                if index == 6:
                    index += 1

                if index == 13:
                    index = 0
                    self.board[index] += 1
                    availble_stones -= 1
                else:
                    self.board[index+1] += 1
                    index += 1
                    availble_stones -= 1
            if last_index == 13:
                self.player = 1
            else:
                self.player = 2
            return
        

# Called from 'main' to start the game
def getBestMove(state):

    # print(state.player)
    valid_moves = state.findValidMoves()
    # print(possible_moves)
    move_evals = []
    max_val = -math.inf
    best_move = None
    for move in valid_moves:
        new_state = copy.deepcopy(state)
        new_state.makeMove(move)
        # print(new_state.board)
        val = minimax(state, 2, state.player)

        move_evals.append((move, val))
        if val > max_val:
            max_val = val
            best_move = move

    # print(best_move)
    # print(state.board)
    best_move = (best_move+1) % 7
    # print(best_move)
    # print(state.board)
    return best_move


def minimax(state, depth, player):
    print(player)

    if state.isOver() or depth == 0:
        return calculateValue(state.board, state.player)
        
    #maximizing player
    if state.player == 2:
        max_eval = -math.inf
        validMoves = state.findValidMoves()
        
        # For every valid move, simulate a new move, where do i simualate the move though
        for v in validMoves:
            new_board = copy.deepcopy(state)
            new_board.makeMove(v)

            evaluate = minimax(new_board, depth-1, state.player)
            maxEval = max(max_eval, evaluate)
        return maxEval
    else:
        min_eval = math.inf
        validMoves = state.findValidMoves()

        # For every valid move, simulate a new move, where do i simualate the move though
        for v in validMoves:
            new_board = copy.deepcopy(state)
            new_board.makeMove(v)

            evaluate = minimax(new_board, depth-1, state.player)
            minEval = min(min_eval, evaluate)
        return minEval

# Calculate the current score of the game, to be used as heuristic value
def calculateValue(board, player):
    
    player1stones = 0
    for i in range(6):
        player1stones += board[i]
    player1stones += board[6] * 1.5

    player2stones = 0
    for i in range(7,14):
        player2stones += board[i]
    player2stones += board[13] * 1.5

    if player == 2:
        return player2stones - player1stones
    else:
        return player1stones - player2stones

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
        # playerTurn = int(data[0])
        # board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        # state = GameState(playerTurn, board, 0)
        # move = state.findBestMove()
        state = GameState(playerTurn, board)
        move = getBestMove(state)
        # print(move)
        #I believe that it works, but i do not check which is the best move, only which has the best heuristic value
        # move = minimax(b, 2, b.player)
        # TODO: Minimax funktion för att avgöra det bästa möjliga draget. Måste fixa någon dank datastruktur för att hålla koll
        #på alla värden. Träd med massa noder exempelvis

        # Using your intelligent bot, assign a move to "move"
        #
        # example: move = '1';  Possible moves from '1' to '6' if the game's rules allows those moves.
        # TODO: Change this
        ################
        

        # move = str(r)
        ################
        send(s, move)
