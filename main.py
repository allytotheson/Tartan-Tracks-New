from cmu_graphics import *
from PIL import Image, ImageDraw
from constants import * 
import random 

from Obstacle import Obstacle, Train, Fence
from Player import Player
from Coin import Coin
import Obstacle as OBS
import functions as func
import Coin as CO

def onAppStart(app):
    func.start(app)

def game_redrawAll(app):
    #draw backgrounds/screens
    drawImage(CMUImage(app.bg), 0, 0)
    drawImage(CMUImage(app.bg), 0, BACKGROUND_HEIGHT)


    #PLAYER 1 SCREEN
    for lst in func.drawSpritesInOrder(app.player1Obstacles + 
                                       app.player1Coins):
        for sprite in lst:
            if isinstance(sprite, Coin):
                for i in range(sprite.count):
                    x, y = sprite.location[0] + i*COIN_WIDTH, sprite.location[1]
                    img = func.loadImage(sprite)
                    drawImage(CMUImage(img), x, y)
            else:      
                x, y = sprite.location
                img = func.loadImage(sprite)
                drawImage(CMUImage(img), x, y)
    
    #PLAYER 2 SCREEN
    for lst in func.drawSpritesInOrder(app.player2Obstacles + 
                                       app.player2Coins):
        for sprite in lst:
            if isinstance(sprite, Coin):
                for i in range(sprite.count):
                    x, y = sprite.location[0] + i*COIN_WIDTH, sprite.location[1] + BACKGROUND_HEIGHT
                    img = func.loadImage(sprite)
                    drawImage(CMUImage(img), x, y)
            else:      
                x, y = sprite.location[0], sprite.location[1] + BACKGROUND_HEIGHT
                img = func.loadImage(sprite)
                drawImage(CMUImage(img), x, y)

    #draw players
    for player in app.players:
        for screen in range(2):
            x, y = player.location[0], player.location[1] + screen*BACKGROUND_HEIGHT
            img = func.loadImage(player)
            drawImage(CMUImage(img), x, y)

def game_onStep(app):
    app.stepsPerSecond = 10
    if app.stepCount < 30:
        app.stepCount += 1
    else:
        app.stepCount = 0
    
    if not app.gameOver and not app.isPaused:
        #keep nextObstacles & nextCoins lists updated
        n = 4 - min(len(app.player1Obstacles), len(app.player2Obstacles)) #obstacles needed
        #to be generated to keep obstacles list at 4
        for i in range(n):
            newObstacle = OBS.loadObstacle()
            if True:#OBS.isLegalObstacle():
                app.nextObstacles.append(newObstacle)
        

        n = 3 - min(len(app.player1Coins), len(app.player2Coins))
        for i in range(n):
            newCoinString = CO.loadCoin()
            if True: #CO.isLegalCoin():
                app.nextCoins.append(newCoinString)

        #add new obstacles and coins to players view
        #PLAYER 1
        if app.stepCount % OBSTACLE_GENERATION_SPEED[app.player1.speed] == 0 :
            #obstacles
            if len(app.player1Obstacles) < 3:
                app.player1Obstacles.append(app.nextObstacles[0]) 
            #coins
            if len(app.player1Coins) < 3:
                app.player1Coins.append(app.nextCoins[0])
        #PLAYER 2
        if app.stepCount % OBSTACLE_GENERATION_SPEED[app.player2.speed] == 0:
            if len(app.player2Obstacles) < 3:
                app.player2Obstacles.append(app.nextObstacles[0])  
            if len(app.player2Coins) < 3:
                app.player2Coins.append(app.nextCoins[0])

        #remove obstacles on nextObstacles and coins on nextCoins that have
        #appeared on both screens
        app.nextObstacles = func.removeNext(app.nextObstacles, app.player1Obstacles,
                                            app.player2Obstacles)
        app.nextCoins = func.removeNext(app.nextCoins, app.player1Coins, app.player2Coins)
        #update sprite locations for player 1 and player 2
        for i in range(len(app.player1Obstacles)):
            app.player1Obstacles[i].updateLocation(app.player1.speed)
        for i in range(len(app.player1Coins)):
            app.player1Coins[i].updateLocation(app.player1.speed)
        
        for i in range(len(app.player2Obstacles)):
            app.player2Obstacles[i].updateLocation(app.player2.speed)
        for i in range(len(app.player2Coins)):
            app.player2Coins[i].updateLocation(app.player2.speed)
        #remove sprites that are off the map
        app.player1Obstacles = func.removeOffScreen(app.player1Obstacles)
        app.player2Obstacles = func.removeOffScreen(app.player2Obstacles)

        app.player1Coins = func.removeOffScreen(app.player1Coins)
        app.player2Coins = func.removeOffScreen(app.player2Coins)

        #actions
        if app.player1.isJump:
            app.player1.jump()
        if app.player2.isJump:
            app.player2.jump()
        
        #if player 1 collides with coin
        if app.player1.isCoinCollision(app.player1Coins)[0] == "True": #(True, coin)
            coin = app.player1.isCoinCollision(app.player1Coins)[1]
            lists = func.removeCollectedCoins(coin, app.player1Coins,
                                              app.player2Coins,
                                              app.nextCoins)
            app.player1Coins = lists[0]
            app.player2Coins = lists[1]
            app.nextCoins = lists[2]
        #if player 2 collides with coin
        if app.player2.isCoinCollision(app.player2Coins)[0] == "True":
            coin = app.player2.isCoinCollision(app.player2Coins)[1]
            lists = func.removeCollectedCoins(coin, app.player1Coins,
                                              app.player2Coins,
                                              app.nextCoins)
            app.player1Coins = lists[0]
            app.player2Coins = lists[1]
            app.nextCoins = lists[2]
        
        #if players collide with obstacle
        if app.player1.isObstacleCollision(app.player1Obstacles):
            app.gameOver == True
            app.winner = "Player 2"
        if app.player2.isObstacleCollision(app.player2Obstacles):
            app.gameOver == True
            app.winner = "Player 1"
        
        #if players collide with each other

        #if game over
def game_onKeyPress(app, key):
    if not app.gameOver and not app.isPaused:
        if key == "left" and not app.player1.isJump:
            app.player1.switchLanes(-1)
        elif key == "right" and not app.player1.isJump:
            app.player1.switchLanes(+1)
        elif key == "up":
            app.player1.isJump = True
        
        if key == "a" and not app.player2.isJump:
            app.player2.switchLanes(-1)
        elif key == "d" and not app.player2.isJump:
            app.player2.switchLanes(+1)
        elif key == "w":
            app.player2.isJump = True


    if not app.gameOver:
        if key == "p":
            app.isPaused = not app.isPaused

def main():
    runAppWithScreens(initialScreen = "game")

main()
        
    





    

