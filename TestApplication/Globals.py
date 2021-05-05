#Variables to alter game
width = 19
n = 5
numberOfSimulations = 50
playingAgainstMCTS = True

#Variance identifies the max range of possible moves the game can explore.
#If you want it to make less value-centric moves and focus instead on exploring, increase these variables.
#If you want to make generally tighter, less exploratory moves, decrease these variables.

#Max allowed variance of the First Priority.  Should probably not make this variable than 2
FIRST_VARIANCE = 0
#Max allowed variance of the Second Priority.  
SECOND_VARIANCE = 0