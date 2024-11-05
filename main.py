import pygame
from configuration import configuration
from objects import Player
from functional import generate_world

pygame.init()

screen = pygame.display.set_mode(tuple(configuration.screen))

pygame.display.set_caption(configuration.screen.caption)

clock = pygame.time.Clock()

# World generation
block_list, world_data, seed = generate_world()
print(f"Seed: {seed}")

# Now create the player at the correct position
player = Player(*configuration.player.start_position)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

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
            elif event.key == pygame.K_UP:
                player.jump()
            elif event.key == pygame.K_e:
                player.do_something()

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player.stop()

    # Update player with collision detection
    player.update(block_list)

    desired_player_screen_y = configuration.screen.height * (2/3)
    # desired_player_screen_x = configuration.screen.width * 2 // 3

    # Camera logic to follow the player
    camera_x = player.rect.centerx - configuration.screen.width // 2
    camera_y = player.rect.centery - desired_player_screen_y

    # Limit the camera to the world boundaries
    max_camera_x = configuration.world.width - configuration.screen.width
    max_camera_y = configuration.world.height - configuration.screen.height

    camera_x = max(0, min(camera_x, max_camera_x))
    camera_y = max(0, min(camera_y, max_camera_y))

    # Fill the screen with the background color
    screen.fill(configuration.screen.background_color)

    # Draw the blocks with camera offset
    for block in block_list:
        screen.blit(block.image, (block.rect.x - camera_x, block.rect.y - camera_y))

    # Draw the player with camera offset
    screen.blit(player.image, (player.rect.x - camera_x, player.rect.y - camera_y))

    # Update the display
    pygame.display.flip()
    clock.tick(configuration.screen.fps)

pygame.quit()