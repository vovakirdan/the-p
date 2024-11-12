import pygame
import random
from typing import Literal, Tuple, List, Iterable

from objects import Block, textures_dict, generate_grass_type_3, color_to_texture
from configuration import configuration, SKY_WATER, SKY, Color

def _generate_ocean_biome(
        block_list: pygame.sprite.Group,
        biom_size: int = configuration.world.size[0],
        start_x: int = 0,
        ground_level: int = configuration.world.ground_level,
        next_biome_sky_color: Color = SKY
    ):
    """Generates ocean biome"""
    # if we start from the beginning of the world, we have to make a slide from the minimum to the ground level
    x = start_x
    start_ground_level = int(configuration.world.ground_level / 4)
    end_ground_level = ground_level
    increase_gr_lev_coeff = (end_ground_level - start_ground_level) / biom_size
    water_level = ground_level - random.randint(1, 30)
    if x != 0:
        start_ground_level, end_ground_level = end_ground_level, start_ground_level
        increase_gr_lev_coeff = -increase_gr_lev_coeff

    # count gradient from start sky color to the next sky color
    sky_gradient = [
        (
            int(SKY_WATER[0] + (next_biome_sky_color[0] - SKY_WATER[0]) * (x / biom_size)),
            int(SKY_WATER[1] + (next_biome_sky_color[1] - SKY_WATER[1]) * (x / biom_size)),
            int(SKY_WATER[2] + (next_biome_sky_color[2] - SKY_WATER[2]) * (x / biom_size))
        )
        for x in range(biom_size)
    ]
    
    # generate biome from top to the bottom
    while x < biom_size:
        ground_level = int(ground_level + increase_gr_lev_coeff)
        for y in range(0, water_level + 1):
            # generate sky
            block_list.add(Block(x, y, collide=False, color=sky_gradient[x]))  # todo cache it to increase performance
        for y in range(water_level + 1, ground_level):
            # generate water
            block_list.add(Block(x, y, texture=textures_dict['water']['type_1']))
        for y in range(ground_level + 1, configuration.world.height):
            # generate sand
            block_list.add(Block(x, y, texture=textures_dict['sand']['type_1']))
        x += 1
    return end_ground_level

def generate_biome(
        type_: Literal['default', 'ocean', 'forest'] = 'default',
        biom_size: int = configuration.world.size[0],
        start_x: int = 0,
        ground_level: int = configuration.world.ground_level
    ):
    """Generates biome"""
    x = start_x
    next_ground_level = ground_level + random.randint(-biom_size, biom_size)  # not greater than x size of the biome
    while x < biom_size:

        x += 1

def generate_world(seed=None) -> Tuple[Iterable[pygame.sprite.Group], List[str], int]:
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
    ground_level = configuration.world.ground_level

    block_list = pygame.sprite.Group()
    ground_level = _generate_ocean_biome(block_list, 1000)
    for x in range(1001, configuration.world.size[0]):
        block_list.add(Block(x, ground_level, texture=generate_grass_type_3()))
    # for y in range(blocks_y):
    #     row = []
    #     for x in range(blocks_x):
    #         rand = random.randint(0, 100)
    #         if y > ground_level + random.randint(-1, 1):
    #             if rand < 5:
    #                 row.append('rock')
    #             elif rand < 7:
    #                 row.append('mud')
    #             elif rand < 10:
    #                 row.append('gold')
    #             else:
    #                 row.append('earth')
    #         elif y == ground_level:
    #             row.append('grass')
    #         else:
    #             row.append(None)
    #     world_data.append(row)

    # # Create block sprites based on the world data
    # block_list = pygame.sprite.Group()

    # for y, row in enumerate(world_data):
    #     for x, tile_type in enumerate(row):
    #         block = None
    #         x_pos = x * block_size
    #         y_pos = y * block_size

    #         if tile_type == 'earth':
    #             block = Block(x_pos, y_pos, type_=tile_type, texture=textures_dict['earth']['type_1'])
    #         elif tile_type == 'grass':
    #             block = Block(x_pos, y_pos, collide=False, type_=tile_type, texture=generate_grass_type_3())
    #         # elif tile_type == 'rock':
    #         #     block = Rock(x_pos, y_pos)
    #         # elif tile_type == 'mud':
    #         #     block = Mud(x_pos, y_pos)
    #         # elif tile_type == 'gold':
    #             # block = Gold(x_pos, y_pos)
    #         if block:
    #             block_list.add(block)

    # Place the player at the center of the world, above ground level
    player_width = configuration.player.width
    player_height = configuration.player.height

    player_x = (WORLD_WIDTH // 2) - (player_width // 2)
    player_y = (ground_level * block_height) - player_height

    # Ensure the player is not stuck in a block
    configuration.player.start_position = (player_x, player_y)

    return block_list, world_data, seed