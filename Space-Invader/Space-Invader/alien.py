import pygame
from laser import Laser

class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y, player_sprite, laser_sprite, surface, screen_height, game_difficulty=2):
        super().__init__()
        file_path = 'Space-invaders-main/graphics/' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))
        self.color = color
        self.laser_sprite = laser_sprite
        self.surface = surface
        self.screen_height = screen_height
        self.game_difficulty = game_difficulty
        self.pause_time = 0
        for player in player_sprite:
            self.player = player

        if color == 'red':
            self.value = 100
            if self.game_difficulty == 3 or self.game_difficulty == 4:
                self.health_point = 3
            else:
                self.health_point = 2
        elif color == 'green':
            self.value = 200
            self.health_point = 1
        elif color == 'yellow':
            self.value = 300
            self.health_point = 1
            # Yellow-specific attack system
            self.state = 'normal'

            if self.game_difficulty == 1:
                self.lock_duration = 5000
                self.cooldown = 10000
            elif self.game_difficulty == 2:
                self.lock_duration = 5000
                self.cooldown = 7500
            else:
                self.lock_duration = 5000
                self.cooldown = 5000

            self.lock_start_time = 0
            self.aim_direction = pygame.Vector2(0, 1)
            self.ready_to_lock = False
            self.lock_cooldown = pygame.time.get_ticks() + 3000
            self.original_image = pygame.image.load('Space-invaders-main/graphics/yellow.png')
            self.second_shot_pending = False
            self.second_shot_time = 0

    def yellow_behavior(self):
        if self.state == 'normal':
            # After cooldown, ready to lock
            if self.current_time >= self.lock_cooldown:
                self.state = 'locking'
                self.lock_start_time = self.current_time

        elif self.state == 'locking':
            # Lock onto player
            if self.player:
                direction = pygame.Vector2(self.player.rect.center) - pygame.Vector2(self.rect.center)
                if direction.length() != 0:
                    self.aim_direction = direction.normalize()

                # Rotate the alien to face the player
                angle = self.aim_direction.angle_to(pygame.Vector2(0, -1))
                self.image = pygame.transform.rotate(self.original_image, angle + 180)
                self.rect = self.image.get_rect(center=self.rect.center)

            # Finish locking after time
            if self.current_time - self.lock_start_time >= self.lock_duration:
                self.shoot()  # First shot immediately
                self.second_shot_pending = True
                self.second_shot_time = self.current_time + 200
                self.state = 'normal'
                self.lock_cooldown = self.current_time + self.cooldown
                self.image = self.original_image  # Reset rotation
                self.rect = self.image.get_rect(center=self.rect.center)
        return self.state

    def shoot(self):
        if self.player:
            # Calculate the angle between alien and player
            direction_vector = pygame.Vector2(self.player.rect.center) - pygame.Vector2(self.rect.center)
            angle = direction_vector.angle_to(pygame.Vector2(0, 1))  # Negative because of y-axis inversion

            # Create Laser with angle
            laser = Laser(self.rect.center, self.screen_height, 12, 'yellow_alien', angle)
            self.laser_sprite.add(laser)

    def draw_red_line(self, surface):
        if self.color == 'yellow' and self.state == 'locking':
            if self.player:
                temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
                start_pos = self.rect.center
                end_pos = self.player.rect.center
                pygame.draw.line(temp_surface, (255, 0, 0, 120), start_pos, end_pos, 2)
                surface.blit(temp_surface, (0, 0))

    def update(self, direction, pause_time):
        self.rect.x += direction
        self.draw_red_line(self.surface)
        current_time = pygame.time.get_ticks()
        self.pause_time = pause_time
        self.current_time = current_time - self.pause_time

        if self.color == 'yellow':
            self.yellow_behavior()
            if self.game_difficulty == 4:
                if self.second_shot_pending and self.current_time >= self.second_shot_time:
                    self.shoot()
                    self.second_shot_pending = False

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width, surface):
        super().__init__()
        # Load and scale alien
        image = pygame.image.load('Space-invaders-main/graphics/extra.png').convert_alpha()
        self.image = pygame.transform.scale(image, (60, 20))
        self.rect = self.image.get_rect()
        self.surface = surface

        # Load and scale warning sign
        self.warning_image = pygame.image.load('Space-invaders-main/graphics/warning_sign.png').convert_alpha()
        self.warning_image = pygame.transform.scale(self.warning_image, (100, 100))

        # Set direction and initial position
        self.side = side
        self.screen_width = screen_width

        if side == 'right':
            x = screen_width + 10
            self.speed = -3
        else:
            x = -self.rect.width - 10
            self.speed = 3

        self.rect.topleft = (x, 80)

        # Warning state
        self.show_warning = True
        self.warning_start_time = pygame.time.get_ticks()
        self.warning_duration = 1000
        self.flash_interval = 200

    def draw(self, surface):
        current_time = pygame.time.get_ticks()

        if self.show_warning:
            if (current_time // self.flash_interval) % 2 == 0:
                if self.side == 'left':
                    surface.blit(self.warning_image, (10, 10))
                elif self.side == 'right':
                    surface.blit(self.warning_image, (self.screen_width - self.warning_image.get_width() - 10, 10))
        else:
            surface.blit(self.image, self.rect)

    def update(self):
        self.draw(self.surface)
        # Hide warning after time passes
        if self.show_warning and pygame.time.get_ticks() - self.warning_start_time >= self.warning_duration:
            self.show_warning = False

        # Move once warning is done
        if not self.show_warning:
            self.rect.x += self.speed

