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

    app.players = [Player("bluePlayer", 0, 10, 0), Player("redPlayer", 1, 10, 1)]
    app.player1 = app.players[0]
    app.player2 = app.players[1]
    app.staticPlayer1 = StaticPerson("bluePlayer", 0, 10, 0)
    app.staticPlayer2 = StaticPerson("redPlayer", 1, 10, 1)
    app.player1Obstacles = []
    app.player1Coins = []
    app.player2Obstacles = []
    app.player2Coins = []

    app.isPaused = False
    app.gameOver = False
    app.winner = None
    app.gameOverStep = 0
    app.crashLocation = None
    app.helpShown = False


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
    if newSprite == None:
        return player1List, player2List
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
    #drawImage(CMUImage(img), x, y)
    x1, y1 = player2.location[0], player2.location[1] + BACKGROUND_HEIGHT
    img1 = loadImage(player2)
    #drawImage(CMUImage(img1), x1, y1)


    if player1.track < player2.track:
        drawImage(CMUImage(img), x, y)
        drawImage(CMUImage(img1), x1, y1)
    else:
        drawImage(CMUImage(img1), x1, y1)
        drawImage(CMUImage(img), x, y)


def maintainStaticPlayers(app, player1, player2, player1Static, player2Static):
    player1Static.updateSelf(player1, player2)
    player2Static.updateSelf(player2, player1)

    if player1.isJump:
        player1Static.jump()
    if player2.isJump:
        player2Static.jump()
    
    if player1.isSwitch:
        player1Static.switch()
    if player2.isSwitch:
        player2Static.switch()
    
def checkSpeed(player, val):
    if 7 < player.speed + val < 13:
        return True
    else:
        return False


        
        
            
            
def gameOverDrawing(app):
    drawImage(CMUImage(app.bg), 0,0)
    drawImage(CMUImage(app.bg), 0, BACKGROUND_HEIGHT)
    drawImage(CMUImage(GAME_OVER), BOARD_WIDTH/2, BOARD_HEIGHT/2, align = "center")
    if app.winner == "Player 1":
        drawImage(CMUImage(BLUE_PLAYER), 120, 330)
    else:
        drawImage(CMUImage(RED_PLAYER), 120, 330)
    drawLabel(f"{app.winner} won!", BOARD_WIDTH/2, BOARD_HEIGHT/2 + 40, size = 16)
    drawLabel(f"Player 1 Stats - Coins : {app.player1.coinCount}, Distance : {app.player1.distance}",
              BOARD_WIDTH/2, BOARD_HEIGHT/2 + 60, size = 12)
    drawLabel(f"Player 2 Stats - Coins : {app.player2.coinCount}, Distance : {app.player2.distance}",
              BOARD_WIDTH/2, BOARD_HEIGHT/2 + 75, size = 12)
    drawLabel("Press any key to restart :)", BOARD_WIDTH/2, BOARD_HEIGHT/2 + 90, size = 12)