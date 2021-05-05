from keras.models import load_model
import keras.models
import numpy as np
import tensorflow as tf
from keras.utils.np_utils import to_categorical
#import  gomokuAI
import random

def initBoard():
    board = []
    for i in range(0, 19):
        row = []
        for ii in range(0, 19):
            row.append(0)
        board.append(row)
    return board


# creates a list of all possible moves (not sure what this is used for, was in tutorial
def getMoves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                moves.append((i, j))
    return moves


# should be called after every move to check if anyone has won
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
                # print(candidate, how_many_so_far)
            # print(how_many_so_far)
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
                for d in range(0, 5):
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
                    if i + d >= len(board) or j - d < 0 or candidate != board[i + d][j - d]:
                        break
                    else:
                        how_many_so_far += 1
                    # Determine whether the front-runner has all the slots
                    if how_many_so_far == 5 and candidate > 0:
                        won = candidate
                        return won
                # print(candidate, how_many_so_far)
            # print(how_many_so_far)
    if won > 0:
        return won

    # Still no winner?
    if (len(getMoves(board)) == 0):
        # It's a draw
        return 0
    else:
        # Still more moves to make
        return -1


# prints ascii board from the board given
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
        # bot1_Roll = rd.randint(1, 7)
        # bot2_Roll = rd.randint(1, 19)

        # Chosen move for player1
        if playertoMove == 1 and rand == False:
            probs = model(np.array(board).reshape((-1, 361)))[0]
            threshhold = max(probs) - .000001
            layer = tf.keras.layers.ReLU(max_value=1.0, threshold=threshhold)
            output = layer(np.array(probs))
            for index, prob in enumerate(output):
                if prob != 0:
                    move = [index // 19, index % 19]
                    #print(move)
            board[move[0]][move[1]] = 1

        elif playertoMove == 2:  # and rand == True:
            moves = getMoves(board)
            move = moves[random.randint(0, len(moves) - 1)]
            # x = int(input("enter x: "))
            # y = int(input("enter y: "))
            board[move[0]][move[1]] = 2

        # Player move now occupies board (0, 1, 2)
        # board[move.x][move.y] = playertoMove

        # Append playertoMove and coordinates to history
        history.append([playertoMove, [move[0], move[1]]])

        # Switch between player 1 and player 2
        playertoMove = 1 if playertoMove == 2 else 2

        # Swap AI approach
        # rand = True if rand == False else True

    # moveList = trial.getBestMovesInAnArray(board)
    # move = rd.choice(moveList)

    # print(f"{move.x} {move.y}")
    # print(f"{move2.x} {move2.y}")
    #printBoard(movesToBoard(history))
    return history



model = load_model("attempt4.h5")
#import pdb; pdb.set_trace()
def showMove(move_probs):
    probs = model(np.array(initBoard()).reshape((-1, 361)))[0]
    threshhold = max(probs) - .000001
    layer = tf.keras.layers.ReLU(max_value=1.0, threshold=threshhold)
    output = layer(np.array(probs))
    for index, prob in enumerate(output):
        if prob != 0:
            print([index // 19, index % 19])

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



# games = [simulateGame() for _ in range(50)]
# print("done simulation")
# gameStats(games)


#play against model
board = initBoard()
counter = 0
while(counter >= 0):
    if counter % 2 == 0:
        probs = model(np.array(board).reshape((-1, 361)))[0]
        threshhold = max(probs) - .000001
        layer = tf.keras.layers.ReLU(max_value=1.0, threshold=threshhold)
        output = layer(np.array(probs))
        for index, prob in enumerate(output):
            if prob != 0:
                move = [index // 19, index % 19]
                print(move)
        board[move[0]][move[1]] = 1
    else:
        #moves = getMoves(board)
        #move = moves[random.randint(0, len(moves) - 1)]
        x = int(input("enter x: "))
        y = int(input("enter y: "))
        board[x][y] = 2
    print("move #" +  str(counter) + ": ")
    printBoard(board)
    print()
    counter += 1
    # winner = getWinner(board)
    # if winner > 0:
    #     counter = -1
    #     print("Winner: Player " + str(winner))
