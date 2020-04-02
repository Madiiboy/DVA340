#!/usr/bin/python           # This is server.py file

import socket  # Import socket module
import numpy as np
import time
from multiprocessing.pool import ThreadPool
import os
import random
import math

class GameState():
    def __init__(self, player_turn, board, depth, value = 0):
        self.player = player_turn
        self.board = board
        self.depth = depth
        self.value = value
        
    def findValidMoves(self, b):
        #Hmm, ska denna vara jag?
        if self.player:
            return [i for i in range(6) if b[i] != 0]
        #get other players possible moves
        else:
            return [i for i in range(7,14) if b[i] != 0]

    def minimax(move):
        pass

    # Function where i test each move ane evaluate how good it is
    def makeMove(self, bucket):
        
        # We pick up the stones
        stones = self.board[bucket]
        self.board[bucket] = 0

        offset = 0
        #Put stones in new buckets
        while(offset < stones):

            bucket_index = (bucket + offset + 1) % (6 * 2 + 2)

            #we skip the oponents "pit"
            if((bucket < 6 and bucket_index == 6 * 2 + 1) or (bucket > 6 and bucket_index == 6)):
                stones += 1

            else:
                self.board[bucket_index] += 1
            offset += 1

        if self.board[bucket_index] == 1 and bucket_index != 6 and bucket_index != 6 * 2 + 1:
            if bucket < 6 and bucket_index < 6:
                self.board[6] += self.board[(2 * 6)- bucket_index] + 1
                self.board[bucket_index] = 0
                self.board[(2 * 6)-bucket_index] = 0

            elif bucket > 6 and bucket_index > 6:
                self.board[-1] += self.board[(2*6)-bucket_index] + 1
                self.board[bucket_index] = 0
                self.board[(2 * 6)-bucket_index] = 0
        self.num_moves += 1
        return bucket
        

    #Find the best possible move
    def findBestMove(self): 
        possible_moves = self.findValidMoves(self.board)
    
        for move in possible_moves:
            minimax(move)
            
    
            

        


def receive(socket):
    msg = ''.encode()  # type: str

    try:
        data = socket.recv(1024)  # type: object
        msg += data
    except:
        pass
    return msg.decode()

def send(socket, msg):
    socket.sendall(msg.encode())

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

        state = GameState(playerTurn, board)
        move = state.findBestMove()

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
