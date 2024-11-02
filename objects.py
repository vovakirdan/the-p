import pygame

from configuration import Configuration, Color

configuration = Configuration()

class Block(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, color: Color):
        super().__init__()
        self.image = pygame.Surface(configuration.block.size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

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

    def update(self, tiles):
        # Apply gravity
        self.velocity.y += self.gravity
        
        # Update position
        self.rect.x += self.velocity.x
        self.collide(self.velocity.x, 0, tiles)
        self.rect.y += self.velocity.y
        self.collide(0, self.velocity.y, tiles)
        
        # Prevent player from falling below the ground
        # if self.rect.bottom >= 500:  # Assuming ground level is at y = 500
        #     self.rect.bottom = 500
        #     self.velocity.y = 0

    def collide(self, xvel, yvel, tiles):
        collisions = pygame.sprite.spritecollide(self, tiles, False)
        for tile in collisions:
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
        # Allow jumping if the player is on the ground
        # if self.rect.bottom >= 500:
        #     self.velocity.y = self.jump_strength
        if self.on_ground:
            self.velocity.y = self.jump_strength
            self.on_ground = False

    def do_something(self):
        if self.object_in_hand:
            # Placeholder for interaction logic
            print("Interacting with the object in hand!")
        else:
            print("No object to interact with.")