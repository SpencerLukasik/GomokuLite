#Takes in a 2D array of integers and outputs a Coordinate Pair (x, y) that it believes is the best move to make
import Globals as g
import Classes as c
import Functions as func
import MCTS as MCTS
import random

#Runs a Monty-Carlo search using the moves it finds off of getBestMovesInAnArray
#A Little slow, but accurate
def getMCTS_Move(board):
    #Variables
    combinations = []
    playerCombinations = []
    values = [[0 for i in range(g.width)] for j in range(g.width)]
    playerValues = [[0 for i in range(g.width)] for j in range(g.width)]
    #Populate
    func.populate(combinations, values)
    func.populate(playerCombinations, playerValues)
    #Correct according to the current boardstate 
    RePopulate(board, values, playerValues, combinations, playerCombinations)
    #Update the new values
    func.updateValues(board, combinations, values, False)
    func.updateValues(board, playerCombinations, playerValues, True)

    return MCTS.MCTS_Move(board, combinations, values, playerCombinations, playerValues, False)


#Compares the values of all agressive and defensive moves, and returns the highest summation of both strategies.
#This is much better for getting the best general move, but it can get confused in complex boardstates, as it does
#not consider how close the opponent is to making a winning move; it considers the highest value per square, which
#often times is the best blocking or aggressive move, but may not always be so
def getBestMove(board):
    #Variables
    combinations = []
    playerCombinations = []
    values = [[0 for i in range(g.width)] for j in range(g.width)]
    playerValues = [[0 for i in range(g.width)] for j in range(g.width)]
    #Populate
    func.populate(combinations, values)
    func.populate(playerCombinations, playerValues)
    #Correct according to the current boardstate
    RePopulate(board, values, playerValues, combinations, playerCombinations)
    #Update the new values
    func.updateValues(board, combinations, values, False)
    func.updateValues(board, playerCombinations, playerValues, True)

    aiGuessDimensions = c.CoordinatePair(0, 0)
    curPotential = c.Value(0, 0, 0)
    for i in range(g.width):
        for j in range(g.width):
      #Takes the Aggregate Potential of both player's possible moves
            if (values[j][i].thirdPriority > -1 and playerValues[j][i].thirdPriority > -1 and (values[j][i]+playerValues[j][i]) > curPotential):
                curPotential.firstPriority = values[j][i].firstPriority + playerValues[j][i].firstPriority
                curPotential.secondPriority = values[j][i].secondPriority + playerValues[j][i].secondPriority
                curPotential.thirdPriority = values[j][i].thirdPriority + playerValues[j][i].thirdPriority
                aiGuessDimensions = c.CoordinatePair(j, i)

    return aiGuessDimensions

#First gets the highest potential of the most aggressive move, the highest potential of a defensive move,
#and compares the two.  This approach is better when considering the alternative strategies for white
#and black, but it may make worse general moves when there is no need to be overly defensive.
#Generally leads to longer games
def getBestAggressiveOrDefensiveMove(board):
    #Variables
    combinations = []
    playerCombinations = []
    values = [[0 for i in range(g.width)] for j in range(g.width)]
    playerValues = [[0 for i in range(g.width)] for j in range(g.width)]
    #Populate
    func.populate(combinations, values)
    func.populate(playerCombinations, playerValues)
    #Correct according to the current boardstate
    RePopulate(board, values, playerValues, combinations, playerCombinations)
    #Update the new values
    func.updateValues(board, combinations, values, False)
    func.updateValues(board, playerCombinations, playerValues, True)

    aiGuessDimensions = c.CoordinatePair(0, 0)
    curPotential = c.Value(0, 0, 0)

    #Potential of aggressive moces
    for i in range(g.width):
        for j in range(g.width):
        #Check to make sure spot is not taken
            if (values[j][i].thirdPriority > -1 and values[j][i] > curPotential):
                #If first priority is higher, OR if first priority is the same AND second
                #priority is higher, OR if first AND second priorities are the same but THIRD
                #priority is higher, make this the preferred move
                curPotential = values[j][i]
                aiGuessDimensions = c.CoordinatePair(j, i)

    #Defensive moves
    playerCurPotential = c.Value(0, 0, 0)

    for i in range(g.width):
        for j in range(g.width):
            if (playerValues[j][i].thirdPriority > -1 and playerValues[j][i] > playerCurPotential):
                playerCurPotential = playerValues[j][i]
                if (playerCurPotential > curPotential):
                    aiGuessDimensions = c.CoordinatePair(j, i)

    return aiGuessDimensions

#This function returns an array of CoordinatePairs that could all be potential moves
#Gets all moves of equivalent first and second priorities
def getBestMovesInAnArray(board):
    #Variables
    combinations = []
    playerCombinations = []
    values = [[0 for i in range(g.width)] for j in range(g.width)]
    playerValues = [[0 for i in range(g.width)] for j in range(g.width)]
    #Populate
    func.populate(combinations, values)
    func.populate(playerCombinations, playerValues)
    #Correct according to the current boardstate 
    RePopulate(board, values, playerValues, combinations, playerCombinations)
    #Update the new values
    func.updateValues(board, combinations, values, False)
    func.updateValues(board, playerCombinations, playerValues, True)

    possibleMoves = []

    highestFirstAggressive = 0
    highestSecondAggressive = 0
    highestFirstDefensive = 0
    highestSecondDefensive = 0

    for i in range(g.width):
        for j in range(g.width):
      #Make sure the move is not taken
            if (values[j][i].thirdPriority > -1):
        #Get the highest first priority
                if (values[j][i].firstPriority > highestFirstAggressive):
                    highestFirstAggressive = values[j][i].firstPriority  

                if (playerValues[j][i].firstPriority > highestFirstDefensive):
                    highestFirstDefensive = playerValues[j][i].firstPriority
            
    for i in range(g.width):
        for j in range(g.width):
      #Make sure the move is not taken
            if (values[j][i].thirdPriority > -1):
        #Get the highest second priority based on the first
                if (values[j][i].firstPriority == highestFirstAggressive and values[j][i].secondPriority > highestSecondAggressive):
                   highestSecondAggressive = values[j][i].secondPriority
        
                if (playerValues[j][i].firstPriority == highestFirstDefensive and playerValues[j][i].secondPriority > highestSecondDefensive):
                    highestSecondDefensive = playerValues[j][i].secondPriority
       
    #Compare the highest values calculated
    #If the AI has a greater aggressive potential, make the most aggressive move
    #One move away from winning
    if (highestFirstAggressive == (g.n - 1)):
        addToList(possibleMoves, values, highestFirstAggressive, highestSecondAggressive)
    elif (highestFirstDefensive == (g.n - 1)):
        addToList(possibleMoves, playerValues, highestFirstDefensive, highestSecondDefensive)
    #Open 3
    elif (highestFirstAggressive == (g.n - 2) and highestSecondAggressive >= (2)):
        addToList(possibleMoves, values, highestFirstAggressive, highestSecondAggressive)
    elif (highestFirstDefensive == (g.n - 2) and highestSecondDefensive >= (2)):
        addToList(possibleMoves, playerValues, highestFirstDefensive, highestSecondDefensive)
    #Can create 2 Open 3's
    elif (highestFirstAggressive == (g.n - 3) and highestSecondAggressive >= (6)):
        addToList(possibleMoves, values, highestFirstAggressive, highestSecondAggressive)
    elif (highestFirstDefensive == (g.n - 3) and highestSecondDefensive >= (6)):
        addToList(possibleMoves, playerValues, highestFirstDefensive, highestSecondDefensive)
    else:
        highestFirstTotal = 0
        highestSecondTotal = 0
        #First total
        for i in range(g.width):
            for j in range(g.width):
                if (values[j][i].thirdPriority > -1):
                    if (values[j][i].firstPriority + playerValues[j][i].firstPriority > highestFirstTotal):
                        highestFirstTotal = values[j][i].firstPriority + playerValues[j][i].firstPriority
        #Second total
        for i in range(g.width):
            for j in range(g.width):
                if (values[j][i].thirdPriority > -1):
                    if (values[j][i].firstPriority + playerValues[j][i].firstPriority == highestFirstTotal and values[j][i].secondPriority + playerValues[j][i].secondPriority > highestSecondTotal):
                        highestSecondTotal = values[j][i].secondPriority + playerValues[j][i].secondPriority
        #Append
        for i in range(g.width):
            for j in range(g.width):
                if (values[j][i].thirdPriority > -1):
                    if (values[j][i].firstPriority + playerValues[j][i].firstPriority >= (highestFirstTotal-g.FIRST_VARIANCE) and values[j][i].secondPriority + playerValues[j][i].secondPriority >= (highestSecondTotal-g.SECOND_VARIANCE)):
                        possibleMoves.append(c.CoordinatePair(j, i))

    return possibleMoves

#Does the same as the previous, but doesn't have to re-copy the combinations and values
#Only useful for the MCTS_Searching
#Don't touch this
def getBestMovesInAnArrayFast(board, values, playerValues, combinations, playerCombinations, curPlayer):
    func.updateValues(board, combinations, values, curPlayer)
    func.updateValues(board, playerCombinations, playerValues, not curPlayer)

    possibleMoves = []

    highestFirstAggressive = 0
    highestSecondAggressive = 0
    highestFirstDefensive = 0
    highestSecondDefensive = 0

    for i in range(g.width):
        for j in range(g.width):
      #Make sure the move is not taken
            if (values[j][i].thirdPriority > -1):
        #Get the highest first priority
                if (values[j][i].firstPriority > highestFirstAggressive):
                    highestFirstAggressive = values[j][i].firstPriority  

                if (playerValues[j][i].firstPriority > highestFirstDefensive):
                    highestFirstDefensive = playerValues[j][i].firstPriority
            
    for i in range(g.width):
        for j in range(g.width):
      #Make sure the move is not taken
            if (values[j][i].thirdPriority > -1):
        #Get the highest second priority based on the first
                if (values[j][i].firstPriority == highestFirstAggressive and values[j][i].secondPriority > highestSecondAggressive):
                   highestSecondAggressive = values[j][i].secondPriority
        
                if (playerValues[j][i].firstPriority == highestFirstDefensive and playerValues[j][i].secondPriority > highestSecondDefensive):
                    highestSecondDefensive = playerValues[j][i].secondPriority
       
    #Compare the highest values calculated
    #If the AI has a greater aggressive potential, make the most aggressive move
    if (highestFirstAggressive == (g.n - 1)):
        addToList(possibleMoves, values, highestFirstAggressive, highestSecondAggressive)
    elif (highestFirstDefensive == (g.n - 1)):
        addToList(possibleMoves, playerValues, highestFirstDefensive, highestSecondDefensive)
    elif (highestFirstAggressive == (g.n - 2) and highestSecondAggressive >= (2)):
        addToList(possibleMoves, values, highestFirstAggressive, highestSecondAggressive)
    elif (highestFirstDefensive == (g.n - 2) and highestSecondDefensive >= (2)):
        addToList(possibleMoves, playerValues, highestFirstDefensive, highestSecondDefensive)
    elif (highestFirstAggressive == (g.n - 3) and highestSecondAggressive >= (6)):
        addToList(possibleMoves, values, highestFirstAggressive, highestSecondAggressive)
    elif (highestFirstDefensive == (g.n - 3) and highestSecondDefensive >= (6)):
        addToList(possibleMoves, playerValues, highestFirstDefensive, highestSecondDefensive)
    else:
        highestFirstTotal = 0
        highestSecondTotal = 0
        #First total
        for i in range(g.width):
            for j in range(g.width):
                if (values[j][i].thirdPriority > -1):
                    if (values[j][i].firstPriority + playerValues[j][i].firstPriority > highestFirstTotal):
                        highestFirstTotal = values[j][i].firstPriority + playerValues[j][i].firstPriority
        #Second total
        for i in range(g.width):
            for j in range(g.width):
                if (values[j][i].thirdPriority > -1):
                    if (values[j][i].firstPriority + playerValues[j][i].firstPriority == highestFirstTotal and values[j][i].secondPriority + playerValues[j][i].secondPriority > highestSecondTotal):
                        highestSecondTotal = values[j][i].secondPriority + playerValues[j][i].secondPriority
        #Append
        for i in range(g.width):
            for j in range(g.width):
                if (values[j][i].thirdPriority > -1):
                    if (values[j][i].firstPriority + playerValues[j][i].firstPriority >= (highestFirstTotal-g.FIRST_VARIANCE) and values[j][i].secondPriority + playerValues[j][i].secondPriority >= (highestSecondTotal-g.SECOND_VARIANCE)):
                        possibleMoves.append(c.CoordinatePair(j, i))
    
    return possibleMoves

#Fixes combinations and values based on the given board
#Don't touch this
def RePopulate(board, values, playerValues, combinations, playerCombinations):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (board[i][j]==1):
                func.removePotential(combinations, values, c.CoordinatePair(i, j))
                values[i][j].thirdPriority = -1
                playerValues[i][j].thirdPriority = -1
            elif (board[i][j]==2):
                func.removePotential(playerCombinations, playerValues, c.CoordinatePair(i, j))
                values[i][j].thirdPriority = -1
                playerValues[i][j].thirdPriority = -1

#Adds values to the list that are of the highest First priority AND that are 1 away from the highest Second priority
#Don't touch this
def addToList(possibleMoves, values, highestFirst, highestSecond):
    for i in range(g.width):
        for j in range(g.width):
            if (values[j][i].thirdPriority > -1):
                if (values[j][i].firstPriority == highestFirst and values[j][i].secondPriority >= (highestSecond)):
                    possibleMoves.append(c.CoordinatePair(j, i))