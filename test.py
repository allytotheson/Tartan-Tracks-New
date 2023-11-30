from PIL import Image, ImageDraw
COIN = Image.open("images/coin.png")
COIN_WIDTH = COIN.size[0]
COIN_HEIGHT = COIN.size[1]


print(COIN_WIDTH)