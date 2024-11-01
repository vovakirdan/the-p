import random

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

BROWN = Color(139, 69, 19)
SKY = Color(206, 50, 100)
PLAYER_COLOR = Color(0, 128, 255)

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
    def __init__(self):
        self.color = tuple(PLAYER_COLOR)  # blue color
        self.speed = 5
        self.jump_strength = 15
        self.gravity = .5
        self.start_position_x = 0
        self.start_position_y = 0

    @property
    def start_position(self) -> tuple[int, int]:
        return self.start_position_x, self.start_position_y
    
    @start_position.setter
    def start_position(self, position: tuple[int, int]):
        self.start_position_x, self.start_position_y = position

class Block:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.color = tuple(BROWN)

class Configuration:
    def __init__(self):
        self.screen = Screen(800, 600, 'P')
        self.player = PlayerSettings()
        self.player.start_position = (self.screen.width // 2, self.screen.height // 2)
        self.block = Block(50, 50)

if __name__ == '__main__':
    screen = Screen(width=1024, height=768, caption='My Game')
    print(tuple(screen))
