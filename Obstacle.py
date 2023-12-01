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

        self.isJump = False
        self.jumpCount = 7
        self.isSwitch = False
        self.switchCount = 6
        self.dy = TRACK_DIFFERENCE/self.switchCount
        self.direction = 0

    def jump(self):
        if self.jumpCount >= -7:
            x, y = self.location
            dy = (self.jumpCount * abs(self.jumpCount)) * 0.5
            self.location = (x, y - dy)
            self.jumpCount -= 1
        else:
            self.jumpCount = 7
            self.isJump = False
    def switch(self):
        if self.switchCount > 0:
            x, y = self.location
            self.location = (x, y + self.dy*self.direction)
            self.switchCount -= 1
        else:
            self.switchCount = 6
            self.isSwitch = False
            self.direction = 0

    def updateSelf(self, playerSelf, playerOther):
        self.track = playerSelf.track
        self.speed = playerSelf.speed - playerOther.speed
        self.trackDy = TRACK_DIFFERENCE * self.track
        x, y = self.location
        self.location = (x + self.speed, TRACK_1_MIDDLE + self.trackDy - PERSON_HEIGHT)
        self.isJump = playerSelf.jump
        self.isSwitch = playerSelf.switch
        self.direction = playerSelf.direction


def loadObstacle(allObstacles):
    return helperLoadObstacle(allObstacles, 0)
    # randomType = choice(OBSTACLES)
    # randomTrack = randrange(0,3)
    # randomCustomization = choice(CUSTOMIZATION[randomType])

    # if randomType == "Train":
    #     newObstacle = Train(randomTrack, randomCustomization)
    # elif randomType == "Fence":
    #     newObstacle = Fence(randomTrack, randomCustomization)
        
    # if isLegalObstacle(newObstacle, allObstacles):
    #     return newObstacle
    # else:
    #     return loadObstacle(allObstacles)

def helperLoadObstacle(allObstacles, count):
    if count > 4:
        return None
    else:
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
            return helperLoadObstacle(allObstacles, count+1)
        
        



def sortByVertical(obstacleList): 
    return helperSortByVertical(obstacleList, [])

def helperSortByVertical(obstacleList, result):
    if len(obstacleList) == 0:
        return result
    else:
        firstObstacle = obstacleList[0]
        temp = [firstObstacle]
        for i in range(len(obstacleList[1:])):
            obstacle = obstacleList[1+i]
            if (obstacle.location[0] <= 
                firstObstacle.location[0] + firstObstacle.width):
                temp.append(obstacle)
            else:
                if len(temp)!=0:
                    result.append(temp)
                return helperSortByVertical(obstacleList[i+1:], result)
        result.append(temp)
        return result

def isSolvableList(sortedObstacleList):
    for sublist in sortedObstacleList:
        fenceCount = 0
        trainCount = 0
        for obstacle in sublist:
            if isinstance(obstacle, Fence):
                fenceCount += 1
            if isinstance(obstacle, Train):
                trainCount += 1
        if trainCount > 2: #ie all three lanes are covered by trains at 
            #one point in time
            return False
    return True

def isLegalObstacle(newObstacle, allObstacles):
    for obstacle in allObstacles:
        if (newObstacle.location[0] <= (obstacle.location[0] + obstacle.width) and
            newObstacle.track == obstacle.track):
            return False
    
    if not isSolvableList(sortByVertical([newObstacle] + allObstacles)):
        return False
    return True