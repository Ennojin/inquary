import pygame

class Missile(pygame.sprite.Sprite):
    def __init__(self, pos, screen_height, speed=5, max_radius=50, expansion_speed=5):
        super().__init__()
        image = pygame.image.load("Space-invaders-main/graphics/missile.png").convert_alpha()
        self.image = pygame.transform.scale(image, (30, 60))
        self.rect = self.image.get_rect(center=pos)
        self.screen_heigth = screen_height

        self.speed = speed
        self.exploding = False

        # Explosion logic
        self.blast_radius = 0
        self.max_radius = max_radius
        self.expansion_speed = expansion_speed
        self.center = pos  # Center stays fixed once it explodes

        self.missile_explosion_sound = pygame.mixer.Sound('Space-invaders-main/audio/missile_explosion.mp3')
        self.missile_explosion_sound.set_volume(0.5)

    def update(self, obstacle_group):
        if not self.exploding:
            # Move down
            self.rect.y += self.speed
            self.center = self.rect.center
            if pygame.sprite.spritecollide(self, obstacle_group, False):
                self.exploding = True
                self.missile_explosion_sound.play()
                self.image = pygame.Surface((0, 0))  # Hide missile image if needed
                self.blast_radius = 0
        else:
            # Expanding hit radius
            if self.blast_radius < self.max_radius:
                self.blast_radius += self.expansion_speed

                # Check collision with obstacles
                for obstacle in obstacle_group:
                    distance = pygame.math.Vector2(obstacle.rect.center).distance_to(self.center)
                    if distance <= self.blast_radius:
                        obstacle.kill()
            else:
                self.kill()  # Done exploding

        if self.rect.y >= self.screen_heigth+200:
            self.kill()