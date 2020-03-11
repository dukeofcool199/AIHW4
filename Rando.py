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
        self.me = inputPlayerId
        self.enemy = 1 - inputPlayerId

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

            moves = [] 
            moves.append(Gene.geneList[Gene.geneIndex].hillLoc)
            moves.append(Gene.geneList[Gene.geneIndex].tunnelLoc)
            for grass in Gene.geneList[Gene.geneIndex].grassLocs:
                moves.append(grass)
            return moves 
            
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side

            moves = [] 
            food1 = Gene.geneList[Gene.geneIndex].foodLocs[0]
            food2 = Gene.geneList[Gene.geneIndex].foodLocs[1]
            moves.append(MyUtils.findClosestEmpty(currentState,food1[0],food1[1]))
            moves.append(MyUtils.findClosestEmpty(currentState,food2[0],food2[1])) 
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
        theGene = Gene.geneList[Gene.geneIndex]
        if hasWon:
            theGene.fitness + 1
        if theGene.numEvals == Gene.MAX_EVALS:
            Gene.geneIndex += 1
        else:
            Gene.numEvals += 1

        #if we have evaluated all the genes then start making a new population
        if Gene.geneIndex > Gene.POPULATION_SIZE: 
            pass

            


class Gene():
    
    POPULATION_SIZE = 2
    MAX_EVALS = 3
    NUM_GRASS = 9 
    NUM_FOOD = 2

    geneList = []
    geneIndex = 0

    def __init__(self,hillLoc=None,tunnelLoc=None,grassLocs=None,eFoodLocs=None):
        self.hillLoc = hillLoc
        self.tunnelLoc = tunnelLoc
        self.grassLocs = grassLocs
        self.foodLocs = eFoodLocs
        self.fitness = 0
        self.numEvals = 0
        self.occupiedSpots = []

    def toString(self):

        output = "hill: {} \n tunnel: {} \n grass: {} \n food: {} \n fitness: {} \n evals: {} \n spots: {}".format(self.hillLoc,self.tunnelLoc,join(map(str,self.grassLocs)),join(map(str,self.foodLocs)),self.fitness,self.numEvals)


    def toLocationList(self):
        return [self.hillLoc,self.tunnelLoc,self.grassLocs,self.foodLocs]

    def importLocations(self,locations):
        self.hillLoc = locations[0]
        self.tunnelLoc = locations[1]
        self.grassLocs = locations[2]
        self.foodLocs = foodLocs


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
    def makeBabies(dad,mom):

        dadList = dad.toLocationList()
        momList = mom.toLocationList()










        # brother = Gene()
        # sister = Gene()


        # brotherGenes=[random.random(),random.random(),random.random(),random.random(),]
        # sisterGenes=[random.random(),random.random(),random.random(),random.random(),]


        # for x in range(4):
            # if brotherGenes[x] >= .50:
                # if x = 0: 
                    # brother.hillLoc = dad.hillLoc
                # elif x = 1:
                    # brother.tunnelLoc = dad.tunnelLoc 
                # elif x = 2:
                    # brother.grassLocs = dad.grassLocs

                # elif x = 3:


        # hillGeneBrother = random.random()
        # hillGeneSister = random.random()
        # tunnelGeneBrother = random.random()
        # tunnelGeneSister = random.random()
        # grassGeneBrother = random.random()
        # grassGeneSister = random.random()
        # foodGeneBrother = random.random()
        # foodGeneSister = random.random()
        #get the split value to dispere the mommy and daddy genes
        



    @staticmethod
    def makeNewPopulation(oldPeople):

        fitPeople = sorted(oldPeople,key=lambda x: x.fitness)
        #take the top 50 percent in terms of fitness
        fitPeople = fitPeople[len(fitPeople)/2:]

        newPop = []
        while len(newPop) < Gene.POPULATION_SIZE:
            #pick two parents to mate

            dadIndex = random.randint(0,len(fitPeople))
            dad = fitPeople[dadIndex]

            momIndex = random.randint(0,len(fitPeople))
            while momIndex != dadIndex:
                momIndex = random.randint(0,len(fitPeople))
            mom = fitPeople[momIndex]

            babies = Gene.makeBabies(dad,mom)
            newPop.append(babies[0])
            newPop.append(babies[1])

        Gene.geneList = newPop




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
    def spotTaken(currentState,moves):
        if currentState.board[x][y].constr == None :
            return True
        else:
            return False

    ## findClosestEmpty
    @staticmethod
    def findClosestEmpty(currentState,x,y,whosSide="enemy"):

        if getConstrAt(currentState,(x,y)) == None:
            return (x,y)

        if whosSide=="me":
            miny = 0
            maxy = 3
        else:
            miny = 6
            maxy = 9 
        
        #check to left
        for spot in range(x,0,-1):
            closest = getConstrAt(currentState,(spot,y))
            if closest == None:
                return (spot,y)
        #check to right 
        for spot in range(x,9):
            closest = getConstrAt(currentState,(spot,y))
            if closest == None:
                return (spot,y)
        #check up
        for spot in range(y,minY,-1):
            closest = getConstrAt(currentState,(x,spot))
            if closest == None:
                return (x,spot)

        # check down
        for spot in range(y,maxY):
            closest = getConstrAt(currentState,(x,spot))
            if closest == None:
                return (x,spot)



Gene.populationInit()
asciiPrintState(GameState.getBasicState())
