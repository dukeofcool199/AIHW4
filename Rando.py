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

            return Gene.geneList[Gene.geneIndex].constructs
            
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side

            theGene = Gene.geneList[Gene.geneIndex]
            theGene.food[0] = MyUtils.findClosestEmpty(currentState,theGene.food[0])
            theGene.food[1] = MyUtils.findClosestEmpty(currentState,theGene.food[1])
            return Gene.geneList[Gene.geneIndex].food
    
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
            theGene.fitness += 1
        theGene.numEvals += 1
        if theGene.numEvals >= Gene.MAX_EVALS:
            Gene.geneIndex += 1
            print("the new gene {}".format(Gene.geneIndex)) 
        #if we have evaluated all the genes then start making a new population
        if Gene.geneIndex > Gene.POPULATION_SIZE-1: 
            print("make new genes")
            Gene.makeNewPopulation()
            Gene.geneIndex = 0

            


class Gene():
    
    POPULATION_SIZE = 3 
    MAX_EVALS = 3

    geneList = []
    geneIndex = 0

    def __init__(self,constructs=[],food=[]):
        self.constructs = constructs
        self.food = food
        self.fitness = 0
        self.numEvals = 0

        self.occupiedSpots = []


    def mutate(self):
        pass

    ##
    #makeBabies
    #parameters:
    # daddyGene: the first gene
    # mommyGene: the second gene
    #description:
    # creates 2 child genes after mating from parent genes
    @staticmethod
    def makeBabies(dad,mom):
        split = random.randint(0,11)
        dadsplitB = dad.constucts[:split]
        momSplitB = mom.constructs[split:] 

        momSplitS = mom.constructs[:split]
        dadSplitS = dad.constructs[split:]

        brother = Gene() 
        sister = Gene() 

        brother.constructs.append(dadSplitB)
        brother.constructs.append(momSplitB)

        sister.constucts.append(momSplitS)
        sister.constucts.append(dadSplitS) 
        
        brother.food.append(dad.food[0])
        brother.food.append(mom.food[1])

        sister.food.append(mom.food[0])
        brother.food.append(dad.food[1])

        return(brother,sister)



    @staticmethod
    def makeNewPopulation():

        oldPeople = GeneList.copy()
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

        for x in range(Gene.POPULATION_SIZE): 

            newGene = Gene()
            newGene.constructs.clear()
            newGene.food.clear()
            for x in range(11): 
                coord = (random.randint(0,9),random.randint(0,3))
                while coord in newGene.constructs:
                    coord = None
                    coord = (random.randint(0,9),random.randint(0,3)) 
                newGene.constructs.append(coord)
            for x in range(2):
                coord = (random.randint(0,9),random.randint(6,9))
                while coord in newGene.food:
                    coord = None
                    coord = (random.randint(0,9),random.randint(6,9)) 
                newGene.food.append(coord)


            Gene.geneList.append(newGene)
            newGene = None

    
    
    def pickASpotMe(self): 
            loc = (random.randint(0,9),random.randint(0,3))
            while loc in self.constructs:
                loc = (random.randint(0,9),random.randint(0,3)) 
            return loc

    def pickASpotFood(self):
            loc = (random.randint(0,9),random.randint(6,9)) 
            while loc in self.food:
                loc = (random.randint(0,9),random.randint(6,9)) 
            return loc
                

class MyUtils(): 

    @staticmethod
    def spotTaken(currentState,moves):
        if currentState.board[x][y].constr == None :
            return True
        else:
            return False

    ## findClosestEmpty
    @staticmethod
    def findClosestEmpty(currentState,coords,whosSide="enemy"):

        if getConstrAt(currentState,coords) == None:
            return coords

        if whosSide=="me":
            miny = 0
            maxy = 3
        else:
            miny = 6
            maxy = 9 
        
        #check to left
        for spot in range(coords[0],0,-1):
            closest = getConstrAt(currentState,(spot,coords[1]))
            if closest == None:
                return (spot,coords[1])
        #check to right 
        for spot in range(coords[0],9):
            closest = getConstrAt(currentState,(spot,coords[1]))
            if closest == None:
                return (spot,coords[1])
        #check up
        for spot in range(coords[1],minY,-1):
            closest = getConstrAt(currentState,(coords[0],spot))
            if closest == None:
                return (coords[0],spot)

        # check down
        for spot in range(coords[1],maxY):
            closest = getConstrAt(currentState,(coords[0],spot))
            if closest == None:
                return (coords[0],spot)



Gene.populationInit()
