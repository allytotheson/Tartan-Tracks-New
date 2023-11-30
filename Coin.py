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
    
    def updateCollectedCoin(self):
        self.count -= 1
        self.width = self.width = COIN_WIDTH * self.count
        x, y = self.location
        self.location = (x+COIN_WIDTH, TRACK_1_BOTTOM + self.trackDy - self.height - 15)

def isLegalCoin(newCoin, coinList):
    for curCoin in coinList:
        if (newCoin.location[0] <= (curCoin.location[0] + curCoin.width) and
            newCoin.track == curCoin.track):
            return False
        if newCoin.count == curCoin.count:
            return False
    return True
    #coin should not overlap 
    #coins should be different lengths
    #

def loadCoin():
    randomTrack = random.randrange(0,3)
    randomCount = random.randrange(3,6)
    newCoinString = Coin(randomTrack, randomCount)

    return newCoinString