import math
import random
import Globals as g
import Classes as c
import AImodels as trial
import Functions as func

def MCTS_Move(board, combinations, values, playerCombinations, playerValues, curPlayer):
    #Define the starting node.  Set it's parent to itself so that we can verify
    #later on whether or not the node we are currently on is the head
    #(if node == node.parent) this is the head
    head = c.Node(c.CoordinatePair(-1, -1), 5, 0, 0)
    head.parent = head

    #Variables for the simulation
    simBoard = [[0 for i in range(g.width)] for j in range(g.width)]
    simValues = [[0 for i in range(g.width)] for j in range(g.width)]
    simPlayerValues = [[0 for i in range(g.width)] for j in range(g.width)]
    simCombinations = []
    simPlayerCombinations = []
    simCurPlayer = c.Boolean(curPlayer)

    #Create a list of all untaken spaces
    untaken = []
    for i in range(g.width):
        for j in range(g.width):
            if (board[i][j] == 0):
                untaken.append(c.CoordinatePair(i, j))

    #Run simulations according to the number of simulations required
    for i in range(g.numberOfSimulations):
        print(f"Simulation #{i}!")
        #Copy simulated values
        func.copy2DList(board, simBoard)
        func.copy2DValue(values, simValues)
        func.copy2DValue(playerValues, simPlayerValues)
        simCombinations = []
        simPlayerCombinations = []
        func.copyCombination(combinations, simCombinations)
        func.copyCombination(playerCombinations, simPlayerCombinations)
        simCurPlayer.value = curPlayer
        simUntaken = trial.getBestMovesInAnArrayFast(simBoard, simValues, simPlayerValues, simCombinations, simPlayerCombinations, simCurPlayer.value)
        #Selection and Expansion of Node Tree
        start = SelectAndExpand(head, simUntaken, simBoard, simValues, simPlayerValues, simCombinations, simPlayerCombinations, simCurPlayer)
        #Simulate Game is Simulation
        #downPropegate after calling upPropegate
        upPropegate(start, simulateGame(simBoard, simCombinations, simPlayerCombinations, simValues, simPlayerValues, start.coordinates, simUntaken, simCurPlayer))
        downPropegate(head)

    #Prints out final values.  Commend out if you don't want to see them
    #for i in range(len(head.children)):
        #print(f"Child ({head.children[i].coordinates.y}, {head.children[i].coordinates.x}) was visited {head.children[i].visited} times, had a score of {head.children[i].score} and had a uct of {head.children[i].uct}")
  
   
    #Get the highest scoring node and return it back to main
    highest = 0
    for i in range(len(head.children)):
        if (head.children[i].visited > head.children[highest].visited):
            highest = i

    return head.children[highest].coordinates


def simulateGame(simBoard, combinations, playerCombinations, values, playerValues, randoMove, simUntaken, curPlayer):
    #Remember who was first to move; if it is the Human to move, we want the
    #results to come back with the sign flipped
    buff = 1
    if (curPlayer.value):
        buff *= -1
    #While there is space on the board,
    while (len(simUntaken) > 0):
        #func.drawBoard(simBoard)
        #input()
        #If the current player is the human,
        if (curPlayer.value):
            #Set the board space to 1
            simBoard[randoMove.x][randoMove.y] = 1
            #Remove combinations to keep up with the WinCheck
            func.removePotential(combinations, values, randoMove)
            values[randoMove.x][randoMove.y].thirdPriority = -1
            playerValues[randoMove.x][randoMove.y].thirdPriority = -1
            #If there is a win with this player, return -1
            if (func.checkWin(simBoard, playerCombinations, curPlayer.value)):
                #print("This was a loss")
                #func.drawBoard(simBoard)
                return (-1 * buff)
        else:
            simBoard[randoMove.x][randoMove.y] = 2
            #Do the same if it is the AI's turn to move
            func.removePotential(playerCombinations, playerValues, randoMove)
            values[randoMove.x][randoMove.y].thirdPriority = -1
            playerValues[randoMove.x][randoMove.y].thirdPriority = -1
            #Return 1 for a positive outcome
            if (func.checkWin(simBoard, combinations, curPlayer.value)):
                #print("This was a win")
                #func.drawBoard(simBoard)
                return (1 * buff)

    #Remove the untaken space from the list so spaces are not repeated
    #**This could be improved if we make RandoMove an index of untaken rather
    #**than a Coordinate Pair itself, but it does look ugly
        curPlayer.value = not curPlayer.value
        if (curPlayer.value):
            simUntaken = trial.getBestMovesInAnArrayFast(simBoard, playerValues, values, playerCombinations, combinations, curPlayer.value)
        else:
            simUntaken = trial.getBestMovesInAnArrayFast(simBoard, values, playerValues, combinations, playerCombinations, curPlayer.value)

    #Get another random untaken space
        if (len(simUntaken) > 0):
            randoMove = random.choice(simUntaken)

    #Return 0 if it's a catgame
    #print("This was a tie")
    #func.drawBoard(simBoard)
    return 0


def SelectAndExpand(head, untaken, simBoard, simValues, simPlayerValues, simCombinations, simPlayerCombinations, simCurPlayer):
    #If there is a child node that has not yet been visited at all,
    if (len(head.children) < len(untaken)):
        #**EXPAND
        #Make the node (a bit hacky to use heads' children length as the index for
        #Untaken, keep sight of this for further issues)
        head.children.append(c.Node(untaken[len(head.children)], 0, 0, 0))
        #Set the parent of the new node
        head.children[len(head.children) - 1].parent = head
        #Return the newly made node
        return head.children[len(head.children) - 1]

    #Otherwise, get the highest UCT node from the list.
    #Return head if there is no option
    if (len(untaken) == 0):
        return head
    temp = getHighestUCT(head.children)
    #Remove the node recieved from the list of untaken nodes
    for i in range(len(untaken)):
        if (untaken[i] == temp.coordinates):
            untaken.pop(i)
            break

    #Update boardstate
    if (simCurPlayer.value):
        simBoard[temp.coordinates.x][temp.coordinates.y] = 1
        #Check if there is already a win on this new board state
        if (func.checkWin(simBoard, simPlayerCombinations, simCurPlayer.value)):
            return temp
        func.removePotential(simCombinations, simValues, temp.coordinates)
        simValues[temp.coordinates.x][temp.coordinates.y].thirdPriority = -1
        simPlayerValues[temp.coordinates.x][temp.coordinates.y].thirdPriority = -1
    else:
        simBoard[temp.coordinates.x][temp.coordinates.y] = 2
        #Do the same if it is the AI's turn to move
        if (func.checkWin(simBoard, simCombinations, simCurPlayer.value)):
            return temp
        func.removePotential(simPlayerCombinations, simPlayerValues, temp.coordinates)
        simValues[temp.coordinates.x][temp.coordinates.y].thirdPriority = -1
        simPlayerValues[temp.coordinates.x][temp.coordinates.y].thirdPriority = -1

    #Recursively call this function with the updated values
    simCurPlayer.value = not simCurPlayer.value
    return SelectAndExpand(temp, untaken, simBoard, simValues, simPlayerValues, simCombinations, simPlayerCombinations, simCurPlayer)

def upPropegate(start, simResult):
    start.visited += 1
    start.score += simResult

    #Repeat if we are not at the head
    if (start != start.parent):
        upPropegate(start.parent, simResult * -1)


def downPropegate(start): 
    start.uct = (start.score / start.visited) + (1.414 * math.sqrt(math.log(start.parent.visited) / start.visited))
    for i in range(len(start.children)):
        downPropegate(start.children[i])


def getHighestUCT(nodes) :
    curUCT = -1000
    index = 0
    #print(f"This list has {len(nodes)} nodes")
    for i in range(len(nodes)):
        #print(f"Node UCT: {nodes[i].uct}")
        if (nodes[i].uct > curUCT):
            curUCT = nodes[i].uct
            index = i

    return nodes[index]
