class CoordinatePair:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        if(self.x == other.x and self.y == other.y):
            return True
        else:
            return False


class Value:
    def __init__(self, firstPriority, secondPriority, thirdPriority):
        self.firstPriority = firstPriority
        self.secondPriority = secondPriority
        self.thirdPriority = thirdPriority

    def __add__(self, other):
       	return Value(self.firstPriority+other.firstPriority, self.secondPriority+other.secondPriority, self.thirdPriority+other.thirdPriority)

    def __eq__(self, other):
        if (self.firstPriority == other.firstPriority and self.secondPriority == other.secondPriority and self.thirdPrority == other.thirdPrority):
            return True
        else:
            return False

    def __gt__(self, other):
        if ((self.firstPriority > other.firstPriority) or (self.firstPriority == other.firstPriority and self.secondPriority > other.secondPriority) or (self.firstPriority == other.firstPriority and self.secondPriority == other.secondPriority and self.thirdPriority > other.thirdPriority)):
            return True
        else:
            return False

class Node:
    def __init__(self, coordinates, visited, score, uct):
        self.coordinates = coordinates
        self.visited = visited
        self.score = score
        self.uct = uct
        self.parent = 0
        self.children = []
    def __eq__(self, other):
        if(self.coordinates.x == other.coordinates.x and self.coordinates.y == other.coordinates.y):
            return True
        else:
            return False
  

class Boolean:
    def __init__(self, value):
        self.value = value