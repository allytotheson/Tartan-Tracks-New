from PIL import Image, ImageDraw

BACKGROUND = Image.open("images/background.png")
BACKGROUND_WIDTH = BACKGROUND.size[0]
BACKGROUND_HEIGHT = BACKGROUND.size[1]
COIN = Image.open("images/coin.png")
COIN_WIDTH = COIN.size[0]
COIN_HEIGHT = COIN.size[1]
TRAIN = Image.open("images/redTrain.png")
TRAIN_WIDTH = TRAIN.size[0]
TRAIN_HEIGHT = TRAIN.size[1]
FENCE = Image.open("images/solidFence.png")
FENCE_WIDTH = FENCE.size[0]
FENCE_HEIGHT = FENCE.size[1]
PERSON = Image.open("images/bluePlayer.png")
PERSON_WIDTH = PERSON.size[0]
PERSON_HEIGHT = PERSON.size[1]

BOARD_WIDTH = BACKGROUND_WIDTH #640
BOARD_HEIGHT = BACKGROUND_HEIGHT * 2 #720



TRACK_1_BOTTOM = 172.5
TRACK_1_MIDDLE = 140

TRACK_DIFFERENCE = 87.5


OBSTACLES = ["Train", "Fence"]
CUSTOMIZATION = {"Train" : ["red"], "Fence":["solid"]}

ACCELERATION = 10
GRAVITY = 0.5