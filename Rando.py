import random
import sys
sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
from AIPlayerUtils import *


##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "Rando")


    ##
    #mateGenes
    #parameters:
    # daddyGene: the first gene
    # mommyGene: the second gene
    #description:
    # creates 2 child genes after mating 
    # and mutating from parent genes
    def mateGenes(daddyGene,mommyGene):
        pass

    ##
    #getPlacement
    #
    #Description: called during setup phase for each Construction that
    #   must be placed by the player.  These items are: 1 Anthill on
    #   the player's side; 1 tunnel on player's side; 9 grass on the
    #   player's side; and 2 food on the enemy's side.
    #
    #Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, currentState):
        # numToPlace = 0
        # #implemented by students to return their next move
        if currentState.phase == SETUP_PHASE_1:    #stuff on my side
            # numToPlace = 11
            # moves = []
            # for i in range(0, numToPlace):
                # move = None
                # while move == None:
                    # #Choose any x location
                    # x = random.randint(0, 9)
                    # #Choose any y location on your side of the board
                    # y = random.randint(0, 3)
                    # #Set the move if this space is empty
                    # if currentState.board[x][y].constr == None and (x, y) not in moves:
                        # move = (x, y)
                        # #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        # currentState.board[x][y].constr == True
                # moves.append(move)
            # return moves

            moves = [] 
            moves.append(Gene.geneList[Gene.geneIndex].hillLoc)
            moves.append(Gene.geneList[Gene.geneIndex].tunnelLoc)
            for grass in Gene.geneList[Gene.geneIndex].grassLocs:
                moves.append(grass)
            return moves 
            
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side
            # numToPlace = 2
            # moves = []
            # for i in range(0, numToPlace):
                # move = None
                # while move == None:
                    # #Choose any x location
                    # x = random.randint(0, 9)
                    # #Choose any y location on enemy side of the board
                    # y = random.randint(6, 9)
                    # #Set the move if this space is empty
                    # if currentState.board[x][y].constr == None and (x, y) not in moves:
                        # move = (x, y)
                        # #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        # currentState.board[x][y].constr == True
                # moves.append(move)
            # return moves
        # else:
            # return [(0, 0)]
            moves = [] 
            moves.append(Gene.geneList[Gene.geneIndex].foodLocs[0])
            moves.append(Gene.geneList[Gene.geneIndex].foodLocs[1])
            return moves
    
    ##
    #getMove
    #Description: Gets the next move from the Player.
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):
        moves = listAllLegalMoves(currentState)
        selectedMove = moves[random.randint(0,len(moves) - 1)];

        #don't do a build move if there are already 3+ ants
        numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
        while (selectedMove.moveType == BUILD and numAnts >= 3):
            selectedMove = moves[random.randint(0,len(moves) - 1)];
            
        return selectedMove
    
    ##
    #getAttack
    #Description: Gets the attack to be made from the Player
    #
    #Parameters:
    #   currentState - A clone of the current state (GameState)
    #   attackingAnt - The ant currently making the attack (Ant)
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        #Attack a random enemy.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]

    ##
    #registerWin
    #
    # This agent doens't learn
    #
    def registerWin(self, hasWon):
        #method templaste, not implemented
        pass

class Gene():
    
    POPULATION_SIZE = 2
    NUM_EVALS = 2
    NUM_GRASS = 9 
    NUM_FOOD = 2

    geneList = []
    geneIndex = 0

    def __init__(self,hillLoc=None,tunnelLoc=None,grassLocs=None,eFoodLocs=None,fitness=0,numEvals=0):
        self.hillLoc = hillLoc
        self.tunnelLoc = tunnelLoc
        self.grassLocs = grassLocs
        self.FoodLocs = eFoodLocs
        self.fitness = fitness
        self.numEvals = numEvals
        self.occupiedSpots = []

    def toString(self):

        output = "hill: {} \n tunnel: {} \n grass: {} \n food: {} \n fitness: {} \n evals: {} \n spots: {}".format(self.hillLoc,self.tunnelLoc,join(map(str,self.grassLocs)),join(map(str,self.foodLocs)),self.fitness,self.numEvals)


    def mutate(self):
        pass

    ##
    #makeBabies
    #parameters:
    # daddyGene: the first gene
    # mommyGene: the second gene
    #description:
    # creates 2 child genes after mating 
    # and mutating from parent genes
    @staticmethod
    def makeBabies(daddyGene,mommyGene):
        brother = Gene()
        sister = Gene()

        hillGeneBrother = random.random()
        hillGeneSister = random.random()
        tunnelGeneBrother = random.random()
        tunnelGeneSister = random.random()
        #get the split value to dispere the mommy and daddy genes


    @staticmethod
    def makeNewPopulation(oldPeople): 
        newPeople = None


    ##
    #populationInit
    # parameters:
    # self
    #Description:
    # randomnly generates gene attribute values for the start of the learning session
    # and resets all fitness values to 0
    @staticmethod
    def populationInit():
        occupiedSpots = []

        for x in range(Gene.POPULATION_SIZE): 

            hillPlacement = Gene.pickASpotMe() 
            occupiedSpots.append(hillPlacement)


            tunnelPlacement = Gene.pickASpotMe()
            while tunnelPlacement in occupiedSpots:
                tunnelPlacement = Gene.pickASpotMe()
            occupiedSpots.append(tunnelPlacement)

            grassCoords = []
            for x in range(Gene.NUM_GRASS):
                grassPlacement = Gene.pickASpotMe() 
                while grassPlacement in occupiedSpots:
                    grassPlacement = Gene.pickASpotMe()
                grassCoords.append(grassPlacement) 
                occupiedSpots.append(grassPlacement)

            foodCoords = []
            for x in range(Gene.NUM_FOOD):
                foodPlacement = Gene.pickASpotEnemy()
                while foodPlacement in occupiedSpots:
                    foodPlacement = Gene.pickASpotEnemy()
                foodCoords.append(foodPlacement) 
                occupiedSpots.append(foodPlacement)

            Gene.geneList.append(Gene(hillPlacement,tunnelPlacement,grassCoords,foodCoords))

    
    @staticmethod
    def pickASpotMe():
            return (random.randint(0,9),random.randint(0,3))

    @staticmethod
    def pickASpotEnemy():
            return (random.randint(0,9),random.randint(6,9)) 

    def locationUsed(coords):
        if coords in self.occupiedSpots:
            return True
        else:
            return False


class MyUtils(): 

    @staticmethod
    def spotTaken(currentState):
        if currentState.board[x][y].constr == None :
            return True
        else:
            return False

    ## findClosestEmpty
    @staticmethod
    def findClosestEmpty(x,y,currestState,whosSide="me"):
        if whosSide=="me":
            miny = 0
            maxy = 3
        else:
            miny = 6
            maxy = 9




        


        

Gene.populationInit()
