import random
import re
import tensorflow as tf
import valueFunction as vfunc
import Globals as g
import Classes as c
import MCTS
import AImodels as trial
import valueFunction as func
import random as rd
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.backend import reshape
from keras.utils.np_utils import to_categorical
import pandas as pd
import numpy as np
import csv
from timer import Timer
import matplotlib.pyplot as plt
from keras.models import load_model


#Creates board, all empty spots wiht zeros
def initBoard():
    board = []
    for i in range(0,19):
        row = []
        for ii in range(0,19):
            row.append(0)
        board.append(row)
    return board


#creates a list of all possible moves (not sure what this is used for, was in tutorial
def getMoves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                moves.append((i, j))
    return moves


#should be called after every move to check if anyone has won
def getWinner(board):
    candidate = 0
    won = 0

    # Check rows
    for i in range(len(board)):
        candidate = 0
        how_many_so_far = 0
        for j in range(len(board[i])):
            # Make sure there are no gaps
            if candidate != board[i][j]:
                how_many_so_far = 1
                candidate = board[i][j]
            else:
                how_many_so_far += 1
            # Determine whether the front-runner has all the slots
            if how_many_so_far == 5 and candidate > 0:
                won = candidate
                #print(candidate, how_many_so_far)
            #print(how_many_so_far)
    if won > 0:
        return won

    # Check columns
    for j in range(len(board[0])):
        candidate = 0
        how_many_so_far = 0
        for i in range(len(board)):

            # Make sure there are no gaps
            if candidate != board[i][j]:
                how_many_so_far = 1
                candidate = board[i][j]
            else:
                how_many_so_far += 1
            # Determine whether the front-runner has all the slots
            if how_many_so_far == 5 and candidate > 0:
                won = candidate

    if won > 0:
        return won

    # Check diagonals
    for i in range(len(board)):
        for j in range(len(board[i])):
            candidate = board[i][j]
            how_many_so_far = 0
            if candidate > 0 and i <= len(board) - 5 and j <= len(board) - 5:
                for d in range(0,5):
                # Make sure there are no gaps
                    if i + d >= len(board) or j + d > len(board) or candidate != board[i + d][j + d]:
                        break
                    else:
                        how_many_so_far += 1
                # Determine whether the front-runner has all the slots
                    if how_many_so_far == 5 and candidate > 0:
                        won = candidate
                        return won


            how_many_so_far = 0
            if candidate > 0 and i <= len(board):
                for d in range(0, 5):
                    # Make sure there are no gaps
                    if  i + d >= len(board) or j - d < 0 or candidate != board[i + d][j - d]:
                        break
                    else:
                        how_many_so_far += 1
                    # Determine whether the front-runner has all the slots
                    if how_many_so_far == 5 and candidate > 0:
                        won = candidate
                        return won
                #print(candidate, how_many_so_far)
            #print(how_many_so_far)
    if won > 0:
        return won

    # Still no winner?
    if (len(getMoves(board)) == 0):
        # It's a draw
        return 0
    else:
        # Still more moves to make
        return -1

#prints ascii board from the board given
def printBoard(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            mark = '_'
            if board[i][j] == 1:
                mark = 'X'
            elif board[i][j] == 2:
                mark = 'O'
            elif board[i][j] == 3:
                mark = '1'
            elif board[i][j] == 4:
                mark = '2'
            if (j == len(board[i]) - 1):
                print(mark)
            else:
                print(str(mark) + "|", end='')


def movesToBoard(moves):
    board = initBoard()
    for move in moves:
        player = move[0]
        coords = move[1]
        board[coords[0]][coords[1]] = player
    return board

#outputs a list of moves made, "History" that when given to the next function generates the board state
def simulateGame(p1=None, p2=None, rnd=0):
    board = initBoard()
    moveList = []
    playertoMove = 1
    history = []
    tempList = []
    moves = getMoves(board)
    temp = None
    rand = False
    move2 = None
    move1 = None
    move = None

    # Moves keeps track of the available coordinates (x, y) left on the board
    # Board keeps track of the player occupation on board (0, 1, 2)

    while getWinner(board) == -1:
        move = None
        #bot1_Roll = rd.randint(1, 7)
        #bot2_Roll = rd.randint(1, 19)

        # Chosen move for player1
        if playertoMove == 1:# and rand == False:
            moveList = trial.getBestMovesInAnArray(board)
            move = rd.choice(moveList)
            board[move.x][move.y] = playertoMove
            history.append([playertoMove, [move.x, move.y]])

        elif playertoMove == 2: #and rand == True:
            # import pdb; pdb.set_trace() n = nextline s = step in c = continue q = quit
            moveList = getMoves(board)
            move = rd.choice(moveList)
            board[move[0]][move[1]] = playertoMove
            history.append([playertoMove, [move[0], move[1]]])
        # Player move now occupies board (0, 1, 2)


        # Append playertoMove and coordinates to history


        # Switch between player 1 and player 2
        playertoMove = 1 if playertoMove == 2 else 2

        # Swap AI approach
        #rand = True if rand == False else True

    # moveList = trial.getBestMovesInAnArray(board)
    # move = rd.choice(moveList)

    # print(f"{move.x} {move.y}")
    # print(f"{move2.x} {move2.y}")
    printBoard(movesToBoard(history))
    print()
    return history
#this function creates a board given a history from the previous simulated game function



#this function is for viewing stats from the list of a lot of games simulated
def gameStats(games, player=1):
    stats = {"win": 0, "loss": 0, "draw": 0}
    #counter = 0
    for game in games:
        result = getWinner(movesToBoard(game))
        #counter += 1
        #print(str(counter) + ":   " + str(result))
        if result == -1:
            continue
        elif result == player:
            stats["win"] += 1
        elif result == 0:
            stats["draw"] += 1
        else:
            stats["loss"] += 1

    winPct = stats["win"] / len(games) * 100
    lossPct = stats["loss"] / len(games) * 100
    drawPct = stats["draw"] / len(games) * 100

    print("Results for player %d:" % (player))
    print("Wins: %d (%.1f%%)" % (stats["win"], winPct))
    print("Loss: %d (%.1f%%)" % (stats["loss"], lossPct))
    print("Draw: %d (%.1f%%)" % (stats["draw"], drawPct))




def gameHuman(board):

    currPlayer = 1
    history = []
    moveList = []
    move = None
    botOpener = True

    human = int(input("Would you like to be player 1 or 2 (Enter 1 or 2):"), 3)

    print(human)

    while getWinner(board) == -1:
        
        print("in getWinner currPlayer = ", currPlayer)

        if(currPlayer == human):
            inputX = int(input("X: "), 20)
            inputY = int(input("Y: "), 20)

            board[inputX][inputY] = currPlayer

            history.append([currPlayer, [inputX, inputY]])

            currPlayer = 1 if currPlayer == 2 else 2

            botOpener = False

            printBoard(board)

        else:
            
            if(botOpener == True):

                moveList = trial.getBestMovesInAnArray(board)
                move = rd.choice(moveList)

                board[move.x][move.y] = currPlayer

                history.append([currPlayer, [move.x, move.y]])

                currPlayer = 1 if currPlayer == 2 else 2

                botOpener = False

                print("Bot opening move")
                printBoard(board)

            else:
                move = trial.getMCTS_Move(board)

                board[move.x][move.y] = currPlayer

                history.append([currPlayer, [move.x, move.y]])

                currPlayer = 1 if currPlayer == 2 else 2

                print("bot MCTS move")
                printBoard(board)


def dataMagic(garbageData):
    test_string = garbageData

    testStr = test_string.replace(" ", '').replace("[", '').replace("]", '') #remove all but numbers and commas
    testStr = testStr.split(',') #split by commas, leave only numbers

    history = []
   
    for index, element in enumerate(testStr):
        if index % 3 == 0:
            history.append([int(element), [int(testStr[index + 1]), int(testStr[index + 2])]])

    #print(history)
    return(history)


#print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))



#
# games = []
# for i in range(10000):
#     sim = simulateGame()
#     print(i)
#     games.append(sim)
#
#
# with open('algVSrandom.csv', mode='a') as sim_games:
#     sim_games = csv.writer(sim_games, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE, lineterminator='\n')
#     for game in games:
#         sim_games.writerow(game)


#board = initBoard()
#gameHuman(board)
                                                                              #  training model
t = Timer()
t.start()

with open('finalData.csv', 'r') as csvfile:
    csvtext = csvfile.readlines()

myList = []
for line in csvtext:
    myList.append(line)

'''
with open('robertSims.csv', 'r') as csvfile2:
    csvtext2 = csvfile2.readlines()

for line in csvtext2:
    myList.append(line)

with open('algVSrandom.csv', 'r') as csvfile3:
    csvtext3 = csvfile3.readlines()

for line in csvtext3:
    myList.append(line)
'''
totalGames = []

counter = 0
for i in myList:
    history = dataMagic(myList[counter])
    board = movesToBoard(history)
    #printBoard(board)
    #print(history)
    totalGames.append(history)
    counter += 1
    print(counter)
t.stop()
print()
print(counter)

gameStats(totalGames)                   #end here



def getModel():
    numCells = 361 #board 19x19
    outcomes = 361
    model = Sequential()
    model.add(Dense(1020, activation='relu', input_shape=(361, )))
    model.add(Dense(1020, activation='relu'))   #1,020 monomials
    model.add(Dense(1020, activation='relu'))
    model.add(Dense(1020, activation='relu'))
    model.add(Dense(1020, activation='relu'))
    model.add(Dense(outcomes, activation='softmax'))
    model.compile(loss='mse', optimizer='adam', metrics=['acc'])
    return model


def boardNum(move):
    coords = move[1]
    return coords[0] * 19 + coords[1]

def gamesToWinLossData(games):
    X = []
    y = []
    for game in games:
        #winner = getWinner(movesToBoard(game))
        winner = getWinner(movesToBoard(game))
        for move in range(len(game)):
            if move % 2 == 0 and move < len(game) - 2:
                X.append(movesToBoard(game[:(move + 1)]))
                y.append(movesToBoard([game[move + 2]]))

    X = np.array(X).reshape((-1, 361))
    y = np.array(y).reshape((-1, 361))
    #Return an appropriate train/test split
    trainNum = int(len(X) * 0.99)
    return (X[:trainNum], X[trainNum:], y[:trainNum], y[trainNum:])
print('before model')
model = getModel()
print('before model')
                                                                                                                                          #this code
X_train, X_test, y_train, y_test = gamesToWinLossData(totalGames)
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=300, batch_size=200)
model.save('attempt4.h5')
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy- adam, categorical_crossentropy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss- adam, categorical_crossentropy')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
#