import random
from constants import *
from cmu_graphics import *
from PIL import Image, ImageDraw

class Obstacle:
    def __init__(self, track):
        self.track = track #tracks go from 0-2 instead of 1-3

        self.trackDy = TRACK_DIFFERENCE*self.track #gap between each track
        middleOfTrackY = TRACK_1_MIDDLE + self.trackDy
    
    def __repr__(self):
        return str(self.location)
    
    def __eq__(self, other):
        return ((isinstance(other, Obstacle)) and
                (self.track == other.track))

    def __hash__(self):
        return hash(str(self))
    
    def updateLocation(self, speed):
        x, y = self.location
        self.location = (x-speed, y)
        return self.location

class Train(Obstacle):
    def __init__(self, track, color):
        super().__init__(track)
        self.width = TRAIN_WIDTH
        self.height = TRAIN_HEIGHT
        self.color = color
        self.location = (BOARD_WIDTH, TRACK_1_BOTTOM + self.trackDy - self.height)
        self.name = f"images/{self.color}Train.png"
        self.count = 1

class Fence(Obstacle):
    def __init__(self, track, fill):
        super().__init__(track)
        self.width = FENCE_WIDTH
        self.height = FENCE_HEIGHT
        self.fill = fill
        self.location = (BOARD_WIDTH, TRACK_1_BOTTOM + self.trackDy - self.height)
        self.name = f"images/{self.fill}Fence.png"
        self.count = 1

class StaticPerson(Obstacle):
    def __init__(self, name, track, speed, screen):
        super().__init__(track)
        self.width = PERSON_WIDTH
        self.height = PERSON_HEIGHT
        self.name = f"images/{name}.png"
        self.track = track
        self.speed = speed
        self.screen = screen
        self.trackDy = TRACK_DIFFERENCE * self.track
        self.location = (BOARD_WIDTH//6, TRACK_1_MIDDLE + self.trackDy - PERSON_HEIGHT)

    def updateSelf(self, player, otherPlayer):
        self.track = player.track
        self.speed = player.speed-otherPlayer.speed
        self.trackDy = TRACK_DIFFERENCE * self.track
        x, y = self.location
        self.location = (x, TRACK_1_MIDDLE + self.trackDy - PERSON_HEIGHT )

def isLegalObstacle(newObstacle, allObstacles):
    for obstacle in allObstacles:
        if (newObstacle.location[0] <= (obstacle.location[0] + obstacle.width) and
            newObstacle.track == obstacle.track):
            return False
    return True

def loadObstacle(allObstacles):
    randomType = choice(OBSTACLES)
    randomTrack = randrange(0,3)
    randomCustomization = choice(CUSTOMIZATION[randomType])

    if randomType == "Train":
        newObstacle = Train(randomTrack, randomCustomization)
    elif randomType == "Fence":
        newObstacle = Fence(randomTrack, randomCustomization)
        
    if isLegalObstacle(newObstacle, allObstacles):
        return newObstacle
    else:
        return loadObstacle(allObstacles)





        