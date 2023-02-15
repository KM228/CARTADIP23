import time

import random
import pygame
import threading
from threading import Thread
from pygame.locals import *
from enum import Enum, auto
from spritesheet import Spritesheet
from typeHandler import TileTypes, tileType
from tiles import TileMap

class Player:

    #image = pygame.image.load("sprites/playerSprites/littleGuy.png")
    joy = False
    facing = 0 # (0 East) (1 South) (2 West) (3 North)
    mPos = [0, 0]
    myMap = TileMap
    my_spritesheet = Spritesheet("sprites/playerSprites/lilGuyGsheet.png")
    currentSprite = my_spritesheet.get_sprite(0, 0, 16, 16)
    frameCounter = 0
    actionCD = 0.75

    myScore = 0
    currentPuzzle = []
    hasPuzzle = False
    puzzleType = ""

    def __init__(self, tileMap):
        self.joy = True
        self.facing = 0
        self.myMap = tileMap
        self.mPos = tileMap.getStart()
        print (self.mPos)
        self.myScore = 0
        self.lifetime = 0

    def turnTick(self):
        time.sleep(self.actionCD)
        self.lifetime += 1

    def walk(self):
        self.turnTick()
        pos = self.mPos
        if self.facing == 0:
            pos[0] = (pos[0] + 1)
            print("Moving East!")
        elif self.facing == 1:
            pos[1] = (pos[1] + 1)
            print("Moving South!")
        elif self.facing == 2:
            pos[0] = (pos[0] - 1)
            print("Moving West!")
        else:
            pos[1] = (pos[1] - 1)
            print("Moving North!")

        if pos[0] < 0:
            pos[0] = 0
            print("Too far left")
        elif pos[0] >= self.myMap.getSize():
            pos[0] = self.myMap.getSize()-1
            print("Too far right")
        if pos[1] < 0:
            pos[1] = 0
            print("Too far up")
        elif pos[1] >= self.myMap.getSize():
            print("Too far down")
            pos[1] = self.myMap.getSize()-1


        self.mPos = pos
        if self.myMap.getTile(self.mPos[0], self.mPos[1]).getType() == TileTypes.HAZARD:
            penalty = 3
            print("Ouch...")
            self.myScore -= penalty

            if self.myScore > 0:
                print("Lost " + str(penalty) + " points from spikes")
            else:
                self.myScore = 0
                print("0 points remaining! (points don't go below 0)")

    def turnRight(self):
        self.turnTick()
        if self.facing < 3:
            self.facing += 1
        else:
            self.facing = 0

    def turnLeft(self):
        self.turnTick()
        if self.facing > 0:
            self.facing -= 1
        else:
            self.facing = 3

    def interact(self):
        self.turnTick()
        thisTile = self.myMap.getTile(self.mPos[0], self.mPos[1])
        print(thisTile)
        #print(thisTile.checkActive())
        if thisTile.getType() == TileTypes.EXIT:
            print("Exiting Area...")
            print("Points Earned: " + str(self.myScore))
            print("Turns Taken: " + str(self.lifetime))
            print("Time Bonus: " + str(40 * self.myMap.getSize())+ (" - (") + str(self.lifetime) + (" * 20) = ") + str(40 * self.myMap.getSize() - (self.lifetime * 20)))
            print("Total Score: " + str(40 * self.myMap.getSize() - (self.lifetime * 20) + self.myScore))
        elif thisTile.checkPuzzle():
            print("I can use that!")
            thisTile.use(self)
        else:
            print("Can't interact with that!")

    def recPuzzle(self, puzzleInput, puzzleType):
        self.currentPuzzle = puzzleInput
        self.puzzleType = puzzleType
        self.hasPuzzle = True

        print("My current puzzle is [" + str(puzzleType) + "] and the info I have is: " + str(self.currentPuzzle))

    def thisPuzzle(self):
        if self.hasPuzzle:
            return self.currentPuzzle
        else:
            print("I don't have a puzzle to solve...")
            return[]

    def solvePuzzle(self, puzzleOutput):
        try:
            if self.hasPuzzle:
                time.sleep(self.actionCD / 2)
                print("My answer is " + str(puzzleOutput) + "!")
                time.sleep(self.actionCD / 2)
                thisTile = self.myMap.getTile(self.mPos[0], self.mPos[1])

                thisTile.trySolve(puzzleOutput)
            else:
                print("Can't do that without a puzzle!")
        except:
            print("Something went wrong...")

    def getPos(self):
        return self.mPos

    def getFace(self):
        if self.facing == 0:
            return "Facing East!"
        elif self.facing == 1:
            return "Facing South!"
        elif self.facing == 2:
            return "Facing West!"
        else:
            return "Facing North!"

    def getPts(self):
        print("I have " + str(self.myScore) + " points!")
        return self.myScore

    def getTimer(self):
        print("I have taken " + str(self.lifetime) + " turns.")
        return self.lifetime

    def getImage(self):
        return self.currentSprite

    def updtImage(self):
        self.currentSprite = self.my_spritesheet.get_sprite((16 * self.frameCounter) + (144 * self.facing), 0, 16, 16)
        if self.frameCounter < 8:
            self.frameCounter += 1
        else:
            self.frameCounter = 0
