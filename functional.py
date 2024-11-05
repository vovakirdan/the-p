import pygame
import random
from typing import Literal, Tuple

from objects import Block, textures_dict, generate_grass_type_3
from configuration import configuration

def generate_biome(type_: Literal['default', 'ocean', 'forest'] = 'default', biom_size: Tuple[int, int] = configuration.world.size):
    """Generates biome"""
    pass

def generate_world(seed=None):
    """Generates world"""
    # Set seed
    if seed is None:
        seed = random.randint(0, 1000000)
    random.seed(seed)

    # Constants
    BLOCK_COEFFICIENT = configuration.BLOCK_COEFFICIENT  # Should be 20

    # World dimensions
    WORLD_WIDTH = configuration.world.width  # e.g., 8000
    WORLD_HEIGHT = configuration.world.height  # e.g., 4000

    block_size = BLOCK_COEFFICIENT
    block_width = block_height = block_size

    # Calculate number of blocks horizontally and vertically
    blocks_x = WORLD_WIDTH // block_width
    blocks_y = WORLD_HEIGHT // block_height

    # Generate world data
    world_data = []

    # Simple terrain generation with a ground level and some randomness
    ground_level = blocks_y - (blocks_y // 4)  # Ground level towards the bottom

    for y in range(blocks_y):
        row = []
        for x in range(blocks_x):
            rand = random.randint(0, 100)
            if y > ground_level + random.randint(-1, 1):
                if rand < 5:
                    row.append('rock')
                elif rand < 7:
                    row.append('mud')
                elif rand < 10:
                    row.append('gold')
                else:
                    row.append('earth')
            elif y == ground_level:
                row.append('grass')
            else:
                row.append(None)
        world_data.append(row)

    # Create block sprites based on the world data
    block_list = pygame.sprite.Group()

    for y, row in enumerate(world_data):
        for x, tile_type in enumerate(row):
            block = None
            x_pos = x * block_size
            y_pos = y * block_size

            if tile_type == 'earth':
                block = Block(x_pos, y_pos, type_=tile_type, texture=textures_dict['earth']['type_1'])
            elif tile_type == 'grass':
                block = Block(x_pos, y_pos, collide=False, type_=tile_type, texture=generate_grass_type_3())
            # elif tile_type == 'rock':
            #     block = Rock(x_pos, y_pos)
            # elif tile_type == 'mud':
            #     block = Mud(x_pos, y_pos)
            # elif tile_type == 'gold':
                # block = Gold(x_pos, y_pos)
            if block:
                block_list.add(block)

    # Place the player at the center of the world, above ground level
    player_width = configuration.player.width
    player_height = configuration.player.height

    player_x = (WORLD_WIDTH // 2) - (player_width // 2)
    player_y = (ground_level * block_height) - player_height

    # Ensure the player is not stuck in a block
    configuration.player.start_position = (player_x, player_y)

    return block_list, world_data, seed