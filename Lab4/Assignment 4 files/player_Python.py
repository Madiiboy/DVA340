#!/usr/bin/python           # This is server.py file

import socket  # Import socket module
import numpy as np
import time
from multiprocessing.pool import ThreadPool
import os
import random
import math

class game:
    def __init__(self, player):
        self.player = player

class Board:
    
    def __init__(self, board):
        self.board = board
        self.num_moves = 0

    # Some game logic
    def makeMove(self, bucket):
        #Check if valid bucket
        if bucket == 6 or bucket > 6 * 2 or bucket < 0:
            return -1

        # Check if valid move
        if self.num_moves % 2 == 0 and bucket > 6 or self.num_moves % 2 == 1 and bucket < 6:
            return -1

        # We pick up the stones
        stones = self.board[bucket]
        self.board[bucket] = 0

        #Bucket cannot be empty
        if stones == 0:
            return -2

        offset = 0
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

    # Creates a list of possible children of current board
    def children(self):
        children = []

        if self.num_moves % 2 == 0:
            moves = range(6)
        else:
            moves = range(7, 14)

        child = Board(self.board)
        for move in moves:
            move = child.makeMove(move)

            if move >= 0:
                children.append((move, child))
                child = Board(self.board)
        
        return children

    # Return true if a player has no stones on their side
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

    # check if one of the players has no stones left
    def isOver(self):
        for i in range()

    # Returns the score of the game, positive if player1 leads negative if player 2 leads
    def score(self):
        player1 = 0
        for i in range(7):
            player1 += self.board[i]

        player2 = 0
        for i in range(7, 14):
            player2 += self.board[i]

        return player1 - player2


class Player: 
    def __init__(self, depth, player):
        self.depth = depth
        self.player = player

    #Returns optimal pit to move from
    #Dual moves not yet implemented
    def findMove(self, board):

        # Make more for best score
        def findMoveHelper(curr_board, depth, alpha, beta, isMax):
            if board.isOver():
                return (board.score(), -1)

            elif depth == 0:
                return (self.heuristic(curr_board), -1)

            children = curr_board.children()
            finalMove = -1

            if isMax:
                final_score = -math.inf
                should_replace = lambda x: x > final_score
            else:
                final_score = math.inf
                should_replace = lambda x: x < final_score

            for child in children:
                childMove, childBoard = child
                tempVal = findMoveHelper(childBoard, depth - 1, alpha, beta, not isMax)[0]

                if should_replace(tempVal):
                    finalScore = tempVal
                    finalMove = childMove

                if isMax:
                    alpha = max(alpha, tempVal)
                else:
                    beta = min(beta, tempVal)
        
                if alpha > beta:
                    break

            return (finalScore, finalMove)

        score, move = findMoveHelper(board, self.depth, -math.inf, math.inf, self.player)
        return move


    #Evaluate how good a move is
    def heuristic(self, board):

        player1stones = 0
        for i in range(0,6):
            player1stones += board[i]
        player1stones += board[6] * 1.5

        player2stones = 0
        for i in range(7,14):
            player2stones += board[i]
        player2stones += board[13] * 1.5

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

        player = Player(3,True)
        b = Board(board)
        print(b)
        # move = minimax()
        # move = '1'
        move = player.findMove(b)
        print(move)

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
