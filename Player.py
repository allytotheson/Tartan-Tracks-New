from constants import *
from Obstacle import Obstacle
from Coin import Coin

class Player:

    def __init__(self, name, track, speed, screen):
        self.gameName = name
        self.name = f"images/{name}.png"
        self.track = track
        self.trackDy = TRACK_DIFFERENCE*self.track
        self.speed = speed
        self.width = PERSON_WIDTH
        self.height = PERSON_HEIGHT
        self.screen = screen

        self.location = (BOARD_WIDTH//6, TRACK_1_MIDDLE + self.trackDy - PERSON_HEIGHT) 
        
        self.coinCount = 0
        self.distance = 0

        self.isJump = False
        self.jumpCount = 7

        self.isSwitch = False
        self.switchCount = 6
        self.dy = TRACK_DIFFERENCE/self.switchCount
        self.direction = 0
        

    def __repr__(self):
        return f"Player {self.name}"
    
    def __hash__(self):
        return str(self.name)
    
    def __eq__(self, other):
        return ((isinstance(other, Player)) and (self.gameName == other.gameName))

    def addCoins(self):
        self.coinCount += 1
    
    def addDistance(self, speed):
        self.distance += speed
    
    def switchLanes(self, direction):
        if 0<= self.track + direction <= 2:
            self.track+=direction
            self.trackDy = TRACK_DIFFERENCE*self.track
            return True
        return False


    def switch(self):
        if self.switchCount > 0:
            y = self.location[1]
            self.location = (BOARD_WIDTH//6, y + self.dy*self.direction)
            self.switchCount -= 1
        else:
            self.switchCount = 6
            self.isSwitch = False
            self.direction = 0
    def jump(self):
        if self.jumpCount >= -7:
            y = self.location[1]
            dy = (self.jumpCount * abs(self.jumpCount)) * 0.5
            self.location = (BOARD_WIDTH//6, y - dy)
            self.jumpCount -= 1
        else:
            self.jumpCount = 7
            self.isJump = False
    
    
    def isObstacleCollision(self, obstacleList):
        if not self.isJump:
            for obstacle in obstacleList:
                if ((obstacle.location[0] - (self.location[0] + self.width)) <= 0
                    and obstacle.location[0] + obstacle.width >= self.location[0]
                    and obstacle.track == self.track):
                    return True
        return False
        
    def isCoinCollision(self, coinList):
        for coin in coinList:
            if ((coin.location[0] - (self.location[0] + self.width)) <= 0
                and coin.location[0] + COIN_WIDTH >= self.location[0]
                and coin.track == self.track):
                self.addCoins()
                return "True", coin
        return "False"
    
    def isPersonCollision(self, staticPerson):
        if (self.track == staticPerson.track
            and self.location[0] == staticPerson.location[0]):
            return True
        return False
    
    def isLegalCollision(self, staticPerson, direction):
        if 0<=staticPerson.track + direction <=2:
            return True
        else:
            self.track-=direction
            self.trackDy = TRACK_DIFFERENCE*self.track
            self.location = (BOARD_WIDTH//6, TRACK_1_MIDDLE + self.trackDy - PERSON_HEIGHT)
            self.switchCount = 6
            self.isSwitch = False
            self.direction = 0
            return False
            

        
    