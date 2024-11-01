import pygame
import random

from configuration import Configuration

from objects import Player, Block

configuration = Configuration()

pygame.init()

screen = pygame.display.set_mode(tuple(configuration.screen))  # returns a width x height tuple

pygame.display.set_caption(configuration.screen.caption)

clock = pygame.time.Clock()

player = Player(*configuration.player.start_position)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

block_list = pygame.sprite.Group()

# world generation
block_size = 50
screen_width = configuration.screen.width
screen_height = configuration.screen.height
blocks_x = screen_width // block_size
blocks_y = screen_height // block_size

world_data = []

for y in range(blocks_y):
    row = []
    for x in range(blocks_x):
        if y > blocks_y // 2 + random.randint(-1, 1):
            row.append(1)
        else:
            row.append(0)
    world_data.append(row)

# create block sprites based on the world data
for y, row in enumerate(world_data):
    for x, tile in enumerate(row):
        if tile == 1:
            block = Block(x * block_size, y * block_size, block_size)
            block_list.add(block)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()
            elif event.key == pygame.K_SPACE:
                player.jump()
            elif event.key == pygame.K_e:
                player.do_something()

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player.stop()

    player.update(block_list)
    screen.fill(configuration.screen.background_color)
    block_list.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(configuration.screen.fps)
pygame.quit()