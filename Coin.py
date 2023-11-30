from constants import *
import random

class Coin:
    def __init__(self, track, count):
        self.track = track
        self.trackDy = TRACK_DIFFERENCE*self.track
        self.count = count
        self.width = COIN_WIDTH * self.count
        self.height = COIN_HEIGHT
        self.location = (BOARD_WIDTH, TRACK_1_BOTTOM + self.trackDy - self.height - 15)
    
    def __repr__(self):
        return str(self.location)
    
    def __eq__(self, other):
        return (isinstance(other, Coin)
                and (self.count == other.count) and (self.track == other.track))

    def __hash__(self):
        return str(self)
    
    def updateLocation(self, speed):
        x, y = self.location
        self.location = (x-speed, y)

def isLegalCoin():
    pass
    #coin should not overlap 
    #coins should be different lengths
    #

def loadCoin():
    randomTrack = random.randrange(0,3)
    randomCount = random.randrange(3,6)
    newCoinString = Coin(randomTrack, randomCount)

    return newCoinString