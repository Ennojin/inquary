import pygame
from laser import Laser
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint_x, constraint_y, speed):
        super().__init__()
        image = pygame.image.load('Space-invaders-main/graphics/player.png').convert_alpha()
        self.image = pygame.transform.scale(image, (50, 30))
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = constraint_x
        self.max_y_constraint = constraint_y
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 500

        self.lasers = pygame.sprite.Group()

    def get_input(self):
        x, y = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if self.rect.centerx < self.max_x_constraint and self.rect.centerx - x > self.speed:
            self.rect.x -= self.speed
        elif self.rect.centerx > 0 and self.rect.centerx - x < -self.speed:
            self.rect.x += self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, self.max_y_constraint))

    def update(self):
        self.get_input()
        self.recharge()
        self.lasers.update()

'''
keys = pygame.key.get_pressed()

        if keys[pygame.K_d] and self.rect.right < self.max_x_constraint:
            self.rect.x += self.speed
        elif keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()'''