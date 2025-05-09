import pygame

class Special_supply(pygame.sprite.Sprite):
    def __init__(self, type, pos, screen_height):
        super().__init__()
        self.type = type
        self.speed = 3
        self.screen_height = screen_height
        health_restore = pygame.image.load('Space-invaders-main/graphics/health restore.png').convert_alpha()
        obstacle_restore = pygame.image.load('Space-invaders-main/graphics/obstcal restore.png').convert_alpha()
        penetration_attack = pygame.image.load('Space-invaders-main/graphics/stronger attack.png').convert_alpha()

        if self.type == 'health':
            self.original_image = health_restore
        elif self.type == 'attack':
            self.original_image = penetration_attack
        elif self.type == 'obstacle':
            self.original_image = obstacle_restore

        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= self.screen_height:
            self.kill()