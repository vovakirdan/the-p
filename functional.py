import pygame
import random

from objects import Block
from configuration import Configuration

def generate_world(configuration: Configuration, seed=None):

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
            if y > ground_level + random.randint(-1, 1):
                row.append(1)  # Underground block (brown)
            elif y == ground_level + random.randint(-1, 1):
                row.append(2)  # Surface block (green)
            else:
                row.append(0)  # Empty space
        world_data.append(row)

    # Create block sprites based on the world data
    block_list = pygame.sprite.Group()

    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile == 1:
                block = Block(
                    x * block_width,
                    y * block_height,
                    configuration.block.underground_color,
                )
                block_list.add(block)
            elif tile == 2:
                block = Block(
                    x * block_width,
                    y * block_height,
                    configuration.block.surface_color,
                )
                block_list.add(block)

    # Place the player at the center of the world, above ground level
    player_width = configuration.player.width
    player_height = configuration.player.height

    player_x = (WORLD_WIDTH // 2) - (player_width // 2)
    player_y = (ground_level * block_height) - player_height

    # Ensure the player is not stuck in a block
    configuration.player.start_position = (player_x, player_y)

    return block_list, world_data, seed