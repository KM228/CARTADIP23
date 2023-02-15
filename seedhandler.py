import random

class SeedHandler:
    def getRandom(numDigits):
        out = ""
        for i in range(numDigits):
            rInt = random.randint(0, 9)
            out = out + str(rInt)

        return out
#       generates and returns a randomly generated string of numbers, including trailing zeroes.
#       number of digits determined by input

    def decodeSeed(seed):
        out = []
        out[:0]=seed
        return out

#       decodeSeed returns a list of each digit in a given seed, retaining trailing zeroes

    def exprSeed(num):
        random.seed(num)
        return random.randint(0, 7) - 1
#       returns a random number from 0 to 6 based on given seed
#       number range should change as new tiles are added.

SeedHandler.getRandom = staticmethod(SeedHandler.getRandom)
SeedHandler.decodeSeed = staticmethod(SeedHandler.decodeSeed)
