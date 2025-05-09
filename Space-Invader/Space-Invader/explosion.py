import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        explosion_images = [
            pygame.image.load('Space-invaders-main/graphics/explosion animation/explosion1.png').convert_alpha(),
            pygame.image.load('Space-invaders-main/graphics/explosion animation/explosion2.png').convert_alpha(),
            pygame.image.load('Space-invaders-main/graphics/explosion animation/explosion3.png').convert_alpha(),
            pygame.image.load('Space-invaders-main/graphics/explosion animation/explosion4.png').convert_alpha(),
            pygame.image.load('Space-invaders-main/graphics/explosion animation/explosion5.png').convert_alpha(),
            pygame.image.load('Space-invaders-main/graphics/explosion animation/explosion6.png').convert_alpha(),
            pygame.image.load('Space-invaders-main/graphics/explosion animation/explosion7.png').convert_alpha(),
            pygame.image.load('Space-invaders-main/graphics/explosion animation/explosion8.png').convert_alpha(),
            pygame.image.load('Space-invaders-main/graphics/explosion animation/explosion9.png').convert_alpha(),
            pygame.image.load('Space-invaders-main/graphics/explosion animation/explosion10.png').convert_alpha()]
        self.size = size
        self.images = explosion_images
        self.index = 0
        self.image_old = self.images[self.index]
        self.image = pygame.transform.scale(self.image_old, (self.size, self.size))
        self.rect = self.image.get_rect(center=(x, y))
        self.frame_delay = 2
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter >= self.frame_delay:
            self.counter = 0
            self.index += 1
            if self.index < len(self.images):
                self.image_old = self.images[self.index]
                self.image = pygame.transform.scale(self.image_old, (self.size, self.size))
            else:
                self.kill()