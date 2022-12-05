import random

# 定义常用颜色
RED = (255, 0, 0)
ORANGE = (255, 255, 0)
YELLOW = (0, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RGB_COLOR = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE]


def getRandomColor():
    global RGB_COLOR
    randint = random.randint(0, len(RGB_COLOR) - 1)
    return RGB_COLOR[randint]


if __name__ == '__main__':
    for i in range(20):
        color = getRandomColor()
        print(color)
