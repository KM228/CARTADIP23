from seedhandler import SeedHandler
import random
import pygame
from spritesheet import Spritesheet
from typeHandler import TileTypes, tileType

class TileMap:
    mapSize = 0
    mainMap = []
    entrLoc = [0, 0]
    exitLoc = [0, 0]
    totalDifficulty = 0

    def __init__(self, mapSize, mapFormat):

        self.mapSize = mapSize
        self.mainMap = []

        if mapFormat == "Void":
            for i in range(self.mapSize):
                self.mainMap.append([])
            for i in self.mainMap:
                for j in range(self.mapSize):
                    i.append("VOID")
        elif mapFormat == "Empty":
            for i in range(self.mapSize):
                self.mainMap.append([])
            for i in self.mainMap:
                for j in range(self.mapSize):
                    i.append(Tile())
        elif mapFormat == "Random":
            self.randGenerate()
        elif mapFormat == "ID":
            self.randGenerate(False)

    def randGenerate(self, isRandom=True):

        if isRandom:
            coreSeed = SeedHandler.getRandom(self.mapSize**2+4)
        else:
            coreSeed = input("Enter a " + str(self.mapSize**2+4) + " digit code: ")

        print("Current Seed: " + str(coreSeed))

        for i in range(self.mapSize):
            self.mainMap.append([])
        for i in range(self.mapSize):
            for j in range(self.mapSize):
                subSeed = SeedHandler.decodeSeed(coreSeed)[j+(i*self.mapSize)]
                if (SeedHandler.exprSeed(subSeed)) == 0:
                    self.mainMap[i].append(Tile())
                elif (SeedHandler.exprSeed(subSeed)) == 1:
                    self.mainMap[i].append(HazTile())
                elif (SeedHandler.exprSeed(subSeed)) == 2:
                    self.mainMap[i].append(ChestTile())
                elif (SeedHandler.exprSeed(subSeed)) == 3:
                    self.mainMap[i].append(GemAdditionTile())
                elif (SeedHandler.exprSeed(subSeed)) == 4:
                    self.mainMap[i].append(GemMultiplyTile())
                elif (SeedHandler.exprSeed(subSeed)) == 5:
                    self.mainMap[i].append(GemSortingTile())
                elif (SeedHandler.exprSeed(subSeed)) == 6:
                    self.mainMap[i].append(GemSearchTile())
        #Uses seedHandler to generate and fill the map, represented by a 2D array
        for i in range(self.mapSize):
            for j in range(self.mapSize):
                self.totalDifficulty += self.mainMap[i][j].getDifficulty()
                #iterate through array to get total difficulty of map.



        random.seed(int(coreSeed[-1]))
        entrX = random.randint(0, self.mapSize-1)
        random.seed(int(coreSeed[-2]))
        entrY = random.randint(0, self.mapSize-1)
        n = 0
        while True:
            random.seed(int(coreSeed[-3]) + n)
            exitX = random.randint(0, self.mapSize-1)
            random.seed(int(coreSeed[-4]) + n)
            exitY = random.randint(0, self.mapSize-1)
            n += 1
            if (entrX != exitX) or (entrY != exitY):
                break
        self.mainMap[entrX][entrY] = Entrance()
        self.entrLoc = [entrX, entrY]
        self.mainMap[exitX][exitY] = Exit()
        self.exitLoc = [exitX, exitY]

    def getSize(self):
        return self.mapSize

    def getMap(self):
        return self.mainMap

    def showMap(self):

        for i in self.mainMap:
            for j in i:
                if type(j) == 'str':
                    print(j)
                else:
                    print(str(j), end=" \t ")
            print("")

        print("Total Difficulty Rating: " + str(self.totalDifficulty), end=" (")
        starRating = (self.totalDifficulty / (self.mapSize ** 2))
        print("*" * int(starRating) + ")")
        #Returns difficulty rating of a generated map as both a numerical value, and on a scale of 1 to 5 stars

        """
        out = ""
        if Tile == (self.mainMap[x][y]).__bases__:
            for x in range(self.mapSize):
                 for y in range(self.mapSize):
                    out += "[" + str(self.mainMap[x][y]) + "]" + "\t"

                out += "\n"
        else:
            for x in range(self.mapSize):
                for y in range(self.mapSize):
                    out += "[" + str(self.mainMap[x][y]) + "]" + "\t"

                out += "\n"

        print (out)
        """

    def getStart(self):
        return self.entrLoc
    def getEnd(self):
        return self.exitLoc

    def getTile(self, x, y):
        return self.mainMap[x][y]

    def animate(self):
        pass


class Tile:
    type = ""
    difficulty = 1
    isActive = False
    isPuzzle = False
    isAnimated = False
    animCD = 0
    frameCounter = 0
    numFrames = 0

    image = pygame.image.load('sprites/empty.png')
    my_spritesheet = Spritesheet('sprites/empty.png')

    def __init__(self):
        self.type = TileTypes.EMPTY
        self.difficulty = 0
        self.isActive = False
        self.isPuzzle = False
        self.image = pygame.image.load('sprites/empty.png')
        self.my_spritesheet = Spritesheet('sprites/empty.png')
        self.isAnimated = False
        self.animCD = random.randint(6, 24)
        self.frameCounter = 0
        self.numFrames = 0

    def __str__(self):
        return "[" + tileType[self.type] + "]"

    def getType(self):
        return self.type

    def getDifficulty(self):
        return self.difficulty

    def getImage(self):
        return self.image

    def checkActive(self):
        return self.isActive

    def checkPuzzle(self):
        return self.isPuzzle

    #def trySolve(self, plrAns):
        #pass

    def updtImage(self):
        #print(str(self) + str(self.animCD))
        if self.isAnimated and self.animCD <= 0:
            if self.frameCounter < self.numFrames:
                self.frameCounter += 1
            else:
                self.frameCounter = 0
                self.animCD = random.randint(6, 24)
            self.image = self.my_spritesheet.get_sprite((16 * self.frameCounter), 0, 16, 16)
        if self.isAnimated:
            self.animCD -= 1

    def resetImage(self):
        self.image = pygame.image.load('sprites/empty.png')
        self.type = TileTypes.EMPTY


class ChestTile(Tile):

    value = 5

    def __init__(self):
        self.type = TileTypes.CHEST
        self.isPuzzle = True
        self.difficulty = 1
        self.image = pygame.image.load('sprites/chest.png')

    def use(self, player):
        print(str(self.value) + " points awarded")
        player.myScore += self.value
        self.isPuzzle = False
        self.resetImage()


class GemAdditionTile(Tile):
    def __init__(self):
        self.type = TileTypes.GEM
        self.isPuzzle = True
        self.isAnimated = True
        self.difficulty = 2
        self.my_spritesheet = Spritesheet('sprites/tileSpritesheets/gemPuzzleSheet.png')
        self.numFrames = 4
        self.value = 10

        self.puzzleInfo = [random.randint(0, 999), random.randint(0, 999)]
        self.puzzleSolution = self.puzzleInfo[0] + self.puzzleInfo[1]

    def use(self, player):
        self.player = player
        player.recPuzzle(self.puzzleInfo, "Addition")

    def trySolve(self, plrAns):
        if plrAns == self.puzzleSolution:
            print(str(self.value) + " points awarded")
            self.player.myScore += self.value
            self.player.hasPuzzle = False
            self.isPuzzle = False
            self.isAnimated = False
            self.resetImage()
        else:
            print("That wasn't the right answer...")


class GemMultiplyTile(Tile):
    def __init__(self):
        self.type = TileTypes.GEM
        self.isPuzzle = True
        self.isAnimated = True
        self.difficulty = 2
        self.my_spritesheet = Spritesheet('sprites/tileSpritesheets/redGem.png')
        self.numFrames = 4
        self.value = 15

        self.puzzleInfo = [random.randint(0,999), random.randint(0,999)]
        self.puzzleSolution = self.puzzleInfo[0] * self.puzzleInfo[1]

    def use(self, player):
        self.player = player
        player.recPuzzle(self.puzzleInfo, "Multiplication")

    def trySolve(self, plrAns):
        if plrAns == self.puzzleSolution:
            print(str(self.value) + " points awarded")
            self.player.myScore += self.value
            self.player.hasPuzzle = False
            self.isPuzzle = False
            self.isAnimated = False
            self.resetImage()
        else:
            print("That wasn't the right answer...")


class GemSortingTile(Tile):
    def __init__(self):
        self.type = TileTypes.GEM
        self.isPuzzle = True
        self.isAnimated = True
        self.difficulty = 4
        self.my_spritesheet = Spritesheet('sprites/tileSpritesheets/greenGem.png')
        self.numFrames = 4
        self.value = 25

        self.puzzleInfo = []
        for i in range(random.randint(0, 10)):
            self.puzzleInfo.append(random.randint(0, 999))
        self.puzzleSolution = []
        for i in self.puzzleInfo:
            self.puzzleSolution.append(i)
        n = len(self.puzzleSolution)
        for i in range(n):
            for j in range(0, (n - i) - 1):

                if self.puzzleSolution[j] > self.puzzleSolution[j + 1]:
                    self.puzzleSolution[j], self.puzzleSolution[j + 1] = self.puzzleSolution[j + 1], self.puzzleSolution[j]

    def use(self, player):
        self.player = player
        player.recPuzzle(self.puzzleInfo, "Ascending Sort")

    def trySolve(self, plrAns):
        if plrAns == self.puzzleSolution:
            print(str(self.value) + " points awarded")
            self.player.myScore += self.value
            self.player.hasPuzzle = False
            self.isPuzzle = False
            self.isAnimated = False
            self.resetImage()
        else:
            print("That wasn't the right answer...")


class GemSearchTile(Tile):
    def __init__(self):
        self.type = TileTypes.GEM
        self.isPuzzle = True
        self.isAnimated = True
        self.difficulty = random.randint(3, 5)
        self.my_spritesheet = Spritesheet('sprites/tileSpritesheets/orangeGem.png')
        self.numFrames = 4
        self.value = 25

        self.puzzleInfo = []
        self.puzzleSolution = []
        for i in range(2*self.difficulty - random.randint(0,1)):
            self.puzzleInfo.append(random.randint(0, 999999999))
        self.solIndex = random.randint(0, len(self.puzzleInfo) - 1)
        self.puzzleSolution = self.solIndex

    def use(self, player):
        self.player = player
        player.recPuzzle(self.puzzleInfo, ("What is the index of [" + str(self.puzzleInfo[self.solIndex]) + "]? [Integer]"))

    def trySolve(self, plrAns):
        if plrAns == self.puzzleSolution:
            print(str(self.value) + " points awarded")
            self.player.myScore += self.value
            self.player.hasPuzzle = False
            self.isPuzzle = False
            self.isAnimated = False
            self.resetImage()
        else:
            print("That wasn't the right answer...")


class HazTile(Tile):

    def __init__(self):
        self.type = TileTypes.HAZARD
        self.difficulty = 1
        self.image = pygame.image.load('sprites/spikeFloor.png')


class Entrance(Tile):

    def __init__(self):
        self.type = TileTypes.ENTRY
        self.difficulty = 0
        self.image = pygame.image.load('sprites/greenFlag.png')


class Exit(Tile):

    def __init__(self):
        self.type = TileTypes.EXIT
        self.difficulty = 0
        self.image = pygame.image.load('sprites/redFlag.png')
