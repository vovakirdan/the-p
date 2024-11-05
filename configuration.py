import random
from typing import Tuple, Union

class Color:
    def __init__(self, r: int = 255, g: int = 255, b: int = 255):
        self.r = r
        self.g = g
        self.b = b

    def rand(self):
        self.r, self.g, self.b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    
    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b

BROWN = Color(162, 101, 62)
SKY = Color(127, 199, 255)
PLAYER_COLOR = Color(0, 128, 255)
GRASS = Color(56, 128, 4)
WHITE = Color(255, 255, 255)

class Screen:
    def __init__(self, width: int = 0, height: int = 0, caption: str = ''):
        self.width = width
        self.height = height
        self.caption = caption
        self.fps = 60
        self.background_color = tuple(SKY)  # sky

    def __iter__(self):
        yield self.width
        yield self.height

class PlayerSettings:
    def __init__(self, size: Union[int, Tuple[int, int]] = 20):
        self.color = tuple(PLAYER_COLOR)  # blue color
        if isinstance(size, int):
            self.size = (size, size * 2)
        else:
            self.size = size
        self.width = self.size[0]
        self.height = self.size[1]
        self.speed = 5
        self.jump_strength = 10
        self.gravity = .5
        self.start_position_x = 0
        self.start_position_y = 0

    @property
    def start_position(self) -> Tuple[int, int]:
        return self.start_position_x, self.start_position_y
    
    @start_position.setter
    def start_position(self, position: Tuple[int, int]):
        self.start_position_x, self.start_position_y = position

class Block:
    def __init__(self, size: Union[int, Tuple[int, int]] = 20, x: int = 0, y: int = 0):
        if isinstance(size, int):
            self.size = (size, size)
        else:
            self.size = size
        self.x = x
        self.y = y
        self.default_color = tuple(WHITE)

class World:
    def __init__(self):
        self.width = 8000
        self.height = 4000
        self.size = (self.width, self.height)

class Configuration:
    BLOCK_COEFFICIENT = 20
    def __init__(self):
        self.screen = Screen(800, 600, 'P')
        self.player = PlayerSettings(self.BLOCK_COEFFICIENT)
        self.player.start_position = (self.screen.width // 2, self.screen.height // 2)
        self.block = Block(self.BLOCK_COEFFICIENT)
        self.world = World()

configuration = Configuration()

if __name__ == '__main__':
    screen = Screen(width=1024, height=768, caption='My Game')
    print(tuple(screen))
