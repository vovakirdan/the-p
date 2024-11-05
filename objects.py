import pygame
import random
from typing import AnyStr, Tuple

from configuration import configuration
from shades import brown_shades

BLOCK_SIZE = configuration.block.size

class Block(pygame.sprite.Sprite):
    def __init__(self, x: int = None, y: int = None, collide: bool = True, type_: AnyStr = '', texture: pygame.Surface = None):
        super().__init__()
        self.size = configuration.block.size
        if texture:
            self.image = texture
        else:
            self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.collide: bool = collide
        self.type_: AnyStr = type_

    @property
    def texture(self) -> pygame.Surface:
        return self._texture

def generate_grass_type_1() -> pygame.Surface:
    surface = pygame.Surface(BLOCK_SIZE)
    delim = surface.get_height() // 4
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            if y <= delim:
                green_shade = random.randint(80, 120)
                surface.set_at((x, y), (0, green_shade, 0))
            else:
                brown_shade = random.randint(80, 120)
                surface.set_at((x, y), (brown_shade, 42, 42))
    return surface

def generate_grass_type_2() -> pygame.Surface:
    surface = pygame.Surface(BLOCK_SIZE)
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            green_shade = random.randint(100, 200)
            surface.set_at((x, y), (0, green_shade, 0))
    return surface

def generate_grass_type_3() -> pygame.Surface:
    surface = pygame.Surface(BLOCK_SIZE)
    for x in range(surface.get_width()):
        delim = surface.get_height() // 2 + random.randint(0, 5)
        for y in range(surface.get_height()):
            # bg color if y < delim
            if y < delim:
                surface.set_at((x, y), configuration.screen.background_color)
                continue
            green_shade = random.randint(100, 200)
            surface.set_at((x, y), (0, green_shade, 0))
    return surface

grass_type_1 = generate_grass_type_1()
grass_type_2 = generate_grass_type_2()
grass_type_3 = generate_grass_type_3()

def generate_earth_type_1() -> pygame.Surface:
    surface = pygame.Surface(BLOCK_SIZE)
    # create an earth texture with brown shades depends on x and y
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            brown_shade = brown_shades[x][y]
            surface.set_at((x, y), (brown_shade, 42, 42))
    return surface

earth_type_1 = generate_earth_type_1()

class Water(Block):
    def create_texture(self):
        # create a water texture with random blue shades
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                blue_shade = random.randint(100, 200)
                self.image.set_at((x, y), (0, 0, blue_shade))

class Rock(Block):
    def create_texture(self):
        # create a rock texture with random grey shades
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                grey_shade = random.randint(100, 150)
                self.image.set_at((x, y), (grey_shade, grey_shade, grey_shade))

class Mud(Block):
    def create_texture(self):
        # create a mud texture with random brown shades
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                brown_shade = random.randint(60, 80)
                self.image.set_at((x, y), (brown_shade, 30, 30))

class Gold(Block):
    def create_texture(self):
        self.image.fill((255, 215, 0))

textures_dict = {
    'grass': {'type_1': grass_type_1, 'type_2': grass_type_2, 'type_3': grass_type_3},
    'earth': {'type_1': earth_type_1},
    'water': {'type_1': Water},
    'rock': {'type_1': Rock},
    'mud': {'type_1': Mud},
    'gold': {'type_1': Gold}
}

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        # Create a simple rectangle as the player's image
        self.image = pygame.Surface(configuration.player.size)
        self.image.fill(configuration.player.color)  # Blue color
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Movement attributes
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = configuration.player.speed
        self.jump_strength = -configuration.player.jump_strength  # Negative value to move up
        self.gravity = configuration.player.gravity
        
        # Placeholder for object in hand
        self.object_in_hand = None
        self.on_ground = False

    def update(self, tiles: pygame.sprite.Group):
        # Apply gravity
        self.velocity.y += self.gravity

        # Horizontal movement
        self.rect.x += self.velocity.x
        self.collide(self.velocity.x, 0, tiles)
        
        # Vertical movement
        self.rect.y += self.velocity.y
        self.collide(0, self.velocity.y, tiles)
        
        # Prevent player from going beyond world boundaries
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, configuration.world.width)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, configuration.world.height)

    def collide(self, xvel: int, yvel: int, tiles: pygame.sprite.Group):
        collisions = pygame.sprite.spritecollide(self, tiles, False)
        for tile in collisions:
            if not isinstance(tile, Block) or not tile.collide:
                continue  # Skip non-collidable blocks

            if xvel > 0:  # moving right
                self.rect.right = tile.rect.left
            if xvel < 0:  # moving left
                self.rect.left = tile.rect.right
            if yvel > 0:  # falling
                self.rect.bottom = tile.rect.top
                self.velocity.y = 0
                self.on_ground = True
            if yvel < 0:  # jumping
                self.rect.top = tile.rect.bottom
                self.velocity.y = 0

        if not collisions:
            self.on_ground = False

    def move_left(self):
        self.velocity.x = -self.speed

    def move_right(self):
        self.velocity.x = self.speed

    def stop(self):
        self.velocity.x = 0

    def jump(self):
        if self.on_ground:
            self.velocity.y = self.jump_strength
            self.on_ground = False

    def do_something(self):
        if self.object_in_hand:
            # Placeholder for interaction logic
            print("Interacting with the object in hand!")
        else:
            print("No object to interact with.")
