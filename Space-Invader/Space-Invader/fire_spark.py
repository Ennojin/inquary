import pygame

class Fire_spark(pygame.sprite.Sprite):
    def __init__(self, x, y, size, speed):
        super().__init__()
        fire_spark_images = [
            pygame.image.load('Space-invaders-main/graphics/fire spark animation/fire1.png').convert_alpha(),
            pygame.image.load('Space-invaders-main/graphics/fire spark animation/fire2.png').convert_alpha(),
            pygame.image.load('Space-invaders-main/graphics/fire spark animation/fire3.png').convert_alpha(),
            pygame.image.load('Space-invaders-main/graphics/fire spark animation/fire4.png').convert_alpha()]
        self.size = size
        self.images = fire_spark_images
        self.index = 0
        self.image_old = self.images[self.index]
        self.image = pygame.transform.scale(self.image_old, (self.size, self.size))
        if speed >= 0:
            self.rect = self.image.get_rect(center=(x + 30, y + 10))
        else:
            self.rect = self.image.get_rect(center=(x + 10, y + 10))
        self.frame_delay = 3
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