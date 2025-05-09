import pygame
import math

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, screen_height, speed = -8, shooter = 'player', angle = 0):
        super().__init__()
        image_alien = pygame.image.load('Space-invaders-main/graphics/laser.png').convert_alpha()
        image_player = pygame.image.load('Space-invaders-main/graphics/player_laser.png').convert_alpha()
        image_yellow_alien = pygame.image.load('Space-invaders-main/graphics/yellow_laser.png').convert_alpha()
        if shooter == 'player':
            self.image = pygame.transform.scale(image_player, (7, 30))
        elif shooter == 'alien':
            self.image = pygame.transform.scale(image_alien, (7, 30))
        elif shooter == 'yellow_alien':
            self.image = pygame.transform.scale(image_yellow_alien, (7, 30))
        self.rect = self.image.get_rect(center = pos)
        self.height_y_constraint = screen_height
        self.penetrate_time = 0
        self.hit_alien = []

        # Rotate image based on direction
        self.original_image = self.image
        self.image = pygame.transform.rotate(self.original_image, angle)

        # Set velocity based on angle
        radians = math.radians(angle)
        self.velocity = pygame.Vector2(math.sin(radians), math.cos(radians)) * speed

    def destroy(self):
        if self.rect.y < -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        self.destroy()