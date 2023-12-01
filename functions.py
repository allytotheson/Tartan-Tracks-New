from cmu_graphics import *
from PIL import Image, ImageDraw
from constants import * 
import random 
from copy import deepcopy

from Obstacle import Obstacle, Train, Fence, StaticPerson
from Player import Player
from Coin import Coin
import Obstacle as OBS
import Coin as C

def start(app):
    app.width = BOARD_WIDTH
    app.height = BOARD_HEIGHT

    app.bg = BACKGROUND
    app.coin = COIN

    app.players = [Player("bluePlayer", 0, 10.1, 0), Player("redPlayer", 1, 10, 1)]
    app.player1 = app.players[0]
    app.player2 = app.players[1]
    app.staticPlayer1 = StaticPerson("bluePlayer", 0, 0, 0)
    app.staticPlayer2 = StaticPerson("redPlayer", 1, 0, 1)
    app.player1Obstacles = []
    app.player1Coins = []
    app.player2Obstacles = []
    app.player2Coins = []

    app.isPaused = False
    app.gameOver = False
    app.winner = None
    app.stepCount = 0


def removeOffScreen(spritesList):
    i = len(spritesList)-1

    while i>=0:
        sprite = spritesList[i]
        if sprite.location[0] + sprite.width <= 0 or sprite.count <= 0:
            spritesList.pop(i)
        i-=1
    
    return spritesList

def removeCollectedCoins(coin, player1CoinsList, player2CoinsList):
    for i in range(len(player1CoinsList)):
        tempCoin = deepcopy(player1CoinsList[i])
        if tempCoin == coin:
            tempCoin.updateCollectedCoin()
            player1CoinsList[i] = tempCoin
    
    for i in range(len(player2CoinsList)):
        tempCoin = deepcopy(player2CoinsList[i])
        if tempCoin == coin:
            tempCoin.updateCollectedCoin()
            player2CoinsList[i] = tempCoin
    
    return player1CoinsList, player2CoinsList
    

def drawSpritesInOrder(spritesList): #sorts obstacles into smaller lists
    #based on track
    trackList = [[] for i in range(3)] 
    for sprite in spritesList:
        if sprite.location[0] + sprite.width < 0:
            continue
        else:
            trackList[sprite.track].append(sprite)
    
    return trackList

def loadImage(sprite):
    if isinstance(sprite, Train):
        train = Image.open(sprite.name)
        return train
    if isinstance(sprite, Fence):
        fence = Image.open(sprite.name)
        return fence
    if isinstance(sprite, StaticPerson):
        staticPerson = Image.open(sprite.name)
        return staticPerson
    if isinstance(sprite, Coin):
        coin = app.coin
        return coin
    if isinstance(sprite, Player):
        player = Image.open(sprite.name)
        return player


def addSpritesToList(player1, player2, player1List, player2List, newSprite):
    if player1.distance > player2.distance:
        player1List.append(deepcopy(newSprite)) #player 1

        #player 2
        distanceDx = player1.distance - player2.distance
        sprite = deepcopy(newSprite) 
        x, y = sprite.location
        sprite.location = x+distanceDx, y
        player2List.append(sprite)
    elif player2.distance > player1.distance:
        player2List.append(deepcopy(newSprite)) #player 2

        #player 1
        distanceDx = player2.distance - player1.distance
        sprite = deepcopy(newSprite) 
        x, y = sprite.location
        sprite.location = x+distanceDx, y
        player1List.append(sprite)
    else:
        player1List.append(deepcopy(newSprite))
        player2List.append(deepcopy(newSprite))
    

    return player1List, player2List


def drawPlayers(app, player1, player2):
    x, y = player1.location
    img = loadImage(player1)
    drawImage(CMUImage(img), x, y)
    x, y = player2.location[0], player2.location[1] + BACKGROUND_HEIGHT
    img = loadImage(player2)
    drawImage(CMUImage(img), x, y)

def maintainStaticPlayers(app, player1, player2, player1Static, player2Static):
    player1Static.updateSelf(player1, player2)
    player2Static.updateSelf(player2, player1)

    if player1.distance > player2.distance:
        distanceDx = player1.distance - player2.distance
        #what player 1 sees
        x, y = player2Static.location
        player2Static.location = (x-distanceDx, y)
        #what player 2 sees
        x, y = player1Static.location
        player1Static.location = (x+distanceDx, y)
    if player2.distance > player1.distance:
        distanceDx = player2.distance - player1.distance
        #what player 2 sees
        x, y = player1Static.location
        player1Static.location = (x-distanceDx, y)
        #what player1 sees
        x, y = player2Static.location
        player2Static.location = (x+distanceDx, y)
    

