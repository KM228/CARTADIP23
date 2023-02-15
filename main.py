#Coding A Robot Through A Dungeon In Python
import sys
import time
import pygame
from threading import Thread
from player import Player
from tiles import TileMap

#MAIN CODE

pygame.init()

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
grey = (170, 170, 170)
black = (0, 0, 0)


mapType = "Random"
#mapType can be either "Random", "Void", "Empty", or "ID"
"""
Random  - Generate a map using a randomly generated seed, then output generated seed in console.
ID      - Prompt user to input a seed of a set length, generating map based on given seed. (length of seed determined by map size)
Empty   - Generate a map filled with empty tiles. May be useful for testing movement or debugging.
Void    - Generate a 2d array, but does not generate a new map object. Array is populated by placeholder string. (only useful for debug)
"""
mapSize = input("Enter size for map (leave blank for 5): ")
#map is always a square, input determines side length (5 by default).
#minimum value for viable map is 2, generator does not have an enforced maximum.
#site values above 25 are likely to cause errors due to generation method
#and may not be possible on most machines
if mapSize == "":
    mapSize = 5
else:
    mapSize = int(mapSize)
newMap = TileMap(mapSize, mapType)

print(newMap.getSize())

#print(SeedHandler.getRandom(4))
newMap.showMap()

lilGuy = Player(newMap)


def setGame():

    window_size = [800, 800] #size of application window in pixels
    margin = 1
    width = (window_size[1] - (margin * newMap.getSize())) / newMap.getSize()
    height = width
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("CARTADIP")
    screen.fill(black)
    pygame.display.flip()
    #determines fps

    running = True

    clock = pygame.time.Clock()

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        #Tile Spriter System
        for row in range(len(newMap.getMap())):
            for column in range(len(newMap.getMap()[row])):
                thisTile = newMap.getMap()[column][row]

                image = thisTile.getImage()

                image = pygame.transform.scale(image, (width, height))

                screen.blit(image, ((margin+width) * column + margin, (margin + height) * row + margin))

                thisTile.updtImage()

                #pygame.draw.rect(screen, colour, [(margin + width) * column + margin, (margin + height) * row + margin, width, height])

                #screen.blit(image, ((margin+width) * column + margin, (margin + height) * row + margin))
                #print(lilGuy.getPos()[0])
                #print("currentrow: " + str([row, column]))

                charImage = lilGuy.getImage()
                charImage = pygame.transform.scale(charImage, (width, height))

                if row == lilGuy.getPos()[1] and column == lilGuy.getPos()[0]:
                    screen.blit(charImage, ((margin+width) * column + margin, (margin + height) * row + margin))
                    #print("Displaying character!")
                    lilGuy.updtImage()
        #FPS limit
        clock.tick(6)

        pygame.display.flip()

    #pygame.quit()

def playerCode():
    #PLAYER TYPES CODE IN HERE
    #while True:
    """
    time.sleep(2)
    """
    while True:
        for i in range(4):
            lilGuy.walk()
        lilGuy.turnRight()
        lilGuy.getPts()
    """
    lilGuy.walk()
    print(lilGuy.getPos())
    lilGuy.interact()
    lilGuy.solvePuzzle(lilGuy.thisPuzzle()[0] + lilGuy.thisPuzzle()[1])
    lilGuy.walk()
    print(lilGuy.getPos())
    lilGuy.interact()
    lilGuy.solvePuzzle(lilGuy.thisPuzzle()[0] + lilGuy.thisPuzzle()[1])
    lilGuy.turnLeft()
    lilGuy.walk()
    print(lilGuy.getPos())
    lilGuy.interact()
    print(lilGuy.getPts())
    lilGuy.walk()
    lilGuy.interact()
    """

animMap = Thread(target= setGame)
runPC = Thread(target= playerCode)

animMap.start()
runPC.start()

animMap.join()
runPC.join()
#pygame.quit()
sys.exit()
