from Coin import Coin
coin1 = Coin(1, 3)

coin2 = Coin(1, 3)

coin1.location = (200, 300)
print(coin1 == coin2)