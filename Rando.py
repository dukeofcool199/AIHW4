import random
import sys
import time

from src.AIPlayerUtils import listAllLegalMoves

sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
from AIPlayerUtils import *
from datetime import datetime

POPULATION_SIZE = 50 
MAX_EVALS = 10 
FOOD1 = 11
FOOD2 = 12
FOOD_SPLIT = 11
FITNESS = 13
EVAL = 14
STATE = 15

geneIndex = 0
geneList = []


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

    #the number of turns it took random to lose to booger, or at least untill the game ended
    turnsToEnd = 0
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
        self.firstTurn = True
        self.state = None

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
        self.firstTurn = True
        if currentState.phase == SETUP_PHASE_1:    #stuff on my side
            moves = geneList[geneIndex][:FOOD_SPLIT]
            return moves
            
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side
            geneList[geneIndex][11] = findClosestEmpty(currentState,geneList[geneIndex][11])
            geneList[geneIndex][12] = findClosestEmpty(currentState,geneList[geneIndex][12])
            moves = geneList[geneIndex][FOOD_SPLIT:FITNESS]

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
        if self.firstTurn:
            self.firsTurn = False
            self.state = currentState
        moves = listAllLegalMoves(currentState)
        selectedMove = moves[random.randint(0,len(moves) - 1)];

        #don't do a build move if there are already 3+ ants
        numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
        while (selectedMove.moveType == BUILD and numAnts >= 3):
            selectedMove = moves[random.randint(0,len(moves) - 1)];

        if selectedMove.moveType == END:
            geneList[geneIndex][FITNESS] += 1
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
        global geneIndex
        geneList[geneIndex][EVAL] += 1
        if geneList[geneIndex][EVAL] >= MAX_EVALS:
            geneList[geneIndex].append(self.state)
            geneIndex += 1
        #if we have evaluated all the genes then start making a new population
        if geneIndex > POPULATION_SIZE-1:
            makeNewPopulation()
            geneIndex = 0


def mutate(self, gene):
    if random.random() > .20:
        gene[random.randint(0,FOOD_SPLIT)] = None
        gene[random.randint(0,FOOD_SPLIT)] = pickASpotMe(gene)
        
    return gene 


##
#makeBabies
#parameters:
# daddyGene: the first gene
# mommyGene: the second gene
#description:
# creates 2 child genes after mating from parent genes
def makeBabies(self,dad,mom):
    split = random.randint(0,11)
    dadSplitB = dad[:split]
    momSplitB = mom[split:FOOD1]

    momSplitS = mom[:split]
    dadSplitS = dad[split:FOOD1]

    brother = []
    sister = []

    brother.extend(dadSplitB)
    brother.extend(momSplitB)

    sister.extend(momSplitS)
    sister.extend(dadSplitS)

    brother.extend((dad[FOOD1],mom[FOOD2]))

    sister.extend((mom[FOOD1],dad[FOOD2]))

    brother.append(0)
    brother.append(0)
    sister.append(0)
    sister.append(0)
    return(brother,sister)

def makeNewPopulation():
    global geneList
    oldPeople = geneList.copy()
    fitPeople = sorted(oldPeople,key=lambda x: x[FITNESS])
    #take the top 50 percent in terms of fitness
    index = int(len(fitPeople)/2)
    fitPeople = fitPeople[index:]

    with open('evidence.txt',"a") as file:
        print("================\n")
        asciiPrintState(fitPeople[len(fitPeople)-1][STATE])
        print("eval score: {}".format(fitPeople[len(fitPeople)-1][FITNESS]))

    with open('fitGenes.txt', "a") as file:
        file.write("================\n")
        for person in fitPeople: 
            file.write("fitness: {}".format(person[FITNESS])) 
        file.write("================\n")
    newPop = []
    while len(newPop) < POPULATION_SIZE:
        #pick two parents to mate

        dadIndex = random.randint(0,len(fitPeople)-1)
        dad = fitPeople[dadIndex]

        momIndex = random.randint(0,len(fitPeople)-1)
        while momIndex == dadIndex:
            momIndex = random.randint(0,len(fitPeople)-1)
        mom = fitPeople[momIndex]

        babies = makeBabies(dad,mom)
        newPop.append(babies[0])
        newPop.append(babies[1])

    for kid in newPop:
        kid = mutate(kid)

    geneList = newPop


def pickASpotMe(self,locs):
        loc = (random.randint(0,9),random.randint(0,3))
        while loc in locs:
            if not spotTaken(self.state,loc):
                loc = (random.randint(0,9),random.randint(0,3))
        return loc

def pickASpotFood(self,locs):
        loc = (random.randint(0,9),random.randint(6,9))
        while loc in locs:
            if not spotTaken(self.state,loc):
                loc = (random.randint(0,9),random.randint(6,9))
        return loc


def spotTaken(currentState,spot):
    if currentState.board[spot[0]][spot[1]].constr == None :
        return True
    else:
        return False

## findClosestEmpty
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
    for spot in range(coords[1],miny,-1):
        closest = getConstrAt(currentState,(coords[0],spot))
        if closest == None:
            return (coords[0],spot)

    # check down
    for spot in range(coords[1],maxy):
        closest = getConstrAt(currentState,(coords[0],spot))
        if closest == None:
            return (coords[0],spot)

##
#populationInit
# parameters:
# self
#Description:
# randomnly generates gene attribute values for the start of the learning session
# and resets all fitness values to 0
def populationInit():
    genes = []
#for x in range(Gene.POPULATION_SIZE):
    for x in range(POPULATION_SIZE):
        currentGene = []
        for x in range(11):
            currentGene.append(pickASpotMe(currentGene, locs = []))
        for x in range(2):
            currentGene.append(pickASpotFood(currentGene, locs = []))
        #insert 0 for fitness
        currentGene.append(0)
        #insert 0 for number of times evaluated
        currentGene.append(0)
        genes.append(currentGene)

    return genes




geneList = populationInit()

