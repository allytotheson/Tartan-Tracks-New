from cmu_graphics import *
from PIL import Image, ImageDraw
from constants import * 
import random 

from Obstacle import Obstacle, Train, Fence
from Player import Player
from Coin import Coin
import Obstacle as OBS
import Coin as C

def start(app):
    app.width = BOARD_WIDTH
    app.height = BOARD_HEIGHT

    app.bg = BACKGROUND
    app.coin = COIN

    app.players = [Player("bluePlayer", 0, 5, 0), Player("redPlayer", 1, 5, 1)]
    app.player1 = app.players[0]
    app.player2 = app.players[1]

    app.nextObstacles = [Train(1, "red")]
    app.nextCoins = [Coin(2, 6)]

    app.player1Obstacles = []
    app.player1Coins = []
    app.player2Obstacles = []
    app.player2Coins = []

    app.isPaused = False
    app.gameOver = False
    app.winner = None
    app.stepCount = 0
def removeNext(nextSpritesList, Player1SpritesList, Player2SpritesList):
    i = len(nextSpritesList)-1

    while i >= 0:
        sprite = nextSpritesList[i]
        if sprite in Player1SpritesList and sprite in Player2SpritesList:
            nextSpritesList.pop(i)
        i-=1
    
    return nextSpritesList

def removeOffScreen(spritesList):
    i = len(spritesList)-1

    while i>=0:
        sprite = spritesList[i]
        if sprite.location[0] + sprite.width <= 0 or sprite.count <= 0:
            spritesList.pop(i)
        i-=1
    
    return spritesList

def removeCollectedCoins(coin, player1CoinsList, player2CoinsList, nextCoins):
    for i in range(len(player1CoinsList)):
        tempCoin = player1CoinsList[i]
        if tempCoin == coin:
            tempCoin.count -= 1
            x, y = tempCoin.location 
            tempCoin.location = (x+COIN_WIDTH, y)
            player1CoinsList[i] = tempCoin
    
    for i in range(len(player2CoinsList)):
        tempCoin = player2CoinsList[i]
        if tempCoin == coin:
            tempCoin.count -= 1
            x, y = tempCoin.location 
            tempCoin.location = (x+COIN_WIDTH, y)
            player2CoinsList[i] = tempCoin

    for i in range(len(nextCoins)):
        tempCoin = nextCoins[i]
        if tempCoin == coin:
            tempCoin.count -= 1
            x, y = tempCoin.location 
            tempCoin.location = (x+COIN_WIDTH, y)
            nextCoins[i] = tempCoin
    
    return player1CoinsList, player2CoinsList, nextCoins
    

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
    if isinstance(sprite, Coin):
        coin = app.coin
        return coin
    if isinstance(sprite, Player):
        player = Image.open(sprite.name)
        return player