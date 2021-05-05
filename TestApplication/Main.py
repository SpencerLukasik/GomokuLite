import Classes as c
import Globals as g
import Functions as func
import GetBestMove as trial
import random

#Variables for maintaining boardstate
curPlayer = True
board = [[0 for i in range(g.width)] for j in range(g.width)]
values = [[0 for i in range(g.width)] for j in range(g.width)]
playerValues = [[0 for i in range(g.width)] for j in range(g.width)]
combinations = []
playerCombinations = []
prevCoordinates = c.CoordinatePair(-1, -1)


def GameLoop(board, values, playerValues, combinations, playerCombinations, prevCoordinates, curPlayer):
    while (True):
        #If it's the human's turn
        if (curPlayer):
            func.drawBoard(board)
            
            
            prevCoordinates.y = int(input("X: "))
            prevCoordinates.x = int(input("Y: "))

            func.make_move(board, combinations, playerCombinations, values, playerValues, curPlayer, prevCoordinates)
            if (func.checkWin(board, playerCombinations, curPlayer)):
                break
            curPlayer = not curPlayer


        #If it's the AI's turn
        else:
            #MCTS move
            
            if (g.playingAgainstMCTS):
                prevCoordinates = trial.getMCTS_Move(board)
            else:
                prevCoordinates = random.choice(trial.getBestMovesInAnArrayFast(board, values, playerValues, combinations, playerCombinations, curPlayer))

            func.make_move(board, combinations, playerCombinations, values, playerValues, curPlayer, prevCoordinates)
            if (func.checkWin(board, combinations, curPlayer)):
                break
            curPlayer = not curPlayer

    func.drawBoard(board)
    if (curPlayer):
        print("Congratulations to the Human!")
    else:
        print("Congratulations to the AI!")

func.populate(combinations, values)
func.populate(playerCombinations, playerValues)
GameLoop(board, values, playerValues, combinations, playerCombinations, prevCoordinates, curPlayer)