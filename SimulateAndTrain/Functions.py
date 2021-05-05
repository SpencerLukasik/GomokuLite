import Globals as g
import Classes as c

def checkWin(board, combinations, curPlayer):
    winDetected = False
    for i in range(len(combinations)):
        winDetected = True
        for j in range(len(combinations[i])):
            if (curPlayer):
                if (board[combinations[i][j].x][combinations[i][j].y] != 1):
                    winDetected = False
                    break
            else:
                if (board[combinations[i][j].x][combinations[i][j].y] != 2):
                    winDetected = False
                    break

        if (winDetected):
            return True
    return False

def make_move(board, combinations, playerCombinations, values, playerValues, curPlayer, move):
    if (curPlayer):
        board[move.x][move.y] = 1
        values[move.x][move.y].thirdPriority = -1
        playerValues[move.x][move.y].thirdPriority = -1
        removePotential(combinations, values, move)
    else:
        board[move.x][move.y] = 2
        values[move.x][move.y].thirdPriority = -1
        playerValues[move.x][move.y].thirdPriority = -1
        removePotential(playerCombinations, playerValues, move)

def updateValues(board, combinations, values, curPlayer):
      #Creates the combination values, or the greatest number of positions that have been taken within a valid combination
  for i in range(g.width):
    for j in range(g.width):
      values[i][j].firstPriority = 0
      values[i][j].secondPriority = 0
    

  #Aggressive moves
  #Populate First Priority.  Get the highest value combos and set that entire menomial's first
  #priority value to that high value.
  temp = 0
  highest = 0
  for i in range(len(combinations)):
    for j in range(len(combinations[i])):
        #If AI is black
        if (board[combinations[i][j].x][combinations[i][j].y] == 1):
          temp += 1
        elif (board[combinations[i][j].x][combinations[i][j].y] == 2):
          temp += 1
    for j in range(len(combinations[i])):
      if (values[combinations[i][j].x][combinations[i][j].y].firstPriority < temp):
        values[combinations[i][j].x][combinations[i][j].y].firstPriority = temp
  
    if (temp > highest):
      highest = temp
    temp = 0

  #Populate Second Priority.  Check if a single combo has a value in it that contains a combination
  #of the highest first priority.  For every node in that combo, increment it's second potential by 1.
  for i in range(len(combinations)): 
    for j in range(len(combinations[i])): 
      if (board[combinations[i][j].x][combinations[i][j].y] == 1 and values[combinations[i][j].x][combinations[i][j].y].firstPriority == highest):
        for k in range(len(combinations[i])):
          values[combinations[i][k].x][combinations[i][k].y].secondPriority += 1
      elif (board[combinations[i][j].x][combinations[i][j].y] == 2 and values[combinations[i][j].x][combinations[i][j].y].firstPriority == highest):
        for k in range(len(combinations[i])):
          values[combinations[i][k].x][combinations[i][k].y].secondPriority += 1


def removePotential(combinations, values, newCoordinate):
  i = 0
  while (i<len(combinations)):
    #Find all combinations that have the coordinate and remove them from the possible winning configurations
    if (newCoordinate in combinations[i]): 
      #Deduct potential points from coordinates connected to the removed coordinate
      for j in range(len(combinations[i])):
        if (values[combinations[i][j].x][combinations[i][j].y].thirdPriority > -1):
          values[combinations[i][j].x][combinations[i][j].y].thirdPriority -= 1
      combinations.pop(i)
      i = i - 1
    i = i + 1


def populate(combinations, potential):
  for i in range(g.width):
    for j in range(g.width):
      potential[j][i] = c.Value(1, 0, 0)

  curIndex = 0
  for i in range(g.width):
    for j in range(g.width):
      #Check Horizontal wins
      if (j + (g.n - 1) < g.width):
        combinations.append([0]*g.n)

        for k in range(g.n):
          combinations[curIndex][k] = (c.CoordinatePair(j + k, i))
          potential[j + k][i].thirdPriority += 1

        curIndex += 1

      #Check Vertical wins
      if (i + (g.n - 1) < g.width):
        combinations.append([0]*g.n)

        for k in range(g.n):
          combinations[curIndex][k] = (c.CoordinatePair(j, i + k))
          potential[j][i + k].thirdPriority += 1
      
        curIndex += 1
      
      #Check Up-Right wins
      if (j + (g.n - 1) < g.width and i - (g.n - 1) >= 0):
        combinations.append([0]*g.n)

        for k in range(g.n):
          combinations[curIndex][k] = (c.CoordinatePair(j + k, i - k))
          potential[j + k][i - k].thirdPriority += 1

        curIndex += 1
      
      #Check Down-Right wins
      if (j + (g.n - 1) < g.width and i + (g.n - 1) < g.width):
        combinations.append([0]*g.n)

        for k in range(g.n):
          combinations[curIndex][k] = (c.CoordinatePair(j + k, i + k))
          potential[j + k][i + k].thirdPriority += 1

        curIndex += 1

def copy2DList(origin, copy):
  for i in range(len(origin)):
    for j in range(len(origin[i])):
        copy[i][j] = origin[i][j]

def copyCombination(origin, copy):
  for i in range(len(origin)):
    copy.append([0]*g.n)
    for j in range(len(origin[i])):
      copy[i][j] = origin[i][j]

def copy2DValue(origin, copy):
  for i in range(len(origin)):
    for j in range(len(origin[i])):
        copy[i][j] = c.Value(origin[i][j].firstPriority, origin[i][j].secondPriority, origin[i][j].thirdPriority)
def drawBoard(board):
    print("   ", end='')
    for i in range(g.width):
        print(" ", end='')
        if (i < 10):
            print(" ", end='')
        print(f"{i} ", end='')
    
    print("")
    print("   ", end='')
    for i in range(g.width):
        print("----", end='')
    print("")

    for i in range(g.width):
        print(f"{i} ", end='')
        if (i < 10):
            print(" ", end='')
        for j in range(g.width):
            if (board[i][j] == 1):
                print("| o ", end='')
            elif (board[i][j] == 2):
                print("| x ", end='')
            else:
                print("|   ", end='')
    
        print("|", end='')
        print("")

        #Bottom of each line
        print("   ", end='')
        for j in range(g.width):
            print("----", end='')
        print("")